#!/usr/bin/env python3
"""
List the are.na blocks whose images reach the slideshow with no caption.

Captions come from the block's own title and description (see
build_slideshow.block_caption), so anything typed into are.na flows in on the
next fetch_arena.py run. This produces the worklist: which blocks to go and
title, with a direct link to each.

Says *why* each one is bare, which changes what you type:
  - no title          -> the block was never titled
  - title rejected    -> it has a title, but it is a filename, a CDN query
                         string, a bare UUID, or a scraped HTTP error page

Usage:
    python3 scripts/uncaptioned.py                  # print
    python3 scripts/uncaptioned.py --out list.md    # also write markdown
"""
import argparse
import csv
import importlib.util
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
BLOCK_URL = "https://www.are.na/block/{id}"


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "build_slideshow", TOOL_DIR / "build_slideshow.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="also write a markdown checklist here")
    ap.add_argument("--min-px", type=int, default=300)
    ap.add_argument("--root", default=None,
                    help="archive directory to read (default: current directory)")
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else Path.cwd()

    b = load_builder()
    rows = list(csv.DictReader(open(root / "manifest.csv")))

    bare, titled = [], 0
    for r in rows:
        lp = r["local_path"]
        if not lp.startswith("images/") or not (root / lp).exists():
            continue
        size = b.image_size(root / lp)
        if size and max(size) < args.min_px:
            continue                      # dropped from the show anyway
        if b.block_caption(r["title"], r.get("description", "")):
            titled += 1
            continue
        why = "no title" if not r["title"].strip() else "title rejected"
        bare.append({"id": r["id"], "why": why, "raw": r["title"].strip(),
                     "path": lp, "size": f"{size[0]}x{size[1]}" if size else "?"})

    total = titled + len(bare)
    print(f"{len(bare)} of {total} are.na images reach the show with no caption "
          f"({len(bare)/total:.0%})\n")
    for kind in ("no title", "title rejected"):
        group = [x for x in bare if x["why"] == kind]
        if not group:
            continue
        print(f"--- {kind} ({len(group)}) ---")
        for x in group:
            print(f"  {BLOCK_URL.format(id=x['id'])}  {x['size']:>10}  {x['path']}")
            if x["raw"]:
                print(f"      currently: {x['raw'][:88]!r}")
        print()

    if args.out:
        lines = [f"# Uncaptioned blocks in {root.name}",
                 "",
                 f"{len(bare)} of {total} are.na images reach the slideshow with no "
                 f"caption. Title them in are.na; the next `fetch_arena.py` picks it up.",
                 ""]
        for kind in ("no title", "title rejected"):
            group = [x for x in bare if x["why"] == kind]
            if not group:
                continue
            lines += [f"## {kind} ({len(group)})", ""]
            for x in group:
                note = f" — currently `{x['raw'][:70]}`" if x["raw"] else ""
                lines.append(f"- [ ] [{x['id']}]({BLOCK_URL.format(id=x['id'])}) "
                             f"`{x['size']}` `{x['path']}`{note}")
            lines.append("")
        Path(args.out).write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
