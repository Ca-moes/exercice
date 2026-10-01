# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

One person: the owner (André). Uses it as a personal training reference — mostly on his phone in the middle of a home workout, sometimes on a laptop by opening the files locally. The public URL exists only for convenience.

## Product Purpose

A personal home-training plan: a 6-day Push / Pull / Legs split plus a daily ~7-minute postural-correction routine, with the research behind each choice. Success: mid-workout, he can find the exercise he's on and check how to do it correctly (form cues + the exercise animation) in seconds, then put the phone down.

## Operating Context

- Mid-workout, phone in hand or propped up, between sets, possibly sweaty, short glances.
- Sets/reps are already on his Garmin watch (workouts synced from the "Garmin Connect Setup" tables via `garmin/sync.py`), so the site's main job during a workout is **form cues + animation**, not numbers.
- Research pages and the weekly overview are read at home, at leisure.
- Visits the repo rarely; must be understandable after months away.

## Capabilities and Constraints

- Static site: hand-written HTML pages in `site/` + one stylesheet `site/style.css`; no build step, no framework, no Node tooling. Published by GitHub Pages from `site/` (`ca-moes.github.io/exercice`). Pages must also work opened from disk (`file://`), so links are relative and end in `.html`.
- Pages: home (`index.html`), four workout pages (`push`, `pull`, `legs`, `postural`), `weekly-schedule`, `equipment`, `periodization`, and four research pages in `research/`.
- Each workout page ends with a `<section id="garmin">` containing one `<h3>` (exact Garmin workout name) + `<table>` (Step | Exercise | Target | Rest) per Garmin workout. `garmin/sync.py` parses this markup — it must keep that structure.
- Exercise animations are `.webp` files in `site/assets/`; some exercises have none yet.
- Content is maintained mostly with AI help; keep markup simple and consistent so pages stay easy to edit.

## Evidence on Hand

- All content in `site/*.html` (converted from the former Obsidian vault): exercise instructions, callouts ("Feel", targets, tips), weekly schedule, equipment, periodization, research with source links.
- 25 exercise animations in `site/assets/`; favicon `site/icon.png` (white dumbbell on sage-teal).
- No photos, logos, or other brand assets beyond these.

## Product Principles

1. The workout moment wins: an exercise's form cues and animation must be reachable and readable in seconds on a phone.
2. Simple over clever: plain HTML/CSS a person can understand and edit after months away; no tooling.
3. Content is the product: never drop or rewrite training content for the sake of layout.
4. Works offline from disk as well as online.

## Accessibility & Inclusion

Readable at arm's length on a phone in varied light (light and dark mode); large tap targets usable with sweaty hands.
