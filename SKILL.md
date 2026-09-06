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

**Do more with less.** Solid rules instead of shadows. A handful of tokens
instead of an open palette. One accent instead of a rotating cast. Restraint is
the style — not a budget constraint you'd lift if you could.

## The non-negotiables

These are the answer unless a project has a specific stated reason otherwise.
"It's conventional" is not a reason.

**Pink is the accent.** `--color-accent: var(--pink-5)`. Not blue — blue only
ever appeared as an undecided default, so it doesn't get to be the default.
Pink is deliberate: on climate/sustainability work the expected accent is green
or blue, and pink reads as a surprise instead of a cliché. It is the one thing
that marks the work as his across every past pass.

**Warm ground, dark brown line work.** `--color-bg: var(--gray-0)` (a slightly
yellowish gray), `--color-text: var(--brown-8)`. Not black on white. This
pairing is a personal trope that predates the kit.

**Structure from rules and whitespace.** No box-shadow, no gradients, no
border-radius on *chrome* — panels, buttons, dividers, anything framing content.
1–2px solid borders and space instead. Radius is fine on content that floats
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

**Mobile-first, two breakpoints.** Base styles are the stacked single column.
`min-width: 40rem` (tablet) and `55rem` (desktop) layer on top. Written by hand
— the kit has no build step and must work as a plain `<link>`.

**Baseline grid, not a ratio scale.** Line-heights are multiples of 6px
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

Standing bar is WCAG AA; prefer AAA for body text, which most of this palette
already clears.

## Where to read

Load the section from `RULES.md` before working in that area.

| Working on | Read |
|---|---|
| Colors, accent, palette | "Color: pink is the accent", "Color: yellowish-gray background" |
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
| Dark mode | "Dark mode" |
| Token naming | "Naming" |
| Breakpoints | "Layout: mobile-first, two breakpoints" |

Templates in this repo to start from rather than rebuild: `slideshow-template.html`
(ambient/unattended player), `print/` (pandoc → WeasyPrint PDF pipeline),
`showcase.html` and `palette-docs.html` (what the kit looks like applied).

## Using the kit in another project

Copy `kit.css` in and link it plainly; there is no build step and no package.
Override `--color-accent`, `--color-bg`, `--font-display` per project if there's
a reason — the semantic layer exists so a project can differ without forking the
scale. Don't invent a parallel token vocabulary: the names (`--color-accent`,
`--color-text`, `--color-bg`, `--color-frame`) were standardized by hand across
projects before this repo existed.

For a SvelteKit + Tailwind project (his default stack), map the tokens into the
Tailwind theme rather than restating hex values in a config.

## Two open tensions

Don't resolve these silently — they're live design questions, not oversights.
Check `NOTES.md` for the current state before assuming either way.

1. **Deck color vs. kit color have never been reconciled.** The kit is pink on
   warm gray. The AY26 lecture decks are black/white/grayscale with per-lecture
   semantic accents and no pink at all. Neither document references the other.
   If a task touches both, ask whether projection is its own context.

2. **Dark mode is specified but not shipped.** `kit.css` still pins
   `color-scheme: light`. `RULES.md` "Dark mode" has the measured mapping —
   brown scale with its ends swapped, `--brown-9` ground, `--pink-3` accent,
   `--brown-4` as the dimmest token allowed to carry text. It maps the text and
   accent tokens only; the status colors are not yet mapped (see below).
