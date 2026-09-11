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
`bjornpaedia.wjerk.shop`, `stuff.wjerk.shop`). The intent is modular: shared tokens/rules here,
each project free to pick its own typeface and emphasis on top. The old
`ookb.co` repo should get pulled down and checked against this doc too.

## Structure: rules, not chrome

No box-shadow, no gradients, no border-radius on *structural chrome* —
panels, buttons, dividers, the elements that frame content. Structure comes
from solid 1–2px borders and whitespace.

The rule is about chrome, not about scale. It read "no radius at panel scale"
until 2026-09-02, which was wrong: the talk decks have always used large
rounded cards for quote slides, and those are content floating on an image,
not chrome framing a layout. Radius is fine on a floating content block at any
size. Small pill/tag elements (`border-radius: 999px`, see oblique) are the
other standing case.

Buttons and interactive elements show state by inverting foreground/
background on press, not by adding elevation or a hover-glow.

Gradients follow the same chrome/content line. A gradient that *encodes
data* is content, not decoration — wjeather's sky bands (2026-09-10), one
tint per forecast hour, blending only where the weather does. Allowed. A
gradient laid on for mood or depth is still not.

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

`--color-accent` is Wjerk pink (`--pink-5` / `--pink-6`), the color that's
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

Which pink: the original Wjerk Pink's, softer and dustier than the hot pink
the kit carried until 2026-09-11. The scale was rebuilt at the original's
chroma so one family covers both roles by step — around `pink-4` for display
type and fills, `pink-5` (4.78:1 on the White) wherever pink carries small
text: links, buttons, the focus ring. One accent, not two pinks.

## Color: yellowish-gray background, dark brown line work

The default bg/text pairing (`--color-bg: var(--wjerk-white)`, `--color-text:
var(--wjerk-black)`) isn't an arbitrary landing spot — a warm, slightly
yellowish-gray ground with dark brown line work on top is a recurring
personal trope independent of this kit, and the semantic tokens already
encode it as the default rather than plain black-on-white. Projects can
still override it, same as the accent, but this pairing is the answer
unless there's a specific reason to change it.

