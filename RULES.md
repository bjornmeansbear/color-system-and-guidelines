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

**Winslow Homer recurs.** He appears in all three 2026 decks — *Mending the
Nets* (1882), *Art Students and Copyists in the Louvre Gallery* (1864),
*Blackboard* (1877), *The Veteran in a New Field* (1865). Working people,
plain light, no rhetoric. Worth checking him first when a brief involves labour,
attention, or instruction.

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

## Presentations: the slide is not the script

Written from a measurement pass on `~/Code/lectureScripts/
lecture-design-thinking/di200-wk1-deck.html` (67 slides) — every number
below comes from that deck. Expect this section to get revised against a
wider sample; see NOTES.md.

A lecture is two documents. The script carries the argument; the deck does
not. That lecture's script already exists as
`di200-wk1-reading-script.md` (45KB), which means every explanatory
paragraph on a slide is duplicated prose — the deck holding the speaker's
job and competing with the speaker to do it.

**A slide holds what speech cannot.** Four things read better in the eye
than in the ear, and a slide gets one of them:

- a name — `Emic` / `Etic`, `Research`, `Extraction`
- a list, parallel and scannable, no item longer than a line
- a comparison, because contrast is spatial and speech is linear
- a line worth quoting, sized to be read from the back of the room

**A slide never explains itself.** If a line only makes sense with the
sentence beneath it, that is a paragraph with a headline. Cut to the line
that stands alone, or drop it and say it out loud instead.

## Presentations: plain, aphoristic, unexplaining

The register is the same instinct as the `bjorn-voice` skill, one notch
harsher — the medium removes the need to argue at all. Name things, list
them, set them against each other. Nothing superfluous, no explanation,
no qualification.

This is a rule about protecting something already present, not installing
something new. Across that deck's 29 `.lead` lines and 31 headings, 72%
already run 13 words or under, and those are uniformly the strong ones:
"Consent is not transitive." "You cannot code a vibe." "Photograph both.
The photographs are identical." The break in the data is clean — under
~13 words the lines land, over it they turn into argument. The five
weakest leads are all 23–27 words.

So the failure mode is dilution, not absence. **The aphorism should be
the whole slide, not the headline on top of a paragraph.** The worst
slide in that deck (111 words, two `.rows` entries on Leonardo and the
Bauhaus) contains the line that should have been the entire slide —
"That is prototyping as a curriculum" — demoted to an inline `.accent`
span inside the explanation.

## Presentations: density, and the shrink tell

Big type, little on it. Keywords, aphorisms, comparisons; bulleted lists are
good. Not tons of explanatory text.

**The working ceiling is under ten words.** Measured across two decks he built
and stands behind — "On Mending" (FEC, 2026) and "On Making Stuff"
(convocation, 2026) — the content slides run **two to six words**, median about
five. "A person can mend alone …" "Twenty questions." "Everything is material."
"You need practice." Nothing in either deck argues; every slide names.

`di200-wk1-deck.html` runs a median of ~58 words across 67 slides, with 13 over
75. It is the outlier, not the norm — a lecture deck that absorbed its own
script. The rules in this section were first written from it, which means they
were calibrated against the weakest example. Treat ~10 words as the target and
25 as the outer bound for a bulleted comparison, not the other way round.

The count is a symptom rather than the rule. Past roughly that length what is
on screen is *structurally* the wrong thing — explanation, which belongs to the
mouth.

**Never shrink type to fit.** `di200-wk1` carries 10 inline
`style="font-size:1.9cqw"` / `2.1cqw` overrides, each one a slide whose text
did not fit at the sheet's own scale. Every one marks a slide that should have
been split. The type scale is the instrument that tells you a slide is
over-full — spending it to hide the overflow destroys the only warning the
system gives.

## Presentations: the deck is the essay's pull-quotes

Both 2026 decks have the same architecture, and it is the practical form of
"the slide is not the script."

