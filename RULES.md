# Design rules

Personal layout, color, and typography rules — the "why" behind `kit.css`.
Extracted from what's actually shipped in onething, a.wjerk.shop,
bjornpaedia, and oblique, plus direct answers where code alone couldn't
say why. This document changes as the kit changes — rename, restructure,
and rewrite sections freely as more projects get folded in (ookb.co,
oblique.ookb.co, wjerk.shop, whatever's next). Nothing here is precious.

## Scope note: the ookb.co / wjerk.shop family

Projects sit under two domain families — `ookb.co` (+ subdomains like
`oblique.ookb.co`) and `wjerk.shop` (+ subdomains like `a.wjerk.shop`,
`bjornpaedia.wjerk.shop`). The intent is modular: shared tokens/rules here,
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

## Images

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

## Motion

Not part of the base kit — `kit.css` ships no animation utilities.
Animation is a per-project, special-idea flourish, not a system default.
a.wjerk.shop's homepage logo (grayscale→color, red→green over 30s) is that
kind of one-off, not a pattern to reuse elsewhere. This may change as more
projects need it, but the starting rule is: ignore motion unless a
specific idea calls for it.

## Dark mode — deferred

Not implemented. `color-scheme: light` is pinned in `kit.css` for now.
The semantic token layer (`--color-bg`, `--color-text`, etc., all
indirected through the raw scale) is already structured so dark mode could
be added later without a rewrite — just not a priority until the
light-mode system is solid across more projects.

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
