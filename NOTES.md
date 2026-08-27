# Notes

Where things stand: open questions first (most likely to matter next time),
changelog underneath. Update this as work happens — it's meant to be read
before starting a session, not just written to at the end of one.

## Open questions / next steps

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
