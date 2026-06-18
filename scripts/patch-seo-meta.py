#!/usr/bin/env python3
"""Add canonical, Open Graph and Twitter meta to inner HTML pages."""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "node_modules", ".git", "scripts", ".cursor"}
CFG = json.loads((ROOT / "data" / "site-config.json").read_text(encoding="utf-8"))
SITE_URL = (CFG.get("siteUrl") or "https://safariandbushretreats.com").rstrip("/")
OG_IMAGE = SITE_URL + (CFG.get("defaultOgImage") or "/assets/images/serengeti3.jpg")
SITE_NAME = CFG.get("siteName") or "Safari and Bush Retreats"

TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.I)
DESC_RE = re.compile(r'<meta name="description" content="[^"]*">\s*', re.I)


def page_url(rel: Path) -> str:
    if rel.name == "index.html" and rel.parent == ROOT:
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{rel.as_posix()}"


def seo_block(title: str, desc: str, url: str) -> str:
    t = escape(title, quote=True)
    d = escape(desc[:160], quote=True)
    u = escape(url, quote=True)
    img = escape(OG_IMAGE, quote=True)
    name = escape(SITE_NAME, quote=True)
    return f"""  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{u}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{u}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{img}">
  <meta property="og:site_name" content="{name}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{img}">"""


def patch_html(text: str, rel: Path) -> tuple[str, bool]:
    if 'rel="canonical"' in text:
        return text, False
    title_m = TITLE_RE.search(text)
    desc_m = DESC_RE.search(text)
    if not title_m or not desc_m:
        return text, False
    desc_content_m = re.search(r'content="([^"]*)"', desc_m.group(0), re.I)
    desc_text = desc_content_m.group(1) if desc_content_m else ""
    block = seo_block(title_m.group(1), desc_text, page_url(rel))
    return text.replace(desc_m.group(0), desc_m.group(0) + block + "\n", 1), True


def main() -> None:
    patched = 0
    skipped = 0
    for html in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in html.parts):
            continue
        rel = html.relative_to(ROOT)
        if rel.name == "index.html" and rel.parent == Path("."):
            continue
        text = html.read_text(encoding="utf-8")
        new_text, changed = patch_html(text, rel)
        if changed:
            html.write_text(new_text, encoding="utf-8")
            patched += 1
        else:
            skipped += 1
    print(f"Added SEO meta to {patched} pages ({skipped} skipped or already set)")


if __name__ == "__main__":
    main()
