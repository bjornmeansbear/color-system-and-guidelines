#!/usr/bin/env bash
# md2pdf.sh — markdown -> print-ready PDF, using this kit's print styling.
#
#   ./md2pdf.sh Document.md                          # -> output/Document.pdf
#   ./md2pdf.sh Document.md path/Out.pdf             # explicit output path
#   ./md2pdf.sh -x "Internal Notes" Document.md
#       -x drops a top-level (##) section and everything under it. Repeatable.
#
# Markdown may pull in shared boilerplate with a line of the form
#   <!-- include: ../shared/some-file.md -->
# resolved relative to the including file. Includes may nest.
#
# Styling lives in print.css, next to this script — see RULES.md
# "PDF generation" for the toolchain and why print.css restates a kit
# token subset instead of importing kit.css.
#
# Requires pandoc and weasyprint (both installable via Homebrew/pipx).
set -euo pipefail

DROP=()
while [[ "${1:-}" == -x ]]; do
  DROP+=("$2"); shift 2
done

SRC="${1:?usage: md2pdf.sh [-x \"Section Heading\"]... input.md [output.pdf]}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Built PDFs land in output/ next to this script's parent dir by default —
# gitignore that directory rather than committing built PDFs. Pass an
# explicit second argument to write somewhere else.
OUT="${2:-$DIR/output/$(basename "${SRC%.md}").pdf}"
mkdir -p "$(dirname "$OUT")"

# WeasyPrint's pango dependency needs this on macOS/Homebrew; harmless
# elsewhere. Set here rather than assumed to already be in the shell env.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-/usr/local/lib:/usr/lib}"

MD="$(mktemp -t md2pdf).md"
HTML="$(mktemp -t md2pdf).html"
trap 'rm -f "$MD" "$HTML"' EXIT

cp "$SRC" "$MD"

# Expand <!-- include: path/to/file.md --> directives, resolved relative to
# the source file's directory. Lets shared boilerplate live in one place
# instead of being pasted into every document. A missing include aborts
# the build rather than silently producing a partial document.
python3 - "$MD" "$(dirname "$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")")" <<'PYEOF'
import os, re, sys
target, base = sys.argv[1], sys.argv[2]
pat = re.compile(r'^[ \t]*<!--[ \t]*include:[ \t]*(.+?)[ \t]*-->[ \t]*$', re.M)

def expand(text, base, depth=0):
    if depth > 5:
        sys.exit("md2pdf: include nesting too deep (circular include?)")
    def sub(m):
        rel = m.group(1)
        path = os.path.normpath(os.path.join(base, rel))
        if not os.path.isfile(path):
            sys.exit(f"md2pdf: include not found: {rel} (resolved to {path})")
        return expand(open(path).read().rstrip("\n"), os.path.dirname(path), depth + 1)
    return pat.sub(sub, text)

src = open(target).read()
out = expand(src, base)
open(target, "w").write(out)
n = len(pat.findall(src))
if n:
    print(f"   expanded {n} include(s)", file=sys.stderr)
PYEOF

for heading in "${DROP[@]:-}"; do
  [[ -z "$heading" ]] && continue
  awk -v h="## $heading" '
    $0 == h { skip = 1; next }
    /^## / { skip = 0 }
    !skip
  ' "$MD" > "$MD.tmp" && mv "$MD.tmp" "$MD"
done

pandoc "$MD" \
  --from=markdown+pipe_tables+hard_line_breaks+autolink_bare_uris+smart \
  --to=html5 \
  --standalone \
  --template="$DIR/pandoc-template.html" \
  --metadata pagetitle="$(basename "${SRC%.md}")" \
  --output "$HTML"

weasyprint --stylesheet "$DIR/print.css" "$HTML" "$OUT"
echo "-> $OUT  ($(pdfinfo "$OUT" | awk '/^Pages/{print $2}') pages)"
