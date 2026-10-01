---
version: 1
slug: "site-index-html"
primary_target: "site/index.html"
related_targets: ["site/push.html","site/pull.html","site/legs.html","site/postural.html","site/research/pull.html"]
---

# Surface brief — training site (all pages in site/)

Scope: whole static site (home, 4 workout pages, weekly schedule, equipment, periodization, 4 research pages). Mode: Read.
Audience/job: the owner alone, on a phone mid-workout, finding the exercise he's on and checking form cues + the animation in seconds; research read at home.
Constraints: plain HTML/CSS + one small progressive-enhancement JS, works from file://, keep `section#garmin > h3 + table` markup for garmin/sync.py, never drop training content.
History: round 1 "Anatomy Atlas" (seed a5bba618, idx 7) was built and rejected by the user ("reads like markdown in HTML"); round 2 re-roll chose Munich '72; surface round (seed d0767acc) locked the Swipe Deck for workout pages. Research pages: designed in-world without a separate round (user to review).

## Direction contract

THESIS: The training plan as an Olympic programme in Otl Aicher's Munich '72 system; each session a swipeable deck of exercise cards, refusing the long scrolling document.
OWN-WORLD: White ground, dark-navy ink (no black), flat section colour fields: push orange, pull light blue, legs green, postural yellow, silver neutrals; geometric pictograms on a 45/90° grid; Univers-like grotesk (Archivo widths) with lowercase display; square fields and circles, no shadows, no rounded cards.
STORY: He taps today's section, the session tab is preselected, swipes card to card watching each animation and its numbered cues, marks each done; the deck reopens where he left it. At home, research reads as ranked lists, meters and status chips, not tables of prose.
FIRST VIEWPORT: Workout page: full-bleed section colour band (pictogram, lowercase name, muscles), session tabs, then the first exercise card filling the screen with the next card's edge peeking at right.
FORM: Swipe Deck, dealt index 3 of my structural list (lead), surface seed d0767acc; world Munich '72, re-roll round 1 index 3 of seed a5bba618.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