Write the prose first. Then pull its aphorisms — the lines that already stand
alone — and give each one a slide and an image. "On Mending" is six fragments
lifted almost verbatim from the FEC remarks: *Making gets excitement;
Maintenance gets nothing … · A person can mend alone … · Returning to the same
knots … · Where to help with the mending … · A big net takes many hands …*

Two consequences worth stating. The deck cannot hold explanation because the
explanation is still in the essay, where it belongs. And the aphorisms get
written under prose conditions — with an argument around them to earn them —
rather than being invented to fill a slide.

One dense slide per deck is fine when it is genuinely informational (the
Faculty Assembly dates), and it should look like the exception it is.

**The title is a formula.** A short abstract noun phrase, then a parenthetical
gloss in plain speech, usually opening "or,". All three 2026 decks:

- **On Mending** *(What's left to fix so we get back to what matters)*
- **On Making Stuff** *(or, why nobody will just tell you if something's good)*
- **Loose Threads** *(or, Make Hay While Society Crumbles Around Us)*

The noun phrase carries the metaphor; the parenthetical says the thing
straight, and is where the humour goes. Neither half works alone — the abstract
title without the gloss is a mood, the gloss without the title is a memo.

Punctuation carries register. "On Mending" trails five of six fragments on an
ellipsis — the work is ongoing, nothing is closed. "On Making Stuff" ends every
line on a full stop — these are claims made to new students. Same author, same
year, opposite mark, deliberate.

## Presentations: one axis of visual coherence, not two

A deck needs its images to read as a family. There are three ways to get one,
and you pick **one**:

- **Subject.** "On Mending" is seven paintings of people mending nets, spanning
  Avercamp (1634), Homer (1882), Mønsted (1891), Sorolla (1902), Myrer (1954)
  and Collins. Wildly different centuries, palettes and styles; one object.
  `chair-ness` is the same move at archive scale — all chairs, any era, any
  photographic style.
  "Loose Threads" is the same move on a different object: five paintings of
  harvest and haymaking — Stubbs (1785), Homer (1865), Ancher (1905), Hodler
  (1910), Munch (1917) — and the slide text takes its vocabulary straight from
  them: *soil, field, tending, cultivating*. As in "Mending," the pictures
  supply the words.
- **Period.** "On Making Stuff" is the reverse: seven unrelated subjects — the
  Louvre copyists, a raft, a tiger engraving, a blackboard, a Munch — held
  together by falling in a roughly fifty-year band around 1864–1915.
- **Kind.** All paintings, all prints, all etchings. Coarser, and it does
  double duty: it is also a noise filter, because keyword searches otherwise
  return vessels, daggers and reliquaries whose catalogue text merely mentions
  the word.

**Combining axes over-constrains to nothing.** Measured: "chair" filtered to
Victorian etchings returns zero usable results, where either constraint alone
returns plenty. Pick the axis, then let everything else vary.

## Presentations: a closed set of layouts

One deck should not read as five decks interleaved. That deck runs five
unrelated layout modes with no stated rule for which a given slide takes:
`.rows` (year/description table, 11 uses), `.cols`/`.col.ruled` (6),
`ul`/`ul.tight` (16), `.lead` statement slides (16), and
`blockquote.big`.

The rule is a small closed set of named archetypes, each with a stated
trigger — this kind of content takes this layout. **Which archetypes
belong in the set is not decided yet**; it needs a wider sample than one
deck. See NOTES.md.

## Presentations: imagery

Public-domain painting and artwork as full-bleed slide backgrounds,
chosen for a metaphorical relationship to the content, is a deliberate
personal move — treat it as the default ambition for opener/beat slides,
not a decoration to add if there is time. Extends the Images section
above; the sourcing, treatment, and sizing rules there all apply.

**Find the imagery while drafting, not after.** The metaphor runs both ways —
a found image feeds the writing as often as the writing selects the image. The
2026 FEC fall kickoff remarks ("Mending") were illustrated with paintings of
fishermen and women mending nets, and the nets then supplied the prose its
vocabulary: repair, collective, patient, something torn that people take back
out tomorrow. Treated as a final illustration pass, that exchange cannot
happen.

The exchange is not one-directional, and not one-pass. In that piece the
figure is *named* ten paragraphs in but *seeded* six paragraphs before that
("An empty room mends nothing") — a phrase planted on a later revision, working
backwards, so the image would read as recognition rather than introduction.
Choosing artwork early is what makes that third pass possible. The prose-side
rules for carrying a metaphor live in the `bjorn-voice` skill, "Sustaining a
metaphor across a whole piece."

**The brief is yours; the search terms are not.** A slot carries the metaphor
in the writer's own words. Translating it into the concrete nouns a keyword
API can match is the machine's job — a metaphorical brief searched verbatim
returns nothing useful ("ordinary labor in a working interior" returns *The
Death of Socrates*). Keep the two in separate fields so the original is never
flattened into keywords.

**Slots carry intent, not filenames.** A hardcoded
`style="--img:url('images/beat-history.jpg')"` cannot say what the image
is *for*, so it can neither be searched against nor prompt you. Slides
declare a slot and a brief instead:

```html
data-img="beat-history"
data-img-brief="an older lineage — surveying, notebooks, workshop labor"
```

**The working build is loud; the presentation build is silent.** An
unfilled slot must be conspicuous on the desk — slot name and brief,
rendered in accent — and must fall back silently to the flat ground when
projected. Never show a TODO to a room. That deck's `images/README.md`
gets the second half right and the first half backwards: missing files
fall back quietly and the credit line sits commented out, so the system
is silent about its own gaps. All five of its beat images are still
missing, which is what that silence buys.

**Every background image carries a credit line** — source, collection,
year, licence — written at pick time, not deferred.

**Scrim and verify against the worst case.** Contrast over an image
cannot be eyeballed, because the image is not knowable in advance.
`di200-wk1`'s beat slides are the model: a `brown-8` scrim at
`--scrim: 0.80`, computed against a hypothetical pure-white photograph —
`gray-0` text at 9.03:1, `gray-1` at 7.98:1, `pink-2` at 5.20:1. Real
photographs run darker, so actual contrast only improves. Dial the scrim
per-slide for an already-dark image, and recompute: 0.70 drops to
6.29/3.62, AA but not AAA.

## Presentations: sourcing, in this order

Machine narrows, you choose, machine writes the credit line. The
metaphorical judgement is the part that does not automate; reducing four
million public-domain objects to forty worth flipping through is the part
that does.

1. **Your own are.na channels first** — already collected, already
   vetted, credit metadata already attached. (This is the Images
   "Sourcing" rule above, now with a defined order.)
2. **Museum open-access APIs.** The three needing no key: the Met
   (`collectionapi.metmuseum.org`, `isPublicDomain`), the Art Institute
   of Chicago (`api.artic.edu`, `is_public_domain`, IIIF sizing), and
   Cleveland (`openaccess-api.clevelandart.org`, `share_license_status:
   CC0`). Rijksmuseum, Smithsonian, and Harvard work too but want a free
   key.
3. **Wikimedia Commons last**, with the scepticism `chair-ness`'s
   `commons-verified.md` already documents — Commons search matches
   keywords, not objects, and returns a recording studio for *Aeron*.

Filter candidates to public-domain and ≥2000px before they reach your
eye: RULES.md caps upscale at 2.5x, and a projector eats resolution.

## Presentations: local files, never hotlinks

A projected deck references local image files. Network is not a runtime
dependency in a room you do not control. `chair-ness` already models the
split — one manifest, two builds: `slideshow.html` resolves 247 local
`images/` paths, `slideshow-web.html` hotlinks are.na's CDN and ships no
local files.

Image caches stay out of git. `chair-ness` gitignores `images/`,
`links/`, and `vitra/`, holding 423 images and 348MB on disk against a
5.5MB `.git`. The canonical record is the are.na channel plus a
`manifest.csv` — id, title, source URL, licence, `image_url_large`,
`local_path`.

The cache should be shared across projects rather than living inside one
of them; where it lives is an open question (NOTES.md).

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
