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
    drift.py --fix <path>...      rewrite each stale copy to kit.css's value,
                                  in the same notation (hex stays hex)

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


def written_like(old, rgb):
    """Format rgb the way old was written: hex, rgb(a,b,c) or rgb(a, b, c)."""
    if old.startswith("#"):
        h = "#" + "".join(f"{c:02x}" for c in rgb)
        return h.upper() if old[1:].isupper() else h
    sep = ", " if ", " in old else ","
    return f"rgb({sep.join(map(str, rgb))})"


def check(paths, fix=False):
    """Print every stale copy under paths; return how many.
    With fix, rewrite each one to kit.css's value."""
    tokens = parse_kit()
    drifted = 0
    for f in files(paths):
        if f.resolve() == KIT:
            continue
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            continue
        lines = text.splitlines(keepends=True)
        changed = False
        for n, line in enumerate(lines, 1):
            for m in COPY.finditer(line):
                name, literal = m.groups()
                if name not in tokens:
                    continue
                want = to_rgb(name, tokens)
                if to_rgb(literal) != want:
                    drifted += 1
                    print(f"{f}:{n}  --{name} is {literal}, "
                          f"kit.css has rgb({','.join(map(str, want))})")
                    if fix:
                        new = m.group(0)[:m.start(2) - m.start()] + written_like(literal, want)
                        lines[n - 1] = lines[n - 1].replace(m.group(0), new, 1)
                        changed = True
        if changed:
            f.write_text("".join(lines))
    if drifted:
        verb = "fixed" if fix else "stale"
        print(f"\n{drifted} {verb} cop{'y' if drifted == 1 else 'ies'} of kit.css colors.")
    else:
        print("No drift: every pasted kit color matches kit.css.")
    return drifted


def main():
    args = sys.argv[1:]
    fix = "--fix" in args
    paths = [a for a in args if a != "--fix"] or [REPO]
    return 1 if check(paths, fix) and not fix else 0


if __name__ == "__main__":
    sys.exit(main())
