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
