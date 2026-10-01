---
name: Training Vault
description: A personal home-training plan in Otl Aicher's Munich '72 system; static HTML, one stylesheet, swipeable exercise decks.
colors:
  ground: "#ffffff"
  surface: "#eef1f4"
  ink: "#1b2f52"
  ink-2: "#4c5c75"
  rule: "#d3dae2"
  link: "#1e6fb0"
  push: "#f39a45"
  pull: "#5aa9e3"
  legs: "#4cb574"
  postural: "#f5cc3a"
  core: "#b49be0"
  neutral: "#c5cdd5"
  done: "#2e9b58"
  on-field: "#1b2f52"
  ground-dark: "#0e1a2f"
  surface-dark: "#17253f"
  ink-dark: "#eef2f7"
  ink-2-dark: "#a8b5c8"
  rule-dark: "#2a3a57"
  link-dark: "#8cc4f0"
  done-dark: "#5cc98a"
typography:
  display-today:
    fontFamily: "Archivo, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "clamp(3.5rem, 17vw, 8.5rem)"
    fontWeight: 750
    lineHeight: 0.9
    letterSpacing: "-0.04em"
    fontVariation: "'wdth' 95"
  display:
    fontFamily: "Archivo, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "clamp(2.6rem, 11vw, 5rem)"
    fontWeight: 750
    lineHeight: 0.95
    letterSpacing: "-0.03em"
    fontVariation: "'wdth' 95"
  headline:
    fontFamily: "Archivo, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "clamp(1.45rem, 4vw, 1.9rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Archivo, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
    fontVariation: "'wdth' 85"
  body:
    fontFamily: "Archivo, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: "'tnum'"
  label:
    fontFamily: "Archivo, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
    letterSpacing: "0.08em"
  mono:
    fontFamily: "ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "0.82rem"
    lineHeight: 1.65
rounded:
  none: "0"
  circle: "50%"
spacing:
  pad: "clamp(1rem, 5vw, 2.5rem)"
  col: "44rem"
  reading: "56rem"
  wide: "76rem"
  card-gap: "0.75rem"
  card-body: "1rem 1.1rem 1.25rem"
components:
  band:
    backgroundColor: "{colors.push}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.none}"
    padding: "0.75rem clamp(1rem, 5vw, 2.5rem) 1.6rem"
  card:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    width: "min(86vw, 30rem)"
  card-num:
    backgroundColor: "{colors.push}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.circle}"
    size: "2.75rem"
  card-num-done:
    backgroundColor: "{colors.done}"
    textColor: "{colors.ground}"
    rounded: "{rounded.circle}"
    size: "2.75rem"
  button-done:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    height: "3.25rem"
  button-done-pressed:
    backgroundColor: "{colors.done}"
    textColor: "{colors.ground}"
    rounded: "{rounded.none}"
    height: "3.25rem"
  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.45rem 0.85rem"
  chip-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    rounded: "{rounded.none}"
    padding: "0.45rem 0.85rem"
  pip:
    backgroundColor: "transparent"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.circle}"
    size: "2.1rem"
  pip-current:
    backgroundColor: "{colors.push}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.circle}"
    size: "2.1rem"
  callout:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.9rem 1.1rem 1rem"
  today:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    rounded: "{rounded.none}"
---

# Design System: Training Vault

All tokens live as custom properties in `:root` of `site/style.css` (dark values in its `prefers-color-scheme: dark` block). That file is the single source; this document describes it and is the editing guide for `site/*.html`. Plain HTML, no build step, relative `.html` links so pages work from `file://`.

## Overview

**Creative North Star: "The Olympic Programme"**

The plan is set like Otl Aicher's Munich 1972 identity: a white ground, dark-navy ink (never black), one flat colour field per section, geometric stick-figure pictograms, a Univers-like grotesk (Archivo, using its width axis) with lowercase display. Forms are squares and circles only. There are no shadows, no gradients as decoration, and no rounded rectangles.

Each workout session is a horizontal deck of exercise cards (scroll-snap), not a long document. Research and reference pages read as ranked lists, intensity meters and status dots under a sticky chip index. Density is phone-first: one card fills a phone viewport with the next card's edge peeking at the right; on wide screens about two cards show.

