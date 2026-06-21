# Website Customization — Design Spec

**Date:** 2026-06-21
**Branch:** `feat/site-customization` (off `origin/main`)
**Status:** Approved (brainstorming)

## Context

The training vault is live at `ca-moes.github.io/exercice` via Quartz 5, but it's
stock Quartz with only the title changed. The owner wants it to feel like *theirs*
and to be a fast mobile reference. Four areas were chosen (all confirmed via visual
brainstorming): theme/colors, typography, layout decluttering, and identity/home page.

Goal: a cohesive "Clean Slate" look, a trimmed layout suited to a 12-page site, real
page titles, a favicon, and a dashboard-style home page for one-tap access to "today's
workout." This is a presentation/config change — no content rewrites beyond the home
page and title front matter.

## 1. Theme — "Clean Slate"

Edit `quartz.config.yaml` → `configuration.theme`.

**Typography** (`theme.typography`, `fontOrigin: googleFonts` already set):
- `header: Inter Tight`
- `body: Inter`
- `code: IBM Plex Mono` (unchanged)

**Colors** — Quartz semantics: `light`=background, `lightgray`=borders, `gray`=graph/line-numbers,
`darkgray`=body text, `dark`=headings/icons, `secondary`=links/accent, `tertiary`=hover/visited,
`highlight`=internal-link & search bg, `textHighlight`=`==mark==` bg.

`lightMode`:
- light `#fcfcfb` · lightgray `#e8e8e6` · gray `#b3b8b5` · darkgray `#4a524f`
- dark `#1f2a27` · secondary `#2f7d6b` · tertiary `#5aa892`
- highlight `rgba(47,125,107,0.10)` · textHighlight `#f5e49aaa`

`darkMode`:
- light `#16181a` · lightgray `#2a2d30` · gray `#4e5358` · darkgray `#c9ccce`
- dark `#f1f3f4` · secondary `#54b79c` · tertiary `#7fd3bb`
- highlight `rgba(84,183,156,0.15)` · textHighlight `#b3a90288`

The built-in light/dark toggle stays.

## 2. Layout — trim for a 12-page site

Edit `quartz.config.yaml` → `plugins`. Set `enabled: false` on:
- `graph` — a ~12-node graph is gimmicky and eats right-rail space
- `breadcrumbs` — site is flat; only ever shows "Home"
- `content-meta` — removes the per-page created/modified dates **and** reading-time line
  (owner wanted dates gone; reading time is acceptable collateral). Leave the
  `created-modified-date` transformer enabled (harmless; RSS/sitemap may use it).

Keep enabled (no change): `search`, `explorer`, `table-of-contents`, `backlinks`,
`darkmode`, `reader-mode`, `page-title`, `article-title`, `footer`, `content-index`
(RSS/sitemap), `alias-redirects`, `favicon`, `og-image`, `fonts`, the page emitters.

Result: right rail = TOC + backlinks only; no breadcrumb/meta clutter at the top of pages.

## 3. Identity — real titles + favicon

### Page titles
Today the `<title>` (browser tab / bookmark / link preview) is the file slug
(`push-workout`, `index`) because notes have no `title:` front matter and Quartz falls
back to the slug. Fix:

- Add YAML front matter `title:` to each of the 12 content notes (concise names below).
- **Remove the now-redundant first `# H1`** from each body — Quartz's `article-title`
  renders the front-matter title as the top heading, so keeping the H1 would duplicate it.
- Preserve any descriptive suffix from the old H1 (e.g. the muscle list) as a short
  italic lead line under the title so no context is lost.

Titles:
| File | title |
|------|-------|
| index.md | Training Vault |
| push-workout.md | Push Workout |
| pull-workout.md | Pull Workout |
| leg-workout.md | Leg Workout |
| postural-correction.md | Postural Correction |
| weekly-schedule.md | Weekly Schedule |
| equipment-considerations.md | Equipment |
| periodization-notes.md | Periodization |
| push-workout-research.md | Push · Research |
| pull-workout-research.md | Pull · Research |
| leg-workout-research.md | Legs · Research |
| postural-correction-research.md | Postural · Research |

*Implementation note:* if a maintained Quartz v5 community plugin can derive the title
from the first H1, prefer that (zero content edits); otherwise use the front-matter
approach above. Decide during implementation after a quick check.

### Favicon
🏋️ emoji favicon. Implement as an SVG that renders the emoji
(`<text>🏋️</text>` in a small viewBox) placed where Quartz's `favicon` plugin/static
pipeline picks it up (e.g. `quartz/static/icon.*` or `content/static/`). Verify the tab
icon in the local build; fall back to a generated PNG if the SVG emoji doesn't render
consistently.

## 4. Home page — Dashboard landing

Rebuild `content/index.md` (currently a README-style link list) into a scannable
dashboard:

1. **Hero**: "Training Vault" + one-line tagline ("6-day Push / Pull / Legs · home
   strength + posture · ~30 min a session").
2. **Four cards** linking to the routines: Push, Pull, Legs, Postural — each with its
   training days and a 3-word focus. Tappable tiles (the primary mobile shortcut).
3. **Week at a glance**: the existing Mon–Sun schedule table, kept near the top.
4. **Planning & Research**: compact links to weekly-schedule, equipment, periodization,
   and the four research notes.

The card grid needs styling Quartz markdown doesn't provide. Add a custom stylesheet
(Quartz custom CSS, e.g. `quartz/styles/custom.scss` imported by the theme, or the
project's equivalent) defining a `.home-cards` grid + tile styles using the Clean Slate
accent. The home page markdown uses a small inline HTML block for the card grid
(Quartz passes through HTML). Keep it minimal and on-theme.

## Files changed

- `quartz.config.yaml` — theme colors + typography (§1); plugin `enabled` toggles (§2)
- `content/index.md` — rebuilt as the dashboard (§4)
- 12 content notes — add `title:` front matter, drop duplicate H1 (§3)
- custom CSS file (new) — home-card grid + any small theme tweaks
- favicon asset (new) — 🏋️ SVG/PNG

## Verification

- `bun run quartz build` succeeds with no errors and no new broken-link warnings.
- Serve locally (`bun run quartz build --serve`, http://localhost:8080) and confirm:
  - Clean Slate palette in both light and dark; accent on links/callouts; toggle works.
  - Inter Tight headings + Inter body load (no FOUT/fallback).
  - Right rail shows only TOC + backlinks; no graph, breadcrumbs, or date/meta line.
  - Browser tab shows real titles (home = "Training Vault", not "index"); no duplicate
    top heading on any page.
  - 🏋️ favicon appears in the tab.
  - Home page renders the hero + four cards + schedule table; cards link correctly and
    are usable at mobile width.
- Push the branch → open PR → merge to `main` → confirm the live site updates and
  re-check the above on `ca-moes.github.io/exercice` (desktop + phone).

## Out of scope

- Adding the 7 missing exercise gifs (separate pre-existing backlog).
- Custom domain.
- Any content/training changes beyond titles and the home page.
- Re-enabling Dataview on the site (tracking stays in Obsidian).
