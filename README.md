# color-system-and-guidelines

Personal color, layout, and typography system for all my projects (OOKB,
Wjerk, Etc.) — the shared kit so each new project doesn't reinvent the
same rules from scratch.

## Quick start

- **`kit.css`** — drop-in stylesheet: the color scale, semantic tokens
  (`--color-accent`, `--color-text`, etc.), base reset, and the border/
  button/panel primitives every project reuses. No build step — `<link>`
  it directly or `@import` it into a framework's stylesheet.
- **`RULES.md`** — the reasoning behind everything in `kit.css`: why pink
  is the accent, the contrast bar, typography ethos, image treatment, open
  questions (motion, image sourcing links) still being worked out.
- **`NOTES.md`** — open questions, what's left to do, and a dated
  changelog. Read this first when picking work back up.
- **`showcase.html`** — `kit.css`'s type scale, color tokens, and
  components rendered live (it `<link>`s `kit.css` directly), plus a
  side-by-side of how `Code/oblique` independently arrived at equivalent
  primitives. Open it in a browser to see the kit applied, not just listed.
- **`slideshow-template.html`** — drop-in template for an auto-advancing,
  unattended slideshow (gallery projection, ambient background piece).
  No build step — edit the `CONFIG`/`IMAGES`/`TEXTS` values at the top of
  its `<script>` directly. See RULES.md "Slideshows / unattended players".
- **`print/`** — drop-in Markdown-to-PDF toolchain (`md2pdf.sh`, a pandoc
  template, and `print.css`) for print output that uses this kit's colors
  and type scale. See RULES.md "PDF generation".

## References

Books and articles behind specific decisions in `kit.css` / `RULES.md` —
not just further reading, the actual source of a rule:

- **Typography, baseline grid** — Robert Bringhurst, *The Elements of
  Typographic Style*; Ellen Lupton, *Thinking with Type*. The
  vertical-rhythm thinking behind the kit's type scale: line-heights land
  on even multiples of a base unit, font-sizes are chosen to pair with
  those rungs (not the other way around).
- **Typography, fluid sizing** — Tim Brown,
  ["More Meaningful Typography"](https://alistapart.com/article/more-meaningful-typography/)
  (A List Apart) and
  [*Flexible Typesetting*](https://abookapart.com/products/flexible-typesetting.html)
  (A Book Apart). Modular scales, and type that responds fluidly to
  viewport/container instead of jumping at a fixed breakpoint — same
  instinct as `kit.css`'s existing `clamp()` use on `.frame-thick`,
  extended to the type scale's baseline-grid steps.
- **Accessibility, design process** — Alan Dalton,
  ["Good designers, bad websites: a proposal"](https://alistapart.com/article/good-designers-bad-websites-a-proposal/)
  (A List Apart). Accessibility personas + recognition-over-recall as a
  way to catch accessibility problems while designing, not after —
  matches RULES.md's rule to check contrast as tokens are chosen, not as
  a pass at the end.

https://jxnblk.com/blog/color-palette-documentation-for-living-style-guides
hmmm -> what's this? https://github.com/bjornmeansbear/color-documentation

---

Original OOKB (now Wjerk) colors — an earlier web version, as LESS variables. The
Figma set with exact values is in RULES.md "Color: the original Wjerk palette";
its colors are all `--wjerk-*` tokens in kit.css at the Figma values
(`--wjerk-white`, `--wjerk-black`, `--wjerk-med-gray`, `--wjerk-pink`…).

/* Color Palette */
@ookb-pink:          rgba(236,64,121,1);
@ookb-brown:         rgba(47,41,38,1);
@ookb-gray:          rgba(132,132,120,1);
@ookb-darkgray:      rgba(96,103,103,1);
@ookb-lightgray:     rgba(194,211,186,1);

@ookb-red:           rgba(183,80,81,1);
@ookb-orange:        rgba(195,115,99,1);
@ookb-yellow:        rgba(197,192,101,1);
@ookb-green:         rgba(140,165,115,1);
@ookb-blue:          rgba(157,178,176,1);
@ookb-purple:        rgba(174,139,164,1);

(I have more now somewhere else!)

The current scale lives in `kit.css` — link or copy it from there, never from
a pasted block (pasted copies drift; `scripts/drift.py` finds the ones that have).

Color palette stuff:

this is scope creep, but I did start playing around with a wider, improved OOKB color palette based on the work of Jxnblk and MrMrs

https://www.a11yproject.com/
https://clrs.cc/
https://colorable.jxnblk.com/
https://randoma11y.com/
https://jxnblk.com/hello-color

https://github.com/jxnblk/colorable
https://github.com/jxnblk/colorable-app
https://github.com/jxnblk/palx
https://github.com/jxnblk/contrast-swatch
https://github.com/jxnblk/hello-color
https://github.com/jxnblk/hello10k

https://mrmrs.cc/writing/counting-accessible-color-combinations/
https://mrmrs.cc/writing/design-reading/

https://github.com/mrmrs/color-systems
https://github.com/mrmrs/randoma11y-js
https://github.com/mrmrs/css-colors
https://github.com/mrmrs/css-border-colors
https://github.com/mrmrs/skill.color-expert
https://github.com/mrmrs/colors
https://github.com/mrmrs/colors-saturated

https://github.com/johno/css.gui
https://github.com/johno/random-hex-color
https://github.com/johno/random-a11y-api
https://github.com/johno/css-color-list
https://github.com/johno/random-a11y-combo
https://github.com/johno/random-a11y-combo-api
https://github.com/johno/random-a11y-nn
https://github.com/johno/random-a11y-api
https://github.com/johno/colorable
https://github.com/johno/flexbox
https://github.com/johno/clrs
https://github.com/johno/get-contrast
https://github.com/johno/gray
https://github.com/johno/is-named-css-color
https://github.com/johno/named-colors
https://github.com/johno/scrutinize

This should probably break into its own repo