The site works fully without JavaScript. `site/site.js` only enhances: session tabs, deck Prev/Next and numbered pips (a "3 / 9" counter on phones when a deck has more than 5 cards), "Mark done" per card (stored per page per day in localStorage), reopening on the last card viewed in the past 3 hours, chip scroll-spy, and the home "today" block.

**Key Characteristics:**
- One flat colour field per section; ink on every field is the same navy (`--on-field`) in light and dark mode.
- Corners are either square or a full circle; nothing in between.
- Flat surfaces: hierarchy comes from colour fields, 1px rules, a 6px top bar on cards, and type weight. No shadows.
- Display headings are rendered lowercase by CSS; uppercase is only for small tracked labels.
- Numbers are tabular everywhere (`font-variant-numeric: tabular-nums` on body).

## Colors

A white-and-navy ground carrying four saturated section fields plus a silver neutral; colour identifies *where you are*, never decorates.

### Primary (section fields)
- **Munich Orange** (`push`): Push field: band, card top bar, numeral circles, current pip, section rules.
- **Munich Sky** (`pull`): Pull field; also keys `callout.info` and is the meter fallback.
- **Munich Green** (`legs`): Legs field; also keys `callout.tip` and the home "today" label fallback.
- **Munich Yellow** (`postural`): Postural field; also keys `callout.note` and text `::selection`.
- **Light Violet** (`core`, `#b49be0`): Core field (navy text on it ≈ 5.9:1).
- **Silver** (`neutral`): Field for non-section pages (weekly schedule, equipment, periodization), the default callout key, changelog rule, `status-off` ring, scrollbar thumb.

Section colours are **not** redefined in dark mode; the fields stay identical and keep navy ink.

### Secondary
- **Done Green** (`done`, dark `done-dark`): Only for completion: the flooded numeral circle, pressed "Done" button, done pips, and `status-ok` dots. Deliberately darker than Legs green so "done" never reads as "legs".
- **Link Blue** (`link`, dark `link-dark`): Body links and the 3px focus ring.

### Neutral
- **Ground** (`ground` / `ground-dark` deep navy): page and card background.
- **Silver Field** (`surface` / `surface-dark`): chips, tags, callouts, week-day cells, empty-figure placeholder, changelog, `pre`.
- **Navy Ink** (`ink` / `ink-dark`): text; also the inverted "today" block and active chip background.
- **Slate** (`ink-2` / `ink-2-dark`): secondary text, labels, table headers, list markers.
- **Hairline** (`rule` / `rule-dark`): every 1px border and divider.
- **Field Ink** (`on-field`): text and pictograms on any colour field; fixed navy in both modes.

### Named Rules
**The One Field Rule.** A page has exactly one section colour, set once as `--field` (by `data-section` on workout pages, by the `band-*` class on reading pages). Components read `var(--field)`; they never name a section colour directly. The only places that name all colours at once are the home field list, the week grid, and callout keys.

**The Navy-On-Field Rule.** Text on a colour field is always `--on-field` navy, never white, in both modes. Any new section colour must hold at least 4.5:1 against `#1b2f52`.

**The Green Means Done Rule.** `--done` is reserved for completion state. Never use it as a section colour or for decoration.

## Typography

**Display / Body Font:** Archivo variable (self-hosted `site/fonts/archivo.woff2` + `archivo-italic.woff2`, weight 100–900, width 62–125%), with `system-ui` fallback.
**Mono:** system monospace stack (`code`, `pre`).

**Character:** One grotesk family across the whole ramp; contrast comes from weight (400 / 600 / 650 / 700 / 750) and width (`font-stretch` 95% for display, 85% for card titles).

