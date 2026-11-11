# color-system-and-guidelines

The design system for all my projects (OOKB, Wjerk, and the rest): color,
type, layout, print and presentations, in one place so each new project
starts from the same rules instead of reinventing them.

Pink accent on a warm cream ground, dark brown line work, solid rules instead
of shadows, open/libre type, a 6px baseline grid.

## Use it

- **On a web page:** copy `kit.css` into the project and `<link>` it. No
  build step, no package. Override `--color-accent`, `--color-bg` or
  `--font-display` if the project has a reason to.
- **After the kit changes:** `python3 scripts/sync.py --all` re-copies it
  into every project that hasn't edited its copy, then reports any palette
  values pasted elsewhere that went stale (`--dry-run` to look first).
- **Before shipping a color pairing:** `python3 scripts/contrast.py pair
  <fg> <bg>`, or `find <bg>` for everything that passes on a ground.

## What's here

| | |
|---|---|
| `kit.css` | Tokens (color scale, semantic layer, type scale) plus the base reset and primitives. The source of truth for every value. |
| `RULES.md` | Why each rule exists, by topic, with the sources behind them. Read the section before working in that area. |
| `NOTES.md` | Open questions and a dated changelog. Read this first when picking work back up. |
| `showcase.html` | The kit rendered live. Open it in a browser. |
| `scripts/` | `contrast.py` (WCAG checker), `drift.py` (finds stale pasted colors; `--fix` rewrites them), `sync.py` (re-copies the kit into projects), `package-skill.sh` (builds the claude.ai skill). |
| `print/` | Markdown → pandoc → WeasyPrint PDF pipeline. RULES.md "PDF generation". |
| `slideshow-template.html` | A one-file unattended slideshow. RULES.md "Slideshows / unattended players". |
| `tools/slideshow/` | Builds slideshows from an are.na archive. |
| `tools/commons/` | Finds public-domain slide imagery from a metaphorical brief. |
| `tools/bjook/` | Poems as plain text → a typeset book PDF, a saddle-stitch booklet, and a spread preview. RULES.md "Bjook". |
| `SKILL.md` | The `bjorn-design` skill: the always-loaded summary that points into RULES.md. |
| `site/` | Wjavelength, the website for the system: palette, contrast cheat sheet, rules, and a voter for color sets. SvelteKit on Cloudflare Workers; reads `kit.css` and `RULES.md` at build. See `site/README.md`. |

The writing side lives in its own repo, `~/Code/bjorn-voice`.

## License

Public domain (Unlicense). See `LICENSE`.
