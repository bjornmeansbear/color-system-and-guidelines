#!/usr/bin/env python3
"""
Report how the slideshow paces at the current quote and image counts.

Answers the two questions that come up while editing text/quotes.txt:
how long does one loop run before it repeats, and how many images have to
be shown twice so that every quote gets a slot.

Reads the real archive through build_slideshow, so the numbers track
whatever is actually on disk rather than a remembered figure.

Usage:
    python3 scripts/pacing.py
    python3 scripts/pacing.py --max-ipq 8
"""
import argparse
import csv
import importlib.util
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "build_slideshow", TOOL_DIR / "build_slideshow.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def hms(seconds):
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m" if h else f"{m}m {s:02d}s"


def quote_seconds(q):
    """Mirrors slideSeconds() in the templates."""
    chars = len(q["text"]) + len(q["attribution"])
    return max(7.0, min(22.0, 4.5 + chars / 13))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-ipq", type=int, default=6,
                    help="highest --images-per-quote to tabulate (default 6)")
    ap.add_argument("--image-seconds", type=float, default=6.0,
                    help="deck dwell per image (default 6, matches the template)")
    ap.add_argument("--image-ms", type=int, default=600,
                    help="ambient cut speed (default 600)")
    ap.add_argument("--chairs-between-text", type=int, default=7,
                    help="ambient bare chairs between panels (default 7)")
    ap.add_argument("--root", default=None,
                    help="archive directory to read (default: current directory)")
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else Path.cwd()

    b = load_builder()
    manifest = list(csv.DictReader(open(root / "manifest.csv")))
    vitra_path = root / "vitra.csv"
    vitra = list(csv.DictReader(open(vitra_path))) if vitra_path.exists() else []
    quotes = b.load_quotes(root / "text" / "quotes.txt")

    local = b.collect_images(root, manifest, vitra, 300, False, False)
    web = b.collect_images(root, manifest, vitra, 300, False, True)

    qsecs = [quote_seconds(q) for q in quotes]
    print(f"{len(quotes)} quotes  |  dwell {min(qsecs):.0f}-{max(qsecs):.0f}s, "
          f"{sum(qsecs)/len(qsecs):.1f}s average, {hms(sum(qsecs))} of reading in total")
    print(f"images: {len(local)} local (gallery), {len(web)} are.na-hosted (web)\n")

    for label, imgs in (("slideshow.html (local)", local),
                        ("slideshow-web.html (hotlink)", web)):
        print(f"{label} — {len(imgs)} unique images")
        print(f"  {'ipq':>4} {'repeats':>8} {'slides':>7} {'one loop':>10}   quote density")
        for ipq in range(2, args.max_ipq + 1):
            need = max(0, len(quotes) - 1) * ipq
            shown = max(len(imgs), need)
            repeats = shown - len(imgs)
            inserts = shown // ipq
            # quotes cycle, so a long deck may run the list more than once
            qtime = sum(qsecs[(i + 1) % len(quotes)] for i in range(inserts)) + qsecs[0]
            total = shown * args.image_seconds + qtime
            covered = "all" if inserts >= len(quotes) - 1 else f"{inserts + 1}/{len(quotes)}"
            flag = "" if repeats == 0 else "  <- repeats"
            print(f"  {ipq:>4} {repeats:>8} {shown + inserts + 1:>7} {hms(total):>10}   "
                  f"quote every {ipq} images, {covered}{flag}")
        print()

    # ambient runs two independent tracks, so its loop length is the chair track
    for label, imgs in (("slideshow-ambient.html", local),
                        ("slideshow-ambient-web.html", web)):
        chair_loop = len(imgs) * args.image_ms / 1000
        avg_panel = sum(qsecs) / len(qsecs)
        cycle = args.chairs_between_text * args.image_ms / 1000 + avg_panel
        print(f"{label} — {len(imgs)} chairs at {args.image_ms}ms")
        print(f"  chair track loops every {hms(chair_loop)}")
        print(f"  a quote roughly every {cycle:.0f}s "
              f"({args.chairs_between_text} bare chairs + a {avg_panel:.0f}s panel)")
        print(f"  all {len(quotes)} quotes seen in about {hms(len(quotes) * cycle)}\n")


if __name__ == "__main__":
    main()
