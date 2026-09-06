#!/usr/bin/env bash
# Package this repo as a self-contained skill zip for upload to claude.ai.
#
# The local skill is a symlink to this repo, so it always reads the live files.
# The web version can't do that — it has to carry copies. Re-run this after
# editing RULES.md, kit.css, or SKILL.md, and re-upload.
#
# Allowlist, not denylist: .env holds an Are.na token and must never ship.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="bjorn-design"
OUT="$REPO/dist"
STAGE="$OUT/$NAME"

rm -rf "$STAGE" "$OUT/$NAME.zip"
mkdir -p "$STAGE/scripts" "$STAGE/print"

# --- core: what the skill actually reads -----------------------------------
cp "$REPO/RULES.md" "$REPO/NOTES.md" "$REPO/kit.css" "$STAGE/"
cp "$REPO/scripts/contrast.py" "$STAGE/scripts/"

# --- templates the SKILL.md points at --------------------------------------
cp "$REPO/slideshow-template.html" "$STAGE/"
cp "$REPO/showcase.html" "$REPO/palette-docs.html" "$STAGE/"
cp "$REPO/print/print.css" "$REPO/print/pandoc-template.html" \
   "$REPO/print/md2pdf.sh" "$STAGE/print/"

# --- SKILL.md, with a snapshot note injected after the frontmatter ----------
awk '
  /^---$/ { d++ }
  { print }
  d == 2 && !done {
    print ""
    print "> **Packaged snapshot.** This is an exported copy of the"
    print "> `color-system-and-guidelines` repo for claude.ai. The repo is the"
    print "> source of truth; if these files look stale, ask before trusting a"
    print "> detail over what he tells you. Regenerate with"
    print "> `scripts/package-skill.sh`."
    done = 1
  }
' "$REPO/SKILL.md" > "$STAGE/SKILL.md"

# --- verify before zipping --------------------------------------------------
if find "$STAGE" \( -name '.env' -o -name '.git' -o -name '*.pyc' \) | grep -q .; then
  echo "REFUSING: excluded file made it into the stage dir" >&2
  exit 1
fi
head -2 "$STAGE/SKILL.md" | grep -q '^---$' || { echo "REFUSING: no frontmatter" >&2; exit 1; }

cd "$OUT"
zip -qr "$NAME.zip" "$NAME"
rm -rf "$STAGE"

echo "Built $OUT/$NAME.zip"
unzip -l "$NAME.zip" | tail -n +4 | head -20
