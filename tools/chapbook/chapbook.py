#!/usr/bin/env python3
"""
chapbook — poems as plain text -> a typeset book PDF, a printer's booklet,
and a spread preview in the browser.

    chapbook new ~/Code/my-book --channel <are.na-slug>
    chapbook fetch            # pull are.na text blocks into poems/
    chapbook build            # build/<slug>.pdf, -booklet.pdf, preview.html
    chapbook build --snap "first proof"
    chapbook watch            # rebuild on save, preview reloads itself
    chapbook specimen Gentium Spectral "Libre Caslon Text"

Run from inside a book folder, or pass --root. The design reasoning lives
in RULES.md, "Chapbooks"; README.md here is how to run it.

Runs on the Python inside WeasyPrint's pipx venv (the `chapbook` wrapper
next to this file finds it), which also carries fontTools and pypdf.
"""
import argparse
import datetime
import functools
import html
import http.server
import json
import re
import shutil
import subprocess
import sys
import threading
import time
import tomllib
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
API = "https://api.are.na/v3"
USER_AGENT = "arena-archive-script/1.0 (personal are.na export)"

DEFAULTS = {
    "title": "Untitled",
    "author": "",
    "slug": "",
    "arena": "",
    "page": {
        "width": "5.5in", "height": "8.5in",
        "top": "0.75in", "bottom": "0.875in",
        "inside": "0.75in", "outside": "0.625in",
    },
    "type": {
        "text": "Gentium", "display": "",
        "size": "10pt", "leading": "15pt",
        "fonts_dir": "~/Code/libreFontLibrary/Families",
    },
    "book": {
        "contents": True,
        "colophon": "",
        "smart_quotes": True,
        "ink": "#000",
    },
}

SPECIMEN_FACES = [
    "Gentium", "Spectral", "Libre Caslon Text", "Source Serif 4",
    "Cormorant Garamond", "Charis SIL", "Inria Serif", "Libre Baskerville",
]


def die(msg):
    sys.exit(f"chapbook: {msg}")


# ---------------------------------------------------------------- config

def load_config(root):
    path = root / "book.toml"
    if not path.is_file():
        die(f"no book.toml in {root} — run from a book folder, pass --root, "
            "or start one with `chapbook new <dir>`")
    user = tomllib.loads(path.read_text())
    cfg = {}
    for key, default in DEFAULTS.items():
        if isinstance(default, dict):
            cfg[key] = {**default, **user.get(key, {})}
        else:
            cfg[key] = user.get(key, default)
    cfg["slug"] = cfg["slug"] or slugify(cfg["title"])
    cfg["type"]["display"] = cfg["type"]["display"] or cfg["type"]["text"]
    return cfg


def to_pt(value):
    m = re.fullmatch(r"\s*([0-9.]+)\s*(in|pt|mm|cm|pc)\s*", str(value))
    if not m:
        die(f"can't read the length {value!r} — use in, pt, mm, cm or pc")
    return float(m.group(1)) * {"in": 72, "pt": 1, "mm": 72 / 25.4,
                                "cm": 72 / 2.54, "pc": 12}[m.group(2)]


def slugify(text, maxlen=50):
    text = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return text[:maxlen].strip("-") or "untitled"


# ----------------------------------------------------------------- poems

def read_poem(path):
    """A poem file: optional ---frontmatter--- (title, arena, date), then the
    lines. A blank line is a stanza break."""
    text = path.read_text()
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n?", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    stanzas = [s.split("\n") for s in re.split(r"\n\s*\n", text.strip("\n")) if s.strip()]
    return {"file": path.name, "slug": slugify(path.stem), "title": meta.get("title", ""),
            "meta": meta, "stanzas": [[l.rstrip() for l in s] for s in stanzas]}


def ordered_poems(root):
    """order.txt is the sequence: one poem filename per line. Lines starting
    with # are left out of the book, so dropping a poem is commenting it."""
    order = root / "order.txt"
    if not order.is_file():
        die("no order.txt — run `chapbook fetch`, or list poem filenames in it")
    poems = []
    for line in order.read_text().splitlines():
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        path = root / "poems" / name
        if not path.is_file():
            die(f"order.txt lists {name}, but poems/{name} doesn't exist")
        poems.append(read_poem(path))
    if not poems:
        die("order.txt has no poems in it")
    return poems


def first_line(poem, limit=48):
    """What an untitled poem is called in the contents: its first line, cut
    at a word if it is long."""
    line = poem["stanzas"][0][0].strip()
    if len(line) <= limit:
        return line.rstrip(",;:—–- ")
    return line[:limit].rsplit(" ", 1)[0].rstrip(",;:.—–- ") + "…"


