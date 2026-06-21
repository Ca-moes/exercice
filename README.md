# Training Vault

A personal home strength + postural-health training system, published as a
website with [Quartz 5](https://quartz.jzhao.xyz) and hosted on GitHub Pages.

**Live site:** https://ca-moes.github.io/exercice

## How it works

- The notes live in [`content/`](content/) — open **that folder** as an Obsidian
  vault to edit. The home page is `content/index.md`.
- Everything else at the repo root is Quartz (the static-site generator) and is
  rarely touched.
- `content/dataview-queries.md` and `content/templates/` are Obsidian-only
  (tracking/logging) and are excluded from the published site via
  `ignorePatterns` in `quartz.config.yaml`.

## Local preview

Requires Node v22+ (and Bun, optionally, for installs/commands):

```bash
npm ci                      # or: bun install
npx quartz plugin install   # fetch plugins from quartz.lock.json
npx quartz build --serve    # preview at http://localhost:8080
```

> With Bun: prefix the Quartz commands with `bun run` (e.g. `bun run quartz build --serve`).
> Node v22+ must still be on PATH — the Quartz CLI spawns `node` to build.

## Publishing

Push to `main`. The GitHub Actions workflow in `.github/workflows/deploy.yml`
builds the site and deploys it to GitHub Pages automatically. One-time setup:
**Settings → Pages → Source → "GitHub Actions"**.

Or use `npx quartz sync` (`bun run quartz sync`) to stage, commit, and push in one step.
