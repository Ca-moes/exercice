# Plain-HTML site + Garmin sync — Design

**Date:** 2026-10-01
**Status:** Approved in conversation; temporary file (delete once implemented — git history keeps it)

## Goal

Keep this repo simple enough to understand at a glance after months away. Two parts, done in order:

1. **Replace the Obsidian vault + Quartz with plain HTML pages** served directly by GitHub Pages.
2. **Add a small Python script that creates/updates workouts in Garmin Connect** from tables in those pages.

## Constraints (from the user)

- Notes are for reading during workouts (laptop: open the file locally; phone: the website). No logging/Dataview/editing in Obsidian is needed.
- No TypeScript/Node tooling. No tests, no extra "best practice" scaffolding.
- Pages must stay written for a human reader.

## Part 1 — Plain-HTML site

### Final repo layout

```
site/
  index.html                 home dashboard (cards + week table)
  push.html  pull.html  legs.html  postural.html
  weekly-schedule.html  equipment.html  periodization.html
  research/push.html  research/pull.html  research/legs.html  research/postural.html
  style.css                  the only stylesheet
  assets/                    existing .webp exercise animations (moved from content/assets/gifs/)
garmin/                      (Part 2)
.github/workflows/deploy.yml publishes site/ to GitHub Pages
README.md                    what's here, how to view, how to run the Garmin script
```

### Source → page mapping

| Source (content/) | Page (site/) |
|---|---|
| index.md | index.html |
| push-workout.md | push.html |
| pull-workout.md (incl. uncommitted "Chin-ups 3×5-8" edit) | pull.html |
| leg-workout.md | legs.html |
| postural-correction.md | postural.html |
| weekly-schedule.md | weekly-schedule.html |
| equipment-considerations.md | equipment.html |
| periodization-notes.md | periodization.html |
| push/pull/leg/postural-correction-research.md | research/push.html, research/pull.html, research/legs.html, research/postural.html |

Dropped (Obsidian-only): `dataview-queries.md`, `templates/`, `assets/HOW-TO-ADD-GIFS.md` (any still-useful guidance goes into README), and the "Tracking lives in Obsidian" note on the home page.

### Conversion rules (one-time, done by hand/throwaway script, then reviewed page by page)

- `[[note]]`, `[[note|label]]`, `[[note#Heading|label]]` → relative `<a href>`; headings get `id`s so anchors resolve.
- Callouts `> [!type] Title` → `<aside class="callout type">` with a title line. Types in use: info, tip, summary, note (plus any others found).
- Images → `<img src="assets/…webp" alt="…" loading="lazy">` (`../assets/` from research pages).
- Tables, emphasis, lists → plain HTML equivalents. Home-page cards keep their existing markup.
- YAML frontmatter `title` → `<title>` and `<h1>`.

### Page shell

Every page: `<!doctype html>`, `lang="en"`, viewport meta, link to `style.css`, small header with "← Home" link (omitted on index), `<main>` with the content. The header is duplicated across pages on purpose — no templating.

### Styling (`style.css`)

- Mobile-first, readable line length, comfortable tap targets.
- Light/dark via `prefers-color-scheme`.
- Palette carried over from the current Clean Slate customization.
- Styles for: callouts (per type), tables (horizontally scrollable on small screens), home cards, images (max-width 100%).

### Deploy

`.github/workflows/deploy.yml`: on push to `main` (and manual dispatch) → checkout → `actions/upload-pages-artifact` with `path: site` → `actions/deploy-pages`. No build step. URL unchanged: `ca-moes.github.io/exercice`.

### Removed from the repo

`quartz/`, `plugins/`, `content/`, `.obsidian/`, `package.json`, `package-lock.json`, `tsconfig.json`, `globals.d.ts`, `index.d.ts`, `quartz.ts`, `quartz.config.yaml`, `quartz.config.default.yaml`, `quartz.lock.json`, `.node-version`, `.npmrc`, `.prettierrc`, `.prettierignore`, `LICENSE.txt` (Quartz's MIT license, not the user's), `docs/` (old Quartz spec; this spec and its plan are deleted at the end too). `.obsidian/` is already git-ignored; the local folder is deleted too. `.conductor/` (empty, untracked, another tool's folder) is left alone. `.gitignore` trimmed to `.DS_Store`.

### Done when

- Every page opens correctly from disk (`open site/index.html`) and on the deployed site.
- All internal links and heading anchors resolve; all images load.
- Pages read well on a phone-width viewport in light and dark mode.

## Part 2 — Garmin sync

### Files

```
garmin/
  sync.py          single uv script (PEP 723 inline deps: garminconnect, pyyaml, beautifulsoup4)
  exercises.yaml   table exercise label → Garmin exercise category/name
```

### Data source: Garmin tables in the pages

Each workout page (push, pull, legs, postural) has a `Garmin Setup` section (`<section id="garmin">`). Inside it, one `<h3>` per Garmin workout whose text is the exact Garmin workout name (e.g. "Pull 1 (Home)"), followed by a `<table>` with columns **Step | Exercise | Target | Rest** — the same columns as today's markdown tables.

Row rules:
- **Step** `Warm up` → warmup step; `Repeat ×N` → repeat group of N × (exercise step + rest step); `Cool down` → cooldown step.
- **Target** `10` → reps; `40s` / `2 min` → time; `Lap Button` → ends on lap press. Other notations ("8 each", "per side") are resolved by matching what the existing Garmin workouts do (seen via `pull`) and documented in the script.
- **Rest** `90s` → timed rest step; `—` → no rest step.

The postural correction page gets its Garmin table written from the existing Garmin workout.

### Commands

- `uv run garmin/sync.py pull` — log in and print existing Garmin workouts (names, steps, exercise category/name). Read-only. Used once to fill `exercises.yaml` and write the postural table; later for spot-checks.
- `uv run garmin/sync.py push [--dry-run]` — parse every Garmin table; build a strength workout per table; if a workout with the same name exists, update it in place, otherwise create it. `--dry-run` prints what would be sent and touches nothing.

### Auth

python-garminconnect's mobile-SSO login (works after Garmin's March 2026 auth change). Email/password prompted on first run, MFA supported; tokens cached in `~/.garminconnect/` (outside the repo). No credentials in git.

### Safety

- Never deletes workouts.
- Validation happens before any upload: an unmapped exercise or unparseable row aborts the whole run with page + workout + row in the message.
- Fallback if Garmin blocks the library again: browser-driven approach (out of scope unless needed).

### Done when

- `pull` lists the current workouts.
- `push --dry-run` parses all workouts (push 1/2, pull 1/2, legs 1/2, postural) with no errors.
- A real `push` updates the existing Garmin workouts without creating duplicates, and they show up correctly in Garmin Connect / on the watch.
