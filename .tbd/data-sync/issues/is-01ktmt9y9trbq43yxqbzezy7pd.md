---
type: is
id: is-01ktmt9y9trbq43yxqbzezy7pd
title: "Site: h3 sub-header font-size can mismatch body text (rem vs hardcoded px)"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-06-08T23:50:21.753Z
updated_at: 2026-06-08T23:54:51.222Z
closed_at: 2026-06-08T23:54:51.221Z
close_reason: null
---
In site/style.css, body is set to a hardcoded font-size: 16px, while h3 (and the rest of the type scale) use --fs-body: 1rem, which resolves against the ROOT (html) font-size, not body. If the browser/user root font-size is not 16px, h3 renders at a different size than body text, so the sub-headers look too small even though they are 'the same' token-wise. Fix: anchor the rem scale (html { font-size: 16px }) and set body to use var(--fs-body) so body and h3 are both 1rem and always equal.
