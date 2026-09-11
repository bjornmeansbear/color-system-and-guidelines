# slideshow

The are.na-archive slideshow player. Pulls a channel down to disk, then builds
self-contained HTML decks from it — a single-slide deck, or the two-layer
ambient piece meant to run unattended on a projector for hours.

The design reasoning lives in `RULES.md`, **"Slideshows / unattended players"**.
This file is just how to run it. For a one-off deck with no archive behind it,
use `../../slideshow-template.html` instead — no build step, edit the values at
the top of its `<script>`.

## Built with it

- `~/Code/chair-ness` — the original, plus its own museum-specific scripts
- `~/Code/WritingPlanning/gd420/exhibiting-ness` — exhibiting graphic design

## Use

Everything takes `--root`, defaulting to the current directory. Run from inside
an archive and you can leave it off.

```sh
cd ~/Code/some-archive

# 1. pull a channel (re-runnable; skips files already on disk)
python3 ~/Code/color-system-and-guidelines/tools/slideshow/fetch_arena.py \
  --channel <are.na-slug>

# 2. write text/quotes.txt — blank-line separated panels,
#    "— Attribution" on its own line

# 3. build
python3 ~/Code/color-system-and-guidelines/tools/slideshow/build_slideshow.py \
  --title "some-archive" --ambient
```

`--ambient` picks the mode, `--hotlink` picks the image source, and they
compose into four builds:

| Flags | Output | What it is |
|---|---|---|
| — | `slideshow.html` | Deck. One image at a time, cross-fade, local images. |
| `--hotlink` | `slideshow-web.html` | Deck, images served from are.na. Publishable, ships no copies. |
| `--ambient` | `slideshow-ambient.html` | Two layers. Images hard-cut underneath; text surfaces over them on opaque panels. **The projection build.** |
| `--ambient --hotlink` | `slideshow-ambient-web.html` | The ambient piece, are.na-sourced. |

Useful flags: `--title`, `--channel-label` and `--channel-url` (the credit
line), `--min-px` (drop images too small to project, default 300),
`--include-links` (use `links/` og:image previews as well — off by default
because they're usually social-share cards, but worth it when the link blocks
are the named references), `--image-ms` / `--chairs-between-text` (ambient
pacing), `--no-embed-fonts`.

## Two more scripts

```sh
python3 .../pacing.py                      # how the current counts actually play
python3 .../uncaptioned.py --out list.md   # which blocks reach the show bare
```

## Before the first commit of a new archive

Add this to that project's `.gitignore`:

```
images/
links/
```

They're a cache — `fetch_arena.py` rebuilds them in minutes. Committing them
put 268 MB into a syllabus repo once and took a history rewrite to undo.

## Fonts

The six OFL faces the text panels rotate through ship here, beside the script,
and get base64-embedded into each build so a deck plays off a local file with
no network. About 214 KB per build. `--no-embed-fonts` falls back to the system
stack. Licenses are in `fonts/`.
