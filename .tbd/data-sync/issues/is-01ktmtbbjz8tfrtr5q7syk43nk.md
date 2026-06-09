---
type: is
id: is-01ktmtbbjz8tfrtr5q7syk43nk
title: "Site: re-sync homepage with README (Why header removed, several h3s promoted to h2)"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-06-08T23:51:08.126Z
updated_at: 2026-06-08T23:54:51.761Z
closed_at: 2026-06-08T23:54:51.761Z
close_reason: null
---
Per site/sync-process.runbook.md, the site homepage half is downstream of README.md. The README changed: the 'Why' wrapper header was removed and several h3 sub-headers were promoted to h2 major sections. Re-mirror that structure into site/index.html: drop the 'Why' h2 wrapper, and promote the affected About/section headings from h3 to h2 to match the README's current heading hierarchy. Update the top nav anchors if section ids change.
