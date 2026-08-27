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

Fixed by RULES.md, and it stops as soon as it has enough:

1. **Your are.na** — already collected, already vetted. `GET /v3/search` with
   `user_id`, so it is one request against everything you have saved rather
   than a walk over a configured channel list. Needs `ARENA_ACCESS_TOKEN`;
   without one the source is skipped and the cascade falls through. Token is
   read from `.env` in this repo, then `chair-ness`, then `sentence-a-day` —
   commented lines are skipped, since those files keep an old read-only token
   commented above the live one.

   **Expect your own blocks to fail the size filter.** are.na saves whatever
   the source page served, so a 150x150 Flickr thumbnail is common. Searching
   "mending" returns Sorolla's *Mending the Nets* — the actual painting from
   the deck — at 150px. That is still the most useful result on the sheet: it
   tells you which artwork you already chose, and the museum sources can then
   find it at a printable size.
2. **Art Institute of Chicago** — one request, real relevance ranking, reports
   dimensions, IIIF sizing.
3. **The Met** — good ranking on `q` alone. Note the quirk handled in
   `sources.py`: adding `medium=` / `isPublicDomain=` / `hasImages=` alongside
   the query *destroys* the ranking (`q=kitchen` filtered leads with a Saint
   Jerome; unfiltered it leads with "Kitchen Scene"). So the query goes in
   clean and public-domain is tested per object. The Met also rate-limits
   bursts — hence 4 workers and a backoff.
4. **Cleveland** — CC0 flag, good print-size derivatives.
5. **Wikimedia Commons, last** — Commons search matches keywords, not objects.
   It returns a recording studio for *Aeron*. Treat every result as unverified.

Every candidate is filtered to public domain and ≥2000px **before it reaches
your eye**. Unknown size fails closed. Where an API does not report dimensions
the file's JPEG/PNG header is probed by streaming only the first few KB —
`sources.probe_size`.

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
