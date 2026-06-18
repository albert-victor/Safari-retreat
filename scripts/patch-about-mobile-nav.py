#!/usr/bin/env python3
"""Restore full mobile navigation on about.html."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABOUT = ROOT / "about.html"

spec = importlib.util.spec_from_file_location("pt", ROOT / "scripts" / "page-templates.py")
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

MOBILE_START = '  <div class="mobile-menu" id="mobileMenu"'
MOBILE_END = '  </div>\n\n  <main id="main-content">'


def mobile_block() -> str:
    prefix = ""
    circuit_prefix = "circuits/"
    category_prefix = "categories/"
    mobile_circuit_nav = pt.build_circuit_nav(
        circuit_prefix, "destinations/", "kenya.html", "uganda.html", "rwanda.html", mobile=True
    )
    safari_nav = pt.MOBILE_SAFARI_CATEGORY_NAV.format(prefix=prefix, category_prefix=category_prefix)
    return f"""  <div class="mobile-menu" id="mobileMenu" aria-hidden="true" role="dialog" aria-label="Mobile navigation">
    <div class="mobile-menu__overlay" id="mobileMenuOverlay"></div>
    <div class="mobile-menu__panel">
      <button class="mobile-menu__close" id="mobileMenuClose" aria-label="Close navigation menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
      <div class="mobile-menu__theme">
        <button type="button" class="theme-toggle" id="themeToggleMobile" aria-label="Switch theme" aria-pressed="false">
          <i class="fa-solid fa-moon theme-toggle__icon theme-toggle__icon--moon" aria-hidden="true"></i>
          <i class="fa-solid fa-sun theme-toggle__icon theme-toggle__icon--sun" aria-hidden="true"></i>
        </button>
      </div>
      <nav aria-label="Mobile navigation">
        <ul class="mobile-menu__list">
          <li><a href="index.html#home" class="mobile-menu__link">Home</a></li>
          <li class="mobile-menu__item mobile-menu__item--dest">
            <button type="button" class="mobile-menu__link mobile-menu__dest-trigger" aria-expanded="false" aria-controls="mobileDestPanel">
              <span>Circuits</span>
              <span class="mobile-menu__dest-plus" aria-hidden="true">+</span>
              <i class="fa-solid fa-chevron-down mobile-menu__dest-chevron" aria-hidden="true"></i>
            </button>
            <div class="mobile-menu__dest-panel" id="mobileDestPanel">
              <a href="circuits/index.html" class="mobile-menu__dest-overview">View all circuits</a>
              <ul class="mobile-menu__dest-grid">
{mobile_circuit_nav}
              </ul>
            </div>
          </li>
          <li><a href="about.html" class="mobile-menu__link active">About Us</a></li>
          <li><a href="index.html#experiences" class="mobile-menu__link">Experiences</a></li>
          <li class="mobile-menu__item mobile-menu__item--dest">
            <button type="button" class="mobile-menu__link mobile-menu__dest-trigger" aria-expanded="false" aria-controls="mobileSafariPanel">
              <span>Safaris</span>
              <span class="mobile-menu__dest-plus" aria-hidden="true">+</span>
              <i class="fa-solid fa-chevron-down mobile-menu__dest-chevron" aria-hidden="true"></i>
            </button>
            <div class="mobile-menu__dest-panel" id="mobileSafariPanel">
              <ul class="mobile-menu__dest-grid">
{safari_nav}
              </ul>
            </div>
          </li>
          <li><a href="index.html#accommodation" class="mobile-menu__link">Accommodation</a></li>
          <li><a href="index.html#gallery" class="mobile-menu__link">Gallery</a></li>
        </ul>
      </nav>
      <a href="index.html#bookingForm" class="btn btn--primary mobile-menu__cta">Book Your Safari</a>
    </div>
  </div>

  <main id="main-content">"""


def main() -> None:
    text = ABOUT.read_text(encoding="utf-8")
    start = text.find(MOBILE_START)
    end = text.find(MOBILE_END)
    if start == -1 or end == -1:
        raise SystemExit("Could not locate mobile menu block in about.html")
    new_text = text[:start] + mobile_block() + text[end + len(MOBILE_END) :]
    ABOUT.write_text(new_text, encoding="utf-8")
    print("Patched about.html with full mobile navigation")


if __name__ == "__main__":
    main()
