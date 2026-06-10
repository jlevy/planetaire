---
type: is
id: is-01ktpq5qnkdhfg2zq2mskars8j
title: Smoke test live GitHub Pages project URL
kind: task
status: closed
priority: 1
version: 3
labels:
  - deployment
  - github-pages
  - qa
dependencies:
  - type: blocks
    target: is-01ktpq62apsg7akz5j826dnkwn
parent_id: is-01ktnfk8hmkeeje5ydpfaf8ghp
created_at: 2026-06-09T17:34:07.026Z
updated_at: 2026-06-10T10:05:08.471Z
closed_at: 2026-06-10T10:05:08.470Z
close_reason: "Done: live site was verified serving; superseded by ojoshe.com migration verification (plt-i241)"
---
After the Pages workflow succeeds, test the live project URL without a custom domain: https://jlevy.github.io/planetaire/. Verify / and /compare.html over HTTPS, relative assets under /planetaire/ (style.css, compare.css, compare.js, assets/little-planet.svg, fonts/planetaire-mono-text.css, WOFF2 files), homepage tabs/hash anchors, theme persistence, comparator controls, desktop and mobile viewports, no console errors, no horizontal overflow, and that Download/latest release and pinned v0.1.4 Specimen PDF links resolve.
