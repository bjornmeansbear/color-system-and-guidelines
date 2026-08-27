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

1. **Your are.na channels** — already collected, already vetted. Read over the
   public v3 API, no auth, matched locally.
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
| `COMMONS_CHANNELS` | `chair-ness` | are.na slugs searched first |

The cache lives **outside any repo**. `chair-ness` is the model: 423 images and
348MB on disk against a 5.5MB `.git`, because the caches are gitignored. The
canonical record is the are.na channel plus `manifest.csv` — id, title, source
URL, licence, `full_url`, `local_path`, dimensions.

## Not done yet

- **Writing picks back to are.na.** `chair-ness/scripts/arena_add.py` does this
  already, but it needs a working `ARENA_ACCESS_TOKEN` — see NOTES.md. Until
  then step 1 of the cascade never gets smarter from museum picks.
- **Searching your own are.na account** rather than a configured channel list.
  Same blocker.