### Hierarchy
- **Display-today** (750, `clamp(3.5rem, 17vw, 8.5rem)`, 0.9): home "today" session name only.
- **Display** (750, `clamp(2.6rem, 11vw, 5rem)`, 0.95, lowercase): workout band `h1`. Reading bands use `clamp(2rem, 8vw, 3.75rem)`; home `h1` and field names use `clamp(2rem, 8vw, 3.25rem)` and `clamp(2.25rem, 9vw, 4rem)`.
- **Headline** (700, `clamp(1.45rem, 4vw, 1.9rem)`, 1.1): `h2`. Panel, about and home `h2` are lowercase via CSS.
- **Title** (700, 1.4rem, width 85%): card `h3` exercise name. Generic `h3` is 1.2rem.
- **Body** (400, 1.0625rem, 1.55): prose; measure capped at `--col` (44rem). Card dose 1.15rem/650 in `ink-2`.
- **Label** (700, 0.72rem, 0.08em, UPPERCASE): `th`, `band-facts dt`, `card-label`, `card-tags`, `tab-day`, `week-day`, `field-days`.

### Named Rules
**The Lowercase Display Rule.** Large headings are lowercased by CSS (`text-transform: lowercase`), so write them in normal Title Case in the HTML ("Push Workout" renders "push workout"). Never type them lowercase by hand and never uppercase display text.

**The Label Rule.** Uppercase tracked type is only for short functional labels naming the data next to them (a column, a fact, a day). It never appears as a decorative line above a heading.

## Layout

- **Containers:** `main` and band content max `--wide` (76rem), side padding `--pad` (`clamp(1rem, 5vw, 2.5rem)`); prose/about/reference max `--col` (44rem); reading panels max 56rem.
- **Full-bleed fields:** bands, home fields and the "today" block run edge to edge while their content aligns with the page column via `padding-inline: max(var(--pad), calc(50vw - var(--wide) / 2 + var(--pad)))`. Reuse that expression for any new full-bleed strip.
- **Deck:** the track is a single-row grid, card width `min(86vw, 30rem)`, gap 0.75rem, `scroll-snap-type: x mandatory`, scrollbar hidden. JS sets the track height to the tallest card in view. At ≥60rem cards are `(100% - 0.75rem) * 0.44` wide and the deck aligns to the column.
- **Breakpoints:** ≤36rem (compact band, facts collapse into one dotted line, week grid 4 columns, long decks swap pips for a counter); ≤40rem (`table.data` collapses into labelled rows); ≥60rem (tabs size to content, deck to column).
- **Touch:** every interactive target is ≥2.75rem (44px); pips get an invisible 0.35rem hit extension.
- **Rhythm:** paragraphs/lists 1rem bottom; sections separate by 2.75–3.5rem.

## Elevation & Depth

Entirely flat. No `box-shadow` anywhere. Depth and grouping come from colour fields, the silver `surface`, 1px `rule` hairlines, the 6px `--field` top bar on cards and week cells, and the 2px `ink` rule under table headers. The only layering is the sticky chip bar (`z-index: 5`, opaque `ground` background with a bottom hairline).

### Named Rules
**The Flat Field Rule.** If something needs to stand out, give it a field colour, a heavier rule, or inverted ink; never a shadow, blur or gradient.

## Shapes

Two shapes only: squares (radius 0) for fields, cards, chips, tags, callouts, buttons and tables; full circles (50%) for numerals, pips, deck arrows, the muscle dot, callout keys and status dots. The optional-exercise numeral is a 2px dashed circle. Disclosure chevrons are a CSS-drawn bordered square rotated -45° (closed) / 45° (open). The intensity meter is six 0.85rem squares with 0.15rem gaps (CSS mask).

### Pictograms

Four authored inline SVGs, one per section, in Aicher's stick-figure style. Grammar: `viewBox="0 0 48 48"`, `fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"`, a head as `<circle r="4.5" class="fill">` (filled via `.picto .fill`), limbs as straight `<line>` segments, a floor line at `y=45` (x 2–46) where the figure stands or lies. Colour is inherited (`on-field` navy). Size via `.picto` (`clamp(3.25rem, 9vw, 5.5rem)`; 4.5rem in home fields, 2.75rem on phones). Always `aria-hidden="true"`. Limb angles are not strictly 45/90°; keep new figures to a few straight strokes and the same head size and stroke.

Canonical copies live in `site/index.html` (home fields) and are repeated verbatim in each section's band:

```html
<!-- push -->
<svg class="picto" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><line x1="2" y1="45" x2="46" y2="45"/><circle cx="9" cy="22" r="4.5" class="fill"/><line x1="15" y1="27" x2="41" y2="37"/><line x1="17" y1="28" x2="17" y2="44"/><line x1="41" y1="37" x2="44" y2="44"/></svg>
<!-- pull -->
<svg class="picto" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><line x1="6" y1="5" x2="42" y2="5"/><line x1="17" y1="5" x2="21" y2="21"/><line x1="31" y1="5" x2="27" y2="21"/><circle cx="24" cy="15" r="4.5" class="fill"/><line x1="24" y1="22" x2="24" y2="34"/><line x1="24" y1="34" x2="19" y2="44"/><line x1="24" y1="34" x2="29" y2="44"/></svg>
<!-- legs -->
<svg class="picto" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><circle cx="21" cy="7" r="4.5" class="fill"/><line x1="21" y1="14" x2="21" y2="27"/><line x1="21" y1="27" x2="32" y2="30"/><line x1="32" y1="30" x2="32" y2="44"/><line x1="21" y1="27" x2="13" y2="36"/><line x1="13" y1="36" x2="5" y2="33"/><line x1="2" y1="45" x2="46" y2="45"/></svg>
<!-- postural -->
<svg class="picto" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><circle cx="19" cy="9" r="4.5" class="fill"/><line x1="20" y1="16" x2="23" y2="30"/><line x1="20" y1="18" x2="30" y2="7"/><line x1="23" y1="30" x2="34" y2="30"/><line x1="34" y1="30" x2="34" y2="44"/><line x1="23" y1="30" x2="14" y2="44"/><line x1="14" y1="44" x2="4" y2="44"/></svg>
```

Small UI icons (`.icon`, 1rem) use a 16-unit viewBox, stroke 1.8, round caps/joins; the only one is the back/prev chevron (`M10 3 5 8l5 5`), mirrored with `scaleX(-1)` for Next.

## Components

Copy these skeletons when adding content. Pages under `research/` prefix asset paths with `../`.

### Page shells

Every page head: `<link rel="preload" href="fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>`, `style.css`, `icon.png`, `<script src="site.js" defer></script>`.

- Workout page: `<body class="page-workout" data-section="push">`
- Reading page (research, weekly schedule, equipment, periodization): `<body class="page-reading">`, section colour taken from the band class.
- Home: `<body class="page-home">`

### Band (page header)

Full-bleed colour field. `band-push|pull|legs|core|postural` for section pages, `band-neutral` (no pictogram) for general pages.

```html
<header class="band band-push">
<div class="band-inner">
<a class="back" href="index.html"><svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg><span>training vault</span></a>
<div class="band-title"><!-- section picto SVG --><h1>Push Workout</h1></div>
<p class="band-muscles">Chest · Front Delts · Lateral Delts · Triceps</p>   <!-- workout pages -->
<dl class="band-facts">                                                       <!-- workout pages -->
<div><dt>Days</dt><dd>Monday (Push 1) + Thursday (Push 2)</dd></div>
<div><dt>Duration</dt><dd>~20–22 min each</dd></div>
<div><dt>Research</dt><dd><a href="research/push.html">Push · Research</a></dd></div>
</dl>
<!-- reading pages use instead: <p class="band-lede">…</p> -->
</div>
</header>
```

On phones the first fact (Days) is hidden on Push/Pull/Legs pages (their tabs show the weekday); keep Days first there. Postural and Core have no Days fact, so nothing is hidden.

### Session tabs (workout pages)

One tab per session; `href` = the deck's `id`; `data-day` = JS weekday (0 Sun … 6 Sat) so today's session is preselected. Active tab: 4px `--field` underline and a 14% field tint.

```html
<main>
<nav class="tabs" aria-label="Sessions">
<a class="tab" href="#push-1-shoulders-triceps-long-head" data-day="1"><span class="tab-name">Push 1 <span class="tab-day">Mon</span></span><span class="tab-sub">Shoulders + Triceps Long Head</span></a>
<a class="tab" href="#push-2-chest-stretch-dips" data-day="4"><span class="tab-name">Push 2 <span class="tab-day">Thu</span></span><span class="tab-sub">Chest Stretch + Dips</span></a>
</nav>
```

### Swipe deck and exercise card (signature)

