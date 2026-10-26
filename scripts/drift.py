#!/usr/bin/env python3
"""Find pasted copies of kit.css colors that no longer match kit.css.

No project reads kit.css live — each keeps its own copy (print.css, onething,
wjeather, the decks), and the copies drift when the kit changes. This finds
every raw token written next to a literal color (`--pink-5: rgb(...)` in CSS,
"`--pink-5` `rgb(...)`" in a Markdown table) and checks it against kit.css.

Only raw tokens are checked (`pink-5`, `white-0`, `wjerk-navy`). Semantic
tokens (`--color-accent`) are a project's to override, so they're skipped.

Usage:
    drift.py                      check this repo
    drift.py <path>...            check files or folders (other projects too)

Exits nonzero if anything drifted.
"""

import re
import sys
from pathlib import Path

from contrast import KIT, parse_kit, to_rgb

REPO = KIT.parent
EXTS = {".css", ".html", ".md", ".py", ".svelte", ".js", ".ts", ".tid"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__",
             ".svelte-kit", ".next", ".vercel", ".wrangler", ".netlify"}
COPY = re.compile(r"--((?:[a-z]+-)+\d|wjerk-[a-z-]+)\W{1,4}"
                  r"(rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b)")


def files(paths):
    for p in paths:
        p = Path(p)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if (f.is_file() and f.suffix in EXTS
                        and not SKIP_DIRS & set(f.parts)):
                    yield f


def check(paths):
    """Print every stale copy under paths; return how many."""
    tokens = parse_kit()
    drifted = 0
    for f in files(paths):
        if f.resolve() == KIT:
            continue
        try:
            lines = f.read_text().splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            for name, literal in COPY.findall(line):
                if name not in tokens:
                    continue
                want = to_rgb(name, tokens)
                if to_rgb(literal) != want:
                    drifted += 1
                    print(f"{f}:{n}  --{name} is {literal}, "
                          f"kit.css has rgb({','.join(map(str, want))})")
    if drifted:
        print(f"\n{drifted} stale cop{'y' if drifted == 1 else 'ies'} of kit.css colors.")
    else:
        print("No drift: every pasted kit color matches kit.css.")
    return drifted


def main():
    return 1 if check(sys.argv[1:] or [REPO]) else 0


if __name__ == "__main__":
    sys.exit(main())
