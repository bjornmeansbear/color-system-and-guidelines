# Notes

Where things stand: open questions first (most likely to matter next time),
changelog underneath. Update this as work happens — it's meant to be read
before starting a session, not just written to at the end of one.

## Open questions / next steps

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
  specific project idea calls for it, not as a system default.
- **Dark mode — colors answered, not yet wired.** RULES.md now carries the
  measured dark palette and the light→dark semantic token mapping. What's
  left is a decision, not a design: whether to ship the flip in `kit.css`
  (which still pins `color-scheme: light`) or keep leaving it to projects
  that need it.

## Changelog

<<<<<<< HEAD
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
=======
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
>>>>>>> 5d22dcfb7cb10c1d56bc6ed5d22e37c6aff0c868

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
