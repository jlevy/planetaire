---
type: is
id: is-01ktnfk8hmkeeje5ydpfaf8ghp
title: Package & deploy the site to GitHub Pages
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-06-09T06:02:27.251Z
updated_at: 2026-06-09T06:33:01.164Z
---
Finish production deployment of site/ to GitHub Pages. Steps: (1) Enable Pages (repo Settings -> Pages -> Build and deployment -> Source: GitHub Actions) -- the workflow .github/workflows/pages.yml cannot do this. (2) After merging PR #18 to main, confirm the Deploy workflow runs and publishes site/. (3) Decide on a custom domain (CNAME) if wanted. (4) Bump the pinned jsDelivr URLs in site/index.html (currently @v0.1.4) to the current release; grep site/index.html for cdn.jsdelivr.net. See docs/website.runbook.md section 5.

## Notes

Package/deploy code path is ready in PR #18: site/ remains self-contained, pages.yml deploys site/ from main, latest release is v0.1.4 so pinned jsDelivr PDF URLs are already current, and no CNAME was added because no custom domain was specified. GitHub Pages is not configured yet (gh api repos/jlevy/planetaire/pages returns 404); remaining work is repository Settings -> Pages -> Source: GitHub Actions, then merge PR #18 to main and verify the Pages deploy.
