# Static site release validation

Use this checklist for every meaningful `site/` release or GitHub Pages deploy. The
automated checks should stay small and fast; the manual pass covers the judgment calls
that static tools cannot make reliably.

## Automated gate

Start from a clean dependency install:

```bash
npm ci
uv sync --all-extras
```

Run the site gate:

```bash
npm run site:lint
```

That command checks:

- Biome formatting and lint rules for committed CSS and JavaScript;
- `tsc --checkJs` over the plain JavaScript in `site/`;
- `html-validate` recommended HTML rules;
- local HTML/CSS asset references and local fragment links;
- JavaScript syntax for external and inline scripts;
- a `jsdom` runtime smoke test that executes the pages and verifies dynamic DOM
  invariants on the homepage and comparator.

Run the full repository gate before release:

```bash
make lint-check
uv run pytest
```

If fonts, specimen data, or vendored web fonts changed, also run the relevant font build
checks from `docs/fonts-build-and-release.md`.

When adding or upgrading npm dev tools, use exact versions and confirm the selected package
version has been published for at least 14 days before committing the lockfile.

## Manual browser pass

Serve the committed static files:

```bash
npm run site:serve
```

Open `http://127.0.0.1:8765/` and `http://127.0.0.1:8765/compare.html`.

Check these items before approving a release:

- Browser console is clean on both pages after reload.
- Homepage loads Planetaire Mono Text, not a fallback font; weights and italics render.
- Hero, primary nav, tabs, theme switch, anchors, footer, and external links behave as
  expected.
- About, Samples, and Installation panels all contain the expected content and no stale
  placeholder text.
- Comparator renders default proof cards; sample, size, weight, style, card/page view,
  font selection, show-labels, popular/all/clear controls all respond.
- Desktop width and a narrow mobile width have no horizontal overflow or text collisions.
- Keyboard tab order reaches nav, theme controls, tabs, form controls, and proofs with a
  visible focus state.
- Release links point at the intended version: latest release, specimen PDF, jsDelivr
  versioned assets, and GitHub repository links.
- README, PDF specimen, and site agree for any prose, metrics, install instructions, or
  source-of-truth values touched by the change.

## When to do a heavier pass

The default smoke test is intentionally not a full browser automation suite. Add a
temporary or permanent Playwright-style browser pass only when a change depends on real
layout, canvas, font measurement, animation timing, media loading, or cross-browser
behavior that `jsdom` cannot observe.

For ordinary copy, CSS, static asset, and plain JavaScript changes, the automated gate plus
the manual browser pass above is the expected release floor.

## Post-deploy check

After merging to `main`, confirm the Pages workflow is green and spot-check the live Pages
URL with the same two-page browser pass. If the live site differs from local preview, check
cache-busted CSS/JS query strings and versioned CDN links first.
