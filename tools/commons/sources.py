"""
Candidate sources for slide imagery, searched in the order RULES.md fixes:
are.na channels first, then the no-key museum APIs, then Wikimedia Commons.

Every source normalises to the same Candidate shape so the contact sheet and
the picker do not care where a thing came from.
"""
import concurrent.futures as cf
import io
import json
import re
import pathlib
import struct
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "commons-tool/0.1 (personal research; slide imagery)"}
TIMEOUT = 30

# RULES.md caps upscale at 2.5x and a projector eats resolution.
MIN_PX = 2000


class Candidate(dict):
    """source, id, title, artist, date, license, credit, page_url,
    thumb_url, full_url, width, height."""

    @property
    def key(self):
        return f"{self['source']}:{self['id']}"


def _get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def _qs(base, **params):
    return base + "?" + urllib.parse.urlencode(
        {k: v for k, v in params.items() if v is not None})


# ---------------------------------------------------------------- dimensions

def probe_size(url, budget=196608):
    """Pixel dimensions from an image's header without downloading the file.

    Reads in 8KB chunks up to `budget` and stops at the first JPEG SOF / PNG
    IHDR marker. Returns (width, height) or (None, None) if it cannot tell.
    """
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            buf = b""
            while len(buf) < budget:
                chunk = r.read(8192)
                if not chunk:
                    break
                buf += chunk
                wh = _parse_size(buf)
                if wh:
                    return wh
    except Exception:
        pass
    return (None, None)


