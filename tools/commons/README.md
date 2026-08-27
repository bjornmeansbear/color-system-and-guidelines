# commons

Slide imagery for decks. **Machine narrows, you choose, machine writes the
credit line.**

Metaphorical judgement — which painting actually rhymes with the slide — does
not automate. Reducing four million public-domain objects to forty worth
flipping through does. This tool does only the second half.

See RULES.md "Presentations: sourcing, in this order" and "Presentations:
imagery" for the rules this implements.

## Slots, not filenames

A hardcoded `url('images/beat-history.jpg')` cannot say what the image is
*for*, so it can neither be searched against nor prompt you. Slides declare
intent instead:

```html
<section class="slide opener beat"
         data-img="beat-history"
         data-img-brief="an older lineage — surveying, notebooks, workshop labor"
         data-img-terms="surveying, workshop, notebook, apprentice">
```

**The brief is yours. The terms are not yours to write.** Translating a
metaphor into concrete nouns is the machine's job — being asked for keywords
inverts the whole premise. Leave `data-img-terms` off and the brief's content
words are searched instead; fill it in when you want a better search than that.

**The brief is for you. The terms are for the machine.** Museum APIs match a
short concrete noun, not a metaphor — searching the brief verbatim returns
*The Death of Socrates* for "ordinary labor in a working interior". Terms are
comma-separated and each is searched separately. Without them the brief is
used, which usually works for concrete briefs and badly for poetic ones.

## Use

```
commons.py slots   DECK                    what is declared, what is empty
commons.py fill    DECK [SLOT] [--terms …] search, build a contact sheet, open it
commons.py search  QUERY                   ad-hoc, no deck needed
commons.py pick    DECK SLOT SOURCE:ID     cache, record, write the credit back
commons.py resolve DECK [--web|--work]     emit a build
```

Pick from the contact sheet by clicking — it copies the exact `pick` command
to your clipboard.

## Three builds, one source

| build | images | empty slots |
|---|---|---|
| `resolve` | local files | silent flat ground |
| `resolve --web` | hotlinked source URLs | silent flat ground |
| `resolve --work` | local files | **loud pink marker + the brief** |

Loud on the desk, silent in the room. Never show a TODO to an audience — and
never let a gap stay invisible while you still have time to fill it.

**Anything projected uses the local build.** Network is not a runtime
dependency in a room you do not control.

## Search order

**One channel per deck.** A deck names its own are.na research channel and
everything in it is a candidate — channel membership is the curation:

```html
<meta name="commons-channel" content="lecture-mending-nets">
```

That channel holds the 21 blocks behind "On Mending" (18 of them printable).
The cascade below only tops it up.

1. **The deck's channel**, unfiltered.
2. **The rest of your are.na** — `/v3/search` with `user_id`, one request
   against everything you have saved. Needs `ARENA_ACCESS_TOKEN`, read from
   this repo's `.env`, then `chair-ness`, then `sentence-a-day`, skipping
   commented lines.
3. **Wikimedia Commons.**
4. **AIC, the Met, Cleveland.**

**Route by query shape.** Measured, not assumed:

| you are searching for | use | why |
|---|---|---|
| a concept — "ordinary labor" | museum APIs | curated subject metadata; Commons returns a recording studio for *Aeron* |
| a named artist or work — "Sorolla mending nets" | Commons | museums only hold their own; AIC returns its Homers for every European painter |

The American museum APIs are a depth source, not a breadth source. They found
none of Sorolla, Mønsted, Israëls, Avercamp or Kuniyoshi — all of whom are in
the Mending deck, and all of whom Commons has.

**Undersized are.na hits survive as leads.** are.na saves what the source page
served, so his own blocks are often 150px thumbnails. Sorolla's *Mending the
Nets* comes back at 150×150 — the actual painting from the deck. It is kept,
marked "already yours · too small to project", and the other sources find a
printable copy.

Every candidate is filtered to public domain and ≥2000px before it reaches your
eye. Unknown size fails closed. Where an API does not report dimensions the
JPEG/PNG header is probed by streaming a few KB — `sources.probe_size`.

Two API quirks handled rather than papered over: the Met's ranking collapses
when `medium=` / `isPublicDomain=` accompany the query (`q=kitchen` filtered
leads with a Saint Jerome; unfiltered it leads with "Kitchen Scene"), and AIC
ignores the top-level `q` once an Elasticsearch body is supplied, so the
keyword goes inside the bool or the material filter returns the same rows for
every subject.

## Config

| var | default | |
|---|---|---|
| `COMMONS_CACHE` | `~/Media/commons` | image cache + `manifest.csv` |
| `COMMONS_CHANNELS` | `chair-ness` | legacy; the are.na source now searches your whole account |

The cache lives **outside any repo**. `chair-ness` is the model: 423 images and
348MB on disk against a 5.5MB `.git`, because the caches are gitignored. The
canonical record is the are.na channel plus `manifest.csv` — id, title, source
URL, licence, `full_url`, `local_path`, dimensions.

## Not done yet

- **Writing picks back to are.na.** The token is now read+write and the spec is
  at `~/Code/sentence-a-day/openapi` (YAML, are.na v3.0.0): `POST /v3/blocks`
  to create, `POST /v3/connections` to connect it to a channel. Not wired up
  yet — until it is, step 1 never gets smarter from museum picks.
