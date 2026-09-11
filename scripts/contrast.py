#!/usr/bin/env python3
"""WCAG contrast checker for kit.css.

The rule this enforces (RULES.md, "Contrast: high-contrast pairs only"):
don't trust a token's name. A "muted" token that reads fine as an isolated
swatch shipped at 4.35:1 once already. Compute the number.

Usage:
    contrast.py                       audit every semantic pair, light + dark
    contrast.py --light               light mode only
    contrast.py --dark                dark mode only
    contrast.py pair <fg> <bg>        check one pair
    contrast.py find <bg> [--aaa]     list every scale token that passes on <bg>

<fg>/<bg> accept a token name (brown-8, --pink-5, color-text), a hex
(#191513), or rgb(25,21,19).
"""

import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "kit.css"

# Dark mode lives in RULES.md ("Dark mode"), not yet in kit.css. When the
# flip ships, delete this and let the parser find it.
DARK_OVERRIDES = {
    "color-bg": "brown-9",
    "color-surface": "brown-9",
    "color-surface-2": "brown-9",
    "color-text": "brown-0",
    "color-text-muted": "brown-3",
    "color-text-subtle": "brown-4",
    "color-accent": "pink-3",
    # Status colors flip to the light end of their own hue, the way text does
    # (2026-09-11): ~10:1 on brown-9. Panels take step 8 of the same family.
    "color-accent-hover": "pink-2",
    "color-success": "green-3",
    "color-warning": "yellow-3",
    "color-danger": "red-3",
    "color-info": "dark-gray-3",
    "color-success-bg": "light-gray-8",
    "color-warning-bg": "yellow-8",
    "color-danger-bg": "red-8",
    "color-info-bg": "dark-gray-8",
}

# fg tokens checked against every ground, in report order.
FOREGROUNDS = [
    "color-text", "color-text-muted", "color-text-subtle", "color-accent",
    "color-accent-hover", "color-success", "color-warning", "color-danger",
    "color-info",
]
GROUNDS = ["color-bg", "color-surface", "color-surface-2"]


def parse_kit():
    """--name: value pairs from kit.css :root, in file order."""
    text = KIT.read_text()
    return dict(re.findall(r"--([\w-]+)\s*:\s*([^;]+);", text))


def resolve(name, tokens, overrides=None, _seen=None):
    """Follow var() indirection to a literal color."""
    _seen = _seen or set()
    name = name.lstrip("-")
    if name in _seen:
        raise ValueError(f"circular var reference at --{name}")
    _seen.add(name)
    if overrides and name in overrides:
        return resolve(overrides[name], tokens, overrides, _seen)
    if name not in tokens:
        raise KeyError(name)
    value = tokens[name].strip()
    m = re.fullmatch(r"var\(\s*--([\w-]+)\s*\)", value)
    if m:
        return resolve(m.group(1), tokens, overrides, _seen)
    return value


def to_rgb(value, tokens=None, overrides=None):
    """Literal or token name -> (r, g, b)."""
    value = value.strip()
    m = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", value)
    if m:
        return tuple(int(g) for g in m.groups())
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", value)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", value)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    if tokens is not None:
        return to_rgb(resolve(value, tokens, overrides))
    raise ValueError(f"can't parse color: {value}")


def luminance(rgb):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    lo, hi = sorted((a, b))
    return (hi + 0.05) / (lo + 0.05)


def grade(r):
    """Worst-case grade: normal-size body text."""
    if r >= 7.0:
        return "AAA"
    if r >= 4.5:
        return "AA "
    if r >= 3.0:
        return "AA-large"
    return "FAIL"


def report(mode, tokens, overrides):
    print(f"\n{mode.upper()}  (grades are for normal-size text)")
    print("-" * 58)
    worst = []
    for ground in GROUNDS:
        try:
            bg = to_rgb(ground, tokens, overrides)
        except KeyError:
            continue
        seen = set()
        for fgname in FOREGROUNDS:
            try:
                fg = to_rgb(fgname, tokens, overrides)
            except KeyError:
                continue
            key = (fg, bg)
            if key in seen:
                continue
            seen.add(key)
            r = ratio(fg, bg)
            g = grade(r)
            flag = "  <-- fails AA" if r < 4.5 else ""
            print(f"  {fgname:<20} on {ground:<16} {r:6.2f}:1  {g}{flag}")
            if r < 4.5:
                worst.append((fgname, ground, r))
        print()
    return worst


def cmd_find(bg_arg, aaa):
    tokens = parse_kit()
    bg = to_rgb(bg_arg, tokens)
    floor = 7.0 if aaa else 4.5
    label = "AAA" if aaa else "AA"
    print(f"\nScale tokens reaching {label} ({floor}:1) on {bg_arg}:\n")
    hits = []
    for name, value in tokens.items():
        if not re.fullmatch(r"[a-z-]+-\d", name):
            continue
        r = ratio(to_rgb(value, tokens), bg)
        if r >= floor:
            hits.append((r, name))
    for r, name in sorted(hits, reverse=True):
        print(f"  --{name:<16} {r:6.2f}:1  {grade(r)}")
    if not hits:
        print("  none")
    print()


def main():
    args = sys.argv[1:]

    if args and args[0] == "pair":
        if len(args) != 3:
            sys.exit("usage: contrast.py pair <fg> <bg>")
        tokens = parse_kit()
        fg, bg = to_rgb(args[1], tokens), to_rgb(args[2], tokens)
        r = ratio(fg, bg)
        print(f"\n  {args[1]} on {args[2]}: {r:.2f}:1  {grade(r)}")
        print(f"  normal text  AA {'pass' if r >= 4.5 else 'FAIL'}   "
              f"AAA {'pass' if r >= 7.0 else 'FAIL'}")
        print(f"  large text   AA {'pass' if r >= 3.0 else 'FAIL'}   "
              f"AAA {'pass' if r >= 4.5 else 'FAIL'}\n")
        return 0 if r >= 4.5 else 1

    if args and args[0] == "find":
        if len(args) < 2:
            sys.exit("usage: contrast.py find <bg> [--aaa]")
        cmd_find(args[1], "--aaa" in args)
        return 0

    tokens = parse_kit()
    failures = []
    if "--dark" not in args:
        failures += report("light mode", tokens, None)
    if "--light" not in args:
        failures += report("dark mode (RULES.md mapping, not yet in kit.css)",
                           tokens, DARK_OVERRIDES)

    if failures:
        print(f"{len(failures)} pair(s) below AA:")
        for fg, bg, r in failures:
            print(f"  {fg} on {bg} — {r:.2f}:1")
        return 1
    print("All semantic pairs pass WCAG AA for normal text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
