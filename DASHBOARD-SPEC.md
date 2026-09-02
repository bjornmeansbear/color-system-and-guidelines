# OOKB / Wjerk design system — handoff spec

A short, self-contained brief for building an HTML dashboard that matches the
family. Canonical source is `kit.css` + `RULES.md` in this repo; this file is
the subset a dashboard actually needs, plus the places the repos disagree.

Verified against: `color-system-and-guidelines`, `onething`, `oblique`,
`a.wjerk.shop`, `bjornpaedia`, `chair-ness` (2026-09-02).

---

## 1. Color

### Raw scale

11 ramps × 10 steps, OKLCH-derived. `0` = lightest, `9` = darkest. Copy the
`:root` block from `kit.css` verbatim — all 110 values are byte-identical
across every repo that ships them, so there is one correct set.

Two things about the ramps that surprise people:

- The **grays are not neutral.** `--gray-*` is warm/yellowish (the family
  ground), `--dark-gray-*` is cool blue-gray, `--light-gray-*` is green-tinted.
- **`--blue-*` is a desaturated teal-gray**, not a usable blue accent. Do not
  reach for it to signal interactivity. Pink does that job.

### Semantic layer — light

| Token | Value | On `--color-bg` |
|---|---|---|
| `--color-bg` | `--gray-0` `rgb(247,248,238)` | — |
| `--color-surface` | `--gray-0` | — |
| `--color-surface-2` | `--gray-0` | — |
| `--color-text` | `--brown-8` `rgb(25,21,19)` | **16.94:1** AAA |
| `--color-text-muted` | `--gray-6` `rgb(83,83,72)` | **7.27:1** AAA |
| `--color-text-subtle` | `--gray-6` | **7.27:1** AAA |
| `--color-border` | = `--color-text` | — |
| `--color-frame` | = `--color-text` | — |
| `--color-accent` | `--pink-5` `rgb(214,0,97)` | **4.87:1** AA |
| `--color-accent-hover` | `--pink-6` `rgb(164,0,65)` | 7.39:1 AAA |
| `--color-accent-subtle` | `--pink-0` | background use only |

Status colors, each measured on its own `-bg` companion:

| Token | Fg / Bg | Ratio |
|---|---|---|
| success | `--green-6` on `--light-gray-0` | 7.05:1 AAA |
| warning | `--yellow-6` on `--yellow-0` | 7.16:1 AAA |
| danger | `--red-6` on `--red-0` | 6.63:1 AA |
| info | `--dark-gray-6` on `--dark-gray-0` | 7.21:1 AAA |

> **`--color-surface` and `--color-surface-2` are placeholders.** Both resolve
> to `--color-bg`. This system has no surface-elevation concept — panels are
> separated by rules and whitespace, never by a lighter/darker fill. A
> dashboard should not build a card hierarchy that depends on them differing.

### Semantic layer — dark

Same brown ramp with its ends swapped. Ground is `--brown-9`, **not black** —
black loses the warmth the light mode is built on. Pink stays the only accent,
but steps down to `--pink-3`.

| Token | Light | Dark | Dark ratio on `--brown-9` |
|---|---|---|---|
| `--color-bg` | `--gray-0` | `--brown-9` `rgb(8,5,4)` | — |
| `--color-text` | `--brown-8` | `--brown-0` `rgb(251,245,242)` | **18.81:1** AAA |
| `--color-text-muted` | `--gray-6` | `--brown-3` `rgb(192,185,181)` | **10.49:1** AAA |
| `--color-text-subtle` | `--gray-6` | `--brown-4` `rgb(158,151,147)` | **7.06:1** AAA |
| `--color-accent` | `--pink-5` | `--pink-3` `rgb(255,129,169)` | **8.67:1** AAA |

**`--brown-4` is the dimness floor.** `--brown-5` measures 4.36:1 — it reads
like a usable gray on screen and is not one. Nothing dimmer than `--brown-4`
carries text a reader has to read.

