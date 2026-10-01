# Training

My home strength + posture training plan.

- **Read it:** https://ca-moes.github.io/exercice (phone) or open `site/index.html` locally.
- **Edit it:** edit the HTML files in `site/` directly. Styling for every page is in `site/style.css`.
- **Publish:** push to `main` — `.github/workflows/deploy.yml` uploads `site/` to GitHub Pages as-is (no build).
- **Exercise animations:** `.webp` files in `site/assets/`, shown inside a card's `<figure class="card-fig">` with `<img src="assets/name.webp" alt="…" loading="lazy">`.

## Missing animations (to get from MuscleWiki)

Save the video from the exercise's page on [musclewiki.com](https://musclewiki.com), convert it, and replace the card's
`<figure class="card-fig is-empty">…</figure>` with `<figure class="card-fig"><img …></figure>`.
MuscleWiki allows non-profit reuse with their branding kept and a link back, so keep the watermark.

    ffmpeg -i input.mp4 -vf "fps=12,scale=480:-1" -loop 0 -c:v libwebp -quality 70 site/assets/<file>.webp

| Page | Exercise | File |
|---|---|---|
| core | Cat-camel (warm-up) | `cat-camel.webp` |
| core | Glute bridge (warm-up) | `glute-bridge.webp` |
| core | Scapular pull-up (warm-up) | `scapular-pull-ups.webp` |
| core | Captain's chair knee raise | `captains-chair-knee-raise.webp` |
| core | Half-kneeling band Pallof press | `pallof-press.webp` |
| core | Body saw | `body-saw.webp` |
| core | Side plank | `side-plank.webp` |
| core | Bird dog | `bird-dog.webp` |
| pull | Incline dumbbell curls | `incline-dumbbell-curls.webp` |
| legs | Sliding leg curls | `sliding-leg-curls.webp` |
| legs | B-stance Romanian deadlift | `b-stance-rdl.webp` |
| legs | Hip thrust / glute bridge | `hip-thrust.webp` |
| postural | Butterfly stretch | `butterfly-stretch.webp` |
| postural | Supine figure-4 | `supine-figure-4.webp` |
| postural | Hands-elevated child's pose | `childs-pose.webp` |

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
