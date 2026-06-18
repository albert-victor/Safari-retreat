#!/usr/bin/env python3
"""Apply site-wide UX fixes: remove mobile 'All safari packages', favicon/manifest links, hash-nav."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "node_modules", ".git", "scripts"}

OVERVIEW_RE = re.compile(
    r'\s*<a href="[^"]*" class="mobile-menu__dest-overview">All safari packages</a>\n',
    re.IGNORECASE,
)

FAVICON_BLOCK = """  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/images/favicon.png">
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/images/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/images/apple-touch-icon.png">
  <link rel="manifest" href="{manifest}">"""

OLD_FAVICON_RE = re.compile(
    r'  <link rel="icon" type="image/png" href="[^"]+">\n'
    r'  <link rel="apple-touch-icon" href="[^"]+">\n'
)

HASH_NAV_SCRIPT = """  <script>
    (function () {
      var hash = window.location.hash;
      if (!hash || hash === '#') return;
      if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
      document.documentElement.classList.add('sbr-hash-nav');
    })();
  </script>"""


def depth_prefix(html: Path) -> str:
    depth = len(html.relative_to(ROOT).parts) - 1
    return "../" * depth


def manifest_href(html: Path) -> str:
    depth = len(html.relative_to(ROOT).parts) - 1
    return ("../" * depth) + "site.webmanifest"


def patch_favicon(text: str, prefix: str, manifest: str) -> str:
    block = FAVICON_BLOCK.format(prefix=prefix, manifest=manifest)
    if "site.webmanifest" in text:
        return text
    if OLD_FAVICON_RE.search(text):
        return OLD_FAVICON_RE.sub(block + "\n", text, count=1)
    return text


def patch_hash_nav(text: str, is_index: bool) -> str:
    if not is_index or "sbr-hash-nav" in text:
        return text
    marker = '  </script>\n  <meta name="viewport"'
    if marker in text:
        return text.replace(marker, "  </script>\n" + HASH_NAV_SCRIPT + "\n  <meta name=\"viewport\"", 1)
    return text


def main() -> None:
    removed = 0
    favicon_patched = 0
    hash_patched = 0

    for html in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in html.parts):
            continue
        text = html.read_text(encoding="utf-8")
        original = text

        new_text, n = OVERVIEW_RE.subn("", text)
        if n:
            removed += n
            text = new_text

        prefix = depth_prefix(html)
        manifest = manifest_href(html)
        favicon_new = patch_favicon(text, prefix, manifest)
        if favicon_new != text:
            favicon_patched += 1
            text = favicon_new

        is_index = html.name == "index.html" and html.parent == ROOT
        hash_new = patch_hash_nav(text, is_index)
        if hash_new != text:
            hash_patched += 1
            text = hash_new

        if text != original:
            html.write_text(text, encoding="utf-8")

    print(f"Removed {removed} 'All safari packages' mobile links")
    print(f"Patched favicon/manifest on {favicon_patched} pages")
    print(f"Added hash-nav script on {hash_patched} page(s)")


if __name__ == "__main__":
    main()
