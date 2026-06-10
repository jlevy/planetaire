---
type: is
id: is-01ktrbead7snne8xe5714w6vxe
title: Repoint canonical/social URLs to ojoshe.com/planetaire
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-06-10-migrate-hosting-to-ojoshe.md
labels:
  - hosting
dependencies:
  - type: blocks
    target: is-01ktrbeb9r53mqxn1g831yt2mc
parent_id: is-01ktrbea4hppvkg87tkehkev1v
created_at: 2026-06-10T08:47:34.310Z
updated_at: 2026-06-10T08:50:27.663Z
closed_at: 2026-06-10T08:50:27.662Z
close_reason: "Done in PR #23: 5 metadata URL tags repointed per page in site/index.html and site/compare.html"
---
In site/index.html and site/compare.html, replace https://jlevy.github.io/planetaire with https://ojoshe.com/planetaire in the 5 absolute-URL tags per page: canonical, og:url, og:image, og:image:secure_url, twitter:image. jsDelivr font URLs and GitHub repo links stay.
