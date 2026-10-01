# Plain-HTML Site + Garmin Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Obsidian vault + Quartz with hand-maintainable plain HTML pages on GitHub Pages, then add a one-file Python script that creates/updates the Garmin Connect workouts from tables in those pages.

**Architecture:** A throwaway converter (run once, never committed) turns `content/*.md` into `site/*.html`; after that the HTML is the source of truth and is edited directly. GitHub Pages publishes `site/` as-is (no build). `garmin/sync.py` is a PEP 723 `uv` script that reads `<section id="garmin">` tables from the pages, maps exercise labels via `garmin/exercises.yaml`, and sends raw workout JSON through python-garminconnect.

**Tech Stack:** HTML + one CSS file; GitHub Actions (`upload-pages-artifact` + `deploy-pages`); Python ≥3.12 via `uv run` with `garminconnect`, `pyyaml`, `beautifulsoup4`.

**Spec:** `docs/superpowers/specs/2026-10-01-html-site-and-garmin-sync-design.md`

## Global Constraints

- No TypeScript/Node tooling remains in the repo. No test suite, no linters, no extra scaffolding (user's explicit request) — verification is done with throwaway commands shown in each task.
- Pages are written for a human reader; the Garmin tables stay readable (columns **Step | Exercise | Target | Rest**).
- All internal links are relative and end in `.html` so pages work from disk (`file://`) and on `ca-moes.github.io/exercice`.
- Garmin credentials/tokens never enter the repo (tokens live in `~/.garminconnect/`).
- `sync.py` never deletes Garmin workouts; it validates every table before uploading anything.
- The user's uncommitted edit in `content/pull-workout.md` ("Chin-ups, Underhand — 3×5-8") must be carried into `site/pull.html`.
- Pushing to GitHub and writing to the Garmin account are outward-facing: ask the user before each.
- Every commit message ends with a blank line and `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (omitted from the commit snippets below for brevity).

## Review Focus

- **Heading links with em dashes** (`[[push-workout#Push 1 — Shoulders + Triceps Long Head|Push 1]]`) must land on the right heading → the link checker in Task 1 verifies every `#anchor` matches an `id`.
- **Pages inside `research/`** need `../` for CSS, icon, links and images → the link checker covers `href` and `src` from every page, including research ones.
- **Opening from disk** must work → Task 2 opens `site/index.html` via `file://` and clicks through.
- **Workout name mismatch on push** (e.g. heading text differs from the Garmin name by a space) would silently create a duplicate → real `push` prints "update"/"create" per workout and asks `Proceed? [y/N]` before writing (Task 7).
- **Expired/missing Garmin tokens** → `login()` falls back to prompting email/password/MFA and re-saves tokens (Task 4).

---

## Part 1 — Plain-HTML site

### Task 1: Generate `site/` from the vault (throwaway converter)

**Files:**
- Create (throwaway, NOT committed): `/tmp/convert_vault.py`, `/tmp/check_links.py`
- Create: `site/*.html`, `site/research/*.html`, `site/assets/*.webp`, `site/icon.png`

**Interfaces:**
- Produces: the page set below; workout pages contain `<section id="garmin">` with one `<h3>` (exact Garmin workout name) + `<table>` per workout. Task 4–6 rely on this markup.

| Source (content/) | Page (site/) |
|---|---|
| index | index.html |
| push-workout | push.html |
| pull-workout | pull.html |
| leg-workout | legs.html |
| postural-correction | postural.html |
| weekly-schedule | weekly-schedule.html |
| equipment-considerations | equipment.html |
| periodization-notes | periodization.html |
| push/pull/leg/postural-correction-research | research/push.html, research/pull.html, research/legs.html, research/postural.html |

- [ ] **Step 1: Write the converter**

`/tmp/convert_vault.py`:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["markdown-it-py", "mdit-py-plugins", "pyyaml"]
# ///
"""One-time conversion of the Obsidian vault (content/) to plain HTML (site/). Run from repo root."""
import os, re, shutil
from pathlib import Path

import yaml
from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin

SRC, OUT = Path("content"), Path("site")
PAGES = {
    "index": "index.html",
    "push-workout": "push.html",
    "pull-workout": "pull.html",
    "leg-workout": "legs.html",
    "postural-correction": "postural.html",
    "weekly-schedule": "weekly-schedule.html",
    "equipment-considerations": "equipment.html",
    "periodization-notes": "periodization.html",
    "push-workout-research": "research/push.html",
    "pull-workout-research": "research/pull.html",
    "leg-workout-research": "research/legs.html",
    "postural-correction-research": "research/postural.html",
}

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{root}style.css">
<link rel="icon" href="{root}icon.png">
</head>
<body>
{header}<main>
<h1>{title}</h1>
{body}</main>
</body>
</html>
"""
HEADER = '<header><a href="{root}index.html">← Home</a></header>\n'


def slug(text):
    return re.sub(r"[^\w]+", "-", text.lower()).strip("-")


md = (
    MarkdownIt("commonmark", {"html": True})
    .enable(["table", "strikethrough"])
    .use(anchors_plugin, min_level=2, max_level=4, slug_func=slug)
)


def split_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return (yaml.safe_load(m[1]), text[m.end():]) if m else ({}, text)


TITLES = {stem: split_frontmatter((SRC / f"{stem}.md").read_text())[0].get("title", stem) for stem in PAGES}


def rel(target, here):
    return os.path.relpath(target, os.path.dirname(here) or ".")


def wikilinks(text, here):
    def repl(m):
        note, heading, label = m[1], m[2], m[3]
        href = rel(PAGES[note], here) + (f"#{slug(heading)}" if heading else "")
        return f"[{label or TITLES[note]}]({href})"
    return re.sub(r"\[\[([^\]|#\\]+)(?:#([^\]|\\]+))?(?:\\?\|([^\]]+))?\]\]", repl, text)


def callouts(text):
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        m = re.match(r"> \[!(\w+)\][-+]?\s*(.*)", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        kind, title = m[1].lower(), m[2] or m[1].title()
        body, i = [], i + 1
        while i < len(lines) and lines[i].startswith(">"):
            body.append(re.sub(r"^> ?", "", lines[i])); i += 1
        out += [f'<aside class="callout {kind}">', f'<p class="callout-title">{md.renderInline(title)}</p>',
                "", *body, "", "</aside>", ""]
    return "\n".join(out)


def garmin_section(text):
    head, sep, rest = text.partition("\n## Garmin Connect Setup\n")
    if not sep:
        return text
    section, nxt, tail = rest.partition("\n## ")
    section = re.sub(r"^\*\*(.+)\*\*\s*$", r"### \1", section, flags=re.M)
    return f'{head}\n<section id="garmin">\n\n## Garmin Connect Setup\n{section}\n\n</section>\n{nxt}{tail}'


for stem, target in PAGES.items():
    _, text = split_frontmatter((SRC / f"{stem}.md").read_text())
    root = rel(".", target) + "/" if "/" in target else ""
    text = garmin_section(callouts(wikilinks(text, target)))
    html = md.render(text)
    html = html.replace('src="assets/gifs/', f'src="{root}assets/').replace("<img ", '<img loading="lazy" ')
    html = re.sub(r'href="\./([\w-]+)"', lambda m: f'href="{rel(PAGES[m[1]], target)}"', html)
    page = SHELL.format(title=TITLES[stem], root=root, body=html,
                        header="" if stem == "index" else HEADER.format(root=root))
    (OUT / target).parent.mkdir(parents=True, exist_ok=True)
    (OUT / target).write_text(page)
    print("wrote", OUT / target)

(OUT / "assets").mkdir(exist_ok=True)
for f in (SRC / "assets/gifs").glob("*.webp"):
    shutil.copy2(f, OUT / "assets" / f.name)
shutil.copy2("quartz/static/icon.png", OUT / "icon.png")
```

- [ ] **Step 2: Run it**

Run: `cd /Users/andregomes/Projects/Exercice && uv run /tmp/convert_vault.py`
Expected: 12 `wrote site/...` lines, no traceback.

- [ ] **Step 3: Write the link checker**

`/tmp/check_links.py`:

```python
# /// script
# dependencies = ["beautifulsoup4"]
# ///
"""Check every local href/src in site/ resolves to a file, and every #anchor to an id."""
from pathlib import Path
from bs4 import BeautifulSoup

site, bad = Path("site"), 0
ids = {p: {t["id"] for t in BeautifulSoup(p.read_text(), "html.parser").select("[id]")} for p in site.rglob("*.html")}
for page in ids:
    soup = BeautifulSoup(page.read_text(), "html.parser")
    for tag in soup.select("[href], [src]"):
        url = tag.get("href") or tag.get("src")
        if url.startswith(("http:", "https:", "mailto:")):
            continue
        path, _, anchor = url.partition("#")
        target = (page.parent / path).resolve() if path else page.resolve()
        if not target.exists():
            print(f"{page}: missing file {url}"); bad += 1
        elif anchor and anchor not in ids.get(target.relative_to(Path.cwd()), set()):
            print(f"{page}: missing anchor {url}"); bad += 1
print("OK" if not bad else f"{bad} problem(s)")
```

- [ ] **Step 4: Run the checker and fix**

Run: `uv run /tmp/check_links.py`
Expected: `OK`. If not, fix the converter and rerun Steps 2 and 4.

- [ ] **Step 5: Spot-check the output**

Run: `grep -c '<section id="garmin">' site/push.html site/pull.html site/legs.html` → each `1`.
Run: `grep -o '<h3[^>]*>[^<]*</h3>' site/pull.html | tail -2` → `Pull 1 (Home)` and `Pull 2 (Home)`.
Run: `grep -c 'Chin-ups, Underhand — 3×5-8' site/pull.html` → `1`.
Run: `grep -c '\[!' site/*.html site/research/*.html | grep -v ':0'` → no output (all callouts converted).

- [ ] **Step 6: Commit**

```bash
git add site/
git commit -m "Add plain-HTML site converted from the Obsidian vault"
```

### Task 2: Stylesheet and page polish

**Files:**
- Create: `site/style.css`
- Modify: `site/index.html` (remove the Obsidian-tracking callout)

- [ ] **Step 1: Write `site/style.css`**

```css
/* One stylesheet for every page. Palette: "Clean Slate" sage-teal. */
:root {
  color-scheme: light dark;
  --bg: #fcfcfb;
  --surface: #ffffff;
  --border: #e8e8e6;
  --muted: #4a524f;
  --faint: #8a918e;
  --text: #1f2a27;
  --accent: #2f7d6b;
  --accent-soft: rgba(47, 125, 107, 0.1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16181a;
    --surface: #1d2023;
    --border: #2a2d30;
    --muted: #c9ccce;
    --faint: #8b9196;
    --text: #f1f3f4;
    --accent: #54b79c;
    --accent-soft: rgba(84, 183, 156, 0.15);
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}

header, main { max-width: 46rem; margin: 0 auto; padding: 0 1rem; }
header { padding-top: 1rem; font-size: 0.95rem; }
main { padding-bottom: 4rem; }

h1, h2, h3, h4 { line-height: 1.25; margin: 2rem 0 0.6rem; }
h1 { font-size: 1.9rem; margin-top: 1rem; }
h2 { font-size: 1.45rem; padding-top: 1rem; border-top: 1px solid var(--border); }
h3 { font-size: 1.15rem; }

a { color: var(--accent); }
hr { border: 0; border-top: 1px solid var(--border); margin: 2rem 0; }
img { display: block; max-width: 100%; height: auto; margin: 0.8rem 0; border-radius: 8px; }
code { font-size: 0.9em; padding: 0.1em 0.3em; border-radius: 4px; background: var(--accent-soft); }
blockquote { margin: 1rem 0; padding-left: 1rem; border-left: 3px solid var(--border); color: var(--muted); }

/* Tables scroll sideways on narrow screens instead of squashing */
table { display: block; overflow-x: auto; border-collapse: collapse; margin: 1rem 0; font-size: 0.92rem; }
th, td { padding: 0.4rem 0.6rem; border: 1px solid var(--border); text-align: left; vertical-align: top; }
th { background: var(--accent-soft); }

/* Callouts (were Obsidian "> [!type]" blocks) */
.callout {
  --c: var(--accent);
  margin: 1rem 0;
  padding: 0.7rem 1rem;
  border-left: 4px solid var(--c);
  border-radius: 6px;
  background: color-mix(in srgb, var(--c) 9%, transparent);
}
.callout > :first-child { margin-top: 0; }
.callout > :last-child { margin-bottom: 0; }
.callout-title { font-weight: 700; color: var(--c); }
.callout.info { --c: #3b82c4; }
.callout.tip { --c: var(--accent); }
.callout.summary { --c: #6b7f8a; }
.callout.note { --c: #7c6bbf; }
.callout.warning { --c: #c98a1b; }

/* Home dashboard */
.home-hero { font-size: 1.05rem; color: var(--muted); margin: 0.1rem 0 1.6rem; }
.home-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.8rem; margin: 0 0 2.2rem; }
a.home-card {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.9rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 10px;
  text-decoration: none;
}
a.home-card:hover { border-color: var(--accent); }
.hc-days { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent); }
.hc-name { font-size: 1.35rem; font-weight: 700; line-height: 1.1; color: var(--text); }
.hc-focus { font-size: 0.82rem; color: var(--faint); }

@media (max-width: 34rem) {
  .home-cards { grid-template-columns: 1fr; }
  h1 { font-size: 1.6rem; }
}
```

- [ ] **Step 2: Remove the Obsidian-only callout from `site/index.html`**

Delete the whole `<aside class="callout note">…Tracking lives in Obsidian…</aside>` block (Dataview/logging no longer exist).

- [ ] **Step 3: Review every page in a browser**

Run: `open site/index.html` (file://, no server). Click every card and link; open each of the 12 pages. Check, at desktop width and at phone width (devtools responsive mode, ~390px), in light and dark mode (devtools → Rendering → prefers-color-scheme):
- callouts styled with title line; tables scroll sideways rather than overflow; images load and fit;
- the "← Home" link works from top-level and `research/` pages;
- heading links from Weekly Schedule (Push 1, Pull 2, …) jump to the right section.
Fix any conversion leftovers by editing the HTML directly (the vault is no longer the source).

- [ ] **Step 4: Re-run the link checker**

Run: `uv run /tmp/check_links.py` → `OK`.

- [ ] **Step 5: Commit**

```bash
git add site/
git commit -m "Style the HTML site (Clean Slate palette, light/dark, mobile-first)"
```

### Task 3: Remove the vault + Quartz, new deploy workflow and README

**Files:**
- Delete: `content/`, `quartz/`, `plugins/`, `package.json`, `package-lock.json`, `tsconfig.json`, `globals.d.ts`, `index.d.ts`, `quartz.ts`, `quartz.config.yaml`, `quartz.config.default.yaml`, `quartz.lock.json`, `.node-version`, `.npmrc`, `.prettierrc`, `.prettierignore`, `LICENSE.txt`, `docs/superpowers/specs/2026-06-21-website-customization-design.md`; local untracked `.obsidian/`
- Rewrite: `.github/workflows/deploy.yml`, `README.md`, `.gitignore`
- Keep: `.gitattributes`, `.conductor/` (another tool's folder, untracked)

- [ ] **Step 1: Delete**

```bash
git rm -r -q content quartz plugins package.json package-lock.json tsconfig.json globals.d.ts index.d.ts quartz.ts quartz.config.yaml quartz.config.default.yaml quartz.lock.json .node-version .npmrc .prettierrc .prettierignore LICENSE.txt docs/superpowers/specs/2026-06-21-website-customization-design.md
rm -rf .obsidian content node_modules public .quartz .quartz-cache
```

(The `rm -rf content` also removes the now-converted uncommitted `pull-workout.md` edit — it already lives in `site/pull.html`, verified in Task 1 Step 5.)

- [ ] **Step 2: Write `.github/workflows/deploy.yml`**

```yaml
name: Deploy site to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Write `.gitignore`**

```
.DS_Store
```

- [ ] **Step 4: Write `README.md`**

```markdown
# Training

My home strength + posture training plan.

- **Read it:** https://ca-moes.github.io/exercice (phone) or open `site/index.html` locally.
- **Edit it:** edit the HTML files in `site/` directly. Styling for every page is in `site/style.css`.
- **Publish:** push to `main` — `.github/workflows/deploy.yml` uploads `site/` to GitHub Pages as-is (no build).
- **Exercise animations:** `.webp` files in `site/assets/`, shown with `<img src="assets/name.webp" alt="…" loading="lazy">`.

## Garmin Connect

`garmin/sync.py` creates/updates my Garmin workouts from the "Garmin Connect Setup" tables
in the workout pages. Needs [uv](https://docs.astral.sh/uv/).

    uv run garmin/sync.py pull                    # list workouts on Garmin
    uv run garmin/sync.py pull "Pull 1 (Home)"    # show one workout in full (JSON)
    uv run garmin/sync.py push --dry-run          # show what would be uploaded
    uv run garmin/sync.py push                    # create/update on Garmin (asks first)

First run asks for Garmin email/password (+ MFA code); the login is saved in `~/.garminconnect/`.
Exercise names in the tables are mapped to Garmin's exercise list in `garmin/exercises.yaml` —
add a line there when a table uses a new exercise.
```

(The Garmin section describes Part 2; it's written now so the README is done once. If Part 2 changes a command, update it in Task 8.)

- [ ] **Step 5: Verify nothing references the removed tooling**

Run: `git ls-files | grep -v '^site/' ` → only `.gitattributes`, `.gitignore`, `.github/workflows/deploy.yml`, `README.md`, and `docs/superpowers/…` (this spec + plan).
Run: `uv run /tmp/check_links.py` → `OK`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "Replace Quartz and the Obsidian vault with the plain-HTML site"
```

- [ ] **Step 7: Publish (ask the user first)**

Ask the user to confirm pushing `main`. Then:

```bash
git push origin main
gh run watch --exit-status $(gh run list --workflow deploy.yml --limit 1 --json databaseId -q '.[0].databaseId')
```

Expected: run succeeds. Open https://ca-moes.github.io/exercice/ , click through home → a workout page → a research page → a heading link; confirm images load.

---

## Part 2 — Garmin sync

### Task 4: `sync.py` with `pull` (login + read)

**Files:**
- Create: `garmin/sync.py`

**Interfaces:**
- Produces: `login() -> Garmin`; CLI `pull [NAME]`. Task 6 adds `push` to the same file.

- [ ] **Step 1: Write `garmin/sync.py`**

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["garminconnect>=0.3", "pyyaml", "beautifulsoup4"]
# ///
"""Sync the "Garmin Connect Setup" tables in site/*.html to Garmin Connect workouts.

  uv run garmin/sync.py pull                   list workouts on Garmin (read-only)
  uv run garmin/sync.py pull "Pull 1 (Home)"   print one workout in full (JSON)
  uv run garmin/sync.py push --dry-run         print the workouts that would be uploaded
  uv run garmin/sync.py push                   create/update workouts on Garmin (asks first)
"""
import json
import sys
from getpass import getpass

from garminconnect import Garmin

TOKENS = "~/.garminconnect"


def login():
    """Use saved tokens; if missing or expired, ask for credentials and save new tokens."""
    try:
        client = Garmin()
        client.login(TOKENS)
    except Exception:
        client = Garmin(input("Garmin email: "), getpass("Garmin password: "), prompt_mfa=lambda: input("MFA code: "))
        client.login(TOKENS)
    return client


def pull(name=None):
    client = login()
    workouts = client.get_workouts(0, 500)
    if not name:
        for w in workouts:
            print(f'{w["workoutId"]}  {w["workoutName"]}  ({w["sportType"]["sportTypeKey"]})')
        return
    match = next((w for w in workouts if w["workoutName"] == name), None)
    if not match:
        sys.exit(f"No workout named {name!r} on Garmin.")
    print(json.dumps(client.get_workout_by_id(match["workoutId"]), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["pull"]:
        pull(args[1] if len(args) > 1 else None)
    else:
        sys.exit(__doc__)
```

- [ ] **Step 2: First login (user runs it — interactive password/MFA)**

Ask the user to type in the Claude Code prompt: `! uv run garmin/sync.py pull`
Expected: prompts for email, password, maybe MFA; then one line per workout, including the 6 PPL workouts ("Push 1 (Home)" … "Legs 2 (Home)") and the postural one. Note the postural workout's exact name.

If login fails with a Cloudflare/403 error, stop and report to the user: that's the spec's fallback case (browser-driven approach), out of scope for this plan.

- [ ] **Step 3: Save every existing workout's JSON for reference (not committed)**

```bash
mkdir -p /tmp/garmin
for n in "Push 1 (Home)" "Push 2 (Home)" "Pull 1 (Home)" "Pull 2 (Home)" "Legs 1 (Home)" "Legs 2 (Home)" "<postural name from Step 2>"; do
  uv run garmin/sync.py pull "$n" > "/tmp/garmin/$n.json"
done
ls -la /tmp/garmin
```

Expected: 7 non-empty JSON files (tokens are saved, so no prompts now).

- [ ] **Step 4: Commit**

```bash
git add garmin/sync.py
git commit -m "Add garmin/sync.py with login and pull"
```

### Task 5: Exercise mapping + postural table from the existing workouts

**Files:**
- Create: `garmin/exercises.yaml`
- Modify: `site/postural.html` (add Garmin section), possibly `site/push.html`, `site/pull.html`, `site/legs.html` (only if the Garmin workout and the table disagree)

- [ ] **Step 1: Read the step structure of the existing workouts**

```bash
for f in /tmp/garmin/*.json; do echo "== $f"; jq -r '
  def s: if .type=="RepeatGroupDTO" then "repeat ×\(.numberOfIterations): " + ([.workoutSteps[]|s]|join(" | "))
         else "\(.stepType.stepTypeKey) \(.category // "-")/\(.exerciseName // "-") \(.endCondition.conditionTypeKey)=\(.endConditionValue // "") desc=\(.description // "")" end;
  .workoutSegments[].workoutSteps[] | s' "$f"; done
```

Record for each table row: the Garmin `category`/`exerciseName` the user chose, how per-side/"each" targets were entered (reps value? description?), and what the warm-up step looks like. Also note any extra fields present on steps (e.g. `targetType`, `weightValue`, `exerciseName` null for warm-up), and each workout's `sportType` (`jq .sportType`) — the postural one may not be `strength_training`; `push` keeps whatever sport the existing workout has.

- [ ] **Step 2: Write `garmin/exercises.yaml`**

One entry per distinct Exercise label used in a `Repeat` row of any Garmin table, values copied from the matching step in Step 1. Labels must match the table text exactly. Current labels (plus the postural ones from Step 3):

```yaml
# Exercise label exactly as written in a page's Garmin table → Garmin exercise-list entry.
# Garmin's list is limited, so some labels map to the closest Garmin exercise.
# Find names with: uv run garmin/sync.py pull "<workout>"  (category / exerciseName fields)

Pull Up (or Assisted Pull Up):          {category: <from JSON>, name: <from JSON>}
Inverted Row / Body Row:                {category: …, name: …}
Reverse Fly / Band Pull Apart:          …
Concentration Curl:                     …
Chin Up (or Assisted Chin Up):          …
Reverse Fly (for Y-T-W):                …
Incline Dumbbell Curl (custom):         …
Shrug (optional):                       …
Pike Push Up (custom):                  …
Push Up (3s eccentric):                 …
Lateral Raise:                          …
Overhead Triceps Extension:             …
Deficit Push Up (custom):               …
Dip:                                    …
Bulgarian Split Squat:                  …
Sissy Squat (custom):                   …
Hamstring Curl (for sliding curl):      …
Standing Calf Raise (single-leg):       …
Single Leg Romanian Deadlift (B-stance): …
Hip Thrust / Glute Bridge:              …
Cossack Squat (custom):                 …
```

Every `…` is replaced by real values from `/tmp/garmin/*.json` — the file must contain no placeholders when committed. If a step on Garmin has no category (user typed a free-text step), ask the user which Garmin exercise to use, find candidates with `uv run --with garminconnect python -c "from garminconnect import exercises; print(exercises.find('<word>'))"`.

- [ ] **Step 3: Add the postural Garmin section to `site/postural.html`**

Insert before `</main>`, built from the postural workout JSON, same shape as the other pages:

```html
<section id="garmin">
<h2 id="garmin-connect-setup">Garmin Connect Setup</h2>
<h3>{exact Garmin workout name}</h3>
<table>
<thead><tr><th>Step</th><th>Exercise</th><th>Target</th><th>Rest</th></tr></thead>
<tbody>
<tr><td>Repeat ×1</td><td>Couch Stretch</td><td>40s/side</td><td>—</td></tr>
<!-- …one row per Garmin step, in Garmin order… -->
</tbody>
</table>
</section>
```

Use the postural page's own exercise names in the Exercise column and add each to `exercises.yaml`. Timed targets are written `40s`, `45s`, `2 min`; per-side as `40s/side` or `8/side`.

- [ ] **Step 4: Reconcile tables with what's on Garmin**

For each PPL workout, compare the Step-1 summary with the page table (sets, reps, rest, order). Where they differ, ask the user which is right and fix the page (the page is the source of truth from now on).

- [ ] **Step 5: Commit**

```bash
git add garmin/exercises.yaml site/
git commit -m "Map table exercises to Garmin and add the postural Garmin table"
```

### Task 6: `push --dry-run` (parse tables → workout JSON)

**Files:**
- Modify: `garmin/sync.py`

**Interfaces:**
- Consumes: `<section id="garmin">` → `<h3>` name + following `<table>` (Task 1/5); `garmin/exercises.yaml` (Task 5); `login()` (Task 4).
- Produces: `read_tables() -> iterator[(page, name, rows)]`, `build_workout(page, name, rows, exercises) -> dict` (Garmin workout JSON), CLI `push [--dry-run]`.

- [ ] **Step 1: Add the parsing and building code**

Add imports at the top (`re`, `pathlib.Path`, `yaml`, `bs4.BeautifulSoup`) and these definitions above `if __name__ == "__main__":`

```python
ROOT = Path(__file__).resolve().parent.parent
PAGES = ["push.html", "pull.html", "legs.html", "postural.html"]
STRENGTH = {"sportTypeId": 5, "sportTypeKey": "strength_training"}
STEP_TYPES = {k: {"stepTypeId": i, "stepTypeKey": k}
              for k, i in [("warmup", 1), ("cooldown", 2), ("interval", 3), ("rest", 5), ("repeat", 6)]}
END = {k: {"conditionTypeId": i, "conditionTypeKey": k}
       for k, i in [("lap.button", 1), ("time", 2), ("iterations", 7), ("reps", 10)]}


def read_tables():
    """Yield (page, workout name, rows) for each table in the pages' Garmin sections."""
    for page in PAGES:
        soup = BeautifulSoup((ROOT / "site" / page).read_text(), "html.parser")
        for h3 in soup.select("section#garmin h3"):
            table = h3.find_next_sibling("table")
            rows = [[td.get_text(" ", strip=True) for td in tr.find_all("td")]
                    for tr in table.find_all("tr") if tr.find("td")]
            yield page, h3.get_text(strip=True), rows


def parse_target(text):
    """'10' → reps; '40s' / '2 min' → time; 'Lap Button' → lap press. '/side' or 'each' is kept as a note."""
    t = text.strip().lower()
    if t == "lap button":
        return "lap.button", None, None
    m = re.fullmatch(r"(\d+)\s*(s|min)?\s*(/\s*side|per side|each)?", t)
    if not m:
        raise ValueError(f"can't read target {text!r}")
    n, unit, side = int(m[1]), m[2], m[3]
    note = text if side else None
    if unit:
        return "time", n * 60 if unit == "min" else n, note
    return "reps", n, note


def parse_rest(text):
    """'90s' / '2 min' → seconds; '—' or empty → None."""
    t = text.strip().lower()
    if t in ("", "—", "-"):
        return None
    m = re.fullmatch(r"(\d+)\s*(s|min)", t)
    if not m:
        raise ValueError(f"can't read rest {text!r}")
    return int(m[1]) * (60 if m[2] == "min" else 1)


def step(order, kind, end, value=None, description=None, exercise=None):
    s = {"type": "ExecutableStepDTO", "stepOrder": order, "stepType": STEP_TYPES[kind],
         "endCondition": END[end], "endConditionValue": value, "description": description}
    if exercise:
        s["category"], s["exerciseName"] = exercise["category"], exercise["name"]
    return s


def build_workout(page, name, rows, exercises):
    steps, order = [], 0
    for i, row in enumerate(rows, 1):
        where = f"{page} / {name} / row {i}"
        try:
            kind, label, target, rest = row
            end, value, note = parse_target(target)
            order += 1
            if kind.lower() in ("warm up", "cool down"):
                steps.append(step(order, kind.lower().replace(" ", ""), end, value, label))
                continue
            m = re.fullmatch(r"repeat\s*[×x]\s*(\d+)", kind.strip().lower())
            if not m:
                raise ValueError(f"unknown step {kind!r} (use Warm up / Cool down / Repeat ×N)")
            if label not in exercises:
                raise ValueError(f"{label!r} is not in garmin/exercises.yaml")
            sets = int(m[1])
            group = {"type": "RepeatGroupDTO", "stepOrder": order, "stepType": STEP_TYPES["repeat"],
                     "numberOfIterations": sets, "smartRepeat": False,
                     "endCondition": END["iterations"], "endConditionValue": sets, "workoutSteps": []}
            order += 1
            description = f"{label} — {note}" if note else label
            group["workoutSteps"].append(step(order, "interval", end, value, description, exercises[label]))
            if (seconds := parse_rest(rest)) is not None:
                order += 1
                group["workoutSteps"].append(step(order, "rest", "time", seconds))
            steps.append(group)
        except ValueError as e:
            sys.exit(f"{where}: {e}")
    return {"workoutName": name, "sportType": STRENGTH,
            "workoutSegments": [{"segmentOrder": 1, "sportType": STRENGTH, "workoutSteps": steps}]}


def push(dry_run):
    exercises = yaml.safe_load((ROOT / "garmin/exercises.yaml").read_text())
    # Build (and so validate) every workout before talking to Garmin.
    workouts = [build_workout(page, name, rows, exercises) for page, name, rows in read_tables()]
    if dry_run:
        print(json.dumps(workouts, indent=2, ensure_ascii=False))
        return
    client = login()
    existing = {w["workoutName"]: w["workoutId"] for w in client.get_workouts(0, 500)}
    for w in workouts:
        print(("update  " if w["workoutName"] in existing else "create  ") + w["workoutName"])
    if input("Proceed? [y/N] ").strip().lower() != "y":
        sys.exit("Nothing changed.")
    for w in workouts:
        if (workout_id := existing.get(w["workoutName"])):
            current = client.get_workout_by_id(workout_id)
            for segment in w["workoutSegments"]:  # keep the workout's own sport (postural may not be "strength")
                segment["sportType"] = current["sportType"]
            current["workoutSegments"] = w["workoutSegments"]
            client.update_workout(workout_id, current)
            print(f"updated  {w['workoutName']}")
        else:
            client.upload_workout(w)
            print(f"created  {w['workoutName']}")
```

Extend the CLI block:

```python
    elif args[:1] == ["push"]:
        push("--dry-run" in args)
```

- [ ] **Step 2: Align the step JSON with what Garmin really stores**

Compare the dry-run output for one workout with the saved original:

```bash
uv run garmin/sync.py push --dry-run | jq '.[] | select(.workoutName=="Pull 1 (Home)") | .workoutSegments[0].workoutSteps' > /tmp/garmin/built.json
jq '.workoutSegments[0].workoutSteps | map(del(.. | .stepId?, .childStepId?) )' "/tmp/garmin/Pull 1 (Home).json" > /tmp/garmin/orig.json
diff <(jq -S . /tmp/garmin/orig.json) <(jq -S . /tmp/garmin/built.json) | head -80
```

Expected differences only in: per-side/each handling and descriptions (decided in Task 5), server-only fields (ids, `preferredEndConditionUnit`, null-valued keys). If the original carries a field Garmin needs that `step()` lacks (e.g. `targetType`), add it to `step()`; if per-side targets were entered differently on Garmin (e.g. reps doubled), change `parse_target` accordingly and update its docstring.

- [ ] **Step 3: Check validation messages**

Run: `uv run garmin/sync.py push --dry-run > /dev/null && echo parsed-all`
Expected: `parsed-all` (all 7 workouts parse).
Then temporarily change one Exercise cell in `site/pull.html` to `Nonexistent`, rerun → expect `pull.html / Pull 1 (Home) / row N: 'Nonexistent' is not in garmin/exercises.yaml`, exit code 1. Revert with `git checkout site/pull.html`.

- [ ] **Step 4: Commit**

```bash
git add garmin/sync.py
git commit -m "Add push (with --dry-run) to garmin/sync.py"
```

### Task 7: Real push to Garmin

- [ ] **Step 1: Ask the user before writing to their Garmin account**

Explain: it will update the 7 existing workouts in place (same IDs, no deletes).

- [ ] **Step 2: User runs the push (confirmation prompt is interactive)**

Ask the user to type: `! uv run garmin/sync.py push`
Expected: 7 lines all starting with `update` (no `create` — a `create` means a name mismatch: answer `N` and fix the `<h3>` text), then after `y`, 7 `updated` lines.

- [ ] **Step 3: Verify**

Run: `uv run garmin/sync.py pull` → still exactly one of each workout name (no duplicates).
Rerun the Task 5 Step 1 `jq` summary against fresh `pull` output for 2 workouts and confirm exercises/reps/rest match the tables.
Ask the user to check one workout in Garmin Connect (web or app) and, after sync, on the watch.

- [ ] **Step 4: Commit any fixes made during verification**

```bash
git add garmin/ site/
git commit -m "Fix Garmin sync details found during first push"
```
(Skip if nothing changed.)

### Task 8: Cleanup

- [ ] **Step 1: Remove the temporary spec and plan**

```bash
git rm -r -q docs
```

- [ ] **Step 2: Make sure README commands match `sync.py`'s docstring**; fix README if they differ.

- [ ] **Step 3: Update memory** — `quartz-site-setup.md` in the user's memory dir is now wrong: replace it with a note that the site is plain HTML in `site/` published by GitHub Pages, and that `garmin/sync.py` syncs workouts. Update the `MEMORY.md` index line.

- [ ] **Step 4: Commit and (after asking) push**

```bash
git add -A
git commit -m "Remove temporary design docs"
```
Ask the user, then `git push origin main`.
