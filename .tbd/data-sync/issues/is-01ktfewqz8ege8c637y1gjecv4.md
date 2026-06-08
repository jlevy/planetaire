---
type: is
id: is-01ktfewqz8ege8c637y1gjecv4
title: "Port remaining PR #2 fixes into PR #4 (carlosedp link + verify rest)"
kind: task
status: closed
priority: 2
version: 5
labels: []
dependencies:
  - type: blocks
    target: is-01ktfewra77jn0fhwa0wx96n5v
  - type: blocks
    target: is-01ktfewpdcygyn84mgdfqw3jk6
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:42.792Z
updated_at: 2026-06-06T22:13:47.930Z
closed_at: 2026-06-06T22:13:47.930Z
close_reason: Ported carlosedp link fix (verified /carlosedp/b612 live, B612-Mono-Liga-NerdFont is 404). Confirmed variant counts(8/4), pangram 'pondent', CLI/ops hardening already present. generate_showcase.py obsolete/removed.
---
Diff PR #2 (claude/awesome-thompson-kV4n7) against current and reapply anything still relevant:
- carlosedp credit link: current README uses github.com/carlosedp/B612-Mono-Liga-NerdFont; PR#2 commit 490a42b changed it to github.com/carlosedp/b612 ('404 -> live repo'). Verify which URL is live, then apply the correct one.
- Already ported (verify): variant counts (8/4), pangram 'pondent', CLI/ops hardening (cli.py StrEnum/main/ValidationError, regression trivial-vs-changed, merge setGlyphOrder/GSUB NotImplementedError, embolden repr()).
- Obsolete, skip: scripts/generate_showcase.py (removed; images now via Typst). tbd v0.2.2 upgrade (already current).
