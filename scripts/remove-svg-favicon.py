#!/usr/bin/env python3
"""Remove SVG favicon links so browsers use logo-nav PNG favicon."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "node_modules", ".git", "scripts", "dist"}
PAT = re.compile(r'\n  <link rel="icon" type="image/svg\+xml" href="[^"]+">')


def main() -> None:
    n = 0
    for html in ROOT.rglob("*.html"):
        if any(part in SKIP for part in html.parts):
            continue
        text = html.read_text(encoding="utf-8")
        new = PAT.sub("", text)
        if new != text:
            html.write_text(new, encoding="utf-8")
            n += 1
    print(f"Removed SVG favicon from {n} HTML files")


if __name__ == "__main__":
    main()
