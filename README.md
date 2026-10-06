# Gürkan Çamok — professional digital health portfolio

Live site: https://gurkancamok.github.io/

## Purpose

An evidence-led professional portfolio explaining personal technical contributions, implementation context, independent media coverage and the current boundaries of digital health projects.

## Content

- Six product case studies with development attribution and actual project stage.
- An evidence register separating study results, institutional access figures and prototype demonstrations.
- Published project features and independent reporting separated from authored articles.
- KTM October 2026 feature with the original PDF, previews of pages 39 and 41 and publisher-hosted contents link.
- Professional profile, accessible mobile navigation, social previews and sitemap.
- An awards gallery using original photographs, with arrow buttons, keyboard navigation and touch swipes.
- Legacy redirect to preserve the former insulin application URL.

The existing `insulin-infusion/index.html` application is preserved. Portfolio edits do not modify its clinical rules.

## Local preview

Run `python3 -m http.server 8765` from the repository directory.

## Website verification

Run `python3 tests/static-check.py` for content and asset checks. Run `node tests/site-check.mjs` with Playwright and Chromium installed for the full browser suite. A noindex `/tests/viewport.html` fixture supports manual responsive verification. The suite checks responsive layout, mobile navigation, awards-gallery navigation and captions, internal links, image loading, metadata and structured data.

These are website checks, not clinical algorithm validation. Operational figures and publication status are documented on `/evidence/` and must remain accurate when the portfolio is updated.

## Update content

`build_site.py` generates the portfolio HTML. The shared presentation and mobile-navigation behaviour are in `assets/site.css` and `assets/site.js`. Awards-gallery entries are in `recognition_gallery.json`; its controls are in `assets/gallery.js`. Add original photographs with accurate dates, award titles, captions and alternative text. Re-run the generator after changing content and refresh version dates only when applicable.
