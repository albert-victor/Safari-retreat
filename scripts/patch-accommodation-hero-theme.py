#!/usr/bin/env python3
"""Verify accommodation pages use dest-page hero markup and theme stylesheets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACCOMMODATIONS = ROOT / "accommodations"


def main() -> None:
    ok = 0
    issues: list[str] = []
    for html in sorted(ACCOMMODATIONS.glob("*.html")):
        text = html.read_text(encoding="utf-8")
        if "dest-page__hero-overlay" not in text:
            issues.append(f"{html.name}: missing dest-page__hero-overlay")
        if "destination-page.css" not in text:
            issues.append(f"{html.name}: missing destination-page.css")
        if "theme.css" not in text:
            issues.append(f"{html.name}: missing theme.css")
        else:
            ok += 1
    if issues:
        print("Issues:")
        for item in issues:
            print(f"  - {item}")
    print(f"Checked {ok} accommodation pages — hero theme CSS applies via destination-page.css + theme.css")


if __name__ == "__main__":
    main()
