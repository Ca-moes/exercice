# /// script
# requires-python = ">=3.12"
# dependencies = ["garminconnect>=0.3", "pyyaml", "beautifulsoup4"]
# ///
"""Sync the "Garmin Connect Setup" tables in site/*.html to Garmin Connect workouts.

  uv run garmin/sync.py pull                 list workouts on Garmin (read-only)
  uv run garmin/sync.py pull "Pull 1"        print one workout in full (JSON)
  uv run garmin/sync.py push --dry-run       print the workouts that would be uploaded
  uv run garmin/sync.py push                 create/update workouts on Garmin (asks first), then send them to the watch
  uv run garmin/sync.py push "Core"          the same for one workout
  uv run garmin/sync.py send                 send the site's workouts to the watch again
"""
import json
import re
import sys
from getpass import getpass
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from garminconnect import Garmin

TOKENS = "~/.garminconnect"
ROOT = Path(__file__).resolve().parent.parent
PAGES = ["push.html", "pull.html", "legs.html", "core.html", "postural.html"]
WATCH = "Forerunner 265"  # device that receives the workouts
NOTE_LIMIT = 200  # Garmin cuts step notes at 200 characters
STRENGTH = {"sportTypeId": 5, "sportTypeKey": "strength_training"}
NO_TARGET = {"workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target"}
STEP_TYPES = {k: {"stepTypeId": i, "stepTypeKey": k}
              for k, i in [("warmup", 1), ("cooldown", 2), ("interval", 3), ("rest", 5), ("repeat", 6)]}
END = {k: {"conditionTypeId": i, "conditionTypeKey": k}
       for k, i in [("lap.button", 1), ("time", 2), ("iterations", 7), ("reps", 10)]}


def login():
    """Use saved tokens; if missing or expired, ask for credentials and save new tokens."""
    try:
        client = Garmin()
        client.login(TOKENS)
    except Exception:
        if not sys.stdin.isatty():
            sys.exit("Not logged in to Garmin. Run this once in a terminal to log in: uv run garmin/sync.py pull")
        client = Garmin(input("Garmin email: "), getpass("Garmin password: "), prompt_mfa=lambda: input("MFA code: "))
        client.login(TOKENS)
    return client


def all_workouts(client):
    workouts, page = [], 100
    while batch := client.get_workouts(len(workouts), page):
        workouts += batch
        if len(batch) < page:
            break
    return workouts


def pull(name=None):
    client = login()
    workouts = all_workouts(client)
    if not name:
        for w in workouts:
            print(f'{w["workoutId"]}  {w["workoutName"]}  ({w["sportType"]["sportTypeKey"]})')
        return
    match = next((w for w in workouts if w["workoutName"] == name), None)
    if not match:
        sys.exit(f"No workout named {name!r} on Garmin.")
    print(json.dumps(client.get_workout_by_id(match["workoutId"]), indent=2, ensure_ascii=False))


# ── push ─────────────────────────────────────────────────────

def card_note(card):
    """'Name — dose' then the how-to cues (or the first paragraph), cut at a word to fit Garmin's limit."""
    title = card.h3.get_text(" ", strip=True)
    dose = card.select_one(".card-dose")
    head = f"{title} — {dose.get_text(' ', strip=True)}" if dose else title
    lines = [li.get_text(" ", strip=True) for li in card.select(".cues li")]
    if not lines:
        para = card.select_one(".card-body > p:not([class])")
        lines = [para.get_text(" ", strip=True)] if para else []
    note = head
    for i, line in enumerate(lines):
        sep = "\n\n" if i == 0 else "\n"
        if len(note + sep + line) > NOTE_LIMIT:
            room = NOTE_LIMIT - 1 - len(note + sep)
            cut = line[:room].rsplit(" ", 1)[0].rstrip(",;:—-– ") if room > 0 else ""
            return note + sep + cut + "…" if len(cut) >= 15 else note
        note += sep + line
    return note