**Do not carry `--pink-5` into dark mode.** It drops to 3.90:1 on `--brown-9`
— large-text only. `--pink-3` is the dark accent.

---

## 2. Typography

- **Default is the system stack.** No webfont, no download, nothing to license.
- A project earns a different `--font-display` only by self-hosting an
  **open/libre** face (OFL etc.). Never a proprietary webfont. `oblique` is the
  precedent: Basteleur + Sligoil Micro, both Velvetyne, OFL-1.1, with the
  license kept beside the files.
- For a dashboard: **use the system stack.** Don't introduce a font.

```
--font-sans:    system-ui, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
--font-display: var(--font-sans);
--font-mono:    ui-monospace, 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace;
```

### Scale — baseline grid, not a ratio scale

Line-heights are even multiples of a **6px (0.375rem)** unit — 18, 24, 30, 36,
42, 54. Font sizes are chosen to pair with those rungs, so the ratio *shrinks*
as size grows (small text needs more leading, large text less). Everything is
`rem`. Do not substitute a 1.25× modular scale; it will not land on the grid.

| Token | Size | Leading | Use |
|---|---|---|---|
| `--text-2xs` | 0.75rem / 12px | 1.125rem / 18px | fine print, timestamps |
| `--text-xs` | 0.8125rem / 13px | 1.125rem / 18px | labels, meta |
| `--text-sm` | 0.875rem / 14px | 1.125rem / 18px | captions, secondary UI |
| `--text-base` | 1rem / 16px | 1.5rem / 24px | body, default |
| `--text-md` | 1.125rem / 18px | 1.5rem / 24px | lead paragraph |
| `--text-lg` | 1.375rem / 22px | 1.875rem / 30px | h4 |
| `--text-xl` | 1.75rem / 28px | 2.25rem / 36px | h3 |
| `--text-2xl` | 2.25rem / 36px | 2.625rem / 42px | h2 |
| `--text-3xl` | 3rem / 48px | 3.375rem / 54px | h1 |

Headings are **bold**, mapped h1→`3xl` down to h6→`base`. Block margin on all
headings and paragraphs is `0 0 1.5rem` — one base line, keeping the rhythm.

Two recurring meta treatments:

- `.label-upper` — `--text-xs`, uppercase, `letter-spacing: 0.12em`, muted.
- `.caption-muted` — `--text-sm`, italic, muted.

---

## 3. Spacing, borders, radius

**Spacing** rides the same 6px baseline unit. Observed conventions:

| Context | Value |
|---|---|
| Baseline unit | 0.375rem / 6px |
| Block rhythm (heading + para margin, divider) | 1.5rem |
| Panel body padding | 2rem |
| Panel header padding | 1.25rem 2rem |
| Panel footer padding | 1rem 2rem |
| Button padding | 0.875rem 1.75rem |
| Tag padding | 0.2em 0.9em |

**Borders carry all the structure.** `1px solid var(--color-border)`, where
border *is* the text color. Structure comes from rules and whitespace.

- **No `box-shadow`.** No elevation, ever, on structural elements.
- **No gradients.**
- **No `border-radius` on anything structural** — panels, cards, buttons,
  inputs, tables are square.

**Radius has exactly one sanctioned use:** pills at badge/tag scale,
`border-radius: 999px`. Nothing between 0 and a full pill.

Two thicker treatments exist:

- `.frame-thick` — `clamp(0.75rem, 4vw, 2rem)` solid `--color-frame`, scales
  with viewport instead of jumping at a breakpoint.
- `.frame-thin` — `2px solid var(--color-text)`.

**State without elevation:** buttons invert fg/bg on `:active` rather than
lifting. `.btn:active { background: var(--color-text); color: var(--color-bg) }`.
Disabled is `opacity: 0.4`.

---

## 4. Layout & interaction

**Breakpoints — mobile-first, two of them.** Base styles are always the
stacked single-column layout; wider treatments layer on via `min-width`:

```css
@media (min-width: 40rem) { /* tablet / two-column */ }
@media (min-width: 55rem) { /* desktop / widest */ }
```

