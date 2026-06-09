---
type: is
id: is-01ktps8td58gyhnvs152fpppys
title: Optional custom domain for GitHub Pages launch
kind: epic
status: open
priority: 1
version: 1
labels:
  - deployment
  - github-pages
  - custom-domain
dependencies: []
created_at: 2026-06-09T18:10:45.279Z
updated_at: 2026-06-09T18:10:45.279Z
---
Optional track if a Planetaire domain is registered before or soon after PR #18 launches. Goal: move the public site from the built-in project URL (https://jlevy.github.io/planetaire/) to a custom domain safely, with DNS, HTTPS, redirects, README/repo links, and live QA tracked explicitly. GitHub docs recommend verifying the custom domain before adding it to the repository to avoid takeover risk; for GitHub Actions Pages, a CNAME file is not created/required and existing CNAME files are ignored, so the repo setting/API is the source of truth.
