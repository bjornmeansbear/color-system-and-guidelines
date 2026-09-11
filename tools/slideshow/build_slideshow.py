#!/usr/bin/env python3
"""
Generate slideshow.html: a single self-contained, offline slideshow for the
an are.na archive. Mixes images from images/, links/ and (if present)
vitra/ with text slides from text/quotes.txt.

Run it from an archive directory, or point --root at one.

Design intent: projected on a gallery wall. Dark background, large light
type, letterboxed centered images, auto-advances on a timer, arrow keys
pause and step through manually, 'f' toggles fullscreen.

Re-run any time images/manifest.csv/quotes.txt change - it's a pure
generator, doesn't touch source data.

Usage:
    python3 scripts/build_slideshow.py [--out slideshow.html] [--seed 1]
                                        [--images-per-quote 5]
"""
import argparse
import csv
import hashlib
import html
import json
import random
import re
import base64
import struct
from pathlib import Path

# This script is a shared tool: fonts ship with it, content comes from --root.
TOOL_DIR = Path(__file__).resolve().parent


def load_quotes(path):
    text = path.read_text(encoding="utf-8")
    quotes = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        attribution = ""
        if lines[-1].strip().startswith("—"):
            attribution = lines[-1].strip().lstrip("—").strip()
            lines = lines[:-1]
        # Newlines are kept, not flattened: a few slides are deliberate lists
        # (reference clusters) where the line breaks are the whole point. The
        # template renders these with white-space: pre-line.
        quote = "\n".join(l.strip() for l in lines)
        quotes.append({"text": quote, "attribution": attribution})
    return quotes