Character: one exercise per card, animation first, numbered cues, one big "Mark done". Card: `ground` background, 1px `rule` border, 6px `--field` top bar, square corners. Card `id` = `<deck-short>-<n>` and must be unique on the page (pips, resume and done marks use it). `data-status`: `anchor`, `new` (informational), `optional` (renders a dashed numeral circle). Keep `.card-num` text equal to the card's position. The pips `ol` stays empty (JS fills it).

```html
<section class="deck" id="push-1-shoulders-triceps-long-head" aria-label="Push 1 — Shoulders + Triceps Long Head">
<ol class="track">
<li class="card" id="push-1-1" data-status="anchor">
<figure class="card-fig"><img alt="Pike Push-ups" loading="lazy" src="assets/pike-push-ups.webp"/></figure>
<div class="card-body">
<header class="card-head"><span class="card-num">1</span><h3>Pike Push-ups</h3><p class="card-dose">3×8-10</p></header>
<p class="card-tags"><span>Anchor</span></p>
<p class="card-muscle">Front Delts + Upper Chest + Triceps</p>
<p class="card-feel"><strong>Feel:</strong> Shoulders burning. Hips stay high the whole time.</p>
<p class="card-label">How to</p>
<ol class="cues"><li>First cue</li><li>Second cue</li><li>Third cue</li></ol>
<p><strong>Key cue:</strong> One sentence that matters most.</p>
<details class="card-more"><summary>Notes</summary>
<p>Longer progression or rationale.</p>
</details>
<button class="done" type="button" hidden aria-pressed="false">Mark done</button>
</div>
</li>
<!-- more li.card … -->
</ol>
<div class="deck-nav"><button class="deck-prev" type="button" hidden aria-label="Previous exercise"><svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button><ol class="pips"></ol><button class="deck-next" type="button" hidden aria-label="Next exercise"><svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>
</section>
```

- Optional parts: `card-tags`, `card-feel`, the Key cue paragraph, `details.card-more`. Order is fixed as above.
- Two images side by side: put two `<img>` in one `card-fig` (it switches to a 2-column grid).
- No animation yet: `<figure class="card-fig is-empty"><figcaption>No animation yet</figcaption></figure>` (16:9 silver placeholder).
- `card-fig` keeps a white background in dark mode because the animations have white backgrounds.
- Done state (JS): `.is-done` floods the numeral circle green with a 420ms `clip-path` circle reveal (`cubic-bezier(0.16, 1, 0.3, 1)`), the button fills `done`, and the deck advances to the next card after 450ms. Disabled under `prefers-reduced-motion`.

### About and reference (below the decks, workout pages)

```html
<section class="about" aria-labelledby="about-push">
<h2 id="about-push">About push workout</h2>
<p>…</p>
</section>
<section class="reference" aria-label="Reference">
<details class="ref" id="progression-roadmap"><summary>Progression Roadmap</summary>
<!-- any content: p, ul, table, callout -->
</details>
</section>
```

### Garmin block (hard constraint)

`garmin/sync.py` parses this. Every workout page keeps exactly one `<section id="garmin">`, inside the last `details.ref`. Per Garmin workout: one `<h3>` whose text is the **exact Garmin workout name**, immediately followed by a sibling `<table>` with columns **Step | Exercise | Target | Rest**. Plain `<table>` (no `data`/`ranked` class), no wrappers between `h3` and `table`. The `h2` is visually hidden by CSS but must stay.

```html
<details class="ref"><summary>Garmin Connect Setup</summary>
<section id="garmin">
<h2 id="garmin-connect-setup">Garmin Connect Setup</h2>
<h3 id="push-1-home">Push 1 (Home)</h3>
<table>
<thead>
<tr><th>Step</th><th>Exercise</th><th>Target</th><th>Rest</th></tr>
</thead>
<tbody>
<tr><td>Warm up</td><td>2 min arm circles + 10 easy push-ups</td><td>Lap Button</td><td>—</td></tr>
<tr><td>Repeat ×3</td><td>Pike Push Up (custom)</td><td>10</td><td>90s</td></tr>
</tbody>
</table>
</section>
</details>
```

### Reading page: chips and panels

Sticky chip index; one chip per `section.panel`, `href` = the panel `h2` `id` (JS highlights the chip of the section in view). Panel `h2` gets a 4px `--field` underline and is lowercased by CSS.

