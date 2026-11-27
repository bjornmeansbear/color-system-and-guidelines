---
name: bjorn-design
description: Kristian Bjornard's personal design system — color, typography, layout, presentations, print. Use whenever making visual or front-end decisions in ANY project, not just this repo: picking colors or an accent, writing CSS or Tailwind config, choosing typefaces, setting a type scale, building a page/component/landing page, designing a slide deck or lecture presentation, generating a PDF or poster, adding dark mode, or checking contrast and accessibility. Also use when he says something looks "off," "not mine," "too generic," or asks what the house style is.
---

# Bjorn's Design System

The source of truth is this repo, not this file. `kit.css` holds the tokens,
`RULES.md` holds the reasoning, `NOTES.md` holds what's unsettled. This file is
the always-loaded layer: the decisions that don't change, plus where to read for
depth. **Read the relevant `RULES.md` section before doing substantial work in
that area** — it carries the why, and the why is what makes the rule applicable
to a case it doesn't literally cover.

Sibling skill: `bjorn-voice`, for prose. Same ethos, other medium — compress
don't shrink, cut what does no conceptual work. If a task involves both writing
and design, both apply.

## The ethos

**Do more with less.** Solid rules instead of shadows. Kit tokens instead of
made-up colors. Start with one accent (the home pink, or navy) for links and
focus; as a project grows more complex, lean into the whole Wjerk palette for
objects, labels, stamps and data. Every color still does conceptual work.
Restraint is the style — in the number of moves, not in ambition.

## The non-negotiables

These are the answer unless a project has a specific stated reason otherwise.
"It's conventional" is not a reason.

**Pink is the home accent.** `--color-accent: var(--pink-5)` — the original Wjerk
Pink's softer, dustier pink (the scale was rebuilt at its chroma 2026-09-11). Not blue — blue only
ever appeared as an undecided default, so it doesn't get to be the default.
Pink is deliberate: on climate/sustainability work the expected accent is green
or blue, and pink reads as a surprise instead of a cliché. It is the one thing
that marks the work as his across every past pass. A project may take any
bright Wjerk color as its accent instead (orange, red, goldenrod, cornflower),
contrast-checked, so a family of tools varies while staying in one aesthetic
universe (2026-11-24). Take the measured set for that hue from `RULES.md`
(Accent sets) and override light *and* dark, or dark mode inherits a light
step that fails.

**Warm ground, dark brown line work.** `--color-bg: var(--wjerk-white)`
(#F8FAE7, a warm cream), `--color-text: var(--wjerk-black)` (#2D2826, a soft
brown-black) — the Wjerk palette's own White and Black. Not black on white.
Each heads a scale of its own: `white-0…9` (papers, creamier as they go) and
`black-0…9` (inks; `black-9` is the Black, every step AA text on the White). This
pairing is a personal trope that predates the kit.

**The originals are tokens too.** Every original Wjerk color is in kit.css at
its exact value as `--wjerk-*` (`--wjerk-med-gray`, `--wjerk-pink`,
`--wjerk-navy`…). The ramps were built from those hues but don't always land
on them, so never round an original to its "nearest step" — use the
`--wjerk-*` token when the color is the identity, a ramp step for tints and
guaranteed-contrast steps.

**Structure from rules and whitespace.** No gradients, no border-radius on
*chrome* — panels, buttons, dividers, anything framing content. 1–2px solid
borders and space instead. Shadows aren't banned, but they're never the first
answer to "make these stand apart": try a border, a ground change, whitespace,
or an offset outline first, and use a shadow only when those do the job worse. Radius is fine on content that floats
(a quote card over an image) and on pill/tag elements (`border-radius: 999px`).
Interactive state inverts foreground/background on press — never elevation,
never a hover-glow.

**High-contrast pairs, always computed.** Near-black on light or the reverse;
never mid-gray on light-gray. Do not eyeball this and do not trust a token's
name — a "muted" token already shipped once at 4.35:1 while reading fine as an
isolated swatch. Run the checker (below). Focus is always visible: thick
accent-colored `:focus-visible` outline, never suppressed.

