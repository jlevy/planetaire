# Website runbook

How the static site in [`site/`](../site/) is structured, kept in sync with the other
formats, refreshed, previewed, and deployed.

The same content lives in **three formats**, and they must agree:

1. **`README.md`** — the GitHub landing page (prose, tables, config snippets).
2. **The PDF specimen** — `docs/specimen/*.typ` → `planetaire-mono-specimen.pdf`.
3. **The static site** — `site/index.html` + `site/style.css`, deployed to GitHub Pages.

There is **no generator** — all three are edited by hand. (The old `planetaire build
site` / `build html-specimen` recipes were retired; `site/` is now committed source, not
build output.) This runbook is the manual process that keeps them consistent.

For the site's *visual* rules (colors, type scale, headings, spacing), see
[`site/design-system.md`](../site/design-system.md). This runbook covers **content
provenance, assets, and deployment** only.

---

## 1. Site structure

`site/` is self-contained and deployable as a GitHub Pages root — no `../` references:

```
site/
  index.html                  # the whole page (homepage + live specimen)
  style.css                   # all styling; see site/design-system.md
  design-system.md            # the CSS/visual design system (co-located with style.css)
  assets/
    little-planet.svg         # vendored from docs/images/ (see §3)
  fonts/
    planetaire-mono-text.css  # @font-face for the 10 Text faces
    PlanetaireMonoText-*.woff2 # vendored from the Text release (see §3)
```

The page renders **in the actual font** (the Text web subset), which is the whole point of
having a site rather than the README's screenshots.

---

## 2. Three-way content sync

### Source of truth per content type

Edit the **source of truth** first, then mirror into the other two formats. Never edit a
downstream copy and expect it to flow back.

| Content | Source of truth | In `README.md` | In the PDF specimen | In `site/` |
| --- | --- | --- | --- | --- |
| **Prose** (About B612 / About Planetaire / Personal Note, credits, license summary) | `README.md` | owns | mirrored on the cover + About pages (`planetaire-mono-specimen.typ`) | mirrored as `<p>`/`<h2>` sections |
| **Tables & config** (weights, download, terminal-config snippets) | `README.md` | owns | partial (spec page) | mirrored as `<table>` / `<pre class="code">` |
| **Typeface spec values** (UPM, metrics, glyph counts, advance width) | the **built fonts** → recorded in `planetaire-mono-specimen.typ` | mentioned in prose | owns (the spec page) | mirrored in the `.specgrid` block |
| **Type demos & palettes** (text samples, Turing/RFC passages, weight ladder, size waterfall, legibility pairs, dotted zero, orbit-code, terminal mockup, QA grids, dark/light palettes) | `docs/specimen/content.typ` | rendered as PNGs via `card.typ` → `docs/images/*.png` | rendered by `planetaire-mono-specimen.typ` | re-implemented in HTML/CSS |
| **Section grouping** | `site/index.html` | flat README order | own order (print flow) | grouped into About / Samples / Installation tabs |

`content.typ` is shared by the PDF specimen **and** the README's PNG card images
(`card.typ` → `make images`), so a demo change there flows to both automatically; only the
site's HTML copy is manual.

### When you change X, update Y

| If you change… | …then update |
| --- | --- |
| **Prose** in `README.md` | the matching About/section text on the specimen cover/About pages (`.typ`), **and** the matching `<h2>`/`<p>` block in `site/index.html` (ids and order already match the README headings) |
| **A table or config snippet** in `README.md` | the corresponding `<table>` / `<pre class="code">` in `site/index.html` (keep cell text verbatim) |
| **A type demo** (e.g. the weight-ladder string, the orbit-code tokens, legibility pairs, the QA character rows) in `content.typ` | run `make images` (refreshes the README PNGs) **and** re-mirror the demo in `site/index.html`. The QA character rows live in the `<script>` at the bottom of `index.html` (the `rows` object). |
| **A palette** (`pal-dark` / `pal-light`) in `content.typ` | the `--l-*` / `--d-*` CSS vars at the top of `site/style.css` (a 1:1 copy of the hex values) |
| **Spec values** (metrics, glyph counts) because the font was rebuilt | the spec page in `planetaire-mono-specimen.typ` **and** the `.specgrid` block in `site/index.html` (hand-copied numbers — re-check them all) |
| **Section order** in `README.md` | keep matching prose/table/demo content in `site/index.html`; preserve the site's About / Samples / Installation tab grouping unless the site IA is intentionally revised |
| **The fonts** (new release) | re-vendor `site/fonts/` (see §3) and re-check the spec numbers |

### Intentional divergences (do NOT "fix" these)

The site is deliberately **not** a pixel copy of the PDF:

- **Text subset, not Extended.** The site loads `Planetaire Mono Text` (web-recommended,
  ~65 KB/weight, no icons). So the site does **not** render the Nerd Font icon grid, and
  the terminal mockup **omits the icon column**. To show icons on the web, vendor the
  `PlanetaireMono-Extended` web fonts and scope them to those sections.
- **Live type, not screenshots.** The site does *not* reproduce the README's PNG specimen
  images (`docs/images/*-dark.png` / `*-light.png`) — those samples are live text in the
  site's Samples tab. The README's `## Specimens` gallery has no site counterpart.
- **One theme toggle, not dark/light pairs.** Unlike the PDF's fixed dark+light specimen
  pairs, the site's code/terminal panels follow the page theme: a single `.panel` whose
  syntax colors switch via the `--syn-*` vars (light ↔ dark).

---

## 3. Refreshing vendored assets

Two things are vendored into `site/` from sources elsewhere in the repo / releases.

**Planet graphic** — `site/assets/little-planet.svg` is a copy of
`docs/images/little-planet-vector-trace-v3.svg` (the source of truth, also used by the
specimen header and README banner). If that SVG changes:

```bash
cp docs/images/little-planet-vector-trace-v3.svg site/assets/little-planet.svg
```

**Web fonts** — `site/fonts/` is a copy of the `web/` folder from the `PlanetaireMono-Text`
release archive (10 WOFF2 + `planetaire-mono-text.css`). Vendored because jsDelivr's `/gh/`
path can't unpack the release `.tar.xz`, and the built fonts aren't otherwise in the repo.
Refresh after a new release:

```bash
gh release download --pattern 'PlanetaireMono-Text.tar.xz' --repo jlevy/planetaire -O /tmp/t.tar.xz
tar -xf /tmp/t.tar.xz -C /tmp
cp /tmp/web/*.woff2 /tmp/web/planetaire-mono-text.css site/fonts/
```

The **Specimen PDF** links and a couple of asset links use pinned jsDelivr URLs
(`…/gh/jlevy/planetaire@vX.Y.Z/…`). Bump the version in those `href`s when you cut a release
(grep `site/index.html` for `cdn.jsdelivr.net`).

---

## 4. Local preview

It's a static page — just open it:

```bash
open site/index.html          # macOS; or drag into a browser
```

Fonts and the planet load by relative path, so `file://` works with no server.

---

## 5. Deploy (GitHub Pages)

Deployment is automated by [`.github/workflows/pages.yml`](../.github/workflows/pages.yml):
on push to `main` that touches `site/**`, it uploads `site/` as the Pages artifact and
publishes it. Enable it once under **Settings → Pages → Build and deployment → Source:
GitHub Actions**.

To deploy a content change: make the edits (keeping the three formats in sync per §2),
merge to `main`, and the workflow publishes the updated `site/`. You can also trigger it
manually from the Actions tab (`workflow_dispatch`).