def image_size(path):
    """(width, height) from the file header -- no Pillow/sips dependency.

    Returns None if the format isn't recognised; callers treat that as
    "unknown, keep it" rather than dropping the image.
    """
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", head[6:10])
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            f.seek(12)
            chunk = f.read(30)
            if chunk[:4] == b"VP8X":
                w = int.from_bytes(chunk[8:11], "little") + 1
                h = int.from_bytes(chunk[11:14], "little") + 1
                return w, h
            if chunk[:4] == b"VP8 ":
                return struct.unpack("<HH", chunk[14:18])[0] & 0x3FFF, \
                       struct.unpack("<HH", chunk[16:20])[0] & 0x3FFF
            if chunk[:4] == b"VP8L":
                b = chunk[9:14]
                n = int.from_bytes(b[:4], "little")
                return (n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1
            return None
        if head[:2] == b"\xff\xd8":  # JPEG: walk the segment chain to SOFn
            f.seek(2)
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                while b == b"\xff":
                    b = f.read(1)
                if not b:
                    return None
                marker = b[0]
                if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                    continue
                seg = f.read(2)
                if len(seg) < 2:
                    return None
                seglen = struct.unpack(">H", seg)[0]
                if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                              0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    data = f.read(5)
                    if len(data) < 5:
                        return None
                    h, w = struct.unpack(">HH", data[1:5])
                    return w, h
                f.seek(seglen - 2, 1)
    return None


def looks_like_garbage_title(title, check_length=True):
    """True for titles that are really filenames/CDN junk, not a chair's name.

    These get projected on a gallery wall, so anything that reads as machine
    output is worse than no caption at all.
    """
    if not title:
        return True
    if re.search(r"\.(jpe?g|png|gif|webp)(\?|$)", title, re.I):
        return True
    if re.search(r"_nc_(ht|cat|ohc)=", title):
        return True
    # CDN query strings, e.g. "...851?width=800&height=350"
    if re.search(r"[?&](width|height|w|h|fm|q|auto|fit|crop|ixlib)=", title, re.I):
        return True
    # bare UUIDs / long hex blobs, e.g. "9170d4cd-3945-4318-990b-b2722824f851"
    if re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", title, re.I):
        return True
    if re.search(r"\b[0-9a-f]{16,}\b", title, re.I):
        return True
    # HTTP/interstitial page titles are.na captured instead of a real name
    if re.fullmatch(r"\s*(4\d\d|5\d\d)?\s*(forbidden|not found|access denied|"
                    r"error|untitled|instagram|just a moment\.{0,3}|"
                    r"attention required!?.*|page not found)\s*",
                    title, re.I):
        return True
    if check_length and len(title) > 90:
        return True
    return False


def first_meaningful_line(text):
    """First real line, skipping the bare '.' separators used as line breaks."""
    for line in (text or "").splitlines():
        line = line.strip()
        if line and line.strip(".·-—_ ") != "":
            return line
    return ""


def clean_caption(text):
    """One caption line out of an are.na title or description field.

    Captions live on the block itself, in two places: people paste a whole
    multi-line caption into the *title* (name on the first line, then specs),
    and are.na keeps a *description* that often carries the designer. Neither
    needs any guessing about which block sits next to which.
    """
    t = first_meaningful_line(text)
    if not t:
        return ""
    if re.match(r"^(https?://|www\.)", t, re.I):
        return ""
    t = re.sub(r"^\s*(source\s*:|via\b)\s*", "", t, flags=re.I)
    t = t.lstrip("|").strip()
    # Stock-library tails: the photographer gets their own credit line, so the
    # caption should say what the picture is and stop.
    t = re.sub(r"\s*[-\u2013\u2014|]\s*(free\s+)?photo on unsplash\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*[-\u2013\u2014|]\s*unsplash\s*$", "", t, flags=re.I)
    t = t.strip(" -\u2013\u2014|")
    # Length is judged after taking the first line, so a long multi-line title
    # is trimmed to its name rather than thrown away whole.
    if not t or looks_like_garbage_title(t, check_length=False):
        return ""
    if len(t) > 90:
        m = re.match(r"^(.{30,88}?)[.,;:]\s", t)
        t = (m.group(1) if m else t[:88].rsplit(" ", 1)[0]) + "\u2026"
    return t


def block_caption(title, description):
    """Combine the two fields, preferring whichever actually says more."""
    t = clean_caption(title)
    d = clean_caption(description)
    if not t:
        return d
    if not d:
        return t
    if t.lower() in d.lower():
        return d
    if d.lower() in t.lower():
        return t
    return t + " \u2014 " + d


def vitra_caption(row):
    parts = [row["title"]]
    bits = []
    credit = row.get("designer") or row.get("producer")
    if credit:
        bits.append(credit)
    year = row.get("design_year") or row.get("production_year")
    if year:
        bits.append(year)
    if bits:
        parts.append(", ".join(bits))
    return " — ".join(p for p in parts if p)


def add_image(images, root, rel, caption, min_px, src=None, credit=""):
    """Append an image slide, carrying its real pixel size.

    Size travels with the slide so the page can cap how far a small image is
    allowed to be blown up -- object-fit:contain on a full-viewport box will
    happily scale a 150x150 thumbnail to ~930px, which projects as mush.
    Anything under min_px on its long edge is dropped outright.
    """
    # Measured from the local copy even when the page will point at a remote
    # URL -- same image either way, and it keeps the size filters working.
    size = image_size(root / rel)
    out = src or rel
    if size:
        w, h = size
        if max(w, h) < min_px:
            return
        entry = {"src": out, "caption": caption, "w": w, "h": h}
    else:
        entry = {"src": out, "caption": caption}
    if credit:
        entry["credit"] = credit
    images.append(entry)


UNSPLASH_ID = re.compile(r"unsplash\.com/photos/(?:.*-)?([A-Za-z0-9_-]{11})/?$")
UNSPLASH_BY = re.compile(r"[Pp]hoto by ([^\u2014|]+?) on Unsplash")


def unsplash_credits(manifest_rows):
    """Unsplash photo id -> photographer.

    The licence does not require attribution, but these are people's
    photographs and the show is public, so they get named. Older saves are
    Link blocks whose title are.na captured as "Photo by NAME on Unsplash";
    newer ones are Image blocks with only descriptive alt text. Both carry the
    photo id in the source URL, so the name travels from one to the other.
    """
    names = {}
    for r in manifest_rows:
        i = UNSPLASH_ID.search((r.get("source_url") or "").rstrip("/"))
        n = UNSPLASH_BY.search((r.get("title") or "") + " " + (r.get("description") or ""))
        if i and n:
            names[i.group(1)] = n.group(1).strip()
    return names


# Faces the quote type rotates through. Each new quote takes the next one, so
# the deck reads as a set of related cards rather than one voice. Order is the
# rotation order; a face is skipped silently if its file is missing.
QUOTE_FACES = [
    ("Basteleur", "Basteleur-Bold.woff2", 700),
    ("Space Grotesk", "SpaceGrotesk.woff2", 500),
    ("Cormorant Garamond", "CormorantGaramond.woff2", 600),
    ("Work Sans", "WorkSans.woff2", 500),
    ("Sligoil Micro", "Sligoil-Micro.woff2", 400),
    ("Libre Franklin", "LibreFranklin.woff2", 600),
]


def embedded_faces(root):
    """(@font-face css, [family names]) with the woff2 inlined as data URIs.

    Inlined rather than linked so a built file is one self-contained thing:
    it travels between repos as a single copy, and the gallery build runs off
    a local file where a network fetch would be a liability, not a convenience.
    """
    css, families = [], []
    for family, fname, weight in QUOTE_FACES:
        f = root / "fonts" / fname
        if not f.exists():
            continue
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        css.append(
            "@font-face{font-family:'%s';font-weight:%d;font-style:normal;"
            "font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');}"
            % (family, weight, b64))
        families.append(family)
    return "\n".join(css), families


def load_block_captions(root):
    """arena_block_id -> caption, for images saved off a museum collection page.

    These live in images/ like any other are.na image (so they hotlink), but
    their names come from the museum rather than from anything typed into
    are.na. Written by fetch_vitra_detail.py.
    """
    path = root / "vitra_captions.csv"
    if not path.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(path)):
        bits = []
        credit = r["designer"] or r["producer"]
        if credit:
            bits.append(credit)
        year = r["design_year"] or r["production_year"]
        if year:
            bits.append(year)
        out[r["arena_block_id"]] = " \u2014 ".join(
            [r["title"]] + ([", ".join(bits)] if bits else []))
    return out