**Open/libre type, or the system stack.** OFL or similar, self-hosted — never a
proprietary webfont. `--font-sans` is the system-stack default; reach for it
when a project doesn't need its own voice, and don't treat that as a failure.
A project earns a `--font-display` by self-hosting an OFL face.

**Mobile-first, then the browser's own flexibility.** Base styles are the
stacked single column. Wider layouts come from the natural flexibility of HTML
and CSS (grids and flex rows that wrap and rearrange continuously), not a
skinny column with empty space on both sides. As many breakpoints as the design
needs; `40rem` and `55rem` are the conventional starting values. Written by
hand — the kit has no build step and must work as a plain `<link>`.

**Baseline grid, not a ratio scale — as a starting place.** No single scale
is right for everything; start here and change it per project. Line-heights are multiples of 6px
(18/24/30/36/42/54); font-sizes are chosen to pair with a rung, not generated
by applying a ratio. Everything in rem so the root scales the whole system.
The size/leading ratio sawtooths as sizes share a rung — that's correct, not a
bug. `kit.css` sets no root font-size; it inherits the browser default.

## Check contrast, don't estimate it

```
python3 scripts/contrast.py                  # audit every semantic pair, light + dark
python3 scripts/contrast.py pair pink-5 gray-0
python3 scripts/contrast.py find brown-9     # every token that passes AA on that ground
python3 scripts/contrast.py find gray-0 --aaa
```

Accepts token names, hex, or `rgb()`. Reads `kit.css` directly, so it stays
correct as tokens change. Exits nonzero on an AA failure — usable in a hook or
CI. Run it before shipping any new pairing, especially anything named "muted"
or "subtle."

`python3 scripts/drift.py [path...]` finds pasted copies of kit colors that no
longer match `kit.css` — in this repo by default, or in another project.

Standing bar is WCAG AA; prefer AAA for body text, which most of this palette
already clears.

## Measured, ruled, or asked

Every color, type, or layout decision is one of three kinds. Say which.

- **Measured.** A number from a script: `contrast.py` for any text-on-ground
  pair. Quote the ratio. A pairing with no number hasn't been checked.
- **Ruled.** `RULES.md` already settles it. Name the section. This is his
  taste, written down. Apply it without asking.
- **Judgement.** No number or rule covers it. If it's aesthetic (an accent or
  ground override, a display face, an image, a new token or tint, a layout the
  rules don't describe, breaking a rule), don't pick. Mark it **ASK ME**, offer
  two or three options inside the system, and wait. Mechanical calls (file
  names, implementation details) don't need asking.

Never ask what a rule already settles. When he answers an ASK ME, write the
answer back (below), so the same question doesn't come up twice. That's how a
judgement becomes a rule.

**Tells to catch.** Looks the brief never asked for: a whole UI theme dropped
in, emoji and stock icons, made-up stats, untrue badges, hollow button copy
("Get started," "Unlock"), the centered hero, three equal feature cards,
numbered section labels, hover glow, fade-on-scroll, mood gradients, a skinny
centered column, and the kit itself on autopilot. Each is a question to ask,
not a ban. The full list, with why each happens, is `RULES.md` "Tells:
defaults nobody asked for."

