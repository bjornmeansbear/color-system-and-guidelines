# Notes

Where things stand: open questions first (most likely to matter next time),
changelog underneath. Update this as work happens — it's meant to be read
before starting a session, not just written to at the end of one.

## Open questions / next steps

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
- **`print/` hasn't been run end-to-end yet** — it's a direct
  generalization of `syllabiBuilder/build/`'s working script, but nobody's
  built an actual PDF from the generalized copy to confirm the pandoc/
  WeasyPrint invocation still works with the MICA-specific bits (font
  paths, `--color-tint` token) removed.
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
- **Consolidate the palette HTML files.** `palette-1.html`, `palette-2.html`,
  and `palette-docs.html` read as three sequential drafts of the same
  living-style-guide page, not three distinct tools. `showcase.html` (added
  2026-07-23) covers the "applied, in practice" half of this — type/color
  tokens rendered as real components, not an abstract inventory — but the
  three palette files still duplicate each other and haven't been folded
  in or retired. Decide: merge their swatch/contrast-pair inventory into
  `showcase.html`, or keep the two kinds of document (inventory vs.
  applied) separate on purpose?
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

### 2026-09-11

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