def read_tables():
    """Yield (page, workout name, rows, notes) per table in the pages' Garmin sections.
    notes maps each card title on the page to its watch note."""
    for page in PAGES:
        soup = BeautifulSoup((ROOT / "site" / page).read_text(), "html.parser")
        notes = {}
        for card in soup.select(".card"):
            notes.setdefault(card.h3.get_text(" ", strip=True), card_note(card))
        for h3 in soup.select("section#garmin h3"):
            table = h3.find_next_sibling("table")
            rows = [[td.get_text(" ", strip=True) for td in tr.find_all("td")]
                    for tr in table.find_all("tr") if tr.find("td")]
            yield page, h3.get_text(strip=True), rows, notes


def parse_target(text):
    """'10' / '8/side' / '8 each' → reps; '40s' / '25s/side' / '2 min' → time; 'Lap Button' → lap press."""
    t = text.strip().lower()
    if t == "lap button":
        return "lap.button", None
    m = re.fullmatch(r"(\d+)\s*(s|min)?\s*(/\s*side|per side|each)?", t)
    if not m:
        raise ValueError(f"can't read target {text!r}")
    n, unit = int(m[1]), m[2]
    if unit:
        return "time", n * 60 if unit == "min" else n
    return "reps", n


def parse_rest(text):
    """'90s' / '2 min' → timed rest; 'Lap Button (switch side)' → rest until lap press, with a note; '—' → none."""
    t = text.strip()
    if t in ("", "—", "-"):
        return None
    m = re.fullmatch(r"lap button\s*(?:\((.+)\))?", t, re.I)
    if m:
        return "lap.button", None, m[1] and m[1][0].upper() + m[1][1:]
    m = re.fullmatch(r"(\d+)\s*(s|min)", t.lower())
    if not m:
        raise ValueError(f"can't read rest {text!r}")
    return "time", int(m[1]) * (60 if m[2] == "min" else 1), None


def step(kind, end, value=None, description=None, exercise=None):
    s = {"type": "ExecutableStepDTO", "stepType": STEP_TYPES[kind], "endCondition": END[end],
         "endConditionValue": value, "description": description, "targetType": NO_TARGET}
    if exercise:
        s["category"], s["exerciseName"] = exercise["category"], exercise["name"]
    return s


def build_workout(page, name, rows, exercises, notes):
    """Table rows → Garmin workout JSON.

    Warm up / Cool down    one step (rest, if any, follows it)
    Repeat ×N              N sets of exercise + rest (×1: plain steps, no repeat group)
    Superset ×N            consecutive rows share one repeat group, closed by the row that has a Rest
    """
    blocks = []  # [kind, sets, [steps]]
    for i, row in enumerate(rows, 1):
        try:
            if len(row) != 4:
                raise ValueError("expected 4 cells: Step | Exercise | Target | Rest")
            kind, label, target, rest = row
            kind = kind.strip().lower()
            end, value = parse_target(target)
            rest = parse_rest(rest)
            if kind in ("warm up", "cool down"):
                steps = [step(kind.replace(" ", ""), end, value, notes.get(label, label), exercises.get(label))]
                blocks.append(["single", 1, steps])
            else:
                m = re.fullmatch(r"(repeat|superset)\s*[×x]\s*(\d+)", kind)
                if not m:
                    raise ValueError(f"unknown step {row[0]!r} (use Warm up / Cool down / Repeat ×N / Superset ×N)")
                if label not in exercises:
                    raise ValueError(f"{label!r} is not in garmin/exercises.yaml")
                if label not in notes:
                    raise ValueError(f"{label!r} doesn't match a card title on {page}")
                sets = int(m[2])
                steps = [step("interval", end, value, notes[label], exercises[label])]
                if m[1] == "superset" and blocks and blocks[-1][0] == "open superset" and blocks[-1][1] == sets:
                    blocks[-1][2] += steps
                else:
                    blocks.append([m[1], sets, steps])
                if m[1] == "superset":
                    blocks[-1][0] = "superset" if rest else "open superset"
            if rest:
                blocks[-1][2].append(step("rest", rest[0], rest[1], rest[2]))
        except ValueError as e:
            sys.exit(f"{page} / {name} / row {i}: {e}")
    if any(kind == "open superset" for kind, _, _ in blocks):
        sys.exit(f"{page} / {name}: a Superset run has no Rest on its last row")

    workout_steps, order, group = [], 0, 0
    for _, sets, steps in blocks:
        if sets == 1:
            for s in steps:
                order += 1
                workout_steps.append(s | {"stepOrder": order})
            continue
        order += 1
        group += 1
        repeat = {"type": "RepeatGroupDTO", "stepOrder": order, "stepType": STEP_TYPES["repeat"], "childStepId": group,
                  "numberOfIterations": sets, "smartRepeat": False, "skipLastRestStep": False,
                  "endCondition": END["iterations"], "endConditionValue": sets, "workoutSteps": []}
        for s in steps:
            order += 1
            repeat["workoutSteps"].append(s | {"stepOrder": order, "childStepId": group})
        workout_steps.append(repeat)
    return {"workoutName": name, "sportType": STRENGTH,
            "workoutSegments": [{"segmentOrder": 1, "sportType": STRENGTH, "workoutSteps": workout_steps}]}