```html
<nav class="chips" aria-label="On this page"><a href="#exercise-rankings">Exercise Rankings</a><a href="#sources">Sources</a></nav>
<main>
<section class="panel">
<h2 id="exercise-rankings">Exercise Rankings</h2>
<h3>Sub-heading</h3>
<p>…</p>
</section>
</main>
```

Chips: silver squares, ink text; hover/current inverts to ink background, ground text.

### Tables

All `td` in `ranked` and `data` tables carry `data-label="<column header>"` (used for phone labels).

- **Plain `<table>`**: hairline rows, 2px ink rule under uppercase headers. Used for Garmin and small reference tables.
- **`table.ranked`** (first column is Rank): becomes a list; rank in a silver circle, rank 1 in the field colour; column 2 bold. Columns labelled "Resistance curve" or "Time-under-stretch" get an inline label prefix.
- **`table.data`**: normal table on wide screens; ≤40rem each row becomes a block, first cell bold, other cells prefixed by their `data-label`. Add **`has-num`** when the first column is a row number (`#`): it hides the number and makes column 2 the row title.
- **Intensity meter**: `<td class="intensity" data-label="Intensity"><span aria-hidden="true" class="meter" style="--lvl:6"></span>Very High</td>`. `--lvl` is 1–6 filled squares in `--field`; always keep the text word.
- **Status dot**: `<td class="status status-ok" data-label="Status">Primary</td>`. `status-ok` = done-green dot (covered), `status-warn` = orange dot (optional/partial), `status-off` = open silver ring (not included). Always keep the text word.

```html
<table class="ranked">
<thead><tr><th>Rank</th><th>Exercise</th><th>Intensity</th><th>Why</th></tr></thead>
<tbody>
<tr>
<td data-label="Rank">1</td>
<td data-label="Exercise"><strong>Pull-ups / chin-ups</strong> (requires bar)</td>
<td class="intensity" data-label="Intensity"><span aria-hidden="true" class="meter" style="--lvl:6"></span>Very High</td>
<td data-label="Why">One-line reason.</td>
</tr>
</tbody>
</table>
```

### Sources and changelog

```html
<section class="panel">
<h2 id="sources">Sources</h2>
<ul class="sources">
<li><a href="https://pubmed.ncbi.nlm.nih.gov/26422610/">Inverted Row EMG Activation — PubMed</a><span class="src-domain">pubmed.ncbi.nlm.nih.gov</span></li>
</ul>
</section>
<section class="panel changelog">
<h2 class="changelog-head" id="revision-week-3-2026-06-14">Revision — Week 3 (2026-06-14)</h2>
<ul><li><strong>What changed.</strong> Why.</li></ul>
</section>
```

Changelog panels sit on the silver `surface` with a silver (not field) underline. Add a chip for each.

### Callouts

Silver block with a coloured key dot before the title. Variants map to fixed colours: `info` = pull blue, `tip` = legs green, `warning` = push orange, `note` = postural yellow; no variant = silver.

```html
<aside class="callout warning">
<p class="callout-title">Right inner-groin</p>
<p>Body text.</p>
</aside>
```

### Home