No custom-media variables — `kit.css` has no build step and must work as a
plain `<link>`. These are values to retype, not a token to reference.

**Focus is deliberately loud and never suppressed:**

```css
:focus-visible { outline: 0.25rem solid var(--color-accent); outline-offset: 2px; }
```

It should read as part of the design, not as a browser afterthought.

**Motion:** honor `prefers-reduced-motion: reduce`.

---

## 5. Where the repos disagree

Ranked by how much it should affect the dashboard.

### Things to actually decide

**1. Dark mode is specified but not shipped.** `RULES.md` has the full,
measured mapping (§ above); `kit.css` still pins `color-scheme: light` and
ships no flip. The only implementation is `chair-ness`, which hardcodes the
literals — `rgb(8,5,4)`, `rgb(251,245,242)`, `rgb(192,185,181)`,
`rgb(158,151,147)`, `rgb(255,129,169)` — with **no CSS variables at all**,
because it was built for a projected gallery slideshow.
→ *For the dashboard:* use the `RULES.md` mapping. It is measured and correct.
You will be the first consumer to wire it as tokens, so write it as a
`prefers-color-scheme` block over the same semantic names rather than a
parallel palette.

**2. There is no single "the background."** `oblique` runs on a different
ground entirely — `--color-bg: rgba(132,132,120,1)` (legacy `@ookb-gray`),
not `--gray-0`. Deliberate, documented, and it drags its text down to 4.80:1
(AA, versus 16.94:1 everywhere else).
→ *For the dashboard:* use `--gray-0`. `oblique` is the outlier, not the rule.

**3. `a.wjerk.shop` and `bjornpaedia` use blue as the interaction color.**
Seven `blue` literals in `a.wjerk.shop/style.css` — every nav hover, every
prev/next hover, and the focus ring (`outline: 0.25rem solid blue`). The
`.wjerk-nav` block bolted into `bjornpaedia/static/static.css` inherited the
same `background-color: blue` hover. Neither file links `kit.css` or defines a
single token; `a.wjerk.shop` is raw `black`/`white`/`blue`.
→ This directly contradicts the system's loudest rule: **pink is the accent,
not blue.** These two are the least-conformed repos and should not be used as
reference for a new build.

### Accessibility bugs found

**4. `oblique`'s focus ring is invisible.** `--color-accent` there is
`@ookb-pink` `rgba(236,64,121,1)`, and against its own `--color-bg`
`rgb(132,132,120)` that computes to **1.00:1** — the two colors have
coincidentally identical relative luminance. It is used for
`:focus-visible { outline: 3px solid var(--color-accent) }` and for link
underlines (`border-bottom: 1px solid var(--color-accent)`). The CSS comment
calls the color "decorative only," which is right about the color and wrong
about where it got used. The focus indicator fails WCAG 1.4.11 outright, and
the underline affordance on links is invisible.
→ Worth fixing in `oblique` independently of this dashboard.

**5. `--color-text-subtle` is a name that promises something it doesn't do.**
In light mode it's `--gray-6`, identical to `--color-text-muted`. Only in dark
mode do the two split (`--brown-3` vs `--brown-4`).
→ Don't build a three-tier text hierarchy in light mode; you only have two.

### Drift and stale code

**6. Three files each claim to be the source of truth for the raw scale** —
`kit.css`, `onething/src/app.css`, and `onething/src/lib/palette.css`. All 110
values are currently identical (verified), so nothing is broken yet, but the
header comments point at each other in a loop.

**7. `onething` predates the type scale and the rem convention.** Its
components are px throughout (`32px`, `40px`, `20px`, `14px`) with `2px`
borders and `24px` dividers, where `kit.css` is rem with `1px` borders and
`1.5rem` dividers. It defines no `--text-*` tokens at all.
→ Follow `kit.css`, not `onething`.

