#!/usr/bin/env python3
"""
commons — machine narrows, you choose, machine writes the credit line.

Slide imagery for decks that declare intent-carrying slots:

    <section class="slide opener beat"
             data-img="beat-history"
             data-img-brief="an older lineage — surveying, notebooks, workshop labor"
             data-img-terms="surveying, workshop, notebook, apprentice">

The brief is for you; the terms are for the machine. Keyword APIs match a short
concrete noun, not a metaphor. Without terms, the brief is used as the query.

Commands
    brief   DECK                     the deck-level stake, themes, and material
    slots   DECK                     what is declared, what is still empty
    fill    DECK [SLOT]              search each empty slot, open a contact sheet
    search  QUERY                    ad-hoc cascade, contact sheet, no deck needed
    pick    DECK SLOT SOURCE:ID      cache the file, record it, write the credit
    resolve DECK [--web|--work]      emit the projected, web, or working build

Search order is fixed by RULES.md: your are.na channels, then the Met, the Art
Institute of Chicago, and Cleveland, then Wikimedia Commons last.

Config
    COMMONS_CACHE     image cache root   (default ~/Media/commons)
    COMMONS_CHANNELS  are.na slugs, comma-separated, searched first
"""
import argparse
import csv
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sheet          # noqa: E402
import sources        # noqa: E402

CACHE = pathlib.Path(os.environ.get("COMMONS_CACHE",
                                    pathlib.Path.home() / "Media/commons")).expanduser()
MANIFEST = CACHE / "manifest.csv"
CHANNELS = [s.strip() for s in os.environ.get("COMMONS_CHANNELS", "chair-ness").split(",")
            if s.strip()]
FIELDS = ["slot", "deck", "source", "id", "title", "artist", "date", "license",
          "credit", "page_url", "full_url", "local_path", "width", "height"]

META_RE = re.compile(
    r'<meta\s+name="commons-(stake|themes|material)"\s+content="([^"]*)"\s*/?>')

SLOT_RE = re.compile(r"<(?P<tag>section|div)\b(?P<attrs>[^>]*\bdata-img\s*=[^>]*)>")


# ------------------------------------------------------------------- helpers

def attr(attrs, name):
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', attrs)
    return html.unescape(m.group(1)) if m else None


def read_deck_brief(deck):
    """Deck-level declaration — the stake, the themes, the material family.

        <meta name="commons-stake"    content="the sentence that answers 'so what'">
        <meta name="commons-themes"   content="noticing, attention, the overlooked">
        <meta name="commons-material" content="etching; 1837-1901">

    Slot searches inherit all three, which is what makes a deck's images read
    as one family rather than five unrelated pictures.
    """
    text = pathlib.Path(deck).read_text()
    d = {k: html.unescape(v) for k, v in META_RE.findall(text)}
    return {"stake": d.get("stake", ""), "themes": d.get("themes", ""),
            "material": d.get("material", "")}


def read_slots(deck):
    text = pathlib.Path(deck).read_text()
    out = []
    for m in SLOT_RE.finditer(text):
        a = m.group("attrs")
        out.append({
            "slot": attr(a, "data-img"),
            "brief": attr(a, "data-img-brief") or "",
            "terms": attr(a, "data-img-terms") or "",
            "file": attr(a, "data-img-file"),
            "credit": attr(a, "data-img-credit"),
            "span": m.span(),
        })
    return text, out


def slugify(s, n=60):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return (s[:n].rstrip("-")) or "untitled"


def manifest_rows():
    if not MANIFEST.exists():
        return []
    with MANIFEST.open() as f:
        return list(csv.DictReader(f))


def write_manifest(rows):
    CACHE.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def sheet_dir(deck):
    d = pathlib.Path(deck).resolve().parent / ".commons"
    d.mkdir(exist_ok=True)
    return d


def open_file(p):
    try:
        subprocess.run(["open", str(p)], check=False)
    except Exception:
        pass


# ------------------------------------------------------------------ commands

def cmd_slots(args):
    _, slots = read_slots(args.deck)
    if not slots:
        print("No data-img slots found.\n\nAdd them to the slides that want "
              "imagery:\n  data-img=\"beat-history\"\n  data-img-brief=\"what the "
              "image is for, in your words\"")
        return 1
    empty = [s for s in slots if not s["file"]]
    for s in slots:
        mark = "\033[1;35m○ EMPTY\033[0m" if not s["file"] else "● filled"
        print(f"{mark}  {s['slot']}")
        if s["brief"]:
            print(f"          {s['brief']}")
        if s["file"]:
            print(f"          {s['file']}")
    print(f"\n{len(slots)} slots, {len(empty)} empty.")
    return 0