def collect_images(root, manifest_rows, vitra_rows, min_px=300, include_links=False,
                   hotlink=False):
    vitra_dupe_seen = set()
    vitra_paths_seen = set()
    images = []

    # Hotlinked builds drop the museum photographs. Not a licensing judgement --
    # collection.design-museum.de returns 403 to any foreign Referer (measured
    # 2026-08-26, 6/6), so the images simply would not load from another domain.
    # are.na cannot stand in either: its capture of those Link blocks is a
    # screenshot of the whole collection page, not the object.
    if hotlink:
        vitra_rows = []

    # Vitra: full-res, deduped by content hash (site reuses generic
    # storage-shelf shots as secondary images across many objects)
    # NB: status is "downloaded" on a first pull but "skipped (exists)" on a
    # re-run, so presence on disk -- not the status string -- is the test.
    for row in vitra_rows:
        if not row["local_images"]:
            continue
        caption = vitra_caption(row)
        for rel in [p.strip() for p in row["local_images"].split(";") if p.strip()]:
            fpath = root / rel
            if not fpath.exists():
                continue
            h = hashlib.md5(fpath.read_bytes()).hexdigest()
            if h in vitra_dupe_seen:
                continue
            vitra_dupe_seen.add(h)
            vitra_paths_seen.add(rel)
            add_image(images, root, rel, caption, min_px)

    vitra_block_ids = {row["arena_block_id"] for row in vitra_rows if row["arena_block_id"]}
    block_captions = load_block_captions(root)
    credits = unsplash_credits(manifest_rows)

    for row in manifest_rows:
        if not row["local_path"] or not (root / row["local_path"]).exists():
            continue
        # links/ holds are.na's captured og:image for each Link block. Those are
        # social-share previews, not photographs of the object: low-res, often a
        # site's generic share card, and the source of most of the junk titles
        # ("403 Forbidden", "Instagram", bare UUIDs). Images saved directly to
        # the channel and the museum's own full-res shots are the real archive.
        if not include_links and row["local_path"].startswith("links/"):
            continue
        # Skip design-museum.de link previews - superseded by vitra/ full-res
        if row["id"] in vitra_block_ids and row["domain"] == "collection.design-museum.de":
            continue
        title = row["title"]
        # A museum name beats whatever are.na recorded as the title.
        caption = block_captions.get(row["id"]) or block_caption(title, row.get("description", ""))
        # Hotlinked builds take are.na's resized variant, not the original:
        # same picture, a fraction of the bytes over the wire.
        src = (row.get("image_url_large") or row.get("image_url", "")) \
            if hotlink else row["local_path"]
        if hotlink and not src:
            continue
        pid = UNSPLASH_ID.search((row.get("source_url") or "").rstrip("/"))
        who = credits.get(pid.group(1)) if pid else None
        add_image(images, root, row["local_path"], caption, min_px, src=src,
                  credit=f"Photo: {who} / Unsplash" if who else "")

    return images


def interleave(images, quotes, images_per_quote, seed):
    """One pass of the deck, with every quote guaranteed a slot.

    Quote slots come from the image count, so a short image set silently
    starves the tail of the quote list -- and because the deck replays the
    same array on loop, a starved quote never appears at all rather than
    appearing late. Repeat images until there are enough slots. Never trim
    the other way: a long image set keeps all its images and simply cycles
    the quotes more than once.
    """
    rng = random.Random(seed)

    needed = max(0, len(quotes) - 1) * images_per_quote
    shuffled = []
    while len(shuffled) < max(len(images), needed):
        chunk = images[:]
        rng.shuffle(chunk)
        # don't let a repeat land immediately after itself across the seam
        if shuffled and len(chunk) > 1 and chunk[0]["src"] == shuffled[-1]["src"]:
            chunk.append(chunk.pop(0))
        shuffled.extend(chunk)
    shuffled = shuffled[:max(len(images), needed)]

    slides = []
    if quotes:
        slides.append({"type": "text", **quotes[0]})
    remaining_quotes = quotes[1:] if quotes else []
    qi = 0
    for i, img in enumerate(shuffled, 1):
        slides.append({"type": "image", **img})
        if remaining_quotes and i % images_per_quote == 0:
            slides.append({"type": "text", **remaining_quotes[qi % len(remaining_quotes)]})
            qi += 1
    return slides


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
__FONT_FACES__
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  /* Palette from ~/Code/color-system-and-guidelines: dark brown ground
     (inverted from the kit's light "warm gray bg, dark brown ink" trope),
     pink as the one accent. Contrast-checked against --brown-9 (8,5,4):
     text 18.8:1, caption 10.5:1, attribution/pink 8.7:1, hint 7.1:1 - all AA. */
  html, body {
    margin: 0; padding: 0; width: 100%; height: 100%;
    background: rgb(8,5,4); color: rgb(251,245,242);
    font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
    overflow: hidden;
  }
  #stage {
    position: relative; width: 100vw; height: 100vh;
    display: flex; align-items: center; justify-content: center;
  }
  .slide {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    opacity: 0; transition: opacity 900ms ease;
    pointer-events: none;
  }
  .slide.active { opacity: 1; pointer-events: auto; }

  /* As big as the screen allows, whole chair always visible.
     object-fit:contain does the letterboxing, but contain only fills the box
     it is given -- the box has to be pinned to the viewport with width/height,
     not max-width/max-height, or a small image gets a small box and floats.
     A per-image max-width/max-height is set inline from its real pixel size
     (see MAX_UPSCALE) so low-res files stop short of looking mushy. */
  .slide-image img {
    display: block;
    width: 100vw; height: 100vh;
    object-fit: contain;
  }
  /* Caption is an opaque block anchored in the bottom-left corner, not type
     laid over the photo: many of these are museum shots on white, where light
     type would fail contrast. Opaque ground means the 10.5:1 ratio holds no
     matter what the image behind it is doing. Corner-anchored and narrow so it
     covers only a patch that is nearly always empty in a product shot, which
     lets the image itself keep the whole 100vh. */
  .caption {
    position: absolute; left: 0; bottom: 0;
    max-width: 46vw;
    padding: 1.5vh 2.2vw;
    text-align: left;
    font-size: clamp(14px, 1.6vw, 22px);
    line-height: 1.35;
    letter-spacing: 0.02em;
    color: rgb(192,185,181);
    background: rgb(8,5,4);
  }
  /* Photo credit sits under the object name, one step dimmer. brown-4 is the
     dimmest rung that still clears AAA on this ground (7.06:1). */
  .caption .credit {
    display: block; margin-top: 0.35em;
    font-size: 0.8em; color: rgb(158,151,147);
  }

  .slide-text {
    flex-direction: column;
  }
  .quote, .attribution {
    max-width: 74vw;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    padding: 0 4vw;
  }
  .quote {
    white-space: pre-line;
    overflow-wrap: break-word;
    font-size: clamp(28px, 4.6vw, 68px);
    line-height: 1.25;
    font-weight: 500;
    letter-spacing: -0.01em;
  }
  .attribution {
    margin-top: 2.2rem;
    font-size: clamp(16px, 1.8vw, 26px);
    color: rgb(255,129,169); /* pink-3: the one accent */
  }

  /* Bottom-RIGHT: the caption block owns the bottom-left corner, and this
     stack is only on screen for the first few seconds anyway. The source
     credit rides with the keyboard hint so both appear and fade together. */
  #chrome {
    position: fixed; right: 2.2vw; bottom: 2.2vh;
    display: flex; flex-direction: column; align-items: flex-end; gap: 0.5vh;
    opacity: 1; transition: opacity 1.5s ease;
  }
  #chrome.hidden { opacity: 0; }
  #home, #credit, #hint {
    font-size: 13px; letter-spacing: 0.04em;
    background: rgb(8,5,4); padding: 0.6vh 1vw;
  }
  #home, #credit { color: rgb(192,185,181); }        /* 10.5:1 on the ground */
  #hint { color: rgb(158,151,147); }          /* 7.1:1 on the ground */
  #home a, #credit a {
    color: rgb(255,129,169);                  /* pink-3, the one accent - 8.7:1 */
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  /* Keyboard focus must stay visible even while the chrome is faded out. */
  #home a:focus-visible, #credit a:focus-visible {
    outline: 2px solid rgb(255,129,169);
    outline-offset: 3px;
  }
  #chrome:focus-within { opacity: 1; }
  
  #paused-badge {
    position: fixed; top: 2.5vh; right: 2.5vw;
    font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase;
    color: rgb(255,129,169); border: 1px solid rgb(255,129,169); padding: 6px 12px;
    border-radius: 999px; opacity: 0; transition: opacity 300ms ease;
  }
  #paused-badge.visible { opacity: 1; }
