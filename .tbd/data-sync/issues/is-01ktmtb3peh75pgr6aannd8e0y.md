---
type: is
id: is-01ktmtb3peh75pgr6aannd8e0y
title: "Site: Light/Dark toggle segments render smaller than the CTA buttons"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-06-08T23:51:00.045Z
updated_at: 2026-06-08T23:54:51.579Z
closed_at: 2026-06-08T23:54:51.578Z
close_reason: null
---
The .ts-opt segments set font-size: var(--fs-body) (1rem, root-relative) while .btn inherits body's hardcoded 16px. Same root cause as plt-gx00: if the browser root font-size != 16px, the toggle is smaller than the Download/Specimen buttons. Fixed by anchoring the rem scale to 16px (html { font-size: 16px }) so 1rem == body. Verify segment height matches .btn after the anchor fix.
