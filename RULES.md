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