def push(dry_run, only=None):
    exercises = yaml.safe_load((ROOT / "garmin/exercises.yaml").read_text())
    # Build (and so validate) every workout before talking to Garmin.
    workouts = [build_workout(page, name, rows, exercises, notes) for page, name, rows, notes in read_tables()]
    if only:
        workouts = [w for w in workouts if w["workoutName"] == only] or sys.exit(f"No table named {only!r} on the site.")
    if dry_run:
        print(json.dumps(workouts, indent=2, ensure_ascii=False))
        return
    client = login()
    existing = {}
    for w in all_workouts(client):
        existing.setdefault(w["workoutName"], []).append(w["workoutId"])
    for w in workouts:
        ids = existing.get(w["workoutName"], [])
        if len(ids) > 1:
            sys.exit(f"{len(ids)} workouts on Garmin are named {w['workoutName']!r}; rename or delete the extras first.")
        print(("update  " if ids else "create  ") + w["workoutName"])
    if input("Proceed? [y/N] ").strip().lower() != "y":
        sys.exit("Nothing changed.")
    sent = {}
    for w in workouts:
        if ids := existing.get(w["workoutName"]):
            current = client.get_workout_by_id(ids[0])
            for segment in w["workoutSegments"]:  # keep the workout's own sport
                segment["sportType"] = current["sportType"]
            client.update_workout(ids[0], current | {"workoutSegments": w["workoutSegments"]})
            sent[w["workoutName"]] = ids[0]
            print(f"updated  {w['workoutName']}")
        else:
            sent[w["workoutName"]] = client.upload_workout(w)["workoutId"]
            print(f"created  {w['workoutName']}")
    send(client, sent)


def watch_id(client):
    devices = client.get_devices()
    match = next((d for d in devices if d.get("productDisplayName") == WATCH), None)
    if not match:
        sys.exit(f"No {WATCH!r} on this Garmin account; devices: {[d.get('productDisplayName') for d in devices]}")
    return match["deviceId"]


def send(client, workouts):
    """Queue workouts ({name: id}) for the watch; they land on it at its next sync with the phone."""
    device = watch_id(client)
    for name, workout_id in workouts.items():
        client.push_workout_to_device(workout_id, device)
        print(f"sent     {name} → {WATCH}")


def send_all():
    names = [name for _, name, _, _ in read_tables()]
    client = login()
    ids = {w["workoutName"]: w["workoutId"] for w in all_workouts(client)}
    if missing := [n for n in names if n not in ids]:
        sys.exit(f"Not on Garmin yet (run push first): {', '.join(missing)}")
    send(client, {n: ids[n] for n in names})


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["pull"]:
        pull(args[1] if len(args) > 1 else None)
    elif args[:1] == ["push"]:
        push("--dry-run" in args, next((a for a in args[1:] if a != "--dry-run"), None))
    elif args[:1] == ["send"]:
        send_all()
    else:
        sys.exit(__doc__)
