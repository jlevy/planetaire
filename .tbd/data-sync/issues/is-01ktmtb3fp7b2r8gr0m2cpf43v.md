---
type: is
id: is-01ktmtb3fp7b2r8gr0m2cpf43v
title: "Site: paragraph spacing is less than a full line height (specimen uses a blank line)"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-06-08T23:50:59.828Z
updated_at: 2026-06-08T23:54:51.400Z
closed_at: 2026-06-08T23:54:51.399Z
close_reason: null
---
In site/style.css, --space-para is 1.1rem so the gap between paragraphs is smaller than one line. The PDF specimen uses one full blank line between paragraphs (par spacing ~2.3em vs leading). Fix: set the inter-paragraph gap to a full line height (~1.6rem, matching line-height: 1.6) so paragraphs read like the specimen.
