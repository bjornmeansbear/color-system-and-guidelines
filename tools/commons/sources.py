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

def arena_channels(slugs, query, per_channel=200):
    """Search your own already-collected material first.

    Uses the public v3 contents endpoint (no auth) and matches locally, so
    this works whether or not ARENA_ACCESS_TOKEN is sorted out.
    """
    terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    out = []
    for slug in slugs:
        page, seen = 1, 0
        while seen < per_channel:
            try:
                d = _get(f"https://api.are.na/v3/channels/{slug}/contents"
                         f"?per=100&page={page}")
            except Exception:
                break
            blocks = d.get("contents") or d.get("data") or []
            if not blocks:
                break
            for b in blocks:
                seen += 1
                if (b.get("class") or b.get("type")) not in ("Image", "Link"):
                    continue
                img = b.get("image") or {}
                orig = (img.get("original") or {})
                if not orig.get("url"):
                    continue
                title = _plain(b.get("title")) or ""
                desc = _plain(b.get("description")) or ""
                hay = f"{title} {desc}".lower()
                if terms and not any(t in hay for t in terms):
                    continue
                out.append(Candidate(
                    source="arena", id=str(b.get("id")), title=title or "(untitled)",
                    artist="", date="", license="see description",
                    credit=desc or f"via are.na/{slug}",
                    page_url=f"https://www.are.na/block/{b.get('id')}",
                    thumb_url=(img.get("display") or {}).get("url") or orig["url"],
                    full_url=orig["url"],
                    width=None, height=None))
            if len(blocks) < 100:
                break
            page += 1
    return out


def _plain(v):
    if isinstance(v, dict):
        return v.get("plain") or v.get("markdown") or ""
    return v or ""


# ----------------------------------------------------------------------- Met

def met(query, limit=15):
    """The Met's search ranks well on `q` alone and badly with filters added.

    Sending medium= / isPublicDomain= / hasImages= alongside the query returns
    a differently-ordered set — `q=kitchen` with filters leads with a Saint
    Jerome and portraits, without them it leads with "Kitchen Scene". So the
    query goes in clean and the public-domain test happens per object below.
    """
    s = _get(_qs("https://collectionapi.metmuseum.org/public/collection/v1/search",
                 q=query))
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

def aic(query, limit=25):
    d = _get(_qs("https://api.artic.edu/api/v1/artworks/search",
                 q=query, limit=limit,
                 fields="id,title,artist_title,date_display,is_public_domain,"
                        "image_id,thumbnail"))
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
    """Last resort. Commons search matches keywords, not objects — it will
    return a recording studio for 'Aeron'. Treat every result as unverified."""
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


CASCADE = [
    ("are.na", lambda q, ch: arena_channels(ch, q)),
    # AIC before the Met: one request, real relevance ranking, and it reports
    # dimensions so most candidates need no header probe.
    ("aic", lambda q, ch: aic(q)),
    ("met", lambda q, ch: met(q)),
    ("cleveland", lambda q, ch: cleveland(q)),
    ("wikimedia", lambda q, ch: wikimedia(q)),
]


def search(query, channels=(), want=40, only=None, verbose=True):
    """Run the cascade in RULES.md order, stopping once `want` is satisfied.

    `query` may be several comma-separated terms. Each is searched separately
    and the results merged — keyword APIs match a short concrete noun far
    better than one long metaphorical sentence.
    """
    terms = [t.strip() for t in query.split(",") if t.strip()] or [query]
    found, seen = [], set()
    for name, fn in CASCADE:
        if only and name not in only:
            continue
        try:
            got = []
            for t in terms:
                got += fn(t, list(channels))
        except Exception as e:
            if verbose:
                print(f"  {name:10s} failed: {e}")
            continue
        got = [c for c in got if c.key not in seen]
        fill_sizes(got)
        kept = [c for c in got if big_enough(c)]
        for c in kept:
            seen.add(c.key)
        if verbose:
            small = len(got) - len(kept)
            print(f"  {name:10s} {len(kept):3d} kept"
                  + (f", {small} under {MIN_PX}px" if small else ""))
        found += kept
        if len(found) >= want:
            break
    return found[:want]