def smarten(text):
    text = re.sub(r"(?<=\w)'(?=\w)", "’", text)
    text = re.sub(r"(^|[\s(\[—–-])\"", r"\1“", text)
    text = text.replace('"', "”")
    text = re.sub(r"(^|[\s(\[—–-])'(?=\w)", r"\1‘", text)
    return text.replace("'", "’")


def inline(text, smart):
    if smart:
        text = smarten(text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)[*_](.+?)[*_](?!\w)", r"<em>\1</em>", text)
    return text


def plain(text, smart):
    return re.sub(r"<[^>]+>", "", inline(text, smart))


# ----------------------------------------------------------------- fonts

@functools.cache
def scan_fonts(directory):
    """Every .ttf/.otf under a directory -> (family, weight, italic, variable
    weight range or None, path). Reads the font's own name table, since one
    folder often holds several families."""
    from fontTools.ttLib import TTFont
    found = []
    for path in sorted(Path(directory).rglob("*")):
        if path.suffix.lower() not in (".ttf", ".otf"):
            continue
        if re.search(r"web|woff", str(path.parent), re.I):
            continue
        try:
            font = TTFont(path, lazy=True, fontNumber=0)
            name = font["name"]
            family = name.getDebugName(16) or name.getDebugName(1)
            os2 = font["OS/2"]
            italic = bool(os2.fsSelection & 1) or bool(font["head"].macStyle & 2)
            wght = None
            if "fvar" in font:
                for axis in font["fvar"].axes:
                    if axis.axisTag == "wght":
                        wght = (int(axis.minValue), int(axis.maxValue))
            found.append((family, os2.usWeightClass, italic, wght, path))
            font.close()
        except Exception:
            continue
    return found


def find_family(family, fonts_dir):
    fonts_dir = Path(fonts_dir).expanduser()
    if not fonts_dir.is_dir():
        die(f"fonts_dir {fonts_dir} doesn't exist")
    want = re.sub(r"[^a-z0-9]", "", family.lower())
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    dirs = [d for d in sorted(fonts_dir.iterdir()) if d.is_dir()
            and (want.startswith(norm(d.name)) or norm(d.name).startswith(want))]
    seen = []
    for d in dirs or [fonts_dir]:
        fonts = scan_fonts(d)
        seen += fonts
        hits = [f for f in fonts if norm(f[0]) == want]
        if hits:
            statics = [f for f in hits if f[3] is None]
            return statics or hits
    names = sorted({f[0] for f in seen})
    die(f"no font family named {family!r} under {fonts_dir}"
        + (f" — that folder has: {', '.join(names)}" if dirs and names else ""))


def font_faces(family, fonts_dir, alias=None):
    faces, done = [], set()
    for fam, weight, italic, wght, path in find_family(family, fonts_dir):
        key = (wght or weight, italic)
        if key in done:
            continue
        done.add(key)
        w = f"{wght[0]} {wght[1]}" if wght else weight
        faces.append(
            f"@font-face {{ font-family: '{alias or family}'; src: url('{path.as_uri()}'); "
            f"font-weight: {w}; font-style: {'italic' if italic else 'normal'}; }}")
    return "\n".join(faces)


# ------------------------------------------------------------------ html

def page_css(cfg, label=None):
    p, t = cfg["page"], cfg["type"]
    folio = ("font-family: 'text'; font-size: 8pt; color: var(--ink); "
             "vertical-align: top; padding-top: %s;" % t["leading"])
    left = right = f'string(face) "  ·  {label}"' if label else "counter(page)"
    return f"""
:root {{
  --size: {t['size']}; --leading: {t['leading']};
  --ink: {cfg['book']['ink']};
}}
@page {{ size: {p['width']} {p['height']}; }}
@page :left {{
  margin: {p['top']} {p['inside']} {p['bottom']} {p['outside']};
  @bottom-left {{ content: {left}; {folio} }}
}}
@page :right {{
  margin: {p['top']} {p['outside']} {p['bottom']} {p['inside']};
  @bottom-right {{ content: {right}; {folio} }}
}}
@page plain:left {{ @bottom-left {{ content: none; }} }}
@page plain:right {{ @bottom-right {{ content: none; }} }}
@page :blank {{
  @bottom-left {{ content: none; }}
  @bottom-right {{ content: none; }}
}}
"""


