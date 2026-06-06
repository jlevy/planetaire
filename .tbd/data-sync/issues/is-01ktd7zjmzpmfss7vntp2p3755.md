---
type: is
id: is-01ktd7zjmzpmfss7vntp2p3755
title: "cli: validated --format StrEnum, clean CLIError rendering, ValidationError wiring"
kind: task
status: closed
priority: 2
version: 2
labels:
  - pr2
dependencies: []
created_at: 2026-06-06T01:15:26.751Z
updated_at: 2026-06-06T01:15:28.754Z
closed_at: 2026-06-06T01:15:28.754Z
close_reason: "Implemented in commit dda3728 (port of PR #2 clear wins)"
---
--format was a raw str (invalid values silently treated as text); app() ran without catching CLIError (raw traceback). Added OutputFormat StrEnum, a main() entry point that renders CLIError cleanly with the right exit code, wired ValidationError into validate, and pointed the script entry at cli:main. From PR #2 review.
