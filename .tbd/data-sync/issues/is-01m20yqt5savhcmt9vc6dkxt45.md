---
type: is
id: is-01m20yqt5savhcmt9vc6dkxt45
title: Tooling dirties uv.lock and .tbd/config.yml during a release
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T16:48:36.536Z
updated_at: 2026-09-08T16:48:36.536Z
---
Two files get modified as a side effect of running the release, so a release that is
meant to show only its own diff shows unrelated churn, and the working-tree cleanliness
guards in scripts/release.py see noise.

1. `uv run` rewrites uv.lock. The rewrite is driven by the operator's uv configuration
   (`[options.exclude-newer-package]` entries appear/disappear), not by anything in the
   repo, so it happens on any `uv run` here — `make lint`, `make test`, a release.

   Partly addressed in plt-0204: scripts/release.py now invokes everything through
   `uv run --frozen`, so a release no longer touches the lockfile. The rest of the
   repo's entry points (the Makefile targets, CI) still use a plain `uv run`. Decide
   whether `--frozen` should be the default everywhere, or whether `uv.lock` churn from
   operator-level uv config should be handled another way.

2. `tbd` rewrites .tbd/config.yml. Running any tbd command with tbd 0.8.1 migrates the
   committed config from `tbd_format: f04` to `f08` and rewrites its comments, so
   `tbd show` mid-release leaves a modified file behind. The migration has to land
   eventually, but publishing f08 from one checkout could break other checkouts running
   an older tbd, so it wants a deliberate commit: confirm the tbd version everyone uses,
   then commit the migrated config on its own.