def _parse_size(buf):
    if buf[:8] == b"\x89PNG\r\n\x1a\n" and len(buf) >= 24:
        w, h = struct.unpack(">II", buf[16:24])
        return (w, h)
    if buf[:2] == b"\xff\xd8":  # JPEG
        i = 2
        while i + 9 < len(buf):
            if buf[i] != 0xFF:
                i += 1
                continue
            marker = buf[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            seglen = struct.unpack(">H", buf[i + 2:i + 4])[0]
            # SOF0..SOF15, skipping the non-frame markers in that range
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", buf[i + 5:i + 9])
                return (w, h)
            i += 2 + seglen
    return None


def fill_sizes(cands, workers=8):
    """Probe any candidate whose dimensions the API did not report."""
    todo = [c for c in cands if not c.get("width")]
    if not todo:
        return cands
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for c, (w, h) in zip(todo, ex.map(
                lambda x: probe_size(x["full_url"]), todo)):
            c["width"], c["height"] = w, h
    return cands


def big_enough(c):
    """Unknown size fails closed — RULES.md filters before it reaches the eye."""
    w, h = c.get("width"), c.get("height")
    if not w or not h:
        return False
    return max(w, h) >= MIN_PX


# -------------------------------------------------------------------- are.na

ARENA_ENV_PATHS = [
    pathlib.Path.home() / "Code/color-system-and-guidelines/.env",
    pathlib.Path.home() / "Code/chair-ness/.env",
    pathlib.Path.home() / "Code/sentence-a-day/.env",
]
_ARENA = {"token": ..., "user_id": None}


def arena_token():
    """First uncommented ARENA_ACCESS_TOKEN wins. Commented lines are skipped —
    the .env files keep an old read-only token commented above the live one."""
    if _ARENA["token"] is not ...:
        return _ARENA["token"]
    _ARENA["token"] = None
    for path in ARENA_ENV_PATHS:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            m = re.match(r"(?:export\s+)?ARENA_ACCESS_TOKEN\s*=\s*(.+)", line)
            if m:
                _ARENA["token"] = m.group(1).strip().strip("\"'")
    return _ARENA["token"]


def arena_user_id():
    if _ARENA["user_id"] or not arena_token():
        return _ARENA["user_id"]
    try:
        d = _get("https://api.are.na/v3/me",
                 {"Authorization": "Bearer " + arena_token()})
        _ARENA["user_id"] = (d.get("user") or d).get("id")
    except Exception:
        pass
    return _ARENA["user_id"]


def arena_channel(slug, query=None, limit=100):
    """Every image in one channel — a deck's own research channel.

    He keeps one channel per deck (`lecture-mending-nets` for "On Mending":
    21 blocks of Homer, Sorolla, Israels, Avercamp, Monsted, Kuniyoshi). When
    a deck names its channel, that channel *is* the family and it should be
    searched before anything else.
    """
    tok = arena_token()
    hdr = {"Authorization": "Bearer " + tok} if tok else None
    try:
        d = _get(f"https://api.are.na/v3/channels/{slug}/contents?per={limit}", hdr)
    except Exception:
        return []
    out = []
    for b in (d.get("contents") or d.get("data") or []):
        img = b.get("image") or {}
        if not img.get("src"):
            continue
        src = b.get("source") or {}
        title = _plain(b.get("title")) or "(untitled)"
        if query and not any(t in title.lower()
                             for t in re.split(r"\W+", query.lower()) if len(t) > 3):
            pass  # channel membership is the filter; keep everything
        out.append(Candidate(
            source="arena", id=str(b.get("id")), title=title, artist="", date="",
            license="check the source",
            credit=_plain(b.get("description")) or src.get("url") or "",
            page_url=src.get("url") or f"https://www.are.na/block/{b.get('id')}",
            thumb_url=((img.get("medium") or {}).get("src")) or img["src"],
            full_url=img["src"], width=None, height=None))
    return out


def arena(query, limit=25, **_):
    """Search everything he has already collected, across every channel.

    /v3/search takes user_id, so this is one request against his whole are.na
    rather than a walk over a configured channel list. Needs a token; without
    one this source is simply skipped and the cascade falls through.

    Note that are.na blocks are often saved at whatever size the source page
    served — a 150x150 Flickr thumbnail is common — so many of his own blocks
    fail the projection threshold. They still tell you *which* artwork he
    already liked, which the later sources can then find at full size.
    """
    tok, uid = arena_token(), arena_user_id()
    if not tok or not uid:
        return []
    d = _get(_qs("https://api.are.na/v3/search", query=query, user_id=uid,
                 type="Image", per=limit),
             {"Authorization": "Bearer " + tok})
    out, seen = [], set()
    for b in (d.get("data") or []):
        bid = b.get("id")
        # Dedup on title as well as id: the same image is often saved to
        # several channels as separate blocks.
        key = (_plain(b.get("title")) or "").strip().lower() or bid
        if bid in seen or key in seen:
            continue
        seen.update((bid, key))
        img = b.get("image") or {}
        if not img.get("src"):
            continue
        src = b.get("source") or {}
        title = _plain(b.get("title")) or img.get("filename") or "(untitled)"
        desc = _plain(b.get("description"))
        out.append(Candidate(
            source="arena", id=str(bid), title=title,
            artist="", date="", license="check the source",
            credit=desc or src.get("url") or f"via are.na block {bid}",
            page_url=src.get("url") or f"https://www.are.na/block/{bid}",
            thumb_url=((img.get("medium") or {}).get("src")) or img["src"],
            full_url=img["src"], width=None, height=None))
    return out


def _plain(v):
    if isinstance(v, dict):
        return v.get("plain") or v.get("markdown") or ""
    return v or ""


# ----------------------------------------------------------------------- Met

def met(query, limit=15, material=None):
    """The Met's search ranks well on `q` alone and badly with filters added.

    Sending medium= / isPublicDomain= / hasImages= alongside the query returns
    a differently-ordered set — `q=kitchen` with filters leads with a Saint
    Jerome and portraits, without them it leads with "Kitchen Scene". So the
    query goes in clean and the public-domain test happens per object below.
    """
    extra = {}
    if material and material.medium:
        extra["medium"] = material.medium.title() + "s"
    if material and material.years:
        extra["dateBegin"], extra["dateEnd"] = material.years
    s = _get(_qs("https://collectionapi.metmuseum.org/public/collection/v1/search",
                 q=query, **extra))
    ids = (s.get("objectIDs") or [])[:limit]

    def one(oid):
        for attempt in range(3):
            try:
                return _get("https://collectionapi.metmuseum.org/public/collection/"
                            f"v1/objects/{oid}")
            except urllib.error.HTTPError as e:
                if e.code in (403, 429):        # the Met rate-limits bursts
                    time.sleep(1.5 * (attempt + 1))
                    continue
                return None
            except Exception:
                return None
        return None

    out = []
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for o in ex.map(one, ids):
            if not o or not o.get("isPublicDomain") or not o.get("primaryImage"):
                continue
            if o.get("classification") and "Painting" not in o["classification"] \
                    and "Drawing" not in o["classification"] \
                    and "Print" not in o["classification"]:
                continue
            artist = o.get("artistDisplayName") or "Unknown artist"
            date = o.get("objectDate") or ""
            out.append(Candidate(
                source="met", id=str(o["objectID"]), title=o.get("title") or "(untitled)",
                artist=artist, date=date, license="Public domain (CC0)",
                credit=f"{artist}, {o.get('title','')}, {date}. "
                       "The Metropolitan Museum of Art. Public domain.",
                page_url=o.get("objectURL") or "",
                thumb_url=o.get("primaryImageSmall") or o["primaryImage"],
                full_url=o["primaryImage"], width=None, height=None))
    return out


# ----------------------------------------------------- Art Institute Chicago

def aic(query, limit=25, material=None):
    """`material` is a Material() — medium keyword and/or a year range.

    AIC accepts a full Elasticsearch body on POST, which is the only way to
    hold a deck to one visual family (all etchings, all 19th century) instead
    of five unrelated pictures.
    """
    if material and material:
        # The top-level `q` is ignored once a bool query is supplied, so the
        # keyword has to go inside the bool or the filter returns the same
        # rows for every subject.
        must = [{"term": {"is_public_domain": True}},
                {"multi_match": {
                    "query": query,
                    "fields": ["title^3", "term_titles^2", "subject_titles^2",
                               "artist_title", "description"]}}]
        if material.kind:
            must.append({"match_phrase": {"artwork_type_title": material.kind}})
        if material.medium:
            must.append({"match": {"medium_display": material.medium}})
        if material.years:
            lo, hi = material.years
            must.append({"range": {"date_end": {"gte": lo, "lte": hi}}})
        body = {"query": {"bool": {"must": must}},
                "fields": "id,title,artist_title,date_display,is_public_domain,"
                          "image_id,thumbnail".split(",") if False else
                          ["id", "title", "artist_title", "date_display",
                           "is_public_domain", "image_id", "thumbnail"],
                "limit": limit}
        req = urllib.request.Request(
            "https://api.artic.edu/api/v1/artworks/search",
            data=json.dumps(body).encode(),
            headers={**UA, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return _aic_rows(json.load(r))
    return _aic_plain(query, limit)


def _aic_plain(query, limit=25):
    d = _get(_qs("https://api.artic.edu/api/v1/artworks/search",
                 q=query, limit=limit,
                 fields="id,title,artist_title,date_display,is_public_domain,"
                        "image_id,thumbnail"))
    return _aic_rows(d)


def _aic_rows(d):
    iiif = d.get("config", {}).get("iiif_url", "https://www.artic.edu/iiif/2")
    out = []
    for a in d.get("data", []):
        if not a.get("is_public_domain") or not a.get("image_id"):
            continue
        th = a.get("thumbnail") or {}
        artist = a.get("artist_title") or "Unknown artist"
        date = a.get("date_display") or ""
        out.append(Candidate(
            source="aic", id=str(a["id"]), title=a.get("title") or "(untitled)",
            artist=artist, date=date, license="Public domain (CC0)",
            credit=f"{artist}, {a.get('title','')}, {date}. "
                   "Art Institute of Chicago. Public domain.",
            page_url=f"https://www.artic.edu/artworks/{a['id']}",
            thumb_url=f"{iiif}/{a['image_id']}/full/600,/0/default.jpg",
            full_url=f"{iiif}/{a['image_id']}/full/3000,/0/default.jpg",
            width=th.get("width"), height=th.get("height")))
    return out


# ----------------------------------------------------------------- Cleveland

def cleveland(query, limit=25):
    d = _get(_qs("https://openaccess-api.clevelandart.org/api/artworks/",
                 q=query, limit=limit, cc0="1", has_image="1"))
    out = []
    for a in d.get("data", []):
        if a.get("share_license_status") != "CC0":
            continue
        imgs = a.get("images") or {}
        best = imgs.get("print") or imgs.get("full") or imgs.get("web")
        if not best or not best.get("url"):
            continue
        creators = a.get("creators") or []
        artist = creators[0].get("description") if creators else "Unknown artist"
        date = a.get("creation_date") or ""
        out.append(Candidate(
            source="cleveland", id=str(a.get("id")),
            title=a.get("title") or "(untitled)", artist=artist, date=date,
            license="CC0",
            credit=f"{artist}, {a.get('title','')}, {date}. "
                   "Cleveland Museum of Art. CC0.",
            page_url=a.get("url") or "",
            thumb_url=(imgs.get("web") or best).get("url"),
            full_url=best["url"],
            width=int(best.get("width") or 0) or None,
            height=int(best.get("height") or 0) or None))
    return out


# ---------------------------------------------------------- Wikimedia Commons

def wikimedia(query, limit=25):
    """The breadth source, and the only one that finds most of what he uses.

    The US museum APIs can only return what they own, which is a real bias:
    searching AIC for Sorolla, Monsted, Israels, Avercamp or Kuniyoshi returns
    its own Winslow Homers every time. Commons aggregates across collections
    and has all of them.

    The precision caveat still holds and is about *concepts*, not artists.
    Searching a concept ("ordinary labor") matches catalogue keywords and
    returns junk — a recording studio for "Aeron". Searching a named artwork or
    artist ("Sorolla mending nets") is where Commons is unbeatable. Route
    accordingly: concepts to the museums, names to Commons."""
    d = _get(_qs("https://commons.wikimedia.org/w/api.php",
                 action="query", format="json", generator="search",
                 gsrsearch=f"{query} filetype:bitmap", gsrlimit=limit,
                 gsrnamespace=6, prop="imageinfo", iiprop="url|size|extmetadata",
                 iiurlwidth=600))
    out = []
    for p in (d.get("query", {}).get("pages") or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii.get("url"):
            continue
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName") or {}).get("value", "unknown")
        if not re.search(r"cc0|public domain|pd-", lic, re.I):
            continue
        artist = re.sub(r"<[^>]+>", "", (meta.get("Artist") or {}).get("value", "")).strip()
        out.append(Candidate(
            source="wikimedia", id=str(p.get("pageid")),
            title=(p.get("title") or "").removeprefix("File:"),
            artist=artist or "Unknown", date="", license=lic,
            credit=f"{artist or 'Unknown'}. Via Wikimedia Commons. {lic}.",
            page_url=ii.get("descriptionurl") or "",
            thumb_url=ii.get("thumburl") or ii["url"], full_url=ii["url"],
            width=ii.get("width"), height=ii.get("height")))
    return out


KINDS = {"painting": "Painting", "paintings": "Painting",
         "print": "Print", "prints": "Print",
         "drawing": "Drawing", "drawings": "Drawing",
         "photograph": "Photograph", "photographs": "Photograph",
         "textile": "Textile", "textiles": "Textile"}


class Material:
    """A deck-level constraint. Three grades, coarse to fine:

        "paintings"                  every image is a painting
        "etching"                    every image is an etching
        "etching; 1837-1901"         ...and Victorian

    The coarse grade matters more than it looks: without it, searches return
    vessels, daggers and reliquaries whose catalogue text merely mentions the
    keyword. "paintings" is both a look and a noise filter.
    """

    def __init__(self, spec=""):
        self.medium, self.years, self.kind = None, None, None
        for part in (spec or "").split(";"):
            part = part.strip()
            if not part:
                continue
            m = re.fullmatch(r"(\d{3,4})\s*[-–]\s*(\d{3,4})", part)
            if m:
                self.years = (int(m.group(1)), int(m.group(2)))
            elif part.lower() in KINDS:
                self.kind = KINDS[part.lower()]
            else:
                self.medium = part

    def __bool__(self):
        return bool(self.medium or self.years or self.kind)

    def __repr__(self):
        bits = [b for b in (self.kind, self.medium) if b]
        if self.years:
            bits.append(f"{self.years[0]}\u2013{self.years[1]}")
        return "; ".join(bits) or "(none)"


CASCADE = [
    ("are.na", lambda q, ch, mat: arena(q)),
    # Commons before the museum APIs for named artists/artworks: it aggregates
    # across collections where the museum APIs only hold their own.
    ("wikimedia", lambda q, ch, mat: wikimedia(q)),
    # AIC before the Met: one request, real relevance ranking, and it reports
    # dimensions so most candidates need no header probe.
    ("aic", lambda q, ch, mat: aic(q, material=mat)),
    ("met", lambda q, ch, mat: met(q, material=mat)),
    ("cleveland", lambda q, ch, mat: cleveland(q)),
]


def search(query, channels=(), want=40, only=None, verbose=True, material=None):
    """Run the cascade in RULES.md order, stopping once `want` is satisfied.

    `query` may be several comma-separated terms. Each is searched separately
    and the results merged — keyword APIs match a short concrete noun far
    better than one long metaphorical sentence.
    """
    terms = [t.strip() for t in query.split(",") if t.strip()] or [query]
    if len(terms) == 1 and len(terms[0].split()) > 3:
        # A metaphorical brief sent whole matches nothing useful — keyword APIs
        # want a short concrete noun. Falling back to its content words is
        # cruder than real terms but far better than the sentence.
        terms = content_words(terms[0]) or terms
    found, seen = [], set()
    for name, fn in CASCADE:
        if only and name not in only:
            continue
        try:
            got = []
            for t in terms:
                got += fn(t, list(channels), material)
        except Exception as e:
            if verbose:
                print(f"  {name:10s} failed: {e}")
            continue
        got = [c for c in got if c.key not in seen]
        fill_sizes(got)
        # An are.na hit that is too small to project is still the single most
        # informative row on the sheet: it names an artwork he already chose.
        # Keep it as a lead and let the museum sources find a printable copy.
        for c in got:
            c["lead"] = c["source"] == "arena" and not big_enough(c)
        kept = [c for c in got if big_enough(c) or c["lead"]]
        for c in kept:
            seen.add(c.key)
        if verbose:
            leads = sum(1 for c in kept if c.get("lead"))
            small = len(got) - len(kept)
            print(f"  {name:10s} {len(kept) - leads:3d} kept"
                  + (f", {leads} lead(s) too small to project" if leads else "")
                  + (f", {small} under {MIN_PX}px" if small else ""))
        found += kept
        if len(found) >= want:
            break
    return found[:want]