</style>
</head>
<body>
<div id="stage"></div>
<div id="paused-badge">Paused</div>
<div id="chrome">
__HOME_LINK__  <div id="credit">Source archive: <a href="__CHANNEL_URL__">__CHANNEL_LABEL__</a></div>
  <div id="hint">← → step &nbsp;·&nbsp; space play/pause &nbsp;·&nbsp; f fullscreen</div>
</div>

<script>
const SLIDES = __SLIDES_JSON__;
const IMAGE_SECONDS = __IMAGE_SECONDS__;
// Quotes run a wide spread of lengths, so one fixed dwell either rushes the
// long passages or strands the short ones: a base beat to register the slide,
// plus reading time, clamped at both ends. The rate assumes projected glancing
// rather than sit-down reading -- at a true reading pace the long quotes sit
// on screen long enough to feel stuck.
const TEXT_BASE_SECONDS = __TEXT_BASE__;
const TEXT_CHARS_PER_SECOND = __TEXT_CPS__;
const TEXT_MIN_SECONDS = __TEXT_MIN__;
const TEXT_MAX_SECONDS = __TEXT_MAX__;

// Slides are torn down outside a window around the current one. Left alone,
// every image ever shown stays decoded in memory -- for this set that is
// ~2.6GB (a single 4000x4000 source is 64MB decoded), which an unattended
// gallery display running for hours will not survive.
const KEEP_RADIUS = 2;
const PRELOAD_AHEAD = 3;

const stage = document.getElementById('stage');
const pausedBadge = document.getElementById('paused-badge');
const chrome_ = document.getElementById('chrome');

let current = 0;
let userPaused = false;
let timer = null;
const MAX_UPSCALE = __MAX_UPSCALE__;
const QUOTE_FONTS = __QUOTE_FONTS__;
const BASE_STACK = '-apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif';
const elements = new Array(SLIDES.length).fill(null);
let textCount = 0;
const broken = new Array(SLIDES.length).fill(false);

function buildSlide(i) {
  const s = SLIDES[i];
  const el = document.createElement('div');
  el.className = 'slide';
  if (s.type === 'image') {
    el.classList.add('slide-image');
    const img = document.createElement('img');
    // A slide whose file is missing or undecodable would otherwise sit on a
    // blank ground for its full dwell; mark it and move on instead.
    img.onerror = () => {
      broken[i] = true;
      if (i === current) advance(1);
    };
    img.src = s.src;
    img.loading = 'eager';
    // Cap the blow-up for low-res files; images of unknown size are left alone.
    if (s.w && s.h) {
      img.style.maxWidth = (s.w * MAX_UPSCALE) + 'px';
      img.style.maxHeight = (s.h * MAX_UPSCALE) + 'px';
    }
    el.appendChild(img);
    if (s.caption) {
      const cap = document.createElement('div');
      cap.className = 'caption';
      cap.textContent = s.caption;
      if (s.credit) {
        const cr = document.createElement('span');
        cr.className = 'credit';
        cr.textContent = s.credit;
        cap.appendChild(cr);
      }
      el.appendChild(cap);
    }
  } else {
    el.classList.add('slide-text');
    const q = document.createElement('div');
    q.className = 'quote';
    q.textContent = s.text;
    // Each quote takes the next face in the rotation, so consecutive text
    // slides never share one. Tilt and layout stay put; only the type changes.
    if (QUOTE_FONTS.length) {
      q.style.fontFamily = "'" + QUOTE_FONTS[textCount++ % QUOTE_FONTS.length] +
                           "', " + BASE_STACK;
    }
    el.appendChild(q);
    if (s.attribution) {
      const a = document.createElement('div');
      a.className = 'attribution';
      a.textContent = '— ' + s.attribution;
      el.appendChild(a);
    }
  }
  stage.appendChild(el);
  elements[i] = el;
  return el;
}