def poem_html(poem, smart, extra=""):
    out = [f'<section class="poem" id="{poem["slug"]}"{extra}>']
    if poem["title"]:
        out.append(f'<h2 class="poem-title">{inline(poem["title"], smart)}</h2>')
    else:
        out.append('<div class="poem-title untitled" aria-hidden="true">&nbsp;</div>')
    for stanza in poem["stanzas"]:
        out.append('<div class="stanza">')
        for line in stanza:
            out.append(f'<div class="line">{inline(line, smart) or "&nbsp;"}</div>')
        out.append("</div>")
    out.append("</section>")
    return "\n".join(out)


def document(cfg, body, faces, root, label=None):
    css = (HERE / "book.css").read_text()
    own = root / "style.css"
    own_css = own.read_text() if own.is_file() else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(cfg['title'])}</title>
<meta name="author" content="{html.escape(cfg['author'])}">
<style>
{faces}
{page_css(cfg, label)}
{css}
{own_css}
</style></head><body>
{body}
</body></html>"""


def book_html(cfg, poems, root, blanks=0):
    smart = cfg["book"]["smart_quotes"]
    t = cfg["type"]
    faces = font_faces(t["text"], t["fonts_dir"], "text")
    faces += "\n" + font_faces(t["display"], t["fonts_dir"], "display")
    parts = [f"""<section class="title-page">
