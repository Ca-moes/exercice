# Training

My home strength + posture training plan.

- **Read it:** https://ca-moes.github.io/exercice (phone) or open `site/index.html` locally.
- **Edit it:** edit the HTML files in `site/` directly. Styling for every page is in `site/style.css`.
- **Publish:** push to `main` — `.github/workflows/deploy.yml` uploads `site/` to GitHub Pages as-is (no build).
- **Exercise animations:** `.webp` files in `site/assets/`, shown inside a card's `<figure class="card-fig">` with `<img src="assets/name.webp" alt="…" loading="lazy">`.

## Adding an animation

Every card has one now. To add or replace one, save the video from the exercise's page on
[musclewiki.com](https://musclewiki.com), convert it, and point the card's `<img>` at it.
MuscleWiki allows non-profit reuse with their branding kept and a link back, so keep the watermark.
Note the source in DESIGN.md → asset provenance.

    tools/mp4-to-webp.sh ~/Downloads/clip.mp4 site/assets/<file>.webp          # whole clip
    tools/mp4-to-webp.sh ~/Downloads/clip.mp4 site/assets/<file>.webp 10       # first 10 s only

## Garmin Connect

`garmin/sync.py` creates/updates my Garmin workouts from the "Garmin Connect Setup" tables
in the workout pages. Needs [uv](https://docs.astral.sh/uv/).

    uv run garmin/sync.py pull                    # list workouts on Garmin
    uv run garmin/sync.py pull "Pull 1"           # show one workout in full (JSON)
    uv run garmin/sync.py push --dry-run          # show what would be uploaded
    uv run garmin/sync.py push                    # create/update on Garmin (asks first), then send to the watch
    uv run garmin/sync.py push "Core"             # the same for one workout
    uv run garmin/sync.py send                    # send the workouts to the watch again

Run it once in a terminal to log in (Garmin email/password + MFA code); the login is saved in
`~/.garminconnect/`. Each table row names a card on the same page: the watch note is built from
that card's dose and cues, and the card title is mapped to Garmin's exercise list in
`garmin/exercises.yaml` — add a line there when a table uses a new exercise. Table notation is in
DESIGN.md → "Garmin tables: notation". `push` never deletes anything on Garmin. Workouts go to the Forerunner 265 (`WATCH` in sync.py)
and land on it at its next sync with the phone.