Since 2026-09-11 the pair is the palette's own White (#F8FAE7) and Black
(#2D2826) — `--wjerk-white` / `--wjerk-black`, 13.73:1 — rather than the
near-matches `gray-0` and `brown-8` (16.94:1) the kit used before. Muted text
(`--gray-6`) is 7.34:1 on the White; the pink accent 4.78:1.

**Papers and inks.** The pair also heads two scales of its own (2026-09-11),
so the color story has range without leaving it:

- **`white-0` → `white-9`, papers.** `white-0` is the White exactly; each step
  warmer and creamier, to a butter cream (#E1D3A0). The Black holds on every
  one (≥9.72:1), and so do `gray-6` labels (≥5.20), the pink line (≥3.48) and
  the green line (≥3.03). Neighbouring steps are close (ΔE ~1.4) — paper
  stocks, not a ramp.
- **`black-0` → `black-9`, inks.** `black-9` is the Black exactly; lighter
  warm charcoals below it, every one AA as text on the White (`black-0`
  5.69:1 up to 13.73:1). `black-7` is the palette's Brown (#3C3634, ΔE 0.8).

They break the kit's usual shape — the hue scales run pale to near-black
across all ten steps — because they're a material, not a hue.

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

Added 2026-09-02, from the AY26 lecture decks: **Overpass** (OFL, the
workhorse across every 2026 deck), **Pilowlava** (Velvetyne, OFL — display),
**PicNic** (Velvetyne, display).

PicNic carries a flag the others don't. It is published under Velvetyne's
**CUTE** licence (Conditions d'utilisations typographiques engageantes), not
the OFL — an ethical-use licence with conditions on who may use the font,
rather than an unrestricted libre one. That is not a reason to avoid it, and
the politics are probably congenial, but it is a different category from the
rest of this roster, where "the constant is the licence" has meant OFL. Read
the CUTE terms before PicNic goes into anything shared or client-facing.

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

wjeather's wind drift (2026-09-11) is the one-idea flourish in practice:
when the app opens or refreshes, each hour's wind lines (long dashes, so
movement along them shows) drift the way that hour's wind blows for ~4 s,
then settle still. The motion carries meaning — it tells a north wind from a
south one — and it's brief on purpose: under WCAG 2.2.2's 5-second threshold,
so no pause control is needed, and near-zero battery cost. Unlike an
auto-advancing slideshow, it's a flourish rather than the medium, so under
`prefers-reduced-motion` it's skipped outright; the still lines keep their
angle and spacing.

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

**Short remarks: under ten words a slide.** Measured across three decks he
built and stands behind — "On Mending," "On Making Stuff," and "Loose Threads,"
all 2026 — the content slides run **two to eight words**, median about five.
"A person can mend alone …" "Twenty questions." "Everything is material."
"You need practice." Nothing in these decks argues; every slide names.

These are **five-to-ten-minute ceremonial talks**: convocation, a faculty
assembly opening. Five to seven slides, one aphorism each, one image each.
That is a form, and its density rule is not transferable by itself.

**A long lecture is a different form and its number is not yet known.**
`di200-wk1-deck.html` is 67 slides for a full class session, at a median of ~58
words with 13 slides over 75. It is too dense — the 10 inline font-size
overrides prove that independently, and the explanatory prose is duplicated in
its own script file — but "too dense" is not the same as "should be five
words." A lecture has to carry definitions, comparisons, citations, and a
timeline, and it earns more per slide than a seven-slide address does. The
right ceiling for it will come from lecture decks he stands behind, which do
not exist in this sample yet. See NOTES.md.

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

**Start by looking for a metaphor that can carry the whole arc.** That is the
preferred shape, not one option among several: a single figure, declared up
front, running from the title through every slide to the landing. "On Mending"
and "Loose Threads" both work this way and both are stronger for it. Reach for
the per-slide mode below only when no such figure presents itself — it is the
fallback, not the alternative.

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
- **Period.** Everything inside one era. Note that this axis has not actually
  been used deliberately yet — see the "or don't declare one" note below.
- **Kind.** All paintings, all prints, all etchings. Coarser, and it does
  double duty: it is also a noise filter, because keyword searches otherwise
  return vessels, daggers and reliquaries whose catalogue text merely mentions
  the word.

**The fallback: declare no axis at all.** "On Making Stuff" was built with one
rule —
everything public domain — and then image chosen per slide for what looked
right against that slide's aphorism. Its images do land inside a roughly
1864–1915 band (the Louvre copyists, a raft, a tiger engraving, a blackboard, a
Munch), but that band was **emergent, not chosen**: the product of taste
converging, not a constraint applied. Worth knowing so the coherence is not
mistaken for a rule that was followed.

This is a legitimate mode when no arc-spanning metaphor is available. Declaring
an axis buys guaranteed coherence and costs you the best per-slide match;
choosing per slide buys the match and leaves coherence to your eye. Prefer the
declared axis. What is *not* available either way is declaring two axes — that
returns nothing (below).

**When the prose braids two metaphors, the deck commits the images to one.**
The Spring 2026 remarks run threads and agriculture together — threads staged
as a failure in the opening, agriculture saturating everything after. The deck
keeps both in its title (*Loose Threads (or, Make Hay While Society Crumbles
Around Us)*) and gives every one of its five images to harvest alone. The title
can hold the ambiguity; the pictures cannot, because a set of images is read
all at once and two figures in it reads as indecision.

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

Machine narrows, you choose, machine writes the credit line. The metaphorical
judgement is the part that does not automate; reducing four million
public-domain objects to forty worth flipping through is the part that does.

**One are.na channel per deck.** The established practice, and it is the image
family made concrete: `are.na/kristian-bjornard/lecture-mending-nets` holds the
21 blocks behind "On Mending" — four Homers, Sorolla, Israëls, Avercamp,
Mønsted, Kuniyoshi, Utamaro, Myrer, Collins. Collect into the channel while
drafting; the deck names it and everything in it is a candidate. The cascade
below only tops that up.

1. **The deck's own channel**, if it has one. Everything in it, no filtering —
   channel membership *is* the curation.
2. **The rest of your are.na** — `GET /v3/search` with `user_id` searches
   everything you have ever saved in one request.
3. **Wikimedia Commons** — for a named artist or artwork, this is the one that
   works. See the routing rule below.
4. **Museum open-access APIs** — the Met (`collectionapi.metmuseum.org`), the
   Art Institute of Chicago (`api.artic.edu`), Cleveland
   (`openaccess-api.clevelandart.org`). No key needed. Best metadata, reliable
   high resolution, real subject indexing.

**Route by what you are searching for, not by source quality.** This is the
correction that matters, and it was measured:

- **A concept** ("ordinary labor in a working interior") goes to the museum
  APIs. They have curated subject metadata. Commons matches raw catalogue
  keywords and returns a recording studio for *Aeron*.
- **A named artist or artwork** ("Sorolla mending nets") goes to Commons. The
  museum APIs can only return what they own, which is a severe bias:
  searching AIC for Sorolla, Mønsted, Israëls, Avercamp or Kuniyoshi returns
  its own Winslow Homers every single time. Commons aggregates across
  collections and holds all of them.

The practical consequence is that the American museum APIs are close to
useless for the European and Japanese painting this work actually reaches for.
They are a depth source, not a breadth source.

**An are.na hit that is too small to project is still the best row on the
sheet.** are.na saves whatever the source page served, so a 150px Flickr
thumbnail is common — searching "mending" returns Sorolla's *Mending the Nets*
at 150×150. Do not discard it. It names an artwork already chosen; the other
sources then find a printable copy. Keep it visible and mark it as a lead.

Filter candidates to public domain and ≥2000px before they reach your eye:
RULES.md caps upscale at 2.5x, and a projector eats resolution.

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

## PDF generation: Markdown → pandoc → WeasyPrint

Print output (syllabi first, in `~/Code/syllabiBuilder`) is built from
Markdown, not authored in a page-layout tool or exported from a live web
page. Source: `.md` → `pandoc` (to styled HTML5) → `weasyprint` (to PDF).
Reach for this pipeline before a puppeteer/wkhtmltopdf-style browser-print
or a GUI layout tool — it's plain text in git, diffable, and rebuilds
without a browser.

`print/` in this repo is the generalized, drop-in version of that
toolchain — `print/md2pdf.sh`, `print/pandoc-template.html`,
`print/print.css` — start a new print job by copying that folder rather
than starting from `syllabiBuilder`'s syllabus-specific one.

The print stylesheet is not `kit.css` linked as-is — print has its own
`@page` rules (margins, running headers/footers, page-break control) that
don't belong in a screen stylesheet, so `print/print.css` is a **separate
file that restates the subset of kit tokens it needs** (`--color-text`,
`--color-accent`, `--color-border`, the baseline-grid `--text-*`/
`--leading-*` rungs) rather than importing the whole kit. Same warm-
ground/brown-line-work/pink-accent/OFL-fonts-only rules apply.

Fonts default to `--font-sans`/kit.css's own system-stack fallback, so
`print/print.css` works with zero setup. A project earns its own display
font the same way the kit does — self-host an OFL `@font-face` (a local
file path or a sibling repo's `fonts/`) and override the variable; see the
commented-out example at the top of `print/print.css`. WeasyPrint has no
access to a browser's installed-font fallback or a CDN at build time, so
the font has to be a real file on disk either way.

Two structural conventions worth keeping on the next print job, both
already wired into `print/md2pdf.sh`:

- **Shared boilerplate via include directives** (`<!-- include:
  path/to/file.md -->`, resolved relative to the including file, nesting
  allowed, a missing include aborts the build) — keeps repeated legal/
  policy text in one place instead of pasted into every document.
- **Drop a section by heading** (`-x "Section Heading"` removes an `##`
  section and everything under it before rendering) — lets one source
  document produce both an internal draft and a clean external copy,
  rather than maintaining two files.

On macOS, WeasyPrint's pango dependency needs
`DYLD_FALLBACK_LIBRARY_PATH` pointed at the Homebrew lib dir — `print/
md2pdf.sh` sets this itself rather than assuming it's already in the
shell environment.

## Slideshows / unattended players

Auto-advancing decks meant to run unattended for hours (a gallery
projection, an ambient background piece) carry obligations beyond a
normal web page, on top of the reduced-motion and dwell-time rules
already under "Motion" above. First built for `~/Code/chair-ness`, the player
now lives in this repo at **`tools/slideshow/`** and is shared across
archives (see its README to run it); the
**ambient two-layer pattern is the default to reach for** — images hard-
cut on one layer, text surfaces over them on opaque, rotated panels — not
just one option among several. `slideshow-template.html` in this repo is
the generalized, drop-in version: no build step, edit the `CONFIG`,
`IMAGES`, and `TEXTS` values at the top of its `<script>` directly.

- **One generator, several outputs via composable flags**, not several
  near-duplicate scripts, if a project needs more than one build of the
  same deck (e.g. a local-asset build and a hotlinked/publishable one).
  `tools/slideshow/build_slideshow.py` produces four builds
  (local-image / hotlinked-image × single-slide / two-layer-ambient) from
  two independent flags (`--hotlink`, `--ambient`) that compose, so a
  content change (editing `quotes.txt`) has exactly one script to re-run
  correctly, not four. `slideshow-template.html` doesn't need this — it
  has no build step, so there's nothing to keep in sync across builds in
  the first place.
- **Sizing**: pin the box (`width/height: 100%`) and let `object-fit:
  contain` scale into it — see "Images: Sizing" above. Cap upscale of
  small source images (chair-ness caps at 2.5x) rather than blowing a
  150px thumbnail up to fill a projector.
- **Fonts stay linked (self-hosted `@font-face`, normal file on disk) by
  default** — same as everywhere else in the kit. Embedding a font as
  base64 is a narrow fix for a specific problem, not a slideshow default:
  reach for it only when the build must be one self-contained file with no
  guaranteed network (a projector with no venue wifi) or must travel as a
  single copy to somewhere that can't also hold a `fonts/` folder (chair-
  ness's build gets copied into `a.wjerk.shop` as one file). If neither
  applies, link the font file normally. When it does apply, budget the
  embed against total asset weight rather than treating it as free —
  chair-ness's six embedded OFL faces cost ~214 KB against ~12 MB of
  images, under 2% — and ship a flag to fall back to the system font stack
  when it isn't worth it.
- **Bound memory for a long-running DOM.** Don't leave every slide ever
  shown sitting in the DOM — decoded bitmaps accumulate for as long as the
  tab stays open (chair-ness measured ~2.6 GB uncapped for its image set).
  Keep only slides within a small radius of the current one; tear the rest
  down and let their images release. Preload the next few images off-DOM
  (`new Image()`, cache-only) so a slide is decoded before it's shown, not
  while it's shown.
- **Degrade instead of stalling.** An image that fails to load gets marked
  broken and skipped, not left holding the slide for its full dwell time.
  A backgrounded tab pauses (`visibilitychange`) instead of racing ahead
  while nobody's watching, so it doesn't come back out of sync with the
  room.
- **Caption/metadata provenance**: derive captions from fields on the
  source item itself, in a fixed precedence order (chair-ness: an
  authoritative external source first, then the item's own title, then
  its description), never by pairing an item with whatever happens to sit
  next to it. Suppress machine-generated junk (filenames, CDN query
  strings, bare UUIDs, scraped page titles like "403 Forbidden") — no
  caption beats a wrong one.
- **Hotlinking third-party images carries real risk**: a source may 403
  any foreign `Referer` (chair-ness measured this against
  `collection.design-museum.de`, 6/6), so a "distributable, no local
  copies" build can silently lose exactly the images that matter most.
  Confirm cross-origin hotlinking actually works on that host before
  designing a build around it, and prefer sources whose own CDN is meant
  to be hotlinked (an image upload) over a link/screenshot capture of
  someone else's page.
- **A fetched archive is a cache, not a deliverable — ignore it before the
  first commit, not after.** These players are usually fed by a script that
  pulls someone else's channel down to disk (`chair-ness/scripts/
  fetch_arena.py`, re-runnable, skips what it already has). That image
  folder can be rebuilt from one command, so it never belongs in git.
  chair-ness ignores `images/`, `links/` and `vitra/` from the start. The
  second project built this way, `WritingPlanning/gd420/exhibiting-ness`,
  didn't — 638 images, 268 MB, committed and pushed before anyone noticed,
  taking `.git` from 4.8 MB to 263 MB. A `.gitignore` alone can't fix that
  after the fact: the blobs are already in history, and getting them out
  meant a reset, a re-commit and a force-push over a published branch.
  Write the ignore rule when the directory is created.
- **What does belong in git**: the fetch and merge scripts, the manifest
  CSVs (small, and they're the provenance record — block id, title,
  description, source URL, local path), the text file the panels are
  written in, the README, and the built self-contained HTML. For
  exhibiting-ness that's 22 files against 654, and the four built decks are
  1.6 MB of it — worth keeping precisely because they're self-contained and
  are what actually gets projected.
- **A second project reuses the generator; it doesn't fork it.** When
  exhibiting-ness needed the same four builds from a different archive, the
  fix was three backwards-compatible flags on chair-ness's existing script
  (`--root` for the archive directory, `--title`, `--channel-label`) plus
  making its project-specific metadata file optional — not a copy of 46 KB
  of player code to maintain in two places. Fonts keep resolving from the
  script's own repo while content comes from `--root`, so the tool travels
  and the data stays put. Rebuild the original and diff it after any such
  change: chair-ness's two builds came out byte-identical, which is what
  made the edit safe to keep.

## Slide decks: talks vs. teaching support

Two different genres of slide deck show up across `reference/` (25
lecture PDFs, 2010–2026), and treating them the same is a mistake — a
talk deck earns the whole "full-bleed everything" treatment below, but a
teaching-support deck (screenshots, side-by-side comparisons, reference
material meant to sit in front of students) stays plain and functional on
purpose. The split is by genre, not by date: `WorkingTeachingLecture`
(2023) is as plain/white/bordered as `Entropy` (2010, no images at all),
while `FreeOpenCulture` (2021) already has the full expressive talk-deck
look that `Copyright` / `NewDesignCommons` / `Semiotics` / `FutureCone`
(2026) intensify rather than invent. Check which genre a deck is before
reaching for the rules below.

**Canvas: 16:9 or 16:10, always** — maximizes full-screen view on
whatever the room's projector or a laptop lid actually is.

**Full-bleed is a hard rule for talk decks**: images bleed to all four
edges, tilted/cropped compositions rather than centered or letterboxed —
a deliberate departure from "pin the box, `object-fit: contain` scales
into it" elsewhere in this doc, which is for an image inside a page
layout, not a full-canvas slide. Title/section-break slides get the
busiest version: a full-bleed collage (photo, engraving, or shape
confetti) under a large headline, often tilted to follow the image's own
diagonal.

**Text: short and aphoristic, never a restated sentence.** Slide text
should not repeat what's being said out loud — it either cues the speaker
on where the talk goes next, or illustrates/metaphorizes the point being
made. A quote/aphorism slide pairs a full-bleed photo with an opaque card
(tilted a few degrees, per "Typography: rotation as an accent" above)
holding one or two short lines plus attribution — never a paragraph.

**Illustration over exposition — the working techniques, not just the
principle:**
- Literalize a pun or term visually, sometimes twice in a row for the
  joke to land ("cat burglar" over a cat silhouette, then over an actual
  roof-burglar photo).
- Diagram a concept as a photo-to-photo bridge rather than a caption (a
  1999 headshot → a widening cone → a product photo, one arrow, no
  exposition text — the "futures cone" idea, unstated).
- A mascot delivers a wayfinding instruction instead of plain UI text (a
  cartoon character "speaking" a QR code).
- A closing slide can be pure image, no text at all, when the visual
  carries the whole gesture (a line-art Earth on black, nothing else).

**Typography and color, in practice:**
- Typeface varies slide to slide, matched to the image's mood — the same
  "vary project to project, license is the constant" ethos as the kit's
  typography rules, applied within a single deck instead of across
  projects.
- All-caps for short punchy labels; word-level color-highlighting for key
  terms within a longer line.
- Two color modes recur, not blended on one slide: full-color photo
  background with text set directly on top (no gradient scrim — legibility
  comes from an opaque card or tonal matching, same as "Type over images"
  above), or a black background with one or two saturated accent colors
  for data/closing slides. A cream/off-white "paper" ground is the
  recurring choice for text-forward slides, in both the oldest and newest
  decks sampled.
- A tiny credit line in a bottom corner of every image slide — "TYPE:
  [fonts used]" / "IMAGE: [source, license]" — is a real, portable
  convention worth keeping, not a one-off.
- The vintage-engraving/mascot-collage device (a Victorian etching or a
  cartoon character composited onto a real photo or screenshot) recurs
  from 2021 through 2026 — this is the "Images: Style" Victorian-etchings
  note above showing up as an active compositing technique, not just a
  sourcing preference.

**Pacing**: a talk deck changes visual mode (image/quote → image/title →
clean diagram) roughly every 1–3 slides rather than settling into one
mode for a run — a plain white-background diagram slide reads as a
deliberate reset, not a lapse.

This is about designing the slide canvases themselves (Keynote, Figma,
whatever produces the deck) — it doesn't change
`slideshow-template.html`, which is a different genre again (unattended/
ambient, no speaker in the room) and is already canvas-agnostic: images
`object-fit: contain` into whatever viewport they're given.

## Presentations: how the Figma file is built

Everything above describes what a finished slide looks like. This is about the
file. Working conventions across all 19 pages of `AY26 Lectures and
Presentations` — roughly 2,100 frames, dumped 2026-09-02 with
`lectureScripts/scripts/figma-slides.py`, which pulls a page to markdown so the
deck can be grepped and diffed without opening Figma.

**One flat canvas, sections as rows.** Not a linear stack of slides. Sections
are horizontal bands at a fixed `y`; slides step left to right in `x`, about
2000px apart for a 1920px frame. A talk deck runs 13–17 rows for 90–120 frames
— six to eight slides per section. Zoomed out, the canvas *is* the outline.

**The frame name carries section and position.** Two schemes in use, doing the
same job:

- `<n> <Section Name> <nn>` — `2 Future Cone 09`, `4.1 Quick Examples 13`.
  Dominant in *Design For the Future Today* (71 of 91 frames), the earlier
  *Semiotics* (106 of 121), *Designing Preferable Futures* (80 of 103).
- A bare number whose leading digits are the section — `000`–`006`, then
  `100`–`105`, then `2000`–`2009`. Dominant in *Semiotics Fall* (109 of 113)
  and *DI: What is DI* (50 of 50).

Either way the trailing digits are build order. Frames still called `Frame 4`
or `Group 12` are unfinished, and they cluster — `Chair-ness` carries 26.

**Slides build by duplication.** A run is one idea, and each frame is the
previous frame plus one added element: `2 Future Cone 01`→`15` draws the axis,
then now, then the past, then the cone, then each band label, one per frame.
Animation by copying slides rather than by transitions — which is why it
survives export to PDF and why it works on someone else's projector.

Present in 15 of the 19 pages, and absent in exactly the four short
administrative ones. That is a third genre beyond the talk / teaching-support
split above: a faculty-meeting deck neither bleeds nor builds.

**Consequence worth knowing when writing.** Because sections are rows and runs
build, the deck is a readable outline of the argument before any script exists
— `lecture-some-semiotics/` had a finished 113-frame deck and an empty script
file, and the deck was the only record of the talk. It also means a run's *last*
frame is the finished slide; the earlier ones are the reveal, so read a run
bottom-up when you want to know what a section actually says.

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
| `--pink-3` | accent | 8.80:1 |
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
| `--color-bg` | `--wjerk-white` | `--brown-9` |
| `--color-text` | `--wjerk-black` | `--brown-0` |
| `--color-text-muted` | `--gray-6` | `--brown-3` |
| `--color-text-subtle` | `--gray-6` | `--brown-4` |
| `--color-accent` | `--pink-5` | `--pink-3` |
| `--color-accent-hover` | `--pink-6` | `--pink-2` |
| `--color-success` | `--green-6` | `--green-3` |
| `--color-warning` | `--yellow-6` | `--yellow-3` |
| `--color-danger` | `--red-6` | `--red-3` |
| `--color-info` | `--dark-gray-6` | `--dark-gray-3` |
| `--color-*-bg` (status panels) | step 0 of each family | step 8 of each family |

Status colors follow the text's logic (added 2026-09-11): in the dark they
flip to the light end of their own hue. On `--brown-9` they measure 9.98–10.76:1
(`red-3` lowest), and 8.8–9.5:1 on their step-8 panels — AAA throughout.
`--pink-2` for the pressed accent is 11.07:1, and `--brown-9` on it the same.

`kit.css` still pins `color-scheme: light` and does not ship the flip yet.
The open question was never which colors — it was whether to spend the
complexity. The colors are now answered.

First built and contrast-checked for the chair-ness exhibition slideshow
(`~/Code/chair-ness`), projected dark in a gallery.

First shipped in a web app in wjeather (2026-09-10): a `prefers-color-scheme:
dark` block in the project's own CSS flipping exactly these tokens, `kit.css`
untouched. The mapping held. Tints behind text in dark mode are steps 7–9 —
see "Color: tints behind text".

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

## Color: tints behind text

When a tint sits behind text or a data line — bands, fills, highlighted
rows — the budget, measured 2026-09-10:

- **Light:** steps 0–2 of every scale pass against the kit's text,
  `--wjerk-black` (≥7.8:1, weakest on `pink-2`), `--gray-6` labels (≥5.2) and
  a `--pink-5` line (≥3.1 on every tint but pink's own; weakest `red-2`). Step 3
  fails — `blue-3` drops labels to 4.05 and the pink line to 2.71.
- **Dark:** steps 7–9 pass against `--brown-0`, `--brown-3` and a `--pink-3`
  line (weakest, `yellow-7`: 11.59 / 6.47; the pink line ≥5.4 on any step 7–9).

Contrast isn't the only test. Pale tints crowd each other, so check
distinctness too — OKLab distance ×100; under ~5 reads as the same color.
What the scales look like on screen, not by name:

- **Purple read pink** at steps 0–2 — close enough to be mistaken for the
  accent — until 2026-09-11, when the scale moved from hue ~336° to 315° at
  the same lightness and muted chroma. Step 2 now sits 5.7 from `pink-1` and
  5.1 from `cornflower-2`. Still a gray-purple, not a violet; still worth a
  look beside pink.
- **Green reads olive;** `green-6` reads as more brown. `green-5` is the most
  visibly green step that still holds 3:1 as a line on every pale tint
  wjeather uses.
- **Blue is a teal-gray;** `blue-0` is near-white.
- **Warm gray, peach and pale brown** (`gray-1`, `orange-0`, `brown-1`) sit
  within ~3 of each other — effectively one color.

Blend tints `in oklab`. `oklch` takes the hue arc: yellow → purple passes
through orange, too near the pink.

## Data on screen

From wjeather (2026-09-10), the first project where the kit carries data
rather than prose:

- **One variable per visual channel** — position, hue, edge softness,
  texture. Two variables sharing a channel means neither reads.
- **Pink is the primary series,** a 2px line. A second series takes a hue no
  other layer uses *and* a dash (6/6, on the grid), so it survives grayscale
  and color-blindness.
- **Data tints sit inside the text budget** above, because the number and
  labels sit on them.
- **Texture is line work:** wind as hatching, stars as stipple. The etching
  trope, and a way to add a variable without adding a hue.
- **Anything drawn gets a spoken summary** for screen readers. Color and
  position are never the only carrier.

## Using the kit with Tailwind (v4)

First done in wjeather (SvelteKit + Tailwind 4, 2026-09-10). `kit.css` stays a
verbatim copy; the project's own CSS maps it in:

```css
@import 'tailwindcss';
@import '../lib/kit.css' layer(base); /* layered, so utilities still win */

@theme {
  --color-*: initial;  --text-*: initial;  --font-*: initial;  --breakpoint-*: initial;
  --breakpoint-tablet: 40rem;  --breakpoint-desktop: 55rem;
  --container-tablet: 40rem;   --container-desktop: 55rem; /* @tablet: / @desktop: */
  --spacing: 0.375rem;         /* p-4 = 24px: spacing on the 6px rhythm */
}

@theme inline reference {
  --color-bg: var(--color-bg);  --color-text: var(--color-text); /* …every semantic token */
  --text-base: var(--text-base);  --text-base--line-height: var(--leading-base); /* …every rung */
}
```

- Clearing Tailwind's defaults leaves only kit colors, type rungs and the two
  breakpoints as utilities — the handful-of-tokens rule, enforced by the build.
- `inline reference` makes utilities point straight at the kit's variables
  (`.bg-bg { background-color: var(--color-bg) }`) without Tailwind emitting a
  second, self-referencing copy of them.
- Unlayered, `kit.css` would beat every utility. Importing it into
  `layer(base)` is what lets `text-xl` override the kit's `h1`.
- Project-only tokens (a display size, data colors) live in the project's CSS
  beside the mapping, each with its measured contrast in a comment.

## Icons: one family across sites and apps

Every site and app gets a mark from one family (2026-09-11: onething, oblique
stuff, bjornpaedia, the wjerk.shop stores, wjeather). The frame is constant;
one thing varies.

**Constant**

- **A solid white, full-square background.** Never transparent — iOS fills
  transparency with black — and the white ground is what makes the set read
  as a set on a home screen or tab bar.
- **A bordered square in dark brown line work** (`--brown-8`, #191513), with
  its shadow built from stacked offset outlines rather than a blur. "Rules,
  not shadows," as the mark itself.
- **Generous white margin** around the frame, so platform crops (Android's
  circles and squircles, iOS rounding) only ever trim background.

**Varies, one per site**

- **A single pale fill** inside the square. Prefer a kit tint (steps 0–2,
  measured against the brown); a custom fill is a deliberate exception.
  OneThing's plain white is the neutral root.
- **A monogram in the site's own typeface** — the type rule again: letterforms
  vary by project, the license stays constant. Outlined OFL glyphs are fine in
  a logo.

a.wjerk.shop's etched globe breaks the frame — see NOTES.md.

**Export, all from one SVG**

| Where | File | Notes |
|---|---|---|
| Browser tab | `favicon.svg` | The source SVG as-is |
| iOS home screen | `apple-touch-icon.png`, 180×180 | Opaque; `<link rel="apple-touch-icon">`. iOS rounds the corners — don't pre-round. iOS keeps the icon from when a site was added; re-add it to see a new one |
| Android / installable web app | 192×192 and 512×512 PNG, in a web manifest | Keep the mark inside the centre ~80% (the maskable safe zone) |
| App Store, if ever native | 1024×1024 PNG | Opaque, square, no rounding |

On macOS the PNGs render straight from the SVG with Quick Look —
`qlmanage -t -s 180 -o . icon.svg`, repeated for 192 and 512. Check the result
is fully opaque: Quick Look writes an alpha channel even when no pixel is
transparent.

## Color: the original Wjerk palette

The palette the work used before `kit.css` existed — named for OOKB, and the
Wjerk palette now. It lives as the "OOKB Palette" color styles in Figma (the
AY26 Lectures and Presentations file, also published as a library the decks
pull from); the styles keep the old name so the decks don't break. White and
Black are also kit tokens now, `--wjerk-white` and `--wjerk-black`, and the
kit's ground and text. An earlier web version, as LESS variables, is in
README.md — the same hues a step apart (its pink, #EC4079, is brighter than
the Figma #DB4F7A). Recorded 2026-09-11 from the styles themselves,
not eyeballed. "On White" is contrast against Wjerk White; ΔE is OKLab distance
×100 to the nearest kit token (under ~5 reads as the same color).

| Wjerk | Hex | Nearest kit | ΔE | On White |
|---|---|---|---|---|
| Black | #2D2826 | brown-7 | 4.0 | 13.73 |
| White | #F8FAE7 | light-gray-0 | 1.1 | — |
| Brown | #3C3634 | brown-7 | 1.7 | 11.20 |
| Dark Gray | #616767 | dark-gray-5 | 5.1 | 5.44 |
| Med Gray | #858479 | brown-5 | 5.2 | 3.56 |
| Pink | #DB4F7A | pink-4 | 6.1 | 3.66 |
| Red | #9F5B59 | orange-5 | 3.2 | 4.82 |
| Orange | #B97868 | orange-4 | 4.7 | 3.33 |
| Yellow | #C5C071 | yellow-3 | 0.4 | 1.78 |
| Golden Rod | #CBAA46 | yellow-3 | 5.6 | 2.11 |
| Light Green Gray | #C5D3BD | light-gray-2 | 2.5 | 1.48 |
| Green | #91A478 | green-4 | 1.6 | 2.55 |
| Dark Green | #6A8472 | light-gray-5 | 3.1 | 3.84 |
| Light Blue | #A1B2B1 | blue-3 | 4.0 | 2.08 |
| Cornflower | #627FBB | blue-5 | 10.2 | 3.76 |
| Dark Cornflower | #3E5F9A | blue-6 | 11.0 | 5.99 |
| Navy | #2C416B | blue-7 | 9.5 | 9.55 |
| Purple | #A38DA1 | purple-4 | 1.9 | 2.88 |
| Purple Gray | #777783 | dark-gray-5 | 2.5 | 4.17 |

Plus a **YGB Gradient**: Yellow #C5C071 → Green #91A478 (at 51%) → #92A9A7.

What it says about the kit:

- **The kit grew from it.** Yellow is `yellow-3` almost exactly (0.4), Green
  is `green-4`, Brown is `brown-7`, and Wjerk White is effectively the kit's
  pale ground. The kit's scales are Wjerk's hues run through ten lightness
  steps.
- **The blues didn't make it.** Cornflower, Dark Cornflower and Navy are true
  blues (hue ~262°); the kit's "blue" scale is a teal-gray (~190°), 9.5–11
  away. Golden Rod had no kit match either. **Added back 2026-09-11** as the
  `cornflower` and `goldenrod` scales, on the kit's shared lightness grid
  (0.975 → 0.12) with the green scale's chroma shape. The originals fall
  between grid steps, so each lands near one rather than on it: Cornflower ≈
  `cornflower-5` (ΔE 4.1), Dark Cornflower ≈ `-6` (4.9), Navy ≈ `-7` (5.9),
  Golden Rod ≈ `goldenrod-3` (4.3). Steps 0–2 and 7–9 of both pass the tint
  budget; `-6` and `-7` of both pass as text on `--gray-0` (7.3, 11.9).
  `cornflower-2` also gives the pale range a blue that's distinct from the
  teal (6.1 from `blue-2`).
- **The original pink is softer.** Wjerk Pink (#DB4F7A, OKLCH chroma 0.178) is
  a dustier pink than the kit's old `pink-5` (0.226). At 3.66:1 on White it was
  never a body-text color — and never used as one: pink was for big display
  type and accents, where 3:1 (AA large text and graphics) is the bar.
  **Since 2026-09-11 the kit's pink scale is rebuilt at that chroma** — same
  lightness and hue per step, dustier throughout. The original sits between
  `pink-4` and `pink-5`, and `pink-5` still carries small text (4.78:1).
- **It's a fill palette, made for light type on top.** It grew out of slide
  deck designs and a personal webpage: the colors were backgrounds, with
  White type reversed out of them. `kit.css` building ten tints per hue is
  the same idea taken further. Read the "On White" column both ways — it is
  also White type on that fill. Black, Brown, Navy, Dark Cornflower, Dark Gray
  and Red carry White body text (≥4.5); Pink, Orange, Med Gray, Dark Green,
  Cornflower and Purple Gray carry White display type (≥3, AA large text);
  the pale ones (Yellow, Golden Rod, Light Green Gray, Green, Light Blue,
  Purple) need dark type.
- **Wjerk Purple was already mauve** (hue 329°), so "purple reads pink" is
  partly inherited — a muted, muddled gray-purple, meant to lean blue. The
  kit then drifted pinker still (~336°); since 2026-09-11 it sits at 315°,
  bluer than the original, as intended.
