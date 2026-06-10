# Migration: Host the Site at ojoshe.com/planetaire

**Date:** 2026-06-10

**Author:** jlevy (with Claude Code)

**Status:** In progress

## Overview

The static site in [`site/`](../../../../site/) moves from its own GitHub Pages deploy
(`https://jlevy.github.io/planetaire/`) to `https://ojoshe.com/planetaire/`, a subpath
of the author’s website.
That URL becomes the site’s **only** home: planetaire stops self-publishing, and the old
`jlevy.github.io/planetaire` URL is retired without a redirect (the site was never
widely shared, so there are no legacy links to preserve).

ojoshe.com is maintained in a separate (private) repository.
From planetaire’s point of view the contract is small:

1. ojoshe.com serves this repo’s committed `site/` directory, as-is, under
   `/planetaire/`.
2. Its deploy workflow listens for a `repository_dispatch` event of type
   **`planetaire-release`**; on receiving one it picks up the latest `site/` content and
   redeploys.
3. ojoshe.com owns the domain, DNS, and HTTPS.

## Why this is safe

- `https://ojoshe.com/planetaire/` was confirmed live (homepage, `compare.html`, and
  `assets/social-card.png` all serving) on 2026-06-10, **before** any cutover work in
  this repo, so there is no serving gap.
- `site/` is self-contained and uses **relative** internal links, so it works unchanged
  under a `/planetaire/` subpath.
  The only host-absolute URLs in the site are the canonical/social metadata URLs
  (repointed below) and the jsDelivr font URLs, which are host-independent and stay as
  they are.

## Plan

Tracked under epic **`plt-s5gz`**; every bead links to this spec.

### 1. Repoint canonical and social URLs (`plt-i4dh`)

Replace `https://jlevy.github.io/planetaire` with `https://ojoshe.com/planetaire` in
`site/index.html` and `site/compare.html`. This covers exactly five tags per page:
`canonical`, `og:url`, `og:image`, `og:image:secure_url`, and `twitter:image`.

### 2. Update the website runbook (`plt-6uxg`)

Point [`docs/website.runbook.md`](../../../website.runbook.md) at the new host: the
canonical-URL table and social-card URL in §3, and rewrite §6 (Deploy) to describe the
dispatch-based flow instead of the retired Pages workflow.

### 3. Notify ojoshe.com on site changes (`plt-3m2k`)

Add `.github/workflows/notify-ojoshe.yml`: on push to `main` touching `site/**`, and on
published releases, fire the `planetaire-release` dispatch so ojoshe.com redeploys
automatically.

Requires a repo secret **`OJOSHE_DISPATCH_TOKEN`** — a fine-grained PAT scoped to the
ojoshe repo with **Contents: read/write** — because the default `GITHUB_TOKEN` cannot
dispatch cross-repo.
Creating the PAT and adding the secret is a manual owner step (`plt-hbpe`).

### 4. Retire the self-deploy (`plt-aiz4`)

- Delete `.github/workflows/pages.yml` (in the same PR as steps 1–3).
- After the merge has propagated to ojoshe.com (the new canonicals are live there),
  disable Pages in this repo: **Settings → Pages → Source: None**, so
  `jlevy.github.io/planetaire` stops serving.
- Set the repo’s website field (homepage) to `https://ojoshe.com/planetaire/` (this also
  subsumes `plt-dwes`).

### 5. Verify (`plt-i241`)

- `curl -s https://ojoshe.com/planetaire/ | grep canonical` →
  `https://ojoshe.com/planetaire/` (and the same for `compare.html`).
- The merge to `main` triggered a `Notify ojoshe.com to rebuild` Actions run that
  succeeded, and ojoshe.com picked up the change.
- `https://jlevy.github.io/planetaire/` no longer serves.
- A share-preview check (e.g. an unfurl debugger) resolves the social card at the new
  URL.

## Sequencing

Steps 1–3 land together in one PR. The dispatch secret (`plt-hbpe`) should be in place
**before** that PR merges so the merge itself propagates the new canonicals to
ojoshe.com; Pages is disabled (`plt-aiz4` settings step) only after that propagation is
confirmed. Verification (`plt-i241`) closes the epic.

## Non-Goals

- No redirect stub at the old URL (no legacy links to preserve).
- No path rewriting or build step for `site/` — it stays committed, relative-linked
  static source.
- No documentation here of how ojoshe.com itself builds or deploys; that lives in its
  own (private) repo. This spec records only the public contract above.

## Supersedes

- Epic `plt-ecqy` ("Optional custom domain for GitHub Pages launch") — closed as
  superseded: the site gets a custom-domain home via ojoshe.com rather than a
  planetaire-specific domain on GitHub Pages.
- Task `plt-dwes` ("Publish live Pages URL in repository metadata") — folded into step
  4\.

## References

- [`docs/website.runbook.md`](../../../website.runbook.md) — content sync and deploy
  runbook (§6 rewritten by this plan).
- Prior publication work:
  [`plan-2026-06-05-finalize-and-publish.md`](plan-2026-06-05-finalize-and-publish.md).
