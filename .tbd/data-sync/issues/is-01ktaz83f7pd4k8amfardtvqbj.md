---
type: is
id: is-01ktaz83f7pd4k8amfardtvqbj
title: Shrink/relocate the 13MB golden manifest; reconsider committed source TTFs
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:20.071Z
updated_at: 2026-06-05T16:13:48.036Z
closed_at: 2026-06-05T16:13:48.035Z
close_reason: Manifest slimmed (13.2MB->2.0MB); source TTFs reviewed (~32MB total, fine) and kept vendored by decision (no LFS). Documented in runbook.
---
fonts/golden/manifest.json is ~13MB of verbose per-glyph JSON (12k glyphs x 8 variants) committed to git; ~35MB of source TTFs are also committed (Hack ExtraBold ~4.3MB each). Compact the manifest (hash-of-hashes per variant + gzip/CBOR, or CI fixture) and, once real downloads exist, fetch sources with checksums or Git LFS to keep clones light. See docs/engineering-review.md §5.

## Notes

DONE. Manifest gzipped+completed (13.2MB->2.0MB, 8 variants). Source TTFs: reviewed total repo size = ~32MB tracked / ~33MB .git (Hack ~24MB + B612 ~5MB) — unremarkable for a font repo. Decision: KEEP VENDORED, just commit (NO Git LFS), for reproducible offline builds + no FontForge at build time. Documented in build-assets.runbook.md appendix.
