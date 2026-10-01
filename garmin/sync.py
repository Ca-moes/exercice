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
