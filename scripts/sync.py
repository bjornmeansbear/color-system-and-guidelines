#!/usr/bin/env python3
"""Copy the current kit.css into projects, then check them for drift.

Every project keeps its own kit.css (no build step, no package), so re-copying
after a kit change is the step that gets forgotten. This does it in one go:

  1. Finds each file named kit.css in the project.
  2. Overwrites it with this repo's kit.css, but only if the copy matches some
     committed version of kit.css. A copy with local edits is left alone and
     reported, so a project's own changes never get clobbered silently.
  3. Runs drift.py over the project, which catches the palette pasted into
     other files (app.css, a deck's <style>) that a copy can't fix.

Usage:
    sync.py <project>...          sync these project folders
    sync.py --all                 every project in the folder above this repo
    sync.py --dry-run ...         report only, write nothing

Exits nonzero if any copy was skipped or any drift is left.
"""

import subprocess
import sys
from pathlib import Path

from drift import KIT, REPO, SKIP_DIRS, check


def committed_versions():
    """Every kit.css this repo has ever committed, as text."""
    git = ["git", "-C", str(REPO)]
    shas = subprocess.run(git + ["log", "--format=%H", "--", "kit.css"],
                          capture_output=True, text=True, check=True).stdout.split()
    return {subprocess.run(git + ["show", f"{sha}:kit.css"],
                           capture_output=True, text=True).stdout for sha in shas}


def copies(project):
    return [f for f in sorted(project.rglob("kit.css"))
            if not SKIP_DIRS & set(f.parts) and f.resolve() != KIT]


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    if "--all" in args:
        projects = [p for p in sorted(REPO.parent.iterdir())
                    if p.is_dir() and p != REPO and not p.name.startswith(".")]
    else:
        projects = [Path(a).expanduser() for a in args if not a.startswith("--")]
    if not projects:
        sys.exit(__doc__.strip().split("\n\n")[-2])

    current = KIT.read_text()
    known = committed_versions() | {current}
    skipped = 0
    for project in projects:
        for f in copies(project):
            text = f.read_text()
            if text == current:
                print(f"  current   {f}")
            elif text in known:
                if not dry:
                    f.write_text(current)
                print(f"  {'would update' if dry else 'updated'}   {f}")
            else:
                skipped += 1
                print(f"  SKIPPED   {f}  (local edits; diff it against kit.css by hand)")

    print()
    drifted = check(projects)
    return 1 if skipped or drifted else 0


if __name__ == "__main__":
    sys.exit(main())
