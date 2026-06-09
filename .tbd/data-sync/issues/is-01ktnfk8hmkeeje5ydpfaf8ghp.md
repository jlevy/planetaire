---
type: is
id: is-01ktnfk8hmkeeje5ydpfaf8ghp
title: Launch GitHub Pages site from current repo
kind: epic
status: open
priority: 1
version: 12
labels:
  - deployment
  - github-pages
  - no-custom-domain
dependencies: []
child_order_hints:
  - is-01ktpq427atbwhje6pqqdttbh5
  - is-01ktpq808dh36nzxhr4dx137ah
  - is-01ktpq4pjbdyctq80hg3tpn28q
  - is-01ktpq52a6nvwpwre9nv3skh25
  - is-01ktpq5cwkdcrm8b5rt75xcyxg
  - is-01ktpq5qnkdhfg2zq2mskars8j
  - is-01ktpq62apsg7akz5j826dnkwn
created_at: 2026-06-09T06:02:27.251Z
updated_at: 2026-06-09T17:35:41.526Z
---
Deploy PR #18 as the first public GitHub Pages launch for jlevy/planetaire without a custom domain. Target URL: https://jlevy.github.io/planetaire/. Current status on 2026-06-09: PR #18 is open as a draft from static-site to main, mergeable, and remote CI is green; GitHub repo metadata reports has_pages=false, so Pages is not enabled yet; current local checkout has uncommitted site/compare.css and site/compare.html changes plus unrelated tbd/Codex/flowmark files. This epic tracks everything needed to get the site deployed and fully verified as soon as the PR merges.

## Notes

Package/deploy code path is ready in PR #18: site/ remains self-contained, pages.yml deploys site/ from main, latest release is v0.1.4 so pinned jsDelivr PDF URLs are already current, and no CNAME was added because no custom domain was specified. GitHub Pages is not configured yet (gh api repos/jlevy/planetaire/pages returns 404); remaining work is repository Settings -> Pages -> Source: GitHub Actions, then merge PR #18 to main and verify the Pages deploy.