<h1 class="book-title">{inline(cfg['title'], smart)}</h1>
<p class="book-author">{inline(cfg['author'], smart)}</p>
</section>"""]
    if cfg["book"]["contents"]:
        rows = []
        for poem in poems:
            if poem["title"]:
                label = inline(poem["title"], smart)
            else:
                label = f'<em>{inline(first_line(poem), smart)}</em>'
            rows.append(f'<li><a href="#{poem["slug"]}"><span class="toc-title">{label}</span></a></li>')
        parts.append('<nav class="contents"><h2 class="contents-title">Contents</h2>'
                     f'<ol>{"".join(rows)}</ol></nav>')
    parts += [poem_html(poem, smart) for poem in poems]
    parts += ['<div class="blank"></div>'] * blanks
    if cfg["book"]["colophon"]:
        paras = "".join(f"<p>{inline(p.strip(), smart)}</p>"
                        for p in cfg["book"]["colophon"].strip().split("\n\n"))
        parts.append(f'<section class="colophon">{paras}</section>')
    return document(cfg, "\n".join(parts), faces, root)


# ----------------------------------------------------------------- build

def render(html_text, root):
    from weasyprint import HTML
    return HTML(string=html_text, base_url=str(root)).render()


def impose(src, dest, cfg):
    """Saddle-stitch imposition: two pages side by side on a sheet twice the
    page width, ordered so the printed stack folds into the book. Print
    double-sided, flipping on the SHORT edge."""
    from pypdf import PdfReader, PdfWriter, PageObject, Transformation
    pages = PdfReader(src).pages
    n = len(pages)
    assert n % 4 == 0
    w, h = to_pt(cfg["page"]["width"]), to_pt(cfg["page"]["height"])
    writer = PdfWriter()
    for s in range(n // 4):
        for left, right in ((n - 1 - 2 * s, 2 * s), (2 * s + 1, n - 2 - 2 * s)):
            sheet = PageObject.create_blank_page(width=2 * w, height=h)
            sheet.merge_page(pages[left])
            sheet.merge_transformed_page(pages[right], Transformation().translate(w, 0))
            writer.add_page(sheet)
    writer.write(dest)
    return n // 4


def rasterize(pdf, out_dir, dpi=144):
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(out_dir / "p")],
                   check=True)
    return sorted(p.name for p in out_dir.glob("p-*.png"))


def write_preview(cfg, build, images, stamp):
    p, t = cfg["page"], cfg["type"]
    w, h = to_pt(p["width"]), to_pt(p["height"])
    data = {
        "title": cfg["title"], "stamp": stamp, "images": images,
        "ratio": w / h,
        "margins": {k: to_pt(p[k]) / (h if k in ("top", "bottom") else w) * 100
                    for k in ("top", "bottom", "inside", "outside")},
        "leading": to_pt(t["leading"]) / h * 100,
        "width": p["width"],
        "spec": f'{p["width"]} × {p["height"]} · {t["text"]} {t["size"]}/{t["leading"]}',
    }
    page = (HERE / "preview.html").read_text().replace(
        "/*DATA*/", "window.BOOK = " + json.dumps(data) + ";")
    (build / "preview.html").write_text(page)
    (build / "stamp.txt").write_text(stamp)


def build(root, snap=None, quiet=False):
    cfg = load_config(root)
    poems = ordered_poems(root)
    out = root / "build"
    out.mkdir(exist_ok=True)

    doc = render(book_html(cfg, poems, root), root)
    n = len(doc.pages)
    blanks = (4 - n % 4) % 4
    if blanks:
        doc = render(book_html(cfg, poems, root, blanks), root)
        if len(doc.pages) % 4:
            die(f"padding to a multiple of 4 failed ({len(doc.pages)} pages)")
    total = len(doc.pages)

    pdf = out / f"{cfg['slug']}.pdf"
    booklet = out / f"{cfg['slug']}-booklet.pdf"
    doc.write_pdf(pdf)
    sheets = impose(pdf, booklet, cfg)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    write_preview(cfg, out, rasterize(pdf, out / "pages"), stamp)

    over = overflowing(doc, poems)
    if not quiet or over:
        pad = f" ({n} + {blanks} blank)" if blanks else ""
        print(f"-> {pdf}\n   {len(poems)} poems, {total} pages{pad}, {sheets} sheets")
        print(f"-> {booklet}\n   print double-sided, flip on the short edge")
        print(f"-> {out / 'preview.html'}")
        for title, pages in over:
            print(f"   runs {pages} pages: {title}")
    if snap is not None:
        snaps = root / "snapshots"
        snaps.mkdir(exist_ok=True)
        note = f"-{slugify(snap)}" if snap else ""
        for f in (pdf, booklet):
            dest = snaps / f"{stamp[:15]}{note}-{f.name}"
            shutil.copy2(f, dest)
            print(f"   snapshot: {dest}")
    return cfg


def overflowing(doc, poems):
    """Poems that run past one page, read back from the rendered layout —
    the first thing to look at when a margin or type size changes."""
    first, last = {}, {}

    def walk(box, page_no):
        eid = getattr(getattr(box, "element", None), "get", lambda k: None)("id")
        if eid and getattr(box, "element_tag", "") == "section":
            first.setdefault(eid, page_no)
            last[eid] = page_no
        for child in getattr(box, "children", ()):
            walk(child, page_no)

    for i, page in enumerate(doc.pages, 1):
        walk(page._page_box, i)
    out = []
    for poem in poems:
        s = poem["slug"]
        if s in first and last[s] > first[s]:
            out.append((poem["title"] or first_line(poem), last[s] - first[s] + 1))
    return out


# -------------------------------------------------------------- specimen

def specimen(root, families, poem_name=None):
    cfg = load_config(root)
    poems = ordered_poems(root)
    poem = next((p for p in poems if p["file"] == poem_name), None) if poem_name else None
    if poem_name and not poem:
        die(f"{poem_name} isn't in order.txt")
    poem = poem or max((p for p in poems if p["title"]),
                       key=lambda p: -abs(sum(map(len, p["stanzas"])) - 22))
    t = cfg["type"]
    faces, parts = [], []
    for i, fam in enumerate(families or SPECIMEN_FACES):
        faces.append(font_faces(fam, t["fonts_dir"], f"spec{i}"))
        style = (f' style="font-family: \'spec{i}\'; --font-display: \'spec{i}\'; '
                 f'string-set: face \'{fam}\'"')
        one = dict(poem, slug=f"spec{i}")
        parts.append(poem_html(one, cfg["book"]["smart_quotes"], style))
    faces.append(font_faces(t["text"], t["fonts_dir"], "text"))
    label = f'{t["size"]}/{t["leading"]}'
    out = root / "build"
    out.mkdir(exist_ok=True)
    pdf = out / "specimen.pdf"
    render(document(cfg, "\n".join(parts), "\n".join(faces), root, label), root).write_pdf(pdf)
    rasterize(pdf, out / "specimen")
    print(f"-> {pdf}\n   “{poem['title']}” in {len(parts)} faces at {label}")


# ----------------------------------------------------------------- fetch

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def fetch(root, force=False):
    cfg = load_config(root)
    if not cfg["arena"]:
        die("book.toml has no `arena = \"<channel-slug>\"`")
    blocks, page = [], 1
    while True:
        data = get_json(f"{API}/channels/{cfg['arena']}/contents?per=100&page={page}")
        blocks += data["data"]
        if not data["meta"]["has_more_pages"]:
            break
        page += 1
        time.sleep(0.2)
    blocks = [b for b in blocks if b.get("type") == "Text"]
    blocks.sort(key=lambda b: b["connection"]["connected_at"])

    poems_dir = root / "poems"
    poems_dir.mkdir(exist_ok=True)
    have = {}
    for path in poems_dir.glob("*.md"):
        have[read_poem(path)["meta"].get("arena")] = path
    order = root / "order.txt"
    listed = order.read_text() if order.is_file() else (
        "# The book's sequence: one poem file per line, top to bottom.\n"
        "# Reorder lines to resequence. Put # in front of a line to leave\n"
        "# that poem out.\n\n")
    new = kept = 0
    for b in blocks:
        content = b["content"]
        text = (content.get("markdown") or content.get("plain") or "") if isinstance(content, dict) else (content or "")
        text = text.replace("\r\n", "\n").strip("\n")
        title = (b.get("title") or "").strip()
        # A first line that is all bold, or a markdown heading, is the title.
        m = re.match(r"\s*(?:\*\*(.+?)\*\*|#+[ \t]*(.+?))[ \t]*(?:\n+|$)", text)
        if m:
            title = title or (m.group(1) or m.group(2)).strip()
            text = text[m.end():]
        lines = [re.sub(r"(\\|  +)$", "", l).rstrip() for l in text.split("\n")]
        text = "\n".join(lines)
        first = next((l for l in lines if l.strip()), "untitled")
        date = b["connection"]["connected_at"][:10]
        body = f"---\ntitle: {title}\narena: {b['id']}\ndate: {date}\n---\n\n{text}\n"
        path = have.get(str(b["id"]))
        if path and not force:
            kept += 1
            continue
        if not path:
            stem = slugify(title or first, 40)
            path = poems_dir / f"{stem}.md"
            i = 2
            while path.exists():
                path = poems_dir / f"{stem}-{i}.md"
                i += 1
            listed += path.name + "\n"
            new += 1
        path.write_text(body)
    order.write_text(listed)
    print(f"{len(blocks)} text blocks in {cfg['arena']}: {new} new, "
          f"{kept} already here (left alone)" + (", rest rewritten" if force else ""))


# ------------------------------------------------------------------- new

def new(dest, channel):
    dest = Path(dest).expanduser()
    if (dest / "book.toml").exists():
        die(f"{dest} already has a book.toml")
    (dest / "poems").mkdir(parents=True, exist_ok=True)
    toml = (HERE / "template" / "book.toml").read_text()
    toml = re.sub(r'^arena\s*=\s*""', f'arena  = "{channel or ""}"', toml, flags=re.M)
    (dest / "book.toml").write_text(toml)
    shutil.copy2(HERE / "template" / "style.css", dest / "style.css")
    (dest / ".gitignore").write_text("build/\n.DS_Store\n")
    print(f"-> {dest}\n   edit book.toml, then `chapbook fetch` and `chapbook build`")


# ----------------------------------------------------------------- watch

def sources(root):
    files = [root / "book.toml", root / "order.txt", root / "style.css",
             HERE / "book.css", HERE / "preview.html", HERE / "chapbook.py"]
    files += list((root / "poems").glob("*.md"))
    return {str(f): f.stat().st_mtime for f in files if f.exists()}


def watch(root, port):
    def attempt():
        try:
            build(root, quiet=True)
            print(time.strftime("%H:%M:%S"), "built", flush=True)
        except SystemExit as e:
            print(e)
        except Exception as e:
            print("build failed:", e)

    attempt()
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(root / "build"))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"preview: http://127.0.0.1:{port}/preview.html   (ctrl-c to stop)", flush=True)
    seen = sources(root)
    try:
        while True:
            time.sleep(0.6)
            now = sources(root)
            if now != seen:
                seen = now
                attempt()
    except KeyboardInterrupt:
        print()


def main():
    ap = argparse.ArgumentParser(prog="chapbook", description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=".", help="the book folder (default: here)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="start a book folder")
    n.add_argument("dest")
    n.add_argument("--channel", help="are.na channel slug to pull poems from")
    f = sub.add_parser("fetch", help="pull are.na text blocks into poems/")
    f.add_argument("--force", action="store_true",
                   help="overwrite poems already on disk with the channel's text")
    b = sub.add_parser("build", help="build the PDF, the booklet and the preview")
    b.add_argument("--snap", nargs="?", const="", metavar="NOTE",
                   help="also keep a timestamped copy in snapshots/")
    w = sub.add_parser("watch", help="rebuild on save and serve the preview")
    w.add_argument("--port", type=int, default=8642)
    s = sub.add_parser("specimen", help="one poem set in several faces")
    s.add_argument("families", nargs="*")
    s.add_argument("--poem", help="poem filename to use")
    args = ap.parse_args()
    root = Path(args.root).expanduser().resolve()
    if args.cmd == "new":
        new(args.dest, args.channel)
    elif args.cmd == "fetch":
        fetch(root, args.force)
    elif args.cmd == "build":
        build(root, args.snap)
    elif args.cmd == "watch":
        watch(root, args.port)
    elif args.cmd == "specimen":
        specimen(root, args.families, args.poem)


if __name__ == "__main__":
    main()