**Starting a project:** before building, list in one message what `RULES.md`
doesn't settle for it — accent or ground override, display face, whether it's
projected (see "An open tension") — each marked ASK ME. In the same message,
name which **signatures** (RULES.md "Signatures: what makes it a Wjerk
project") the project will carry, and what new one it might add. Cream and ink
alone don't make a page a Wjerk project; the signatures do.

**Working with him on a page** (learned building library.wjerk.shop):
- **Match the depth to the time.** Two modes, and say which one at kickoff
  (ask if it isn't clear):
  - *The five-minute version*, for something that just needs to exist: the
    house default, rolled out the same way every time. kit.css, system
    stack, cream and ink, ink-ruled controls, a compact header beside the
    content, the footer order with the Elsewhere list, and one signature
    (the stamp for its one action, say). No exploration rounds.
  - *The deep version*, for anything getting hours: everything below
    applies. Find the metaphor, use the whole screen, try many things.
  A five-minute page should still look like family, not like any site.
- **Avant-garde, and still intuitive.** Aim ahead of the average web, not at
  it, and keep it obvious to use: a novel metaphor people already know
  physically, and the whole screen as one composition. The model is
  wjeather (the screen *is* the forecast: time down, temperature across,
  no widgets). If a layout could be any site's, it isn't done.
- **Design, don't arrange.** He isn't after the average answer ("put the text
  in order, left-aligned"). Derive the visual language from the content's own
  metaphor (a library has shelves, boards, spines, labels, bookends) and use
  space as a material: what's full-bleed, what's inset, what overlaps, what
  is tilted. Ask what the physical version of the thing does.
- Check his own projects before inventing a control, and name the source.
- **When an idea is too much, shrink it; don't retreat to the generic.** He
  enjoys the bold version, then often says "too clever" or "too much room".
  The fix that worked was a smaller form of the same metaphor (outlined
  ghosts → one shelf-label card), not a plain counter in the header. A
  metaphor that already carries the content gets noisy when repeated for
  navigation, so pick a different, smaller one there. Build bold ideas where
  they're easy to drop.
- **Try many things.** The wild versions are worth building even when they
  won't ship: they're how the better idea shows up (asking where the count
  could live led through outline ghosts to the shelf label, which stayed).
  Expect several rounds: make, screenshot, react,
  shrink or swap. Keep each round cheap (a switch in the URL, a scratch
  comparison page) so there's appetite for the next one.
- **Use the whole palette.** The family of Wjerk colors seen again and
  again is identity too, not just ink on cream. Reach for the originals
  (`--wjerk-*`: goldenrod, navy, red, cornflower, green, purple…) and
  their ramps for controls, labels, objects and data, and let a project
  carry several of them. The wjavelength results show which pairings he
  likes; use them.
- Color choices come as a drawn lineup of 4–6 contrast-checked options
  from across the palette. Rule out pairs that are AA-large only when the
  element can get small.
- Hover changes color by default (swap or invert). Movement, scale or tilt
  on hover only when the project's metaphor calls for it (a card you'd
  actually pick up, a book that slides off the shelf), not as decoration.
- Rules sparingly in secondary areas (footers, lists): group with space.
- **Use the space; get to the real content fast.** On a wide screen, the
  room is there to be used: tools beside the title, not stacked under it,
  so the content (the books) starts high on the first screen. The layout
  itself should be interesting and beautiful, composed rather than a
  default stack of austere UI. Put new information into text already on
  the page (the blurb became the live description of the filter) before
  adding a line or a box.
- **Open by default, and linked in.** Every project says how it's made,
  states open licenses, shares its data where safe, and credits what
  belongs to others. Launch isn't done until the hubs link to it
  (kristian.bjornard.com, a.wjerk.shop footer and index) and its footer
  links out to the family. RULES.md "Open by default".
- Screenshot phone and desktop after every visual change, before reporting.
- **Small steps, each its own commit, so backtracking is cheap.** Seeing an
  idea often shows him it was wrong and sparks a different one, which can
  mean going back a step or two and setting off on another vector. Keep
  one commit per visual step with a plain message, so "go back two steps"
  is a clean revert, and offer the recent steps by name when he wants to
  backtrack. When a correction is ambiguous, undo the smallest thing it
  could mean and say exactly what changed.
- **Ask for the why, briefly.** When he keeps or rejects a design, ask one
  short ASK ME with a few likely reasons as options (e.g. "too much room",
  "too clever", "not ours / generic", "wrong mood", "hard to read", plus
  his own words), so the reason can steer the next round and go into
  NOTES.md. Skip it when he's already said why. A reason in his words
  ("too clever") is worth more than a guess; record it verbatim.

## Where to read

Load the section from `RULES.md` before working in that area.

| Working on | Read |
|---|---|
| Colors, accent, palette | "Color: pink is the home accent", "Color: yellowish-gray background" |
| Anything that might look generic | "Tells: defaults nobody asked for" |
| Starting a project, choosing a control | "Signatures: what makes it a Wjerk project" |
| Footers, licenses, launching, linking projects | "Open by default: the design commons and the family web" |
| Contrast, focus, a11y | "Contrast: high-contrast pairs only" |
| Panels, buttons, borders | "Structure: rules, not chrome" |
| Choosing a typeface | "Typography: open/libre first", "Typography: the roster" |
| Type scale, leading | "Typography: baseline grid, not a ratio scale" |
| Rotated/tilted elements | "Typography: rotation as an accent" |
| Photos, illustration, sourcing | "Images" |
| Animation | "Motion" |
| **Slides / lecture decks** | The eight "Presentations:" sections — start with "the slide is not the script" |
| Talk vs. teaching deck | "Slide decks: talks vs. teaching support" |
| Auto-advancing / ambient screens | "Slideshows / unattended players" |
| PDF, print, posters | "PDF generation: Markdown → pandoc → WeasyPrint" |
| Risograph, two-ink print, French fold | "Risograph" |
| A book drawn from a catalog (spines) | "Bjook", "Shelves" |
| Dark mode | "Dark mode" |
| Token naming | "Naming" |
| Breakpoints, layout | "Layout: mobile-first, the browser's own flexibility" |
| The pre-kit palette, adding colors | "Color: the original Wjerk palette" |
| Tints behind text, pale fills | "Color: tints behind text" |
| Charts, data layers, gradients as data | "Data on screen" |
| Tailwind setup | "Using the kit with Tailwind (v4)" |
| Favicons, app and home-screen icons | "Icons: one family across sites and apps" |

Templates in this repo to start from rather than rebuild: `slideshow-template.html`
(ambient/unattended player), `print/` (pandoc → WeasyPrint PDF pipeline),
`showcase.html` (what the kit looks like applied).

## Using the kit in another project

Copy `kit.css` in and link it plainly; there is no build step and no package. Copy the whole
file, never a hand-pasted subset of the scale. After a kit change, run
`python3 scripts/sync.py --all` (add `--dry-run` to look first): it re-copies
every project's `kit.css` that has no local edits, then runs the drift check
over pasted fragments. `python3 scripts/drift.py --fix <path>` rewrites those
to the kit's values in the file's own notation — contrast-check the pairings
first if the change is a hue rebuild rather than a rounding fix.
Override `--color-accent`, `--color-bg`, `--font-display` per project if there's
a reason — the semantic layer exists so a project can differ without forking the
scale. Don't invent a parallel token vocabulary: the names (`--color-accent`,
`--color-text`, `--color-bg`, `--color-frame`) were standardized by hand across
projects before this repo existed.

For a SvelteKit + Tailwind project (his default stack), map the tokens into the
Tailwind theme rather than restating hex values in a config — the recipe is in
`RULES.md` "Using the kit with Tailwind (v4)", first done in wjeather.

**Write back.** Any design decision made in another project that touches this
system — a new token or tint, an icon convention, a data-viz pattern, a stack
recipe, a palette finding, an answered ASK ME — gets recorded here as part of
the work: the rule in `RULES.md`, the finding or open question in `NOTES.md`,
plus a changelog entry.

## An open tension

Don't resolve this silently — it's a live design question, not an oversight.
Check `NOTES.md` for the current state before assuming either way.

**Deck color vs. kit color have never been reconciled.** The kit is pink on
warm gray. The AY26 lecture decks are black/white/grayscale with per-lecture
semantic accents and no pink at all. Neither document references the other.
If a task touches both, ask whether projection is its own context.

## Dark mode ships in kit.css

Since 2026-10-26. It follows the system setting: brown scale with its ends
swapped, `--brown-9` ground, `--brown-0` text, `--pink-3` accent, `--brown-4`
the dimmest token allowed to carry text. A project doesn't build its own;
it only overrides tokens it has a reason to (taste-translator lifts cards to
`brown-8`). `data-theme="light"` on `<html>` keeps a page that isn't ready
light; `data-theme="dark"` forces dark for a saved toggle. `RULES.md` "Dark
mode" has the measurements and the toggle recipe.