def _search_to_sheet(query, slot, deck, want, only, brief=None):
    brief = brief or {"themes": "", "material": ""}
    mat = sources.Material(brief.get("material", ""))
    themes = brief.get("themes", "")
    full = ", ".join(t for t in (themes, query) if t)
    print(f"searching: {full}")
    if mat:
        print(f"  material: {mat}")
    cands = sources.search(full, channels=CHANNELS, want=want, only=only,
                           material=mat)
    if not cands:
        print("  nothing survived the filters (public domain + "
              f"≥{sources.MIN_PX}px). Try a broader brief.")
        return None
    d = sheet_dir(deck)
    (d / f"{slot}.json").write_text(json.dumps(cands, indent=1))
    out = sheet.render(slot, query, cands, str(deck), d / f"{slot}.html")
    print(f"  {len(cands)} candidates → {out}")
    return out


def cmd_fill(args):
    _, slots = read_slots(args.deck)
    brief = read_deck_brief(args.deck)
    todo = [s for s in slots if not s["file"] and (not args.slot or s["slot"] == args.slot)]
    if not todo:
        print("Nothing to fill.")
        return 0
    for s in todo:
        query = args.terms or s["terms"] or s["brief"] or s["slot"].replace("-", " ")
        out = _search_to_sheet(query, s["slot"], args.deck, args.n, args.only, brief)
        if out and not args.no_open:
            open_file(out)
    return 0


def cmd_search(args):
    out = _search_to_sheet(args.query, slugify(args.query, 40),
                           args.deck or ".", args.n, args.only)
    if out and not args.no_open:
        open_file(out)
    return 0


def cmd_brief(args):
    b = read_deck_brief(args.deck)
    if not any(b.values()):
        print("No deck brief. Add to <head>:\n"
              '  <meta name="commons-stake"    content="the sentence that answers '
              "'so what'\">\n"
              '  <meta name="commons-themes"   content="two or three metaphors">\n'
              '  <meta name="commons-material" content="etching; 1837-1901">')
        return 1
    print(f"stake     {b['stake'] or '—'}")
    print(f"themes    {b['themes'] or '—'}")
    print(f"material  {sources.Material(b['material']) if b['material'] else '—'}")
    return 0


def cmd_pick(args):
    d = sheet_dir(args.deck)
    cache_json = d / f"{args.slot}.json"
    if not cache_json.exists():
        print(f"No search cached for '{args.slot}'. Run `fill` first.")
        return 1
    cands = json.loads(cache_json.read_text())
    src, _, cid = args.ref.partition(":")
    hit = next((c for c in cands if c["source"] == src and str(c["id"]) == cid), None)
    if not hit:
        print(f"'{args.ref}' is not in that search.")
        return 1

    # cache the file
    folder = CACHE / hit["source"]
    folder.mkdir(parents=True, exist_ok=True)
    ext = (pathlib.Path(urllib.parse.urlparse(hit["full_url"]).path).suffix
           or ".jpg").split("?")[0]
    dest = folder / f"{hit['id']}-{slugify(hit['title'])}{ext}"
    if not dest.exists():
        print(f"downloading → {dest}")
        req = urllib.request.Request(hit["full_url"], headers=sources.UA)
        with urllib.request.urlopen(req, timeout=120) as r, dest.open("wb") as f:
            f.write(r.read())
    else:
        print(f"already cached → {dest}")

    w, h = sources.probe_size(dest.as_uri())
    if w and max(w, h) < sources.MIN_PX:
        print(f"  refusing: {w}×{h} is under {sources.MIN_PX}px")
        dest.unlink()
        return 1

    rows = [r for r in manifest_rows()
            if not (r["slot"] == args.slot and r["deck"] == str(args.deck))]
    rows.append({**{k: hit.get(k, "") for k in FIELDS},
                 "slot": args.slot, "deck": str(args.deck),
                 "local_path": str(dest), "width": w or hit.get("width") or "",
                 "height": h or hit.get("height") or ""})
    write_manifest(rows)

    # write the file + credit back into the slot
    text, slots = read_slots(args.deck)
    target = next((s for s in slots if s["slot"] == args.slot), None)
    if target:
        start, end = target["span"]
        tag = text[start:end]
        tag = re.sub(r'\s+data-img-(file|credit)\s*=\s*"[^"]*"', "", tag)
        tag = tag[:-1] + (f'\n           data-img-file="{html.escape(str(dest))}"'
                          f'\n           data-img-credit="{html.escape(hit["credit"])}">')
        pathlib.Path(args.deck).write_text(text[:start] + tag + text[end:])
        print(f"wrote slot '{args.slot}' into {args.deck}")
    print(f"credit: {hit['credit']}")
    return 0


