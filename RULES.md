# Design rules

Personal layout, color, and typography rules — the "why" behind `kit.css`.
Extracted from what's actually shipped in onething, a.wjerk.shop,
bjornpaedia, and oblique, plus direct answers where code alone couldn't
say why. This document changes as the kit changes — rename, restructure,
and rewrite sections freely as more projects get folded in (ookb.co,
oblique.ookb.co, wjerk.shop, whatever's next). Nothing here is precious.

## Ethos: do more with less

The governing instinct behind every rule below: solid rules instead of
shadows, a handful of tokens instead of an open-ended palette, one accent
color instead of a rotating cast. Restraint is the style.

Same instinct as the `bjorn-voice` skill's writing rules — compress,
don't shrink; cut color that does no conceptual work. One ethos, two
mediums.

## Scope note: the ookb.co / wjerk.shop family

Projects sit under two domain families — `ookb.co` (+ subdomains like
`oblique.ookb.co`) and `wjerk.shop` (+ subdomains like `a.wjerk.shop`,
`bjornpaedia.wjerk.shop`, `stuff.wjerk.shop`). The intent is modular: shared tokens/rules here,
each project free to pick its own typeface and emphasis on top. The old
`ookb.co` repo should get pulled down and checked against this doc too.

## Structure: rules, not chrome

No box-shadow, no gradients, no border-radius on structural elements
(panels, buttons, dividers). Structure comes from solid 1–2px borders and
whitespace. The one deliberate exception is small pill/tag elements
(`border-radius: 999px`, see oblique) — radius is fine at "badge" scale,
not at "panel/button" scale.

Buttons and interactive elements show state by inverting foreground/
background on press, not by adding elevation or a hover-glow.

## Contrast: high-contrast pairs only, always verified

Near-black text on a light background, or the reverse — never mid-gray on
light-gray. This isn't a stylistic default, it's load-bearing: a past pass
on onething shipped a "muted" text token that actually failed WCAG AA
(4.35:1) despite reading fine as an isolated swatch. Any new "muted" or
"subtle" token gets its computed contrast checked against the real
background it sits on before it ships — don't trust the name.

Focus is always visible — thick, accent-colored outline via
`:focus-visible`. Never suppressed.

## Color: pink is the accent, not blue

`--color-accent` is OOKB pink (`--pink-5` / `--pink-6`), the color that's
carried through every past iteration of this work. Blue showed up in
a.wjerk.shop, bjornpaedia, and oblique's `--color-accent` only because it
was a convenient default when nothing else was decided — it wasn't a
deliberate choice, so it doesn't get to be the kit's default going forward.

Pink is a deliberate choice for a.wjerk.shop specifically: the site is
climate/sustainability-design work, and the expected accent for "eco" is
green or blue. Pink reads as a surprise instead of the cliché — a
subversion, and unmistakably "mine" across every past pass at this palette.
Projects can still override `--color-accent` for a specific reason, but
pink is the answer unless there's one.

## Color: yellowish-gray background, dark brown line work

The default bg/text pairing (`--color-bg: var(--gray-0)`, `--color-text:
var(--brown-8)`) isn't an arbitrary landing spot — a warm, slightly
yellowish-gray ground with dark brown line work on top is a recurring
personal trope independent of this kit, and the semantic tokens already
encode it as the default rather than plain black-on-white. Projects can
still override it, same as the accent, but this pairing is the answer
unless there's a specific reason to change it.

## Typography: open/libre first, system default when low-energy

The ethos, not a fixed typeface: every font used is either an open/libre
license (OFL etc., self-hosted — see oblique's Basteleur and Sligoil
Micro) or the system font stack. Never a commercial/proprietary webfont.
Within that constraint, typefaces vary a lot project to project — the
constant is the license, not the letterforms.

`--font-sans` in `kit.css` is the system-stack "low-energy" default —
reach for it when a project doesn't need its own voice. `--font-display`
starts out equal to `--font-sans`; a project earns its own display font by
self-hosting an OFL typeface and overriding the variable, the way oblique
does. Not every project needs a --font-display override — system-sans-only
(onething, a.wjerk.shop, bjornpaedia) is a legitimate, common outcome, not
a fallback to feel bad about.

## Typography: the roster

The recurring libre picks reached for across past projects, kept here as
a starting shortlist rather than starting the license/pairing search from
zero each time: League Gothic, Avara, Gentium, Cormorant Garamond, Libre
Franklin, Libre Clarendon, League Mono, Space Mono, Space Grotesk, Work
Sans. This list is a personal snapshot, last revisited ~2018 — expect it
to get pruned and added to as preferences move on; see NOTES.md.

Friz Quadrata, a longtime personal pick, deliberately stays off this
list — it's proprietary, so it can't be self-hosted or shared across
projects the way the open/libre rule above requires. Kept as an
occasional personal choice outside the shared kit.

## Typography: rotation as an accent

Type (and occasionally other elements) rotated a few degrees off
horizontal — typically 7–12deg — is a recurring personal trope, used as a
deliberate accent on a specific element: a stamp, a callout, a heading.
Not yet wired into `kit.css` as a reusable utility; see `.tilt` there for
the starting point.

## Typography: baseline grid, not a ratio scale

`kit.css`'s `--text-*` / `--leading-*` tokens are a vertical-rhythm
baseline grid (Bringhurst, *The Elements of Typographic Style*; Lupton,
*Thinking with Type* — see README references), not a modular ratio scale.
The grid comes first: line-heights are even multiples of a 6px (0.375rem)
base unit — 18px, 24px, 30px, 36px, 42px, 54px. Font-sizes are then chosen
to pair with those rungs, snapping to whichever rung gives a comfortable
ratio at that size, rather than being generated by applying a fixed ratio
to the font-size itself.

The font-size/line-height ratio shrinks as size goes up — small text needs
proportionally more leading to stay readable, large display type needs
less (1.5 at `--text-2xs`/12px down to 1.13 at `--text-3xl`/48px). Because
of that, the ratio doesn't decrease smoothly step to step — two sizes can
share a line-height rung (`--text-base` and `--text-md` both use
`--leading-md`/24px), so the ratio dips within a shared rung, then jumps
back up when a step moves to the next rung. That sawtooth is expected
baseline-grid behavior, not a bug in the scale.

`--text-base` (1rem/16px) pairs with `--leading-base` (1.5rem/24px, ratio
1.5) — body copy at exactly the WCAG 1.4.12 recommended line-height, not a
coincidence, a constraint that shaped where the base step landed.

Every value is in rem, which is what makes "change everything together"
actually work: a project can nudge the whole scale by changing the root
font-size (e.g. a gentle bump at the `55rem` desktop breakpoint) without
touching a single `--text-*`/`--leading-*` value, because every step is
relative to the same root. `kit.css` doesn't set a root font-size itself —
it inherits the browser default (respects user zoom/settings) — this is a
technique to reach for per-project, not a default the kit imposes.

Two existing utilities, `.label-upper` (0.8125rem) and `.caption-muted`
(0.875rem), already matched a scale rung exactly once the grid existed
(`--text-xs` and `--text-sm`) — evidence the grid fits values already
shipping, not just a new invention. They're wired to the tokens now.
`.panel-header`'s `1.25rem` doesn't land on a rung (between `--text-md`
1.125rem and `--text-lg` 1.375rem) — left alone rather than silently
resized, but worth a deliberate call later on which rung it should snap
to.

## Images

**Style**: Victorian etchings are a recurring source material — their
linework pairs naturally with the "dark brown line work on a warm ground"
color trope above, and they're public domain more often than not, which
also serves the sourcing preference below.

**Treatment**: bitmaps get tinted or color-overlaid into the page rather
than dropped in as an untouched rectangle — a.wjerk.shop uses
`mix-blend-mode: multiply` on every photo. Originally a file-size trick
(skip exporting separately tinted variants), it's kept because it also
visually unifies photos from different sources into one consistent page
instead of looking like stock art sitting on top of the design.

**Sourcing**: prefer free, public-domain, or Creative Commons / libre
imagery — flickr.com/commons, unsplash.com, and other sources TK. Also
check the relevant are.na channel(s) for already-collected material before
sourcing new images. *(Links pending — add here once supplied.)*

**Sizing**: `object-fit: contain` fills the box it is given and nothing
more. `max-width`/`max-height` let that box shrink to the image's natural
size, so a small image sits small in the middle of the frame. Pin the box —
`width: 100%; height: 100%` — and contain scales up into it.

Cap the upscale. Read each image's real pixel dimensions at build time and
cap around 2.5x; a 150px source blown up to fill a projector is mush. Set a
minimum source size and drop what falls under it.

**Type over images**: put it on an opaque block. Never straight on the
photo, never on a gradient scrim. You cannot know what is behind it — half
the chair-ness images are museum shots on white, where light type
disappears. An opaque block holds its ratio whatever the image does.

Anchor that block to a corner, a full edge, or dead centre. A panel at an
arbitrary offset reads as a rendering tear rather than a layer.

## Motion

Not part of the base kit — `kit.css` ships no animation utilities.
Animation is a per-project, special-idea flourish, not a system default.
a.wjerk.shop's homepage logo (grayscale→color, red→green over 30s) is that
kind of one-off, not a pattern to reuse elsewhere. This may change as more
projects need it, but the starting rule is: ignore motion unless a
specific idea calls for it.

Auto-advancing media is the exception — a slideshow left running is motion
as the medium, not as a flourish. It carries two obligations. Honour
`prefers-reduced-motion: reduce`, slowing the thing down rather than
stripping it out. And scale dwell time to content length: a 30-character
line and a 270-character passage do not need the same time on screen.

## PDF generation: Markdown → pandoc → WeasyPrint

Print output (syllabi first, in `~/Code/syllabiBuilder`) is built from
Markdown, not authored in a page-layout tool or exported from a live web
page. Source: `.md` → `pandoc` (to styled HTML5) → `weasyprint` (to PDF).
Reach for this pipeline before a puppeteer/wkhtmltopdf-style browser-print
or a GUI layout tool — it's plain text in git, diffable, and rebuilds
without a browser.

`print/` in this repo is the generalized, drop-in version of that
toolchain — `print/md2pdf.sh`, `print/pandoc-template.html`,
`print/print.css` — start a new print job by copying that folder rather
than starting from `syllabiBuilder`'s syllabus-specific one.

The print stylesheet is not `kit.css` linked as-is — print has its own
`@page` rules (margins, running headers/footers, page-break control) that
don't belong in a screen stylesheet, so `print/print.css` is a **separate
file that restates the subset of kit tokens it needs** (`--color-text`,
`--color-accent`, `--color-border`, the baseline-grid `--text-*`/
`--leading-*` rungs) rather than importing the whole kit. Same warm-
ground/brown-line-work/pink-accent/OFL-fonts-only rules apply.

Fonts default to `--font-sans`/kit.css's own system-stack fallback, so
`print/print.css` works with zero setup. A project earns its own display
font the same way the kit does — self-host an OFL `@font-face` (a local
file path or a sibling repo's `fonts/`) and override the variable; see the
commented-out example at the top of `print/print.css`. WeasyPrint has no
access to a browser's installed-font fallback or a CDN at build time, so
the font has to be a real file on disk either way.

Two structural conventions worth keeping on the next print job, both
already wired into `print/md2pdf.sh`:

- **Shared boilerplate via include directives** (`<!-- include:
  path/to/file.md -->`, resolved relative to the including file, nesting
  allowed, a missing include aborts the build) — keeps repeated legal/
  policy text in one place instead of pasted into every document.
- **Drop a section by heading** (`-x "Section Heading"` removes an `##`
  section and everything under it before rendering) — lets one source
  document produce both an internal draft and a clean external copy,
  rather than maintaining two files.

On macOS, WeasyPrint's pango dependency needs
`DYLD_FALLBACK_LIBRARY_PATH` pointed at the Homebrew lib dir — `print/
md2pdf.sh` sets this itself rather than assuming it's already in the
shell environment.

## Slideshows / unattended players

Auto-advancing decks meant to run unattended for hours (a gallery
projection, an ambient background piece) carry obligations beyond a
normal web page, on top of the reduced-motion and dwell-time rules
already under "Motion" above. First built for `~/Code/chair-ness`; the
**ambient two-layer pattern is the default to reach for** — images hard-
cut on one layer, text surfaces over them on opaque, rotated panels — not
just one option among several. `slideshow-template.html` in this repo is
the generalized, drop-in version: no build step, edit the `CONFIG`,
`IMAGES`, and `TEXTS` values at the top of its `<script>` directly.

- **One generator, several outputs via composable flags**, not several
  near-duplicate scripts, if a project needs more than one build of the
  same deck (e.g. a local-asset build and a hotlinked/publishable one).
  `chair-ness/scripts/build_slideshow.py` produces four builds
  (local-image / hotlinked-image × single-slide / two-layer-ambient) from
  two independent flags (`--hotlink`, `--ambient`) that compose, so a
  content change (editing `quotes.txt`) has exactly one script to re-run
  correctly, not four. `slideshow-template.html` doesn't need this — it
  has no build step, so there's nothing to keep in sync across builds in
  the first place.
- **Sizing**: pin the box (`width/height: 100%`) and let `object-fit:
  contain` scale into it — see "Images: Sizing" above. Cap upscale of
  small source images (chair-ness caps at 2.5x) rather than blowing a
  150px thumbnail up to fill a projector.
- **Fonts stay linked (self-hosted `@font-face`, normal file on disk) by
  default** — same as everywhere else in the kit. Embedding a font as
  base64 is a narrow fix for a specific problem, not a slideshow default:
  reach for it only when the build must be one self-contained file with no
  guaranteed network (a projector with no venue wifi) or must travel as a
  single copy to somewhere that can't also hold a `fonts/` folder (chair-
  ness's build gets copied into `a.wjerk.shop` as one file). If neither
  applies, link the font file normally. When it does apply, budget the
  embed against total asset weight rather than treating it as free —
  chair-ness's six embedded OFL faces cost ~214 KB against ~12 MB of
  images, under 2% — and ship a flag to fall back to the system font stack
  when it isn't worth it.
- **Bound memory for a long-running DOM.** Don't leave every slide ever
  shown sitting in the DOM — decoded bitmaps accumulate for as long as the
  tab stays open (chair-ness measured ~2.6 GB uncapped for its image set).
  Keep only slides within a small radius of the current one; tear the rest
  down and let their images release. Preload the next few images off-DOM
  (`new Image()`, cache-only) so a slide is decoded before it's shown, not
  while it's shown.
- **Degrade instead of stalling.** An image that fails to load gets marked
  broken and skipped, not left holding the slide for its full dwell time.
  A backgrounded tab pauses (`visibilitychange`) instead of racing ahead
  while nobody's watching, so it doesn't come back out of sync with the
  room.
- **Caption/metadata provenance**: derive captions from fields on the
  source item itself, in a fixed precedence order (chair-ness: an
  authoritative external source first, then the item's own title, then
  its description), never by pairing an item with whatever happens to sit
  next to it. Suppress machine-generated junk (filenames, CDN query
  strings, bare UUIDs, scraped page titles like "403 Forbidden") — no
  caption beats a wrong one.
- **Hotlinking third-party images carries real risk**: a source may 403
  any foreign `Referer` (chair-ness measured this against
  `collection.design-museum.de`, 6/6), so a "distributable, no local
  copies" build can silently lose exactly the images that matter most.
  Confirm cross-origin hotlinking actually works on that host before
  designing a build around it, and prefer sources whose own CDN is meant
  to be hotlinked (an image upload) over a link/screenshot capture of
  someone else's page.

## Slide decks: talks vs. teaching support

Two different genres of slide deck show up across `reference/` (25
lecture PDFs, 2010–2026), and treating them the same is a mistake — a
talk deck earns the whole "full-bleed everything" treatment below, but a
teaching-support deck (screenshots, side-by-side comparisons, reference
material meant to sit in front of students) stays plain and functional on
purpose. The split is by genre, not by date: `WorkingTeachingLecture`
(2023) is as plain/white/bordered as `Entropy` (2010, no images at all),
while `FreeOpenCulture` (2021) already has the full expressive talk-deck
look that `Copyright` / `NewDesignCommons` / `Semiotics` / `FutureCone`
(2026) intensify rather than invent. Check which genre a deck is before
reaching for the rules below.

**Canvas: 16:9 or 16:10, always** — maximizes full-screen view on
whatever the room's projector or a laptop lid actually is.

**Full-bleed is a hard rule for talk decks**: images bleed to all four
edges, tilted/cropped compositions rather than centered or letterboxed —
a deliberate departure from "pin the box, `object-fit: contain` scales
into it" elsewhere in this doc, which is for an image inside a page
layout, not a full-canvas slide. Title/section-break slides get the
busiest version: a full-bleed collage (photo, engraving, or shape
confetti) under a large headline, often tilted to follow the image's own
diagonal.

**Text: short and aphoristic, never a restated sentence.** Slide text
should not repeat what's being said out loud — it either cues the speaker
on where the talk goes next, or illustrates/metaphorizes the point being
made. A quote/aphorism slide pairs a full-bleed photo with an opaque card
(tilted a few degrees, per "Typography: rotation as an accent" above)
holding one or two short lines plus attribution — never a paragraph.

**Illustration over exposition — the working techniques, not just the
principle:**
- Literalize a pun or term visually, sometimes twice in a row for the
  joke to land ("cat burglar" over a cat silhouette, then over an actual
  roof-burglar photo).
- Diagram a concept as a photo-to-photo bridge rather than a caption (a
  1999 headshot → a widening cone → a product photo, one arrow, no
  exposition text — the "futures cone" idea, unstated).
- A mascot delivers a wayfinding instruction instead of plain UI text (a
  cartoon character "speaking" a QR code).
- A closing slide can be pure image, no text at all, when the visual
  carries the whole gesture (a line-art Earth on black, nothing else).

**Typography and color, in practice:**
- Typeface varies slide to slide, matched to the image's mood — the same
  "vary project to project, license is the constant" ethos as the kit's
  typography rules, applied within a single deck instead of across
  projects.
- All-caps for short punchy labels; word-level color-highlighting for key
  terms within a longer line.
- Two color modes recur, not blended on one slide: full-color photo
  background with text set directly on top (no gradient scrim — legibility
  comes from an opaque card or tonal matching, same as "Type over images"
  above), or a black background with one or two saturated accent colors
  for data/closing slides. A cream/off-white "paper" ground is the
  recurring choice for text-forward slides, in both the oldest and newest
  decks sampled.
- A tiny credit line in a bottom corner of every image slide — "TYPE:
  [fonts used]" / "IMAGE: [source, license]" — is a real, portable
  convention worth keeping, not a one-off.
- The vintage-engraving/mascot-collage device (a Victorian etching or a
  cartoon character composited onto a real photo or screenshot) recurs
  from 2021 through 2026 — this is the "Images: Style" Victorian-etchings
  note above showing up as an active compositing technique, not just a
  sourcing preference.

**Pacing**: a talk deck changes visual mode (image/quote → image/title →
clean diagram) roughly every 1–3 slides rather than settling into one
mode for a run — a plain white-background diagram slide reads as a
deliberate reset, not a lapse.

This is about designing the slide canvases themselves (Keynote, Figma,
whatever produces the deck) — it doesn't change
`slideshow-template.html`, which is a different genre again (unattended/
ambient, no speaker in the room) and is already canvas-agnostic: images
`object-fit: contain` into whatever viewport they're given.

## Dark mode

The palette is settled and measured. It needs no new colors: the dark
pairing is the same brown scale with its ends swapped. `--brown-9` is the
ground, `--brown-0` the text. Pink stays the one accent, at `--pink-3`
rather than the light mode's `--pink-5`.

Measured against `--brown-9`:

| Token | Role | Ratio |
|---|---|---|
| `--brown-0` | primary text | 18.81:1 |
| `--brown-3` | secondary, captions | 10.49:1 |
| `--pink-3` | accent | 8.67:1 |
| `--brown-4` | tertiary, hints | 7.06:1 |

`--brown-4` is the floor. `--brown-5` drops to 4.36:1 — that fails AAA and
fails AA for normal text. It reads as a usable gray on screen and isn't
one. Nothing dimmer than brown-4 carries text a reader has to read.

The ground is `--brown-9`, not black. Black loses the warmth the light mode
is built on.

The semantic layer maps straight across, so wiring this up is a token flip
and not a rewrite:

| Semantic token | Light | Dark |
|---|---|---|
| `--color-bg` | `--gray-0` | `--brown-9` |
| `--color-text` | `--brown-8` | `--brown-0` |
| `--color-text-muted` | `--gray-6` | `--brown-3` |
| `--color-text-subtle` | `--gray-6` | `--brown-4` |
| `--color-accent` | `--pink-5` | `--pink-3` |

`kit.css` still pins `color-scheme: light` and does not ship the flip yet.
The open question was never which colors — it was whether to spend the
complexity. The colors are now answered.

First built and contrast-checked for the chair-ness exhibition slideshow
(`~/Code/chair-ness`), projected dark in a gallery.

## Layout: mobile-first, two breakpoints

Base styles are always the stacked/single-column mobile layout. Wider
treatments layer on top via `min-width` media queries at two conventional
breakpoints: `40rem` (tablet / two-column) and `55rem` (desktop / widest
treatment). No custom-media variables — the kit has no build step and
needs to work as a plain `<link>`, so these are documented values to reuse
by hand, not a variable to reference.

## Naming

Token names are already being hand-standardized across projects before
this doc existed — oblique independently uses `--color-accent`,
`--color-text`, `--color-bg`, and a distinct `--color-frame` for its
decorative thick border. `kit.css` adopts exactly this naming rather than
inventing a new scheme.