function destroySlide(i) {
  const el = elements[i];
  if (!el) return;
  const img = el.querySelector('img');
  if (img) {
    img.onerror = null;
    img.removeAttribute('src');  // release the decoded bitmap
  }
  el.remove();
  elements[i] = null;
}

// Distance between two slides going the short way round the loop, so the
// wrap from the last slide back to the first does not tear down its neighbours.
function ringDistance(a, b) {
  const d = Math.abs(a - b);
  return Math.min(d, SLIDES.length - d);
}

function prune() {
  for (let i = 0; i < SLIDES.length; i++) {
    if (elements[i] && ringDistance(i, current) > KEEP_RADIUS) destroySlide(i);
  }
}

// Warm the next few images in the browser cache without putting them in the
// DOM, so a slide is decoded and ready before it fades in.
const warmed = new Set();
function preloadAhead() {
  for (let n = 1; n <= PRELOAD_AHEAD; n++) {
    const i = (current + n) % SLIDES.length;
    if (SLIDES[i].type !== 'image' || warmed.has(i)) continue;
    warmed.add(i);
    new Image().src = SLIDES[i].src;
  }
}

// Next non-broken slide in the given direction; stays put if every slide is
// broken rather than spinning through the whole deck forever.
function step(dir) {
  let i = current;
  for (let n = 0; n < SLIDES.length; n++) {
    i = (i + dir + SLIDES.length) % SLIDES.length;
    if (!broken[i]) return i;
  }
  return current;
}

function advance(dir) { show(step(dir)); }

function show(i) {
  current = (i + SLIDES.length) % SLIDES.length;
  if (!elements[current]) buildSlide(current);
  const nxt = (current + 1) % SLIDES.length;
  if (!elements[nxt]) buildSlide(nxt);
  elements.forEach((el, idx) => { if (el) el.classList.toggle('active', idx === current); });
  prune();
  preloadAhead();
  scheduleNext();
}

function slideSeconds(i) {
  const s = SLIDES[i];
  if (s.type !== 'text') return IMAGE_SECONDS;
  const chars = (s.text || '').length + (s.attribution || '').length;
  const secs = TEXT_BASE_SECONDS + chars / TEXT_CHARS_PER_SECOND;
  return Math.max(TEXT_MIN_SECONDS, Math.min(TEXT_MAX_SECONDS, secs));
}

function scheduleNext() {
  clearTimeout(timer);
  timer = null;
  if (userPaused || document.hidden) return;
  timer = setTimeout(() => advance(1), slideSeconds(current) * 1000);
}

function setPaused(v) {
  userPaused = v;
  applyPause();
}

// A backgrounded tab keeps its timers running, so the show would jump ahead
// while nobody is watching. Hidden pauses without lighting the paused badge --
// that badge is feedback for a deliberate keypress.
function applyPause() {
  pausedBadge.classList.toggle('visible', userPaused);
  clearTimeout(timer);
  timer = null;
  if (!userPaused && !document.hidden) scheduleNext();
}
document.addEventListener('visibilitychange', applyPause);

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') { setPaused(true); advance(1); }
  else if (e.key === 'ArrowLeft') { setPaused(true); advance(-1); }
  else if (e.key === ' ') { e.preventDefault(); setPaused(!userPaused); }
  else if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }
});

let chromeTimer = setTimeout(() => chrome_.classList.add('hidden'), 6000);
function wakeChrome() {
  chrome_.classList.remove('hidden');
  clearTimeout(chromeTimer);
  chromeTimer = setTimeout(() => chrome_.classList.add('hidden'), 4000);
}
document.addEventListener('mousemove', wakeChrome);
// Tabbing to the credit link must bring the chrome back, or the link is
// focusable but invisible.
document.addEventListener('focusin', wakeChrome);