**8. `onething/tailwind.config.js` still ships the dead Mac-chrome skin:**
`boxShadow.mac` (`2px 2px 0px #000000`), `boxShadow.mac-inset`, and
`backgroundImage.titlebar` (a `linear-gradient`). Zero usages in `src/`
(grepped). They contradict the no-shadow/no-gradient rule and should be
deleted. Relatedly, `.btn-black` is now a *pink* button — a stale name.

**9. `oblique` uses its own breakpoints** — `30rem` / `50rem` / `70rem`, versus
the documented `40rem` / `55rem`. Its focus ring is also `3px` / offset `3px`
rather than `0.25rem` / offset `2px`, and `.strategy` carries a
`box-shadow: 0 1rem 2rem` that the no-shadow rule doesn't carve an exception
for.

**10. `--color-accent-hover` means two different things.** In `kit.css` it's
`--pink-6`, a *darker* text/border color. In `oblique` it's `--pink-5` used as
a *background* behind white text. Same token name, opposite role.

**11. `bjornpaedia` is essentially unstyled by this system.** It's stock
TiddlyWiki 5.3.8 + modern-normalize: `#fff` grounds, `#000` text, `#0000ff`
links, and ~20 scattered `border-radius` values from `2px` to `20px`. Only the
`.wjerk-header` / `.wjerk-nav` block is family styling.

**12. Housekeeping:** `RULES.md` has an uncommitted working-tree edit that
strips leftover `<<<<<<< HEAD` / `>>>>>>>` merge-conflict markers from around
the Presentations sections. Worth committing.

---

## 6. Drop-in token block

Light + dark, both measured. Paste into the dashboard, then add the raw ramp
from `kit.css` above it (or inline just the steps referenced here).

```css
:root {
  color-scheme: light dark;

  --color-bg: var(--gray-0);
  --color-surface: var(--gray-0);
  --color-text: var(--brown-8);
  --color-text-muted: var(--gray-6);
  --color-text-subtle: var(--gray-6);
  --color-border: var(--color-text);
  --color-frame: var(--color-text);
  --color-accent: var(--pink-5);
  --color-accent-hover: var(--pink-6);
  --color-accent-subtle: var(--pink-0);

  --color-success: var(--green-6);  --color-success-bg: var(--light-gray-0);
  --color-warning: var(--yellow-6); --color-warning-bg: var(--yellow-0);
  --color-danger:  var(--red-6);    --color-danger-bg:  var(--red-0);
  --color-info:    var(--dark-gray-6); --color-info-bg: var(--dark-gray-0);

  --font-sans: system-ui, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --font-display: var(--font-sans);
  --font-mono: ui-monospace, 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace;

  --text-2xs: 0.75rem;   --leading-2xs: 1.125rem;
  --text-xs:  0.8125rem; --leading-xs:  1.125rem;
  --text-sm:  0.875rem;  --leading-sm:  1.125rem;
  --text-base:1rem;      --leading-base:1.5rem;
  --text-md:  1.125rem;  --leading-md:  1.5rem;
  --text-lg:  1.375rem;  --leading-lg:  1.875rem;
  --text-xl:  1.75rem;   --leading-xl:  2.25rem;
  --text-2xl: 2.25rem;   --leading-2xl: 2.625rem;
  --text-3xl: 3rem;      --leading-3xl: 3.375rem;

  --space-unit: 0.375rem;  /* 6px baseline */
  --radius-pill: 999px;    /* the only radius */
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: var(--brown-9);
    --color-surface: var(--brown-9);
    --color-text: var(--brown-0);
    --color-text-muted: var(--brown-3);
    --color-text-subtle: var(--brown-4);   /* dimness floor — nothing lower */
    --color-accent: var(--pink-3);         /* NOT pink-5: 3.90:1, fails */
    --color-accent-hover: var(--pink-2);
    --color-accent-subtle: var(--pink-8);
  }
}
```

Status colors are not remapped for dark above — the `-6`/`-0` pairs are built
for light grounds and need their own pass before a dark dashboard uses them.
Until then, signal status in dark mode with the accent plus a text label
rather than a colored chip.
