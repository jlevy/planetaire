# Build-Assets Runbook

Reproducible steps for (re)generating every build artifact in this repo: the fonts, the
golden manifest, the README images, the PDF specimen, the HTML specimen, the static
site, and the terminal demo.

This complements [`fonts-build-and-release.md`](fonts-build-and-release.md) (the
day-to-day workflow); this file is the full “how the assets are made” reference,
including the external tools and the gotchas hit while producing them.

> All commands run from the repo root. Generated fonts land in `fonts/output/`
> (gitignored); committed assets land in `docs/images/`, `docs/specimen/`, and the
> golden manifest in `fonts/golden/`.

## 0. Toolchain

| Tool | Needed for | Install |
| --- | --- | --- |
| **uv** and Python 3.12+ | everything | <https://docs.astral.sh/uv/> |
| **FontForge** | regenerating intermediate/ExtraBold weights (optional; weights are vendored) | `apt-get install -y fontforge` |
| **Typst** ≥ 0.13 | PDF specimen and README images | prebuilt binary (below) |
| **VHS** and **ttyd** and **ffmpeg** | terminal demo GIF | binaries (below) |

`brotli`/`zopfli` for WOFF2/WOFF come in automatically via `fonttools[woff]`
(`uv sync --all-extras`).

### Installing Typst (prebuilt binary)

```shell
ver=v0.13.1
curl -sSL -o /tmp/typst.tar.xz \
  "https://github.com/typst/typst/releases/download/${ver}/typst-x86_64-unknown-linux-musl.tar.xz"
mkdir -p /tmp/typst && tar -xJf /tmp/typst.tar.xz -C /tmp/typst --strip-components=1
install -m755 /tmp/typst/typst /usr/local/bin/typst
typst --version
```

### Installing the VHS stack

```shell
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg ttyd
vver=v0.10.0
curl -sSL -o /tmp/vhs.tar.gz \
  "https://github.com/charmbracelet/vhs/releases/download/${vver}/vhs_${vver#v}_Linux_x86_64.tar.gz"
mkdir -p /tmp/vhs && tar -xzf /tmp/vhs.tar.gz -C /tmp/vhs --strip-components=1
install -m755 /tmp/vhs/vhs /usr/local/bin/vhs
vhs --version
```

## 1. Build the fonts

```shell
uv sync --all-extras
uv run planetaire build download          # verify vendored sources against SHA256SUMS
uv run planetaire build planetaire-mono   # Extended: 8 TTFs -> fonts/output/
uv run planetaire build text              # Text: TTF + WOFF2 + WOFF + @font-face CSS
uv run planetaire validate fonts/output/PlanetaireMonoExtended-*.ttf
uv run planetaire validate fonts/output/PlanetaireMonoText-*.ttf
```

## 2. Regenerate the golden manifest

The manifest is committed gzipped (`fonts/golden/manifest.json.gz`, ~2 MB). Regenerate
only after an *intended* outline change, using the canonical version as the label:

```shell
VER=$(uv run python -c "from planetaire.version import get_version, to_font_version; print(to_font_version(get_version()))")
uv run planetaire regression generate --output fonts/golden/manifest.json.gz --version "$VER"
uv run planetaire regression verify     # must report PASS / all identical
```

## 3. README images (Typst → PNG, in sync with the PDF)

```shell
uv run planetaire build images          # docs/images/{terminal,text,weights,features}-{dark,light}.png
```

The home-page images render from `docs/specimen/card.typ`, which `#import`s
`docs/specimen/content.typ`, the **same** module the PDF specimen imports. The terminal
mockup, Turing text excerpt, weight ladder, and legibility/dotted-zero cards are
therefore the same content as the specimen and cannot drift; edit `content.typ` to
change both at once. Each card renders as a matched dark/light pair
(`--input theme=dark|light`) so the README can switch with the GitHub color scheme via
`<picture>`. (This replaced the PIL `generate_showcase.py`.)

## 4. PDF specimen (Typst)

```shell
uv run planetaire build specimen        # docs/specimen/planetaire-mono-specimen.pdf
```

Version and build date are injected via Typst `--input` (`sys.inputs`), so the cover and
footer never go stale. Source: `docs/specimen/planetaire-mono-specimen.typ`.

## 5. HTML specimen and static site

```shell
uv run planetaire build html-specimen   # fonts/output/specimen.html (loads Text WOFF2)
uv run planetaire build site            # site/ (landing + specimen + web fonts)
```

The site pulls `terminal-dark.png` and `terminal-demo.*` from `docs/images/` when
present. `site/` is gitignored (build it locally; deployment is intentionally out of
scope).

## 6. Terminal demo (VHS → GIF)

The demo records a real shell session in Planetaire Mono.

```shell
# Install the built font so ttyd/Chromium can resolve it by family name:
mkdir -p ~/.local/share/fonts/planetaire
cp fonts/output/PlanetaireMonoExtended-Regular.ttf fonts/output/PlanetaireMonoExtended-Bold.ttf \
   ~/.local/share/fonts/planetaire/
fc-cache -f

vhs docs/specimen/terminal-demo.tape    # -> docs/images/terminal-demo.gif + .png
```

**Gotcha: Chromium as root.** VHS downloads a headless Chromium (via go-rod) on first
run. Running as root it fails with *“Running as root without --no-sandbox is not
supported.”* Wrap the cached binary to inject the flag, then re-run `vhs`:

```shell
CHROME=$(find ~/.cache/rod/browser -type f -name chrome | head -1)
mv "$CHROME" "${CHROME}.real"
printf '#!/bin/sh\nexec "%s" --no-sandbox --disable-gpu --disable-dev-shm-usage "$@"\n' \
  "${CHROME}.real" > "$CHROME"
chmod +x "$CHROME"
```

Edit the session in `docs/specimen/terminal-demo.tape` (it sources `.venv` so the
`planetaire` CLI is on PATH, and uses a plain `PS1` to avoid escape-code artifacts).

## 7. Release

Publishing a GitHub Release (tag `vX.Y.Z`) triggers
`.github/workflows/release-fonts.yml`, which rebuilds both families and uploads
`PlanetaireMono-Extended.*`, `PlanetaireMono-Text.*` (with WOFF2/WOFF/CSS), and
`SHA256SUMS`. See [`fonts-build-and-release.md`](fonts-build-and-release.md).

## Appendix: why the source fonts are vendored

The B612 and Hack source TTFs are committed under `fonts/source/`, verified by
`fonts/source/SHA256SUMS`. This is a deliberate choice, and the repo size confirms it’s
a non-issue:

|  | Size |
| --- | --- |
| Total tracked content | **~32 MB** |
| `.git` | ~33 MB |
| `fonts/source/` (Hack ~24 MB and B612 ~5 MB) | ~29 MB |
| `fonts/golden/manifest.json.gz` | ~2 MB |
| `docs/images/` and specimen PDF | ~0.9 MB |

A ~32 MB repo is unremarkable for a font project; the source TTFs are large binaries by
nature. **We just commit them.** Rationale:

- **Reproducible, offline builds.** No dependency on upstream availability or a network
  fetch at build time; CI builds the fonts straight from the committed inputs.
- **No FontForge required at build time.** The intermediate Medium and ExtraBold weights
  are *generated* (via FontForge emboldening) and committed, so the normal build and CI
  don’t need FontForge installed.

We are explicitly **not** using Git LFS: it would reintroduce a tooling/network
dependency (and require `lfs: true` in CI) for no real benefit at this size. The one
genuinely oversized artifact, the former 13 MB golden manifest, was the thing worth
fixing, and it is now gzipped to ~2 MB.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
