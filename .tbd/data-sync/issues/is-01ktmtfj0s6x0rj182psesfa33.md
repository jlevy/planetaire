---
type: is
id: is-01ktmtfj0s6x0rj182psesfa33
title: "Site: Light/Dark segments shorter than CTA buttons due to button line-height"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-06-08T23:53:25.784Z
updated_at: 2026-06-08T23:54:52.273Z
closed_at: 2026-06-08T23:54:52.272Z
close_reason: null
---
Follow-up to plt-d0wd. After matching font-size and padding, the .ts-opt segments are still shorter than .btn because <button> elements do not inherit line-height (UA default ~normal 1.2) while .btn (an <a>) inherits body line-height 1.6. Fix: set line-height: 1.6 on .ts-opt so segment height equals the CTA buttons.
