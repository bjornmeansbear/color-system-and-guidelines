# Notes

Where things stand: open questions first (most likely to matter next time),
changelog underneath. Update this as work happens — it's meant to be read
before starting a session, not just written to at the end of one.

## Open questions / next steps

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
- **Dark mode** — deliberately deferred per RULES.md; the semantic token
  layer is structured to support it later, just not built yet.

## Changelog

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
