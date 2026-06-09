---
type: is
id: is-01ktnfk8hmkeeje5ydpfaf8ghp
title: Package & deploy the site to GitHub Pages
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-06-09T06:02:27.251Z
updated_at: 2026-06-09T06:02:27.251Z
---
Finish production deployment of site/ to GitHub Pages. Steps: (1) Enable Pages (repo Settings -> Pages -> Build and deployment -> Source: GitHub Actions) -- the workflow .github/workflows/pages.yml cannot do this. (2) After merging PR #18 to main, confirm the Deploy workflow runs and publishes site/. (3) Decide on a custom domain (CNAME) if wanted. (4) Bump the pinned jsDelivr URLs in site/index.html (currently @v0.1.4) to the current release; grep site/index.html for cdn.jsdelivr.net. See docs/website.runbook.md section 5.
