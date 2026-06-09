---
type: is
id: is-01ktmx5b9g1xxfkp7amym0gyy7
title: "Site: inconsistent line-heights across text samples; standardize to two"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-06-09T00:40:16.943Z
updated_at: 2026-06-09T00:43:21.210Z
closed_at: 2026-06-09T00:43:21.210Z
close_reason: null
---
site/style.css uses several different line-heights (body 1.6, pre 1.55, ladder 1.5, h2 1.3, h3 1.4, waterfall 1.05, hero 1.05/1.5/1.6). Some text samples read too tight. Standardize to at most two reading line-heights, matching the PDF specimen: (1) standard 1.5 for prose/text samples (specimen leading 0.8em ≈ 1.5), (2) a slightly tighter value (~1.4) for terminal/code panels. Keep intentional demo exceptions (size-waterfall stack, hero wordmark) as-is. Add --lh / --lh-tight tokens.