show(0);
</script>
</body>
</html>
"""



AMBIENT_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
__FONT_FACES__
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0; width: 100%; height: 100%;
    background: rgb(8,5,4); color: rgb(251,245,242);
    font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
    overflow: hidden;
  }
  /* The stage centres its one in-flow child, the text panel. The image
     layers and the caption are absolutely positioned, so they sit outside
     this centring and keep their own placement. */
  #stage {
    position: relative; width: 100vw; height: 100vh;
    display: flex; align-items: center; justify-content: center;
  }

  /* Two stacked layers so the next chair is decoded before it is shown --
     a hard cut to a half-decoded image reads as a flicker. No transition:
     the chairs switch, they do not fade. */
  .layer {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    visibility: hidden;
  }
  .layer.on { visibility: visible; }
  .layer img { display: block; width: 100vw; height: 100vh; object-fit: contain; }

  #caption {
    position: absolute; left: 0; bottom: 0; z-index: 3;
    max-width: 46vw; padding: 1.5vh 2.2vw;
    font-size: clamp(14px, 1.6vw, 22px); line-height: 1.35;
    letter-spacing: 0.02em;
    color: rgb(192,185,181); background: rgb(8,5,4);
  }
  #caption:empty { display: none; }
  #caption .credit {
    display: block; margin-top: 0.35em;
    font-size: 0.8em; color: rgb(158,151,147);
  }
  /* The panel owns the frame while it is up; the caption returns after. */
  #stage.texting #caption { opacity: 0; }
  #caption { transition: opacity 400ms ease; }

  /* The text panel rides over the running chairs on its own opaque ground,
     so contrast holds whatever is behind it. Size comes from the length of
     the quote: a short line covers a corner, a long passage covers most of
     the screen. */
  /* A centred card, in flow, shrink-wrapped to its text -- so how much of the
     frame it covers comes from the length of the quote rather than from a
     fixed footprint. */
  #overlay {
    position: relative; z-index: 4;
    /* A fresh tilt on every new quote, the way oblique tosses a new strategy
       card onto the table -- you register that it changed before you read it. */
    transform: rotate(var(--card-rotation, 0deg));
    background: rgb(8,5,4);
    padding: 4vh 4vw;
    opacity: 0; transition: opacity 700ms ease;
    display: flex; flex-direction: column; justify-content: center;
    text-align: center;
    height: fit-content;
    pointer-events: none;
  }
  #overlay.on { opacity: 1; }
  #overlay .quote {
    white-space: pre-line; margin: 0;
    /* Never let an unbroken run (a URL, a long compound) push past the card. */
    overflow-wrap: break-word;
    line-height: 1.22; letter-spacing: -0.01em;
  }
  #overlay .attribution {
    margin: 1.6rem 0 0; font-size: clamp(14px, 1.4vw, 20px);
    color: rgb(255,129,169);
  }
  /* Three footprints, picked by quote length. The card is centred and in
     flow, so width and type size are what vary -- a short line takes a small
     card, a long passage takes most of the frame. */
  .sz-s { max-width: 44vw; }
  .sz-s .quote { font-size: clamp(20px, 2.4vw, 38px); }
  .sz-m { max-width: 68vw; }
  .sz-m .quote { font-size: clamp(22px, 3.0vw, 46px); }
  .sz-l { max-width: 88vw; }
  .sz-l .quote { font-size: clamp(22px, 3.2vw, 52px); }

  #chrome {
    position: fixed; right: 2.2vw; bottom: 2.2vh; z-index: 5;
    display: flex; flex-direction: column; align-items: flex-end; gap: 0.5vh;
    opacity: 1; transition: opacity 1.5s ease;
  }
  #chrome.hidden { opacity: 0; }
  #chrome:focus-within { opacity: 1; }
  #home, #credit, #hint {
    font-size: 13px; letter-spacing: 0.04em;
    background: rgb(8,5,4); padding: 0.6vh 1vw;
  }
  #home, #credit { color: rgb(192,185,181); }
  #hint { color: rgb(158,151,147); }
  #home a, #credit a { color: rgb(255,129,169); text-decoration: underline; text-underline-offset: 2px; }
  #home a:focus-visible, #credit a:focus-visible { outline: 2px solid rgb(255,129,169); outline-offset: 3px; }
  #paused-badge {
    position: fixed; top: 2.2vh; right: 2.2vw; z-index: 5;
    font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase;
    color: rgb(158,151,147); background: rgb(8,5,4); padding: 0.6vh 1vw;
    opacity: 0; transition: opacity 300ms ease;
  }
  #paused-badge.visible { opacity: 1; }

  /* A 1.2s hard cut is a lot of motion. Anyone who has asked their system to
     reduce it gets a slow, calm version instead of an opt-out. */
  @media (prefers-reduced-motion: reduce) {
    #overlay { transition: none; }
  }
</style>
</head>
<body>
<div id="stage">
  <div class="layer" id="layer0"><img alt=""></div>
  <div class="layer" id="layer1"><img alt=""></div>
  <div id="caption"></div>
  <div id="overlay" aria-live="polite"></div>
</div>
<div id="paused-badge">Paused</div>
<div id="chrome">
__HOME_LINK__  <div id="credit">Source archive: <a href="__CHANNEL_URL__">__CHANNEL_LABEL__</a></div>
  <div id="hint">space play/pause &nbsp;·&nbsp; f fullscreen</div>
</div>
<script>
const IMAGES = __IMAGES_JSON__;
const TEXTS  = __TEXTS_JSON__;
const MAX_UPSCALE = __MAX_UPSCALE__;
const QUOTE_FONTS = __QUOTE_FONTS__;
const BASE_STACK = '-apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif';

const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// Chairs switch this fast; a text panel arrives after this many chairs.
const IMAGE_MS = reduce ? 5000 : __IMAGE_MS__;
const CHAIRS_BETWEEN_TEXT = __CHAIRS_BETWEEN_TEXT__;
const MAX_TILT = __MAX_TILT__;

const layers = [document.getElementById('layer0'), document.getElementById('layer1')];
const capEl = document.getElementById('caption');
const overlay = document.getElementById('overlay');
const badge = document.getElementById('paused-badge');
const chrome_ = document.getElementById('chrome');

const stageEl = document.getElementById('stage');
let li = 0, ii = 0, ti = 0, sinceText = 0, paused = false;
let imgTimer = null, textTimer = null;
// When the current panel is due down, and how long was left on it when the
// show was suspended. Both timers must be re-armed together on resume: the
// panel blocks new quotes while it is up, so a hide timer that is cleared and
// never replaced stalls the quotes permanently while the chairs keep cycling.
let textHideAt = 0, textRemaining = 0;

function applySize(el, s) {
  if (s.w && s.h) {
    el.style.maxWidth = (s.w * MAX_UPSCALE) + 'px';
    el.style.maxHeight = (s.h * MAX_UPSCALE) + 'px';
  } else {
    el.style.maxWidth = el.style.maxHeight = '';
  }
}

// Warm the next few so a hard cut lands on a decoded image.
function warm(from) {
  for (let n = 1; n <= 6; n++) new Image().src = IMAGES[(from + n) % IMAGES.length].src;
}

function showImage(i) {
  const s = IMAGES[i];
  const back = layers[1 - li];
  const img = back.querySelector('img');
  const swap = () => {
    layers[li].classList.remove('on');
    back.classList.add('on');
    li = 1 - li;
    capEl.textContent = s.caption || '';
    if (s.credit) {
      const cr = document.createElement('span');
      cr.className = 'credit';
      cr.textContent = s.credit;
      capEl.appendChild(cr);
    }
  };
  img.onload = swap;
  img.onerror = () => { step(); };   // skip a source that will not load
  applySize(img, s);
  img.src = s.src;
  warm(i);
}

function step() {
  ii = (ii + 1) % IMAGES.length;
  showImage(ii);
  // Only count chairs shown with nothing over them. Counting during a panel
  // spends the gap while the text is still up, so the next panel fires the
  // moment the last one hides and the chairs never get the screen to
  // themselves -- which also means the caption never becomes visible.
  if (overlay.classList.contains('on')) {
    // Safety net: if a panel has outlived its hide time by a wide margin,
    // something dropped its timer. Take it down rather than wedge the show.
    if (textHideAt && Date.now() > textHideAt + 5000) hidePanel();
    return;
  }
  sinceText++;
  if (sinceText >= CHAIRS_BETWEEN_TEXT) showText();
}

function textSeconds(t) {
  const chars = (t.text || '').length + (t.attribution || '').length;
  return Math.max(__TEXT_MIN__, Math.min(__TEXT_MAX__,
                  __TEXT_BASE__ + chars / __TEXT_CPS__));
}

function showText() {
  if (!TEXTS.length) return;
  const t = TEXTS[ti % TEXTS.length];
  const n = (t.text || '').length;
  const size = n < 60 ? 'sz-s' : n < 140 ? 'sz-m' : 'sz-l';
  overlay.className = size;
  // -7deg to +7deg, same range oblique uses.
  overlay.style.setProperty('--card-rotation',
    (Math.random() * 2 * MAX_TILT - MAX_TILT).toFixed(2) + 'deg');
  overlay.innerHTML = '';
  const q = document.createElement('p');
  q.className = 'quote';
  q.textContent = t.text;
  if (QUOTE_FONTS.length) {
    q.style.fontFamily = "'" + QUOTE_FONTS[ti % QUOTE_FONTS.length] + "', " + BASE_STACK;
  }
  overlay.appendChild(q);
  if (t.attribution) {
    const a = document.createElement('p');
    a.className = 'attribution';
    a.textContent = '\u2014 ' + t.attribution;
    overlay.appendChild(a);
  }
  requestAnimationFrame(() => {
    overlay.classList.add('on');
    stageEl.classList.add('texting');
  });
  ti++; sinceText = 0;
  const ms = textSeconds(t) * 1000;
  textHideAt = Date.now() + ms;
  armHide(ms);
}

function hidePanel() {
  overlay.classList.remove('on');
  stageEl.classList.remove('texting');
  textHideAt = 0;
}

function armHide(ms) {
  clearTimeout(textTimer);
  textTimer = setTimeout(hidePanel, Math.max(0, ms));
}

// Freeze both tracks together, keeping whatever was left on the panel.
function suspend() {
  clearInterval(imgTimer); imgTimer = null;
  if (textHideAt) textRemaining = Math.max(0, textHideAt - Date.now());
  clearTimeout(textTimer); textTimer = null;
}

function resume() {
  run();
  if (textHideAt) {
    textHideAt = Date.now() + textRemaining;
    armHide(textRemaining);
  }
}

function run() {
  clearInterval(imgTimer);
  if (paused) return;
  imgTimer = setInterval(step, IMAGE_MS);
}

function setPaused(v) {
  paused = v;
  badge.classList.toggle('visible', paused);
  if (paused) suspend(); else resume();
}

document.addEventListener('keydown', (e) => {
  if (e.key === ' ') { e.preventDefault(); setPaused(!paused); }
  else if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) suspend();
  else if (!paused) resume();
});

let chromeTimer = setTimeout(() => chrome_.classList.add('hidden'), 6000);
function wakeChrome() {
  chrome_.classList.remove('hidden');
  clearTimeout(chromeTimer);
  chromeTimer = setTimeout(() => chrome_.classList.add('hidden'), 4000);
}
document.addEventListener('mousemove', wakeChrome);
document.addEventListener('focusin', wakeChrome);

showImage(0);
run();
</script>
</body>
</html>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None,
                    help="archive directory holding manifest.csv, text/quotes.txt "
                         "and the image folders (default: the current directory). "
                         "Fonts ship with this script and are read from beside it.")
    ap.add_argument("--title", default="chair-ness",
                    help="<title> of the built page")
    ap.add_argument("--channel-label", default="are.na/kristian-bjornard/chair-ness",
                    help="text of the source-archive credit link")
    ap.add_argument("--out", default=None,
                    help="default: slideshow.html, or slideshow-web.html with --hotlink")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--images-per-quote", type=int, default=5)
    ap.add_argument("--min-px", type=int, default=300,
                    help="drop images whose long edge is under this (default 300)")
    ap.add_argument("--max-upscale", type=float, default=2.5,
                    help="how far a small image may be blown up (default 2.5x)")
    ap.add_argument("--home-url", default="",
                    help="if set, a link back to the page this piece belongs to "
                         "(e.g. the case study). Omitted by default so the "
                         "gallery build carries no stray link.")
    ap.add_argument("--home-label", default="Chair-ness",
                    help="text for --home-url (default: Chair-ness)")
    ap.add_argument("--channel-url",
                    default="https://www.are.na/kristian-bjornard/chair-ness",
                    help="source archive credited in the corner")
    ap.add_argument("--ambient", action="store_true",
                    help="two-layer mode: chairs hard-cut fast underneath, text "
                         "panels fade in over them. Writes slideshow-ambient.html.")
    ap.add_argument("--image-ms", type=int, default=600,
                    help="ambient: milliseconds per chair (default 600)")
    ap.add_argument("--image-seconds", type=float, default=5.0,
                    help="deck: seconds each chair holds (default 5)")
    ap.add_argument("--text-base-seconds", type=float, default=3.5,
                    help="beat before reading time starts (default 3.5)")
    ap.add_argument("--text-chars-per-second", type=float, default=18.0,
                    help="assumed glancing rate (default 18)")
    ap.add_argument("--text-min-seconds", type=float, default=6.0)
    ap.add_argument("--text-max-seconds", type=float, default=16.0,
                    help="hard ceiling on a single quote (default 16)")
    ap.add_argument("--no-embed-fonts", action="store_true",
                    help="skip the embedded OFL faces and use the system stack")
    ap.add_argument("--max-tilt", type=float, default=7.0,
                    help="ambient: degrees the quote card may tilt either way "
                         "on each new quote (default 7, matching oblique)")
    ap.add_argument("--chairs-between-text", type=int, default=7,
                    help="ambient: chairs shown between text panels (default 7)")
    ap.add_argument("--hotlink", action="store_true",
                    help="point at the are.na-hosted originals instead of local "
                         "files, and write a separate slideshow-web.html. Drops "
                         "the Vitra photos - that CDN refuses foreign referers.")
    ap.add_argument("--include-links", action="store_true",
                    help="also use links/ og:image previews (off: they are "
                         "low-res social-share cards, not object photos)")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path.cwd()

    manifest_rows = list(csv.DictReader(open(root / "manifest.csv")))
    # vitra.csv is chair-ness-specific: museum object metadata. Absent for any
    # other archive, which just means there are no museum captions to prefer.
    vitra_path = root / "vitra.csv"
    vitra_rows = list(csv.DictReader(open(vitra_path))) if vitra_path.exists() else []
    quotes = load_quotes(root / "text" / "quotes.txt")

    if args.out is None:
        if args.ambient:
            args.out = "slideshow-ambient-web.html" if args.hotlink else "slideshow-ambient.html"
        else:
            args.out = "slideshow-web.html" if args.hotlink else "slideshow.html"

    images = collect_images(root, manifest_rows, vitra_rows, args.min_px,
                            args.include_links, args.hotlink)
    print(f"{len(images)} images, {len(quotes)} quotes")

    out_path = root / args.out
    channel = html.escape(args.channel_url, quote=True)
    face_css, families = embedded_faces(TOOL_DIR)
    timing = {"__TITLE__": html.escape(args.title),
              "__CHANNEL_LABEL__": html.escape(args.channel_label),
              "__IMAGE_SECONDS__": repr(args.image_seconds),
              "__TEXT_BASE__": repr(args.text_base_seconds),
              "__TEXT_CPS__": repr(args.text_chars_per_second),
              "__TEXT_MIN__": repr(args.text_min_seconds),
              "__TEXT_MAX__": repr(args.text_max_seconds)}
    if args.no_embed_fonts:
        face_css, families = "", []
    if families:
        print(f"type rotates through {len(families)}: {', '.join(families)} "
              f"({len(face_css)/1024:.0f} KB embedded)")
    home = ""
    if args.home_url:
        home = ('  <div id="home"><a href="%s">\u2190 %s</a></div>\n'
                % (html.escape(args.home_url, quote=True),
                   html.escape(args.home_label)))

    if args.ambient:
        # Two independent tracks rather than one interleaved deck: the chairs
        # run continuously underneath and the quotes surface over the top.
        rng = random.Random(args.seed)
        shuffled = images[:]
        rng.shuffle(shuffled)
        print(f"{len(shuffled)} chairs on a {args.image_ms}ms cut, "
              f"a quote every {args.chairs_between_text}")
        html_out = (AMBIENT_TEMPLATE
                    .replace("__IMAGES_JSON__", json.dumps(shuffled, ensure_ascii=False))
                    .replace("__TEXTS_JSON__", json.dumps(quotes, ensure_ascii=False))
                    .replace("__MAX_UPSCALE__", repr(args.max_upscale))
                    .replace("__IMAGE_MS__", str(args.image_ms))
                    .replace("__CHAIRS_BETWEEN_TEXT__", str(args.chairs_between_text))
                    .replace("__MAX_TILT__", repr(args.max_tilt))
                    .replace("__CHANNEL_URL__", channel)
                    .replace("__HOME_LINK__", home)
                            .replace("__FONT_FACES__", face_css)
                            .replace("__QUOTE_FONTS__", json.dumps(families)))
    else:
        slides = interleave(images, quotes, args.images_per_quote, args.seed)
        print(f"{len(slides)} total slides")
        html_out = (TEMPLATE.replace("__SLIDES_JSON__", json.dumps(slides, ensure_ascii=False))
                            .replace("__MAX_UPSCALE__", repr(args.max_upscale))
                            .replace("__CHANNEL_URL__", channel)
                            .replace("__HOME_LINK__", home)
                    .replace("__FONT_FACES__", face_css)
                    .replace("__QUOTE_FONTS__", json.dumps(families)))

    for k, v in timing.items():
        html_out = html_out.replace(k, v)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
