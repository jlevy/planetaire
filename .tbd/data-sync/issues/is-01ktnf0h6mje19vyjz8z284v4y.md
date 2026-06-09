---
type: is
id: is-01ktnf0h6mje19vyjz8z284v4y
title: Variable-font spike (single 400-800 WOFF2)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:13.524Z
updated_at: 2026-06-09T05:52:13.524Z
---
A single variable WOFF2 spanning weight 400-800 would beat ten static files for sites wanting the whole ramp and lets the browser interpolate intermediate weights. Real build change: the weight masters are partly FontForge-emboldened, not interpolation-ready, so this needs a spike. For the common two-weight marketing case, static + unicode-range already wins. Ref 6.7. Related: plt-8cyc (OTF/CFF output).
