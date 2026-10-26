# Notes

Where things stand: open questions first (most likely to matter next time),
changelog underneath. Update this as work happens — it's meant to be read
before starting a session, not just written to at the end of one.

## Open questions / next steps

- **Emoji carry their own palette.** taste-translator (2026-10-15) marks
  ratings (❤️ 👍 🙂 😐 👎 🚫) and domains (🎬 🎵 📖 …) with emoji, which bring
  red, yellow and blue that sit outside the kit and can't be contrast-
  checked as tokens. Left in place for now — they're content the app's
  meaning leans on. **Decided 2026-10-15:** a custom ink glyph set, to be
  drawn by hand later (line-drawn, matching the canvas line work). Until
  then the emoji stay, all in one table (`DOMAINS` and `RATINGS` in
  taste-translator's `src/lib/types.ts`), so the swap is one place.
- **No bright green in the kit — data-ink case.** Raised while building
  Wjorth (2026-09-19), a budgeting dashboard needing a clear "good"
  green distinct from the muted `--color-success` (`green-6`, which the
  kit's own tint notes already flag as "reading brown"). Picked `green-5`
  for chart/data-ink use specifically ("the most visibly green step that
  still holds 3:1 as a line," per RULES.md "Data on screen"), reserving
  `green-6`/`green-3` for status flags. Not yet visually validated against
  a real built screen in either light or dark mode — do that before
  treating this as settled, and fold the result back into RULES.md's "Data
  on screen" section either way.
- **Older projects worth a look, same visual vernacular.** Noted in passing
  while working on Wjorth (2026-09-19): `bjornpaedia`, `oblique`, `onething`,
  and `a.wjerk.shop` (the main portfolio site) are all in the same lineage
  as this kit but predate or sit outside it. Not researched as part of that
  work — just a pointer that they're worth revisiting sometime, e.g. for
  older kit.css drift the way `di200-fieldnotes` and `wjeather` were audited
  2026-09-16.
- **Revisit the palette: a wider set, and the original one written down.**
  Raised 2026-09-11 after wjeather ran short of distinct pale tints (see the
  next two items). Two parts: (1) articulate the palette actually used in
  past work, before the kit; (2) widen the options — more distinct hues at
  the pale steps, a true violet, a clearer green — each measured against the
  tint budget in RULES.md before it ships.

  Part (1) done 2026-09-11: the Wjerk palette, read from its Figma styles, is
  in RULES.md "Color: the original Wjerk palette". It points at what to add
  first — **true blues** (Cornflower, Dark Cornflower, Navy; the kit had none)
  and **Golden Rod**. Both added 2026-09-11 as the `cornflower` and
  `goldenrod` scales in `kit.css`.

  The pink question is settled (2026-09-11): the softer original replaced the
  hot one — the scale rebuilt at its chroma, one family, `pink-5` still AA
  for small text. Still open: whether onething, a.wjerk.shop, oblique,
  bjornpaedia or the `palette-*.html` drafts used anything outside the Wjerk
  set.
- **The kit's purples read pink.** Found in wjeather (2026-09-10): `purple-1`
  as a snow band read as the accent, and `purple-0`–`2` as a night sky all read
  rose on screen. Dark `purple-9` reads as a true night purple. Either treat
  purple as a pink-family tint kept away from the accent, or add a cooler
  violet to the scale. RULES.md "Color: tints behind text".
  Intent, stated 2026-09-11: Wjerk Purple was a muted, muddled gray-purple —
  never bright — and meant to lean *blue* of mauve, not pink. The kit drifted
  the wrong way: `purple` sits at OKLCH hue ~336°, pinker than the original's
  329°. **Done 2026-09-11:** the scale moved to hue 315° at the same
  lightness and chroma — the balance point between pink and the new
  `cornflower` (step 2: 5.7 from `pink-1`, 5.1 from `cornflower-2`); 300–310°
  crowded cornflower. No project reads `kit.css` live — onething, fridgechef
  and the lecture decks keep their own pasted copies — so nothing changed
  under them until re-copied. Re-copied 2026-09-11: onething and fridgechef
  in full, the lecture decks purple-only; wjeather's copy is synced.
- **No bright green in the kit.** Every green step is olive; wjeather's
  humidity line settled for `green-5`. Fine for now — decide whether a
  data-viz green earns a token.
- **Icon family: a.wjerk.shop is the outlier.** Its etched globe has no frame
  or stepped shadow. Parent mark of the wjerk.shop family on purpose, or bring
  it in? Also: wjeather's peach fill (#FFCCA0) isn't a kit tint (nearest
  `orange-1`, pinker) — check whether the other icons' fills are. RULES.md
  "Icons".
- **Deck colour and kit colour have never been reconciled.** `kit.css` says
  pink accent on a warm yellowish-gray ground with dark brown line work. The
  AY26 lecture decks are black, white and grayscale, with per-lecture semantic
  accents (green marks "preferable" on the futures cone) and no pink anywhere.
  RULES.md "Presentations: imagery" documents the deck side and the Colour
  sections document the kit side, and neither references the other. Raised
  2026-09-02: this is an accident of the two being written separately, not a
  decision. Worth deciding whether projection is its own context with its own
  palette, or whether the decks should carry the pink.
  Found 2026-09-11: the AD1 deck ("Design For the Future Today!", AY26 Figma
  file) uses the Wjerk ("OOKB Palette") library styles — White, Yellow, Green, Dark Green, Black,
  Light Green Gray. So at least one deck carries the original palette, not
  grayscale; the reconciliation may be the Wjerk palette rather than `kit.css`.
- **No template file yet for the "talk deck" genre** (RULES.md "Slide
  decks: talks vs. teaching support") — unlike the ambient player, this
  one isn't a single reusable HTML file, since the decks themselves live
  in Keynote/Figma/PDF, not a web page. Worth deciding whether a
  lightweight web-based starting point (a static full-bleed-slide HTML
  template, canvas-agnostic like `slideshow-template.html`) is worth
  building, or whether this genre just stays documented-pattern-only
  since the actual authoring happens in another tool.
- **Teaching-support decks aren't specced, only named as the other
  genre.** RULES.md now says they "stay plain and functional on purpose"
  but doesn't document what plain/functional actually means in practice
  (layout, type, screenshot treatment) the way the talk-deck genre now
  is — would need its own pass through `WorkingTeachingLecture.pdf`-style
  references if that's ever worth codifying.
- **Find/build a libre Friz Quadrata alternative.** Friz Quadrata is a
  longtime personal pick but proprietary, so it's deliberately excluded
  from the shared typeface roster (RULES.md "Typography: the roster").
  Worth hunting for an existing OFL-licensed lookalike before considering
  a from-scratch libre remake.
- **Typeface roster is a dated snapshot.** The list in RULES.md
  ("Typography: the roster" — League Gothic, Avara, Gentium, Cormorant
  Garamond, Libre Franklin, Libre Clarendon, League Mono, Space Mono,
  Space Grotesk, Work Sans) was last revisited ~2018 per Kristian; treat
  it as a starting shortlist, not a closed list — revise as current
  preferences get confirmed.
- **"The four freedoms; but for signs on substrates?"** — half-formed
  idea from `Personal tropes.txt`: applying FSF-style software-freedom
  thinking (run/study/share/modify) to physical signage/materials rather
  than fonts or code. Not a rule yet — needs to be worked out into an
  actual position before it belongs in RULES.md.
- **`.tilt` utility just added, unused so far.** kit.css now has a
  rotation utility (`--tilt`, default 9deg) for the "type rotated 7–12deg
  as an accent" trope (RULES.md "Typography: rotation as an accent") —
  no project uses it yet; worth trying on a real element to see if the
  default angle/approach holds up.
- **Two deck forms, and only one is measured.** The short ceremonial talk
  (5–10 minutes, 5–7 slides, one aphorism and one image each) is now well
  evidenced — "On Mending," "On Making Stuff," "Loose Threads," all 2026, all
  two to eight words a slide. The long lecture deck is not. `di200-wk1` is 67
  slides at a median of ~58 words and is clearly too dense, but a lecture
  legitimately carries definitions, comparisons, citations and a timeline that
  a seven-slide address does not. Kristian has said longer lecture decks are
  coming; do not set that ceiling until one he stands behind exists. The
  form-independent rules (never shrink type to fit; the slide is not the
  script; one axis of visual coherence) apply to both.
- **Slide word ceiling is provisional.** RULES.md "Presentations:
  density, and the shrink tell" records the measured facts (median ~58
  words/slide in `di200-wk1`; the strong lines break clean at ~13 words)
  and proposes ~25 words, or ~40 for a bulleted comparison. Not confirmed
  by Kristian yet. A number is falsifiable where a shape rule ("one idea,
  one screen") is not, which is the argument for keeping it numeric —
  but the number itself should be checked against the deck archive below
  before it hardens.
- **The layout archetype set is undecided.** RULES.md "Presentations: a
  closed set of layouts" asserts there should be a small closed set with
  stated triggers, but not which archetypes are in it — one deck is too
  thin a sample. `di200-wk1` runs five modes (`.rows`, `.cols`, `ul`,
  `.lead`, `blockquote.big`) with no rule for choosing. Decide against
  the deck archive.
- **Deck archive pending.** Kristian is selecting ~8 favourite decks
  (Figma exports and old PDFs) as evidence for the Presentations rules —
  PDFs, one per deck, year in the filename, with a note on which he'd
  actually defend. To extract: layout archetypes and how many recur,
  words per slide over time, image treatment, type-size clustering, and
  whether the aphoristic register is consistent or grown into. Until
  this lands, every Presentations rule rests on a single deck.
- **Where the shared image cache lives.** RULES.md "Presentations: local
  files, never hotlinks" says the cache should be shared across projects
  rather than nested in one, but not where. `~/Media/commons/<channel-
  slug>/` was proposed (outside any repo, backed up, symlinked or
  build-resolved into each project). Kristian's call.
- **Do museum picks get pushed back to are.na?** The sourcing cascade
  searches are.na first, then museum APIs. If a museum pick is written
  back into an are.na channel, step 1 compounds — every choice makes the
  next search better, which is the whole argument for a single library.
  If it only lands in a local manifest, the fifth deck re-searches the
  Met from scratch. Leaning yes (push); the cost is channel sprawl, which
  is a naming problem rather than a real one.
- **Writing picks back to are.na is the last unbuilt piece.** Auth is now
  sorted (2026-08-27): a read+write `ARENA_ACCESS_TOKEN` lives in this repo's
  gitignored `.env`, and the `commons` tool reads it there first, then
  `chair-ness`, then `sentence-a-day`, skipping commented lines. The are.na
  API spec is `~/Code/sentence-a-day/openapi` — YAML, v3.0.0, 41 paths. What
  remains is `POST /v3/blocks` plus `POST /v3/connections` so a museum pick
  gets saved into a channel; until that exists, step 1 of the cascade never
  gets smarter from museum picks. Decide the channel-naming question first
  (see the push-back-to-are.na entry above).
- **`lectureScripts` git bloat is SVG, not images.** Its 115MB `.git` is
  524MB of `SampleSlides/CC-SSS-*.svg` in history (~3.4MB each), not
  photography. Worth knowing before anyone "fixes" image storage there —
  the images were never the problem.
- **`.panel-header`'s font-size (`1.25rem`) doesn't land on a type-scale
  rung** — it sits between `--text-md` (1.125rem) and `--text-lg`
  (1.375rem). Left alone rather than silently resized (see RULES.md
  "Typography: baseline grid, not a ratio scale"); needs a deliberate call
  on which rung it should snap to, or whether it's a legitimate
  off-grid exception.
- **Root-font-size "change everything together" technique isn't
  demonstrated anywhere yet.** RULES.md documents that the whole rem-based
  type scale can be nudged by changing the root font-size (e.g. a bump at
  the `55rem` breakpoint), but no project or example does this yet — worth
  trying once a real project needs it, to see if the technique actually
  holds up.
- **Image sourcing links still TK** — RULES.md "Images" section flags this
  as an open gap (flickr commons, unsplash, are.na channels — links
  pending).
- **Motion** — intentionally out of scope per RULES.md; revisit only if a
  specific project idea calls for it, not as a system default. First one
  built: wjeather's wind drift (2026-09-11) — ~4 s on open, then still;
  skipped under `prefers-reduced-motion`. See RULES.md "Motion".
- **Dark mode — colors answered, not yet wired.** RULES.md now carries the
  measured dark palette and the light→dark semantic token mapping. What's
  left is a decision, not a design: whether to ship the flip in `kit.css`
  (which still pins `color-scheme: light`) or keep leaving it to projects
  that need it. wjeather (2026-09-10) is the first project to ship it this
  way; the mapping held, plus dark tints for data at steps 7–9.

## Changelog

### 2026-10-26

- **Pasted copies of the palette had drifted; `scripts/drift.py` now finds
  them.** No project reads `kit.css` live, so every copy goes stale when the
  kit changes. The 2026-09-11 rebuild (pink, purple, ground and text) had not
  reached README.md (a full copy of the old scale headed "Source of truth"),
  `DASHBOARD-SPEC.md`, `print/print.css` or the commons contact sheet: 48
  stale values in all. All fixed; README now points at `kit.css` instead of
  carrying a copy. `drift.py <path>` checks other projects too.
- **All projects clean; `drift.py --fix` added.** The last 41 old-pink copies
  (lectureScripts, syllabiBuilder, vinylCutter) are rewritten, each in its own
  notation. Checked first, old vs new, on every ground they sit on: all hold
  their AA/AAA level, and no ratio moves more than 0.15 (pink-5 on `gray-0`
  4.87 → 4.73, still AA). `sync.py --all` now reports no drift anywhere, so a
  drift report from here on means something changed.
- **`scripts/sync.py` re-copies the kit into projects.** Finds each
  project's `kit.css`, overwrites it only if it matches a committed version of
  this one (a copy with local edits is skipped and reported), then runs
  `drift.py`. First dry run: di200-fieldnotes, taste-translator, wjeather and
  wjorth were one change behind (no `--wjerk-*` originals). Pasted fragments
  still on the old hot pink, which sync can't fix: lectureScripts (book.css
  and the di200 decks), syllabiBuilder (GD420 deck, faculty handbook),
  vinylCutter `app.css`.
- **Deleted `palette-1.html`, `palette-2.html` and `palette-docs.html`**
  (closes "Consolidate the palette HTML files"). Three July drafts of one page,
  linked from nowhere, carrying the pre-rebuild palette and a 3.34:1 muted
  gray; `palette-docs.html` was still shipping in the claude.ai skill bundle.
  `showcase.html` links `kit.css` and covers all of it live.
- **`print/` runs end to end** (closes the open question). Built a test PDF
  through `md2pdf.sh` with `-x`; it works. It left two temp files per run,
  now fixed (one temp dir, removed on exit). It also needs `pdfinfo`, now
  listed.

- **Section labels dark, card footers quiet** (bjornpaedia homepage). The
  section bands went from `surface-muted` to `surface-dark` with cream text
  (7.34:1), and the Start here card footers went from dark slabs to a rule on
  the card's own cream. The labels now carry the hierarchy; the footers stop
  competing with the card titles. Pink text on the muted band was 4.11:1, so
  footer links hover by inverting (accent fill), as the cards do.
- **Line up parts inside cards with subgrid, not a fixed height.** Flexbox
  already gives cards in a row equal heights, but not the parts inside them:
  footers of one, two or three lines put their top rules at different heights,
  and a min-height in lines broke at narrower widths. A 12-column grid with
  each card a two-row subgrid shares one footer row per row of cards.
- **The kind tints as an abstract picture of an archive.** bjornpaedia's
  homepage now lists all 2,083 pages as touching tiles, each tinted by kind
  (about 44% colored). Sorted by title, the timestamped daily entries come
  first as a long cream run, then the collection scatters through A–Z. The
  Collected doors act as the key. Block count per row follows width
  (`flex: 1 1 calc(10rem + gutter*2)`), not a breakpoint.

### 2026-10-23

- **Kind tints for cards** (sentence-a-day TiddlyWiki river; RULES.md
  "Color: tints behind text"). Step 2 is the faintest step that separates
  from the cream ground; about five step-2 hues stay distinct (≥7.1 OKLab
  apart); pink is out because the accent fails on `pink-2` (2.76:1). Three
  in use: `yellow-2` words, `cornflower-2` things, `orange-2` people, each
  with a step-7 label. Your own writing stays on the ground. Local wiki only,
  not the static site. Not yet looked at on screen; check the river before
  treating the pairing as settled.
- **Dashed edge for raw material; tinted collection doors.** Same day: raw
  notes and scraps get a dashed card edge (second channel, not a fourth tint),
  and bjornpaedia's homepage doors are reordered so the collection (Definitions,
  Quotes, Sources, People) is the last row, tinted with the river colors.
- **Definitions get `gray-2`, apart from quotes.** Purple was the first pick
  but sat 5.1 from the Sources blue; gray keeps all four tints ≥7.1 apart.
  That uses up the step-2 tints that stay distinct.
- **Objects share the Sources blue.** A new kind (specific made things:
  chairs, packaging) went into the existing "thing" tint with its own label,
  not a fifth tint. Homepage doors split into two lists, your writing 3×3
  and a "Collected" row of five.

### 2026-10-19

- **Wjerk Med Gray as a ground: what survives on it** (onething, measured
  on #858479). Ink: `brown-9` 5.39:1, `brown-8` 4.81 — `wjerk-black` is only
  3.86, so it fails as small text here. No muted tone passes (`gray-6`
  2.07), so quiet text on the gray is quiet by size/italics, not color.
  `pink-5` is 1.34:1 — **a pink focus ring is invisible on this ground**;
  onething uses a `brown-9` ring instead (5.39 on gray, ~19 on `yellow-0`).
  Light type (`white-0`) and `yellow-0` both sit at ~3.5:1 — fine for fills
  and large type, not small text. Open question for RULES.md: the
  "accent is the focus ring" rule needs a ground-dependent exception.
- **Shadows softened from banned to last resort** (RULES.md "Structure: rules,
  not chrome", SKILL.md, DASHBOARD-SPEC.md). Drop shadows aren't forbidden;
  they just shouldn't be the first way to make things stand apart. Border,
  ground change, whitespace or offset outline first. oblique's strategy-card
  shadow no longer counts as a violation.
- **The whole original Wjerk palette is tokens now** (`--wjerk-*` in kit.css,
  a swatch grid in showcase.html, note in RULES.md). Only White and Black had
  been kept exactly; the rest existed only as a table mapping each to its
  nearest ramp step. Several sit between steps (Med Gray between `gray-4`/`-5`,
  ΔE 5.2 from anything) — and Med Gray is the main gray of years of work, so
  "nearest step" was quietly losing it. Ramps unchanged; the originals sit
  beside them. Values are the Figma styles; the legacy LESS ones in README.md
  are a unit or so off (Med Gray) or brighter (Pink).
  Open question: should the ramps be re-anchored so each original *is* a step?
  It would break equal lightness per step across hues, which is what makes
  "step 6 passes on the ground" true for every hue at once.
- **Card-stack depth by ground step** (onething). Front card `yellow-0`, cards
  underneath `yellow-1`…`yellow-4`, one step per card back — oblique's card
  colour as a family. Tried the `white` scale first: `white-2`→`white-9`
  spans only 1.31:1, invisible on a 3px offset sliver. Yellow reaches 2.5:1
  by `yellow-4`. Capped there: ink border on `yellow-5` falls to 3.18:1.
  Skip tabs step by *tab*, not by card, counted from the back: the
  farthest-back tab is `brown-9`, each tab in front of it a step lighter,
  floored at `brown-6` (white-0 label still 7.34:1). Untabbed cards don't
  use up a step.
  Open question: `yellow-0` is also `--color-warning-bg` — fine while the
  card is the only yellow on screen, worth a look if warnings show up.

### 2026-10-16

- **Canvas vs. card ground** (RULES.md "Data on screen"). taste-translator's
  map moved to `white-4` with cards and chrome on `white-0`; dark mode lifts
  cards to `brown-8` on the `brown-9` canvas. Chosen by eye from a
  `white-0`/`2`/`4`/`6`/`8` contact sheet, every step contrast-checked first.

### 2026-10-15

- **taste-translator joined the kit.** A SvelteKit + Tailwind 4 app that maps
  your taste as a node graph; it was a dark "starfield" with purple/blue/pink
  glass panels, Skeleton's Cerberus theme, and Inter + Fraunces from Google
  Fonts. Now: `kit.css` copied in verbatim and mapped into Tailwind per
  RULES.md, the measured dark mapping under `prefers-color-scheme`, Skeleton
  removed, Inter dropped for the system stack, Fraunces self-hosted through
  Fontsource. All blur, glow, gradient and shadow gone; panels and buttons
  square and ruled, pressed/selected states inverted, pink kept for loved
  things, focus rings and the one primary action. New in RULES.md: network-
  graph edge encoding and rule-carried node states ("Data on screen"), the
  kit-class collision and Fontsource notes (Tailwind section), Fraunces on the
  roster. Project tokens: `--color-tint` (`white-4` / `brown-8`),
  `--color-edge*`, `--color-core-bg`, each with its ratio in the project CSS.
  A11y in the same pass: the "Show Exiled" switch was a `display: none`
  checkbox (unreachable by keyboard) — now a real input under the track;
  the seed input's suppressed focus ring restored; sub-12px text raised to
  the scale; disliked cards no longer faded below AA.
  Later the same day: the app icon (custom rose fill, see RULES.md "Icons"),
  an on-demand key copied from wjeather, a canvas dot grid, and tap/keyboard
  selection so nothing is hover-only (RULES.md "Contrast" and "Data on
  screen"). A review pass also fixed two older bugs: ratings were never
  saved (auto-save only watched node counts), and Reset didn't clear storage.
  Light/dark toggle deliberately skipped, since the system setting is enough here.
  A mono face (IBM Plex Mono, Sligoil Micro) was considered and declined:
  the only live numbers are the zoom % and rating counts, and `tnum` on the
  system stack already keeps their width steady. Two faces were enough.

### 2026-10-08

- **Wjorth: saved theme applied before first paint** (RULES.md "Dark mode").
  The toggle used to set `data-theme` after hydration, so a saved dark choice
  on a light system flashed light on every full load. Now an inline script in
  `app.html` sets it. No colors or tokens changed. Same pass made the
  transaction table's sort headers real buttons with `aria-sort`, and gave
  the unlabeled filters and per-row selects `aria-label`s. **Open:** wjorth's
  dark tokens are still written out twice (the media-query block and the
  `[data-theme='dark']` block), which can drift.

- **Bjornpaedia homepage: doors in place of the full index** (RULES.md
  "Using the kit in a TiddlyWiki static site"). Reuses the nav's
  divider-grid; no new colors or tokens. Checked in headless Chrome at 390px
  (no horizontal overflow) and 1280px, and the search/show-all behaviour
  tested by script. Not yet seen by Kristian in a real browser, not
  published. **Open:** about 840 of 1,900 pages carry none of the twelve door
  tags, and 86 untagged pages have nothing linking to them, so they are
  reachable only through search or the full list.

- **Bjornpaedia: stock green snapped to `green-4`.** Closes the open question
  from 2026-10-06. `tiddler-controls-foreground-selected` is now `#89A271`
  (was `#8ca573`, three units off). On ink 5.18:1, on cornflower 2.78:1, on
  the White 2.65:1 — the same pairs pass and fail as before, so the CSS
  overrides stay.

### 2026-10-07

- **Image ledger on a.wjerk.shop** (RULES.md "Images", "Weight, shown").
  `images.html` lists all 84 image files by size (10.58 MB), filled in by
  `image-index.js` at build time, linked from both footers. Reuses the
  case-study table styles; three small CSS rules added, no new colors. First
  run found 17 files (2.96 MB) that ship but no page loads — mostly the
  photos the dithered tiles were made from — and 10 images hotlinked from
  Flickr and mica.edu that the page-weight numbers can't see. **Not yet
  checked in a browser** at phone or desktop width. The idea came from
  Hannah Gmeiner's permacomputing thesis site, which prints a file size
  beside every image.
  Follow-up the same day: all 10 hotlinked images are now self-hosted (two
  already had identical local copies sitting unused). Hotlinks 0, unused
  files 15 (2.71 MB), 93 images, 11.87 MB. The stated site weight rose from
  9.29 MB to 10.77 MB with no change in what a visitor downloads — the old
  number was under-reporting. A ledger makes the number go up before it
  goes down.

- **onething: pile, stamp, tabs, sticker** (RULES.md "Typography: rotation as
  an accent", "Motion"). Two tilt sizes now written down — 7–12deg for the
  one loud accent, 1.5–4deg per card for a pile. Stickers named as floating
  content that may leave the rectangle. Done is pink, skipped is ink: a
  second state gets shape and side, not a second hue. Measured: `white-0` on
  `pink-5` 4.78:1 (stamp, sticker, tally marks), `white-0` on ink 13.73:1
  (tab); ink outline on `pink-5` is 2.87:1 and so only decorative.
  **Open question:** `.tilt` in `kit.css` covers the accent size only —
  whether the pile tilt deserves a utility waits on a second project using it.

### 2026-10-06

- **Bjornpaedia toolbar icon states** (RULES.md "Using the kit in a
  TiddlyWiki static site", "One palette entry, several backgrounds"). Hover
  on the page and tiddler controls is now `pink-5`; selected on the ground is
  `pink-6`; the editor toolbar keeps its green on ink, with the selected and
  hovered icon colors corrected. All pairs measured, lowest is 4.78:1.
  **Open question:** the green (`#8ca573`) is a leftover from the stock
  ContrastLight palette, not a kit color. It sits within a few units of
  `--green-4` (`#89A271`, 5.18:1 on ink). Kristian likes how it looks; not
  yet decided whether to snap it to `green-4` or whether green belongs in
  this wiki's interaction colors at all, given pink does interaction.

### 2026-10-05

- **App navigation pattern** (RULES.md "Navigation: one bar, grouped, a
  second row for the group"). Wjorth `app/` swapped per-page button rows for
  a site bar (Month · Budget · Debt · Insights) plus a second row inside
  groups with several pages (Budget: Budget/Foundations; Debt:
  Payoff/Steps/Gap/Call prep). Active state is weight + a 3px ink underline,
  not color. Ink on ground measured 13.73:1. Checked in light mode at 390px
  and 1000px; **not yet checked visually in dark mode** (same tokens, so
  contrast should carry, but the underline hasn't been seen there).
- **Stat-tile amounts now fit their card** (RULES.md "Data on screen"). The
  Wjerk dashboard's KPI amounts (`$67,181.73`, 22px mono) overflowed their
  cards at 390px: about 115px of room, 132px of number. Two causes, two
  fixes: the amount scales to its card instead of the viewport (a size
  container plus `clamp(0.75rem, 13cqi, var(--text-lg))`), and the four-up
  row now starts at the 55rem breakpoint, not 40rem, because four cards at
  640px were narrower than two at 390px. Checked at 360, 390, 700 and 1100px,
  and with a $201,545.19 total at 360px. Other pages' big numbers (Call
  prep, Month close-out, Payoff) use whole dollars in wider layouts and
  weren't audited.

### 2026-10-04

- **Shadow exception recorded.** a.wjerk.shop's homepage has one deliberate
  `box-shadow` (faint, on the tilted poster image over the MICA tile). It's
  content-on-content, not chrome, so it fits the existing scope of the
  structure rule; RULES.md now names it as a standing case.
- **bjornpaedia moved onto the kit palette** (TiddlyWiki static site; recipe
  in RULES.md "Using the kit in a TiddlyWiki static site"). Palette tiddler +
  `Wjerk Tokens` stylesheet; links go from default blue to `cornflower-6` (accent stays pink; missing links are pink-6 on a pink-0 tint), ground to
  `--wjerk-white`, nav hover from `blue` to the pink fill a.wjerk.shop uses, nav
  dividers rebuilt with the `gap` pattern. Contrast measured: ink on White
  13.73, `pink-5` links 4.78, `pink-6` hover 7.33, ink on `white-4` bands
  11.81, ink on `pink-0` pill 10.44. **Still open for bjornpaedia:** not yet
  checked in dark mode; the sticky tiddler title (`.tc-title`) is inert as
  built; the homepage intro and entry list use three different side insets;
  the word-count pill's overhang clips off-screen below ~40rem.

### 2026-10-02

- **Compact button size** (`.btn.btn-sm`, `.field`'s 0.375rem/0.75rem padding, about 32px tall) added in Wjorth for secondary actions in dense forms, where kit `.btn` (0.875rem/1.75rem) took over the page. Same square bordered look; meets WCAG 2.2's 24px minimum target. Candidate for kit.css if a second project needs it.
- **Progress bar pattern** added to RULES.md “Data on screen”, from Wjorth's
  Baby Steps page: a square, 1px-bordered track with a flat `--color-data-primary`
  fill, and the number always in words beside it. Measured: pink-5 on white-0
  4.78:1; the dark-mode swap to pink-3 on brown-9 is 8.80:1 (pink-5 there
  would be 4.01:1, still over the 3:1 non-text bar).

### 2026-09-27

- **Fluid type allowed as an exception to the baseline grid** (RULES.md
  “Typography: baseline grid, not a ratio scale”). a.wjerk.shop swapped
  four per-breakpoint font-size stacks for one `clamp()` each, removing
  seven media-query overrides. Endpoints stay in rem; the sizes in between
  are knowingly off-grid.
- **a.wjerk.shop migrated to the kit palette (2026-09-27).** Previously used
  browser-default `blue`/`black`/`white`. Now: `--wjerk-white` (white-0
  #F8FAE7) as the page ground, `--wjerk-black` (black-9 #2D2826) for text,
  `--pink-5` for hover/focus accent fill and focus ring, `--cornflower-6`
  for inline running-text link color (7.38:1 on white-0). Self-contained
  `:root` block in style.css with inline rgb() values — no `@import` of
  kit.css. Pattern to follow for other Wjerk/OOKB static sites.
- **Gap-drawn divider grids** added to RULES.md “Structure: rules, not
  chrome” — replaced ~25 lines of border-borrowing in a.wjerk.shop's nav.
- **Focus on edge-to-edge block links**: inset ring, shared hover fill,
  text-colored ring on accent fill (RULES.md “Contrast”). Came from finding
  the homepage card links' ring clipped by `overflow: hidden`.

### 2026-09-26

- **Slideshow type rotation: 6 families → 33.** Two rules came with it
  (RULES.md "Slideshows / unattended players"): display faces only take
  quotes under 80 characters, and a family with several weights keeps one
  slot and steps to its next weight, width or axis value each time.
  - Velvetyne, from `~/Code/libreFontLibrary`, converted whole (most carry a
    Reserved Font Name): Feroniapi, Anthony, Le Murmure, Compagnon, Combat,
    Terminal Grotesque, and ten Degheest faces (Director, FT88
    Regular/Serif/School/Gothique/Expanded, Louise, Latitude, Equateur,
    Abordage).
  - Google Fonts, Latin subsets from the API: Spectral (all 7 statics),
    Overpass, Newsreader, Atkinson Hyperlegible Next, BioRhyme (weight and
    width axes, so BioRhyme Expanded is the same file), Climate Crisis
    (steps its YEAR axis 1979 → 2050), Fruktur, Oi, Yatra One, Young Serif.
    Astloch has an RFN, so it's the full upstream file instead.
  - **Velvelyne** was requested but is CUTE-licensed, not OFL (same
    category as PicNic). Left out by choice, not pending.
  - Open: Overpass 100 and the 200 weights are hairline at quote
    size and may wash out on a projector. Combat has no curly double
    quotes (the browser falls back for those two glyphs).
- **Every quote credits its typeface.** Small "Type: …" line: face and
  weight/axis shown, designer, SIL OFL, linked to the download page on the
  deck. See RULES.md "Slideshows / unattended players". Also made the deck's
  off-screen slides `inert`, so a link on a hidden neighbour can't take focus.
- **Caption filter catches tab-count prefixes.** "(3) Instagram" was
  projected as a caption; the junk-title pattern now allows a leading
  "(N) ".
- **Two new "Data on screen" bullets: curve the mapping toward the
  everyday range, and let one value take two channels.** In wjeather, the
  wind hatch's line spacing barely moved between 6 and 20 km/h (typical
  days), so it read as constant. A square-root mapping fixed that, and
  line opacity now changes too (0.25→0.4) from the same curve. See
  RULES.md "Data on screen". Open question: whether the √ default should
  become a small shared helper if a second project maps skewed data
  (rain intensity in wjeather is the likely next case).

### 2026-09-24

- **Ledger row tints: zebra stripe and attention row.** Wjorth's
  transaction table got a `white-4` stripe (`brown-8` dark) as a new app
  token, `--color-row-alt`, and uncategorized rows the existing
  `--color-accent-subtle` plus a 3px accent rule on the first cell.
  Contrast and OKLab distance measured for every text color on both tints,
  light and dark. See RULES.md "Color: tints behind text", "Ledger rows".
  `--color-row-alt` lives in the project for now; promote it to `kit.css`
  if a second project needs striped tables.

### 2026-09-20

- **New "Data on screen" bullet: numeric readouts get their own type
  texture.** wjeather added a humidity percentage under the hero
  temperature, set in self-hosted IBM Plex Mono (OFL) rather than
  `--font-sans` — mirrors the texture-as-a-channel idea already in that
  section, now applied to type, plus fixed-width digits so the number
  doesn't jitter the layout as it updates. See RULES.md "Data on screen".
  Colored with the existing `--color-text-muted`, already contrast-checked
  against every sky band; no new token.

### 2026-09-19

- **New RULES.md principle: data portability, plain text as the canonical
  form.** Written while building Wjorth (a budgeting dashboard rebuilt as
  SvelteKit + Tailwind + this kit). Prefer Markdown/JSON/CSV as a project's
  durable data representation over an app-specific opaque store, so it
  stays reusable as needs change. Wjorth's own `state.json`-on-disk (instead
  of browser `localStorage`) is the first concrete instance — see RULES.md
  "Data portability: plain text as the canonical form."
- Wjorth also surfaced the `green-5`-for-data-ink question and a pointer to
  older sibling projects worth revisiting — both logged above under "Open
  questions / next steps."

### 2026-09-16

- **`kit.css` now restores the `hidden` attribute**, closing the open question
  raised 2026-09-11. `[hidden]:not([hidden='until-found']) { display: none
  !important; }` in the base reset, and the rule is written up in RULES.md
  "The `[hidden]` reset" — including why plain `display: none` in the kit
  wouldn't do it (a project's stylesheet loads after and wins on source order).
  Audited first across every project holding kit tokens: onething, fridgechef,
  wjeather, lectureScripts and WritingPlanning use the attribute nowhere at all,
  so the change could not alter any existing rendering. Only two `kit.css`
  copies exist — di200-fieldnotes and wjeather — and both were re-synced from
  canonical; di200's had also drifted, missing the `purple-gray` scale.
  di200-fieldnotes dropped its local one-line patch in favour of the kit's.
- **di200-fieldnotes hit the Notion select-option wall and got a `NOTES.md`.**
  Notion never invents a `select` option on write, so every student's first note
  was a 400 during the 2026-09-14 visit; the same property exists on two
  databases and fixing one wasn't enough. Not a kit matter, but the project now
  carries its own `NOTES.md` in this repo's shape — open items first, reasoning
  underneath — which is a pattern worth repeating in other projects.

### 2026-09-11

- **di200-fieldnotes: the form reordered around what it actually collects.**
  The five things a student is there to record are the observation, the spot,
  the time, and — set once per visit — who they are and which session it is.
  The form had led with Time, which is prefilled and rarely touched, and
  buried Spot sixth under kind/count/photo. Now: what happened, spot, time,
  a rule, then the tags. Three behavior changes worth reusing — the time
  stamps on the first keystroke rather than when the form opened (the form
  can sit open a long while before anything happens); known names are chips,
  which is also how the spelling stays consistent enough for Notion to group
  by it; and Save sticks to the bottom of the viewport. The last two are
  written up in RULES.md "Structure". Found on the way: the `[hidden]` gap
  in `kit.css`, above.
- **The kit's no-build path, used for real.** `~/Code/di200-fieldnotes` is a
  one-screen phone form for class fieldnotes: plain `index.html` linking a
  copied `kit.css`, served by a Cloudflare Worker (static assets plus a small
  `/api`), no framework. Dark mode is the RULES.md token flip in a
  `prefers-color-scheme` block, `kit.css` untouched, as in wjeather. New in
  RULES.md "Structure": choice chips (radio under a pill, inverted when
  checked). Contrast checked: the accent button is `white-0` on `pink-5` at
  4.78:1, AA but not AAA for its bold 16px label; everything else on the page
  clears AAA.
- **The slideshow pattern got a second project, and a version-control rule.**
  `WritingPlanning/gd420/exhibiting-ness` (an are.na archive about exhibiting
  graphic design, built to project in a studio class) reuses chair-ness's
  generator rather than forking it — `build_slideshow.py` gained `--root`,
  `--title` and `--channel-label`, and treats its chair-specific metadata
  file as optional; chair-ness's own builds verified byte-identical after.
  The hard lesson is in RULES.md "Slideshows / unattended players": the
  fetched image folder is a cache, it is re-fetchable from one command, and
  it must be gitignored *before* the first commit. It wasn't, and 268 MB went
  to GitHub — recovering needed a history rewrite and a force-push.

- **Icons became a family.** One frame across every site and app — white
  square ground, brown bordered square, stacked-outline shadow — with one
  pale fill and a monogram in the site's own face varying. RULES.md "Icons"
  carries the rule and the export sizes (SVG tab icon, 180px iOS, 192/512
  manifest, 1024 App Store).
- **wjeather is the first app built on the kit** (SvelteKit + Tailwind 4 on
  Cloudflare), and the first to push it into data. New in RULES.md: "Using the
  kit with Tailwind (v4)" (the mapping recipe), "Color: tints behind text"
  (the step 0–2 / 7–9 budget, and how the scales actually read on screen),
  "Data on screen" (one variable per channel, pink primary, dashed second
  series). "Structure" gained the data-gradient exception. Dark mode shipped
  per project for the first time.
- **Standing practice:** design decisions made in any project that touch this
  system get written here as part of the work, not after.
- **The original Wjerk palette is written down.** Nineteen colors plus the YGB
  gradient, read from the Figma styles into RULES.md with each one's nearest
  kit token and contrast. The kit grew from it, but lost its true blues and
  Golden Rod, and hardened its pink.
- **`kit.css` gained two scales: `cornflower` and `goldenrod`.** The lost
  Wjerk colors, rebuilt on the shared lightness grid so step N means the same
  thing in every scale. No existing token changed.
- **`purple` moved bluer, 336° → 315°.** Same lightness and chroma; it had
  drifted pinker than the original and read as the accent.
- **OOKB → Wjerk.** The palette is named Wjerk throughout the docs now; the
  Figma styles keep "OOKB Palette" so the decks' library doesn't break, and
  the ookb.co domain family is unchanged. White and Black became kit tokens,
  `--wjerk-white` (#F8FAE7) and `--wjerk-black` (#2D2826), and the kit's
  `--color-bg` / `--color-text` point at them — 13.73:1, down from 16.94:1
  with `gray-0` / `brown-8`, still AAA. Projects pick it up when they re-copy
  `kit.css`.
- **White and Black became scales: `white-0…9` and `black-0…9`.** Papers and
  inks, so the long-running cream-and-brown-black story has range of its own.
  `white-0` and `black-9` are the originals exactly; `--wjerk-white` /
  `--wjerk-black` are now aliases for them. Every white holds the Black at AAA;
  every black is AA text on the White; `black-7` is the palette's Brown.
- **Changelog merge conflict resolved.** The two sides held different
  entries (2026-08-27 ×2 vs. 2026-08-29 and 08-30), so both were kept and
  put in date order; nothing was dropped.
- **Dark mode's status colors are mapped.** Success, warning, danger and info
  flip to step 3 of their own hue (~10:1 on `brown-9`), their panels to step 8,
  and the pressed accent to `pink-2` — in RULES.md "Dark mode" and in
  `scripts/contrast.py`, which now audits clean in both modes. The 15 failing
  dark pairs are gone.
- **The softer pink replaced the hot one.** The pink scale was rebuilt at the
  original Wjerk Pink's chroma (0.178, down from 0.226) — same lightness and
  hue per step. Accent 4.78:1 on the White, dark accent 8.80:1; every
  wjeather pink line still ≥3.41:1.
- **The kit was re-copied into the projects.** onething (`src/app.css`,
  `src/lib/palette.css`) and fridgechef (`app/palette.css`) got every changed
  value — pink, purple, and onething's ground and text — plus the new
  goldenrod, cornflower, white and black scales. The two live di200 lecture
  decks took the purple values only; their own background, text, accent and
  font were left alone, and the backup copy was skipped.
- **wjeather's wind drift is built** — the first motion idea in any project;
  see RULES.md "Motion".
- **wjeather got an on-demand key**, and RULES.md "Data on screen" gained the
  rule behind it: an abstract screen needs a way in for sighted viewers, a `?`
  opening a native dialog, never shown first, samples drawn from the screen's
  own tokens.
- **`purple-gray` added; cloud now differs day from night.** The last of the
  Wjerk palette's missing hues (Purple Gray ≈ `purple-gray-5`). wjeather's
  cloudy hours take the warm gray by day and the purple-gray after dark —
  siblings by design, distinct from the clear night and from rain.
- **The sky bands' blur came out.** Edges are hard at every hour now; the
  cloud-cover-softens-the-edge idea is gone, and with it the only use for the
  cloud-cover reading, so wjeather stopped fetching it. Cloud still shows as
  its own band color. See RULES.md "Structure: rules, not chrome".

### 2026-08-30

- **Added "Slide decks: talks vs. teaching support" to RULES.md**, from a
  sampled review of the 25 lecture PDFs Kristian dropped in `reference/`
  (2010–2026). Key finding: the expressive full-bleed/collage/aphorism
  look isn't new — it's fully present by 2021 (`FreeOpenCulture`) and the
  2026 decks intensify it rather than invent it. The real split is genre
  (public talk vs. teaching-support handout), not era — a 2023 teaching
  deck is as plain as a 2010 one.
- New concrete rules captured: 16:9/16:10 canvas (maximize full-screen);
  full-bleed-to-the-edge as a deliberate exception to the kit's usual
  "pin the box, contain scales into it" image sizing; slide text must
  cue-the-speaker or illustrate/metaphorize rather than restate spoken
  words (confirmed directly, ties to the metaphor/illustration examples
  cataloged in RULES.md); a recurring "TYPE: / IMAGE:" credit-caption
  convention; the vintage-etching/mascot-collage compositing device as an
  active technique, not just an image-sourcing preference.
- `reference/` PDFs were sampled (page slices via PyMuPDF), not read
  page-by-page in full — see open questions for what's still unexplored
  (the teaching-deck genre specifically).

### 2026-08-29

- **Added "PDF generation" and "Slideshows / unattended players" to
  RULES.md**, extracted the same way every other section here was —
  from what's actually shipped, this time in `syllabiBuilder`'s
  Markdown→pandoc→WeasyPrint pipeline and `chair-ness`'s
  `build_slideshow.py` ambient-mode player, rather than from a `kit.css`
  screen-CSS pattern.
- **Added two drop-in template files**, not just documentation:
  `slideshow-template.html` (the ambient two-layer pattern — confirmed as
  the default to reach for going forward, not just one of chair-ness's
  four build variants) and `print/` (`md2pdf.sh`,
  `pandoc-template.html`, `print.css`), generalized from their
  syllabus/chair-ness-specific originals. Both work with zero setup
  (system fonts, no external assets) and take on a project's real content
  by editing values in place rather than templating.
- **Font embedding note**: chair-ness's base64-embedded OFL fonts were a
  narrow fix (one self-contained file, no venue wifi guaranteed, and a
  single copy has to travel into another repo's deploy) — not a slideshow
  default. `slideshow-template.html` doesn't embed anything; link fonts
  normally unless one of those specific constraints applies.
- Kristian may provide PDFs and/or Figma prototypes showing more of the
  slide-design vocabulary beyond what chair-ness currently covers — revisit
  `slideshow-template.html` against those once supplied (see open
  questions).

### 2026-08-27 (later)

- **Three decks arrived and recalibrated the density rule, then a fourth fact
  rescoped it.** "On Mending," "On Making Stuff," and "Loose Threads" (all
  2026, all shared as Google Slides) run two to eight words a slide against
  `di200-wk1`'s median of 58. But these are five-to-ten-minute ceremonial
  talks, not lectures — so the number is now scoped to that form and the
  lecture ceiling is deliberately left open rather than guessed at.

- **The deck is the essay's pull-quotes.** All three lift their slide text
  nearly verbatim from prose written first. "On Mending" is six fragments from
  the FEC remarks; "Loose Threads" takes four of five slides straight from its
  own text. This is the practical mechanism behind "the slide is not the
  script" — the explanation stays in the essay because the essay still exists.

- **One axis of visual coherence, never two.** Subject ("On Mending": seven
  painters of nets, 1634–1954; `chair-ness`: all chairs, any style), period
  ("On Making Stuff": unrelated subjects inside 1864–1915), or kind (all
  paintings — which is also a noise filter, since keyword searches otherwise
  return vessels and daggers). Measured: "chair" plus Victorian etchings
  returns zero usable results where either alone returns plenty.

- **The title is a formula** — abstract noun phrase plus a plain-speech
  parenthetical, usually opening "or,". All three follow it.

- **`bjorn-voice` gained the saturated metaphor register.** The restrained
  ratio was derived from "Mending" and stated as universal; "Loose Threads"
  saturates instead — twenty-odd agricultural touches — and is the one he likes
  best. Saturation needs three things at once: wordplay-generating vocabulary,
  a title that admits the conceit is pushed, and real darkness early to earn
  the lightness. Also recorded: staging a failed metaphor as the opening move.

### 2026-08-27

- **RULES.md gained eight `## Presentations:` sections** — the first
  medium-specific block in the document, covering decks, projected
  slideshows, and render-to-PDF work. Everything in web layout so far had
  assumed a scrolling page; a fixed-aspect slide read in a room is a
  different constraint.

  The governing rule is **the slide is not the script**. A lecture is two
  documents and the deck is not the one carrying the argument — most
  explanatory prose on a slide is already written in the script file
  beside it. A slide gets only what reads better in the eye than the ear:
  a name, a list, a comparison, or a line worth quoting.

  Measured from `~/Code/lectureScripts/lecture-design-thinking/
  di200-wk1-deck.html`, 67 slides. Median ~58 words per slide; 13 slides
  over 75. The useful finding was the opposite of expected: **the
  aphoristic voice is already there** — 72% of that deck's `.lead` lines
  and headings run 13 words or under, and those are the strong ones
  ("Consent is not transitive", "You cannot code a vibe"). The failure is
  dilution, not absence, so the rule protects something present rather
  than installing something new.

  The best diagnostic to come out of it: **never shrink type to fit.**
  That deck carries 10 inline `font-size` overrides below its own scale,
  and every one marks a slide that should have been split. Spending the
  type scale to hide overflow destroys the only warning the system gives.

- **Image slots replace hardcoded filenames.** A slide declares
  `data-img` plus a `data-img-brief` describing what the image is *for*,
  so the slot can be searched against and can prompt you. Paired with a
  loud/silent build split: unfilled slots are conspicuous on the desk and
  silent when projected.

  This came out of noticing that `di200-wk1`'s five beat images are still
  missing while its `images/README.md` explicitly designs for silence —
  quiet fallback, credit line commented out. Correct for the podium,
  wrong for the desk, and the reason the gap persisted.

- **Sourcing gained a defined order**: are.na channels first, then the
  three no-key museum APIs (Met, Art Institute of Chicago, Cleveland),
  then Wikimedia Commons last. The Images "Sourcing" rule already said to
  check are.na first; this makes it a cascade and fills in the museum
  half, which the old list (photography-weighted — FSA, Flickr Commons)
  did not cover for paintings.

  The division of labour: machine narrows, you choose, machine writes the
  credit line. Metaphorical judgement does not automate; filtering four
  million objects to forty does.

- **Local files, never hotlinks, for anything projected** — network is not
  a runtime dependency in a room you do not control. `chair-ness` already
  models the two-build split from one manifest, and gitignores its caches
  (423 images, 348MB on disk, 5.5MB `.git`).

### 2026-08-26

- **Dark mode moved from deferred to specified.** The chair-ness exhibition
  slideshow (`~/Code/chair-ness`) needed a dark treatment for gallery
  projection, so the palette got built and contrast-checked for real rather
  than in the abstract. It turned out to need no new colors — it is the
  brown scale with its ends swapped, `--brown-9` ground and `--brown-0`
  text, with `--pink-3` as the accent in place of light mode's `--pink-5`.
  RULES.md "Dark mode" now carries the measured ratios and the semantic
  token mapping.

  The useful finding: `--brown-4` (7.06:1) is the dimmest rung that still
  clears AAA on `--brown-9`. `--brown-5` looks like a usable gray and is
  not — 4.36:1, which fails AA for normal text. That is exactly the kind of
  "muted" tone RULES.md "Contrast" warns about.

- **Images gained "Sizing" and "Type over images."** Both came out of the
  same project. The sizing one is a genuine trap: `object-fit: contain`
  only fills the box it is given, so `max-width`/`max-height` leave small
  images floating at natural size. The type rule is a contrast requirement
  — light type over photographs of unknown content cannot be verified, so
  it goes on an opaque block.

- **Motion gained an exception for auto-advancing media**, with the
  `prefers-reduced-motion` obligation and length-scaled dwell time.

### 2026-08-07
- Folded `Personal tropes.txt` into the system: added "Ethos: do more with
  less," "Color: yellowish-gray background, dark brown line work" (already
  the kit.css default, now documented as deliberate), "Typography: the
  roster" (named libre typeface shortlist), "Typography: rotation as an
  accent," and an Images "Style" note on Victorian etchings — all in
  RULES.md.
- Added `.tilt` utility to `kit.css` for the rotation-as-accent trope.
- Left Friz Quadrata out of the shared roster (proprietary, conflicts with
  the open/libre rule) — see open questions for the libre-alternative
  idea.
- Left "the four freedoms, but for signs on substrates" as an open
  question rather than a rule — not developed enough yet to assert.

### 2026-07-23
- Added `showcase.html` — a live reference page (`<link>`s `kit.css`
  directly) showing the type scale, semantic color pairs with computed
  WCAG contrast ratios, the raw 10-step color ramps, and components
  (`.btn`, `.tag`, `.panel`, `.divider`, `.frame-thick`/`.frame-thin`,
  focus states), plus a side-by-side of `Code/oblique`'s independently-
  arrived-at equivalents (`.cool-border`, pill link, self-hosted
  display font).
- Added a baseline-grid type scale to `kit.css` (`--text-2xs` through
  `--text-3xl`, paired `--leading-*` line-heights on a 6px/0.375rem grid) —
  see RULES.md "Typography: baseline grid, not a ratio scale."
- Wired `html`/`body`, `h1`–`h6`, `p`, `small`, `.label-upper`,
  `.caption-muted`, `.panel-footer`, and `.btn` to the new type tokens.
  `.label-upper`/`.caption-muted`/`.panel-footer`/`.btn` changes are
  zero-visual-diff — their old hardcoded sizes matched scale rungs exactly.
- Added a References section to `README.md`: Bringhurst (*Elements of
  Typographic Style*), Lupton (*Thinking with Type*), Tim Brown ("More
  Meaningful Typography," *Flexible Typesetting*), Alan Dalton ("Good
  designers, bad websites: a proposal").
