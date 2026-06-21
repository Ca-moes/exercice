# How to Add Exercise GIFs

The routine file references GIF files from this `assets/gifs/` folder. Here's how to populate them with consistent-style visuals.

## Recommended Source: MuscleWiki

[MuscleWiki](https://musclewiki.com) has 2000+ exercises with uniform video style (same camera angles, same background, same models). It's free, no registration.

### How to get GIFs from MuscleWiki:

1. Go to [musclewiki.com](https://musclewiki.com)
2. Search for the exercise (e.g., "dead bug", "wall angels")
3. The exercise page shows a short looping video demonstration
4. Right-click the video → "Save video as..." (saves as .mp4)
5. Convert to GIF using any tool (see below) or just rename to .gif if Obsidian handles it

### Converting MP4 to GIF:

**Option A — Online (quickest):**
- [ezgif.com/video-to-gif](https://ezgif.com/video-to-gif)
- Upload the MP4, set width to 200px, click Convert

**Option B — Command line (if you have ffmpeg):**
```bash
ffmpeg -i input.mp4 -vf "fps=12,scale=200:-1" -loop 0 output.gif
```

## Alternative Source: Gym Visual

[gymvisual.com](https://gymvisual.com) has animated exercise GIFs in a consistent 3D-rendered style. Some are free, full library is paid.

## Newly Needed GIFs (after the Week-3 revision)

Most exercise GIFs are already in `assets/gifs/`. The revision added a few new movements — these filenames are referenced by the routines but still need a GIF:

| File | Exercise | MuscleWiki / search term |
|------|----------|--------------------------|
| `butterfly-stretch.gif` | Butterfly (adductor stretch) — postural | "butterfly stretch" / "seated groin stretch" |
| `supine-figure-4.gif` | Supine figure-4 (glute stretch) — postural | "figure 4 stretch" / "supine piriformis stretch" |
| `childs-pose.gif` | Hands-elevated child's pose — postural | "child's pose" (hands on a chair) |
| `sliding-leg-curls.gif` | Sliding leg curls — Legs 1 | "slider leg curl" / "towel hamstring curl" |
| `b-stance-rdl.gif` | B-stance Romanian deadlift — Legs 2 | "b-stance RDL" / "kickstand RDL" |
| `hip-thrust.gif` | Hip thrust / glute bridge — Legs 2 | "hip thrust" / "glute bridge" |
| `incline-dumbbell-curls.gif` | Incline dumbbell curls — Pull 2 | "incline dumbbell curl" |

The TS900 movements (pull-ups, dips, inverted rows, deficit push-ups) already have GIFs: `pull-ups.gif`, `negative-pull-ups.gif`, `chin-ups.gif`, `dips.gif`, `deficit-push-ups.gif`, `inverted-rows.gif`.

> Removed from the routine (GIFs no longer needed): `90-90-hip-stretch`, `chin-tucks`, `nordic-curls`, `single-leg-rdl`, `wide-push-ups`, `elevated-puppy-pose`. The files can stay in the folder harmlessly.

## Tips

- Keep GIFs small (200px wide) — they're reference visuals, not tutorials
- 2-4 seconds looping is ideal (one full rep cycle)
- If MuscleWiki doesn't have an exact match, the closest variation is fine — the text description is the authority, the GIF is just a visual cue
