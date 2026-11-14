# Bjook

Poems as plain text in, three things out: a typeset PDF in reading order, a
booklet PDF imposed for saddle stitch, and a preview of the book as facing
pages that reloads when you save.

The design reasoning lives in `RULES.md`, **"Bjook"**. This file is how to
run it.

## Built with it

- `~/Code/a-poem-a-day` — 56 poems from the are.na channel of the same name

## Setup, once

```sh
pipx install weasyprint
pipx inject weasyprint pypdf
brew install poppler          # pdftoppm, for the preview images
```

`./bjook` runs `bjook.py` on the Python inside that pipx venv. An alias
saves typing:

```sh
alias bjook=~/Code/color-system-and-guidelines/tools/bjook/bjook
```

## Use

```sh
bjook new ~/Code/my-book --channel <are.na-slug>
cd ~/Code/my-book

bjook fetch                 # text blocks -> poems/*.md, listed in order.txt
bjook watch                 # http://127.0.0.1:8642/preview.html, rebuilds on save
bjook build                 # one build, no server
bjook build --snap "note"   # also keep a timestamped copy in snapshots/
bjook specimen              # one poem in eight faces -> build/specimen.pdf
bjook specimen "Spectral" "Inria Serif" --poem some-poem.md
bjook site                  # the book as a website -> build/site/
bjook site --out ~/Code/bjornmeansbook   # into a shared site folder
```

Every command takes `--root` before it, defaulting to the current folder.

## A book folder

| | |
|---|---|
| `book.toml` | Title, author, page size, margins, typeface, size, leading; where the page number sits (`[folio]`); an optional running head (`[head]`) and continues mark (`[continues]`). The template lists every setting. |
| `order.txt` | The sequence, one poem filename per line. Move lines to reorder. `#` in front of a line leaves that poem out. |
| `poems/*.md` | One poem each: a few `key: value` lines between `---` (title, are.na id, date), then the lines. A blank line is a stanza break. `*italic*` and `**bold**` work; leading spaces indent. |
| `style.css` | This book's print overrides, applied after the tool's `book.css`. |
| `site.css` | Optional. This book's website overrides, applied after the tool's `site.css`. |
| `build/` | Output. Disposable, gitignored. |
| `snapshots/` | Proofs kept on purpose. |

`fetch` never overwrites a poem already on disk (it matches on the are.na id),
so edits made here are safe and a re-run only adds what's new. `fetch --force`
replaces local text with the channel's.

## Output

- `build/<slug>.pdf` — pages in reading order. Send this to a print shop that
  imposes for you, or read it on screen.
- `build/<slug>-booklet.pdf` — two pages to a sheet, ordered for folding. Print
  double-sided, **flip on the short edge**, fold the stack, staple the spine.
- `build/preview.html` — facing pages. **Guides** draws the text block and
  baselines; **Actual size** shows the page at its printed width.

- `build/site/` — from `bjook site`: a front page with the contents and
  colophon, one page per poem, the two PDFs to download, and `index.html`,
  a bookshelf with a cover for every book in the folder (`[site] cover`
  sets a cover's tint). Plain static files with no
  JavaScript; open `index.html` directly or upload the folder to any host.
  With `--out`, several books share one site folder, each in a folder named
  from its title (or `[site] path`), and the shelf lists them all.

The build pads the page count to a multiple of four and lists any poem that
runs past one page.

## Typefaces

`[type] text = "Gentium"` is a family name as the font spells it, looked up
under `fonts_dir` (default `~/Code/libreFontLibrary/Families`). If the name
isn't found, the error lists the families in the nearest folder: one folder
often holds several (`Cormorant`, `Cormorant Garamond`).
