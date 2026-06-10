---
type: is
id: is-01ktps8td58gyhnvs152fpppys
title: Optional custom domain for GitHub Pages launch
kind: epic
status: closed
priority: 1
version: 2
labels:
  - deployment
  - github-pages
  - custom-domain
dependencies: []
created_at: 2026-06-09T18:10:45.279Z
updated_at: 2026-06-10T08:47:36.487Z
closed_at: 2026-06-10T08:47:36.486Z
close_reason: "Superseded by plt-s5gz: site is getting its custom-domain home at ojoshe.com/planetaire instead of a planetaire-specific domain on GitHub Pages. See docs/project/specs/active/plan-2026-06-10-migrate-hosting-to-ojoshe.md"
---
Optional track if a Planetaire domain is registered before or soon after PR #18 launches. Goal: move the public site from the built-in project URL (https://jlevy.github.io/planetaire/) to a custom domain safely, with DNS, HTTPS, redirects, README/repo links, and live QA tracked explicitly. GitHub docs recommend verifying the custom domain before adding it to the repository to avoid takeover risk; for GitHub Actions Pages, a CNAME file is not created/required and existing CNAME files are ignored, so the repo setting/API is the source of truth.
