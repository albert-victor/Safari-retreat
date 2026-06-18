#!/usr/bin/env python3
"""Repair description meta tags broken by patch-seo-meta.py."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "node_modules", ".git", "scripts", ".cursor"}

BROKEN_DESC = re.compile(
    r'(<meta name="description" content="[^"]*")\s*\n(\s*<meta name="robots")',
    re.I,
)
DOUBLE_GT = re.compile(r'content="([^"]+)">>', re.I)


def main() -> None:
    fixed = 0
    for html in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in html.parts):
            continue
        text = html.read_text(encoding="utf-8")
        new = BROKEN_DESC.sub(r"\1>\n\2", text)
        new = DOUBLE_GT.sub(r'content="\1">', new)
        if new != text:
            html.write_text(new, encoding="utf-8")
            fixed += 1
    print(f"Repaired {fixed} HTML files")


if __name__ == "__main__":
    main()
