#!/usr/bin/env python3
"""Keep users in-context: fix nav links that unnecessarily bounce to homepage sections."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "node_modules", ".git", "scripts", ".cursor"}

REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "accommodations": [
        ('href="../index.html#accommodation"', 'href="luxury-lodges.html"'),
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
    ],
    "safaris": [
        ('href="../index.html#safaris"', 'href="index.html"'),
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
    ],
    "categories": [
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
    ],
    "circuits": [
        ('href="../index.html#destinations"', 'href="index.html"'),
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
    ],
    "destinations": [
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
    ],
    "kenya": [
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
    ],
    "uganda": [
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
    ],
    "rwanda": [
        ('href="../index.html#accommodation"', 'href="../accommodations/luxury-lodges.html"'),
        ('href="../index.html#safaris"', 'href="../safaris/index.html"'),
    ],
}


def section_for(path: Path) -> str | None:
    rel = path.relative_to(ROOT)
    if len(rel.parts) < 2:
        return None
    folder = rel.parts[0]
    return folder if folder in REPLACEMENTS else None


def main() -> None:
    patched_files = 0
    total_replacements = 0
    for html in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in html.parts):
            continue
        section = section_for(html)
        if not section:
            continue
        text = html.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS[section]:
            text = text.replace(old, new)
        if text != original:
            html.write_text(text, encoding="utf-8")
            patched_files += 1
            total_replacements += sum(original.count(old) for old, _ in REPLACEMENTS[section])
    print(f"Patched {patched_files} files for in-context navigation")


if __name__ == "__main__":
    main()