def cmd_resolve(args):
    text, slots = read_slots(args.deck)
    rows = {(r["slot"], r["deck"]): r for r in manifest_rows()}
    filled = missing = 0
    for s in reversed(slots):          # reversed so spans stay valid
        start, end = s["span"]
        tag = text[start:end]
        row = rows.get((s["slot"], str(args.deck)))
        if not s["file"] and not row:
            missing += 1
            if args.work:
                # Loud on the desk, silent in the room. An empty slot must be
                # impossible to miss while you are working on the deck.
                tag = tag[:-1] + ">" + (
                    '\n    <div style="position:absolute;inset:auto 0 0 0;z-index:9;'
                    'background:rgb(214,0,97);color:rgb(247,248,238);padding:.75rem 1rem;'
                    'font:600 14px/1.2 ui-monospace,Menlo,monospace">'
                    f'EMPTY SLOT · {html.escape(s["slot"])}'
                    + (f'<br><span style="font-weight:400;opacity:.85">'
                       f'{html.escape(s["brief"])}</span>' if s["brief"] else "")
                    + '</div>')
                text = text[:start] + tag + text[end:]
            continue
        src = (row or {}).get("full_url") if args.web else (s["file"] or row["local_path"])
        if not args.web:
            src = os.path.relpath(src, pathlib.Path(args.deck).resolve().parent)
        tag = re.sub(r'\s+style\s*=\s*"[^"]*--img[^"]*"', "", tag)
        tag = tag[:-1] + f" style=\"--img:url('{src}')\">"
        credit = s["credit"] or (row or {}).get("credit")
        if credit:
            tag += f'\n    <p class="credit">{html.escape(credit)}</p>'
        text = text[:start] + tag + text[end:]
        filled += 1
    suffix = "-web.html" if args.web else "-work.html" if args.work else "-print.html"
    out = pathlib.Path(args.out) if args.out else pathlib.Path(
        str(args.deck).replace(".html", suffix))
    out.write_text(text)
    print(f"{out}  —  {filled} slots resolved"
          + (f", {missing} still empty ("
             + ("marked loud" if args.work else "silent fallback") + ")"
             if missing else ""))
    return 0


def main():
    p = argparse.ArgumentParser(prog="commons", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("-n", type=int, default=40, help="candidates wanted (default 40)")
        sp.add_argument("--only", nargs="*", help="restrict to sources, e.g. --only aic met")
        sp.add_argument("--no-open", action="store_true")
        sp.add_argument("--terms", help="override the search terms "
                        "(comma-separated; each searched separately)")

    a = sub.add_parser("slots"); a.add_argument("deck"); a.set_defaults(fn=cmd_slots)
    g = sub.add_parser("brief"); g.add_argument("deck"); g.set_defaults(fn=cmd_brief)
    b = sub.add_parser("fill"); b.add_argument("deck"); b.add_argument("slot", nargs="?")
    common(b); b.set_defaults(fn=cmd_fill)
    c = sub.add_parser("search"); c.add_argument("query"); c.add_argument("--deck")
    common(c); c.set_defaults(fn=cmd_search)
    d = sub.add_parser("pick"); d.add_argument("deck"); d.add_argument("slot")
    d.add_argument("ref"); d.set_defaults(fn=cmd_pick)
    e = sub.add_parser("resolve"); e.add_argument("deck")
    e.add_argument("--web", action="store_true",
                   help="hotlink source URLs instead of local files (web only)")
    e.add_argument("--work", action="store_true",
                   help="mark empty slots conspicuously — for the desk, never the room")
    e.add_argument("--out")
    e.set_defaults(fn=cmd_resolve)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
