#!/usr/bin/env bash
# Convert an exercise video (e.g. from MuscleWiki) to the looping WebP used in site/assets/.
# Needs ffmpeg and img2webp (brew install ffmpeg webp).
# usage: tools/mp4-to-webp.sh input.mp4 site/assets/name.webp [max-seconds] [ffmpeg-crop-filter,]
set -euo pipefail
src=$1; out=$2; dur=${3:-}; crop=${4:-}
tmp=$(mktemp -d)
args=(); [ -n "$dur" ] && args=(-t "$dur")
ffmpeg -v error -y ${args[@]+"${args[@]}"} -i "$src" -an -vf "${crop}fps=12,scale=640:-2:flags=lanczos" "$tmp/f%04d.png"
img2webp -loop 0 -lossy -q 60 -m 6 -d 83 "$tmp"/f*.png -o "$out" >/dev/null 2>&1
printf "%-28s %6s  %s frames\n" "$(basename "$out")" "$(du -h "$out" | cut -f1)" "$(find "$tmp" -name 'f*.png' | wc -l | tr -d ' ')"
rm -rf "$tmp"