`.today` (inverted ink block, filled by JS from the week grid), `nav.fields` (one full-bleed `a.field band-<section>` per section: picto, `field-name`, `field-days`, `field-focus`), `ol.week` (7 cells, `li.week-<section>` with `data-day`, 6px field top bar; today's cell fills with its field), `.home-ref` (auto-fit link lists).

### Adding a section (e.g. "Core")

1. `style.css` `:root`: add `--core: #……;` (a flat Munich-style colour, distinct from the four fields and from `--done`, ≥4.5:1 with `#1b2f52`). Not chosen yet. No dark-mode override.
2. `style.css`, next to the existing rules:
   ```css
   .band-core { --field: var(--core); }
   .page-workout[data-section="core"], .page-reading:has(.band-core) { --field: var(--core); }
   .week-core { --field: var(--core); }
   ```
3. Draw a pictogram on the 48-unit grid (stroke 5, round caps, `r="4.5"` filled head, floor at y=45) and use it in both the home field and the band.
4. `core.html`: copy a workout page, set `data-section="core"`, `band band-core`, tabs with `data-day`, decks, and the `section#garmin` block if it syncs to Garmin. Optional `research/core.html` with `band band-core`.
5. `index.html`: add `<a class="field band-core" href="core.html">…</a>` in `nav.fields`; if Core takes a weekday, use `li.week-core` in the week grid.
6. `site.js` needs no change. On phones the first band fact (Days) is hidden on every workout page except postural; Core is already excluded; a new section without a Days fact needs the same `:not([data-section=…])` added to those two selectors in the 36rem media query.

### Raster provenance

- `site/icon.png` (180×180): authored, not generated. SVG of five flat horizontal stripes in the section colours (push, pull, legs, core, postural), square, rasterised with headless Chrome via Playwright; origin recorded in the PNG `tEXt` chunk `impeccable:prompt`.
- `site/assets/*.webp`: pre-existing exercise animations from the former Obsidian vault, converted GIF→WebP in commit a506ad6, originally sourced per the old HOW-TO note (which recommended MuscleWiki). Per file:
  - MuscleWiki watermark: band-pull-aparts, bulgarian-split-squats, chin-ups, concentration-curls, dead-bug, deficit-push-ups, dips, dumbbell-shrugs, fire-hydrants, inverted-rows, lateral-raises, overhead-band-extension, pull-ups, push-ups, side-lying-leg-raises, single-leg-calf-raises, sissy-squats, supine-hamstring-stretch, wall-angels.
  - Active Life watermark: prone-ytw-raises.
  - "NML" (Nourish Move Love) watermark: couch-stretch.
  - makeagif.com watermark + caption: worlds-greatest-stretch.
  - No visible watermark, source unknown: cossack-squats, negative-pull-ups, pike-push-ups.
  - No animation yet (`card-fig is-empty`): incline dumbbell curls, sliding leg curls, B-stance RDL, hip thrust, butterfly stretch, supine figure-4, hands-elevated child's pose.
- New animations: WebP in `site/assets/`, kebab-case exercise name, white background; add a line here with its source.

## Do's and Don'ts

### Do:
- **Do** set the section colour once (`data-section` / `band-*`) and let components read `var(--field)`.
- **Do** keep text on colour fields navy (`--on-field`) in both modes.
- **Do** use only square (0) or circular (50%) shapes; full circles for numerals, pips, dots.
- **Do** keep every tap target ≥2.75rem (44px).
- **Do** keep the text word next to every meter and status dot; colour is never the only signal.
- **Do** add `data-label` to every cell of `ranked` and `data` tables.
- **Do** keep `section#garmin > h3 + table` (Step | Exercise | Target | Rest) intact on every workout page.
- **Do** write display headings in Title Case and let CSS lowercase them.

### Don't:
- **Don't** add shadows, blurs, decorative gradients, or rounded-rectangle corners.
- **Don't** use pure black for ink or white text on a section field.
- **Don't** use `--done` green for anything except completion.
- **Don't** put small uppercase labels above headings as decoration; uppercase is for column, fact and day labels only.
- **Don't** use emoji or text glyphs as icons; draw icons as stroked SVG on the 16-unit (UI) or 48-unit (pictogram) grid.
- **Don't** hard-code a section hex inside a component rule; add a `--field` mapping instead.
- **Don't** add a second stylesheet, a framework, or absolute links; pages must work from `file://`.

## Garmin tables: supersets

A superset (two exercises back to back, then one rest) is written as consecutive rows with the same Step value `Superset ×N`; only the last row of the pair carries the Rest. Example (core.html):

| Step | Exercise | Target | Rest |
|---|---|---|---|
| Superset ×3 | Captain's Chair Knee Raise | 10 | — |
| Superset ×3 | Half-kneeling Pallof Press | 8/side | 45s |

`garmin/sync.py` turns each run of `Superset ×N` rows into one repeat group of N iterations containing every exercise in order, then the rest.

## Pictogram: core

Side plank on the 48-unit grid: floor line, body diagonal from feet (6,40) to shoulder (34,25), supporting upper arm vertical to the floor with forearm along it, top arm straight up, filled head circle at (39,16).
