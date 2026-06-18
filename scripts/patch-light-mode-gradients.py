#!/usr/bin/env python3
"""Ensure theme.css is linked on all HTML pages (light/dark gradient fixes apply site-wide)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "node_modules", ".git", "scripts"}
THEME_LINE = 'href="{prefix}css/theme.css"'


def depth_prefix(html: Path) -> str:
    depth = len(html.relative_to(ROOT).parts) - 1
    return "../" * depth


def main() -> None:
    missing = []
    ok = 0
    for html in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in html.parts):
            continue
        text = html.read_text(encoding="utf-8")
        prefix = depth_prefix(html)
        if THEME_LINE.format(prefix=prefix) in text or 'href="css/theme.css"' in text:
            ok += 1
        else:
            missing.append(str(html.relative_to(ROOT)))

    if missing:
        print("Pages missing theme.css:")
        for path in missing[:20]:
            print(f"  - {path}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")
    else:
        print(f"All {ok} HTML pages include theme.css (light/dark overlays active)")


if __name__ == "__main__":
    main()
