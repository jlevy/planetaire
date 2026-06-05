"""Assemble a simple static site for Planetaire Mono.

Generates a self-contained ``site/`` directory: a landing page plus the HTML
specimen and the Text web fonts. Optional assets (a hero image, an animated
terminal demo) are included automatically when present, so the site improves as
those land without breaking today. Deployment is intentionally out of scope —
this only builds the pages locally.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from planetaire.config import TEXT_FAMILY_NAME

# (source filename in fonts_dir, kind) for optional presentation assets.
_HERO_CANDIDATES = ("hero.svg", "hero.png")
_DEMO_CANDIDATES = ("terminal-demo.svg", "terminal-demo.gif", "terminal-demo.webm")


def _copy_if_exists(src: Path, dst_dir: Path) -> str | None:
    if src.exists():
        shutil.copy2(src, dst_dir / src.name)
        return src.name
    return None


def generate_site(
    output_dir: Path,
    fonts_dir: Path,
    *,
    images_dir: Path = Path("docs/images"),
    version: str | None = None,
) -> Path:
    """Build the static site into `output_dir`.

    Fonts/CSS/specimen come from `fonts_dir`; the hero image and terminal demo are
    pulled from `images_dir` (falling back to `fonts_dir`) when present.

    Returns the path to the generated ``index.html``.
    """
    if version is None:
        from planetaire.version import get_version, to_font_version

        version = to_font_version(get_version())

    output_dir.mkdir(parents=True, exist_ok=True)

    # Bring in the web fonts + CSS + HTML specimen so the site is self-contained.
    for pattern in ("PlanetaireMonoText-*.woff2", "PlanetaireMonoText-*.woff"):
        for f in fonts_dir.glob(pattern):
            shutil.copy2(f, output_dir / f.name)
    css_name = _copy_if_exists(fonts_dir / "planetaire-mono-text.css", output_dir)
    specimen_name = _copy_if_exists(fonts_dir / "specimen.html", output_dir)

    def _find(candidates: tuple[str, ...]) -> str | None:
        for c in candidates:
            for src in (images_dir / c, fonts_dir / c):
                if (name := _copy_if_exists(src, output_dir)) is not None:
                    return name
        return None

    hero = _find(_HERO_CANDIDATES)
    demo = _find(_DEMO_CANDIDATES)

    index = output_dir / "index.html"
    index.write_text(_render_index(version, css_name, specimen_name, hero, demo))
    return index


def _render_index(
    version: str,
    css_name: str | None,
    specimen_name: str | None,
    hero: str | None,
    demo: str | None,
) -> str:
    family = TEXT_FAMILY_NAME
    css_link = f'<link rel="stylesheet" href="{css_name}">' if css_name else ""
    font_stack = f"'{family}', ui-monospace, monospace" if css_name else "ui-monospace, monospace"

    hero_html = f'<img class="hero" src="{hero}" alt="Planetaire Mono sample">' if hero else ""
    demo_html = ""
    if demo:
        if demo.endswith(".webm"):
            demo_html = f'<video class="demo" src="{demo}" autoplay loop muted playsinline></video>'
        else:
            demo_html = f'<img class="demo" src="{demo}" alt="Terminal demo">'
    specimen_link = (
        f'<a class="btn" href="{specimen_name}">Open the type specimen →</a>'
        if specimen_name
        else ""
    )

    base = "https://github.com/jlevy/planetaire/releases/latest/download"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Planetaire Mono</title>
{css_link}
<style>
  :root {{ --bg:#0d1117; --fg:#e6edf3; --dim:#7d8590; --accent:#58a6ff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--fg); font-family:{font_stack};
          line-height:1.6; padding:3rem clamp(1rem,5vw,5rem); }}
  h1 {{ font-size:clamp(2.5rem,8vw,4.5rem); margin:0; font-weight:800; }}
  .tag {{ color:var(--dim); font-size:1.1rem; margin:.5rem 0 2rem; }}
  .hero, .demo {{ width:100%; border:1px solid #30363d; border-radius:10px; margin:1.5rem 0; }}
  section {{ margin:3rem 0; max-width:60rem; }}
  h2 {{ font-size:.8rem; text-transform:uppercase; letter-spacing:.12em; color:var(--accent); }}
  table {{ border-collapse:collapse; width:100%; }}
  td, th {{ border:1px solid #30363d; padding:.6rem .8rem; text-align:left; }}
  .btn {{ display:inline-block; margin:.4rem .6rem .4rem 0; padding:.6rem 1rem;
          background:#161b22; border:1px solid #30363d; border-radius:8px;
          color:var(--accent); text-decoration:none; }}
  .btn:hover {{ border-color:var(--accent); }}
  footer {{ color:var(--dim); font-size:.85rem; border-top:1px solid #30363d;
            margin-top:4rem; padding-top:1.5rem; }}
  code {{ background:#161b22; padding:.1rem .35rem; border-radius:4px; }}
</style>
</head>
<body>
  <h1>Planetaire Mono</h1>
  <div class="tag">Legible monospace — B612 letterforms on Hack's infrastructure. v{version}</div>
  {hero_html}
  {demo_html}

  <section>
    <h2>Two families</h2>
    <table>
      <tr><th>Family</th><th>Best for</th><th>Coverage</th></tr>
      <tr><td><b>Planetaire Mono</b></td><td>Terminals, coding</td><td>Everything + ~12k Nerd Font icons</td></tr>
      <tr><td><b>Planetaire Mono Text</b></td><td>Web, documents</td><td>Text glyphs + box-drawing (~55 KB/wt WOFF2)</td></tr>
    </table>
  </section>

  <section>
    <h2>Get it</h2>
    <a class="btn" href="{base}/PlanetaireMono-Extended.tar.xz">Download Extended (.tar.xz)</a>
    <a class="btn" href="{base}/PlanetaireMono-Text.tar.xz">Download Text (.tar.xz)</a>
    {specimen_link}
  </section>

  <section>
    <h2>Use on the web</h2>
    <p>The Text family ships WOFF2/WOFF and a ready-made stylesheet:</p>
    <p><code>&lt;link rel="stylesheet" href="planetaire-mono-text.css"&gt;</code><br>
       <code>font-family: "Planetaire Mono Text", monospace;</code></p>
  </section>

  <footer>Generated by <code>planetaire build site</code>. Fonts under OFL-1.1.</footer>
</body>
</html>
"""
