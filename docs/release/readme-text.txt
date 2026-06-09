Planetaire Mono Text

The lightweight Planetaire Mono subset: letters, punctuation, Greek, Cyrillic, and
box-drawing. It drops the Nerd Font icons, so it is much smaller than the Extended
family.

Contents:
  web/   Slim WOFF2 web fonts and @font-face CSS. The base stylesheet
         planetaire-mono-text.css declares Regular/Bold upright faces split into
         latin, latin-ext, greek, cyrillic, and cyrillic-ext ranges. Load
         planetaire-mono-text-italics.css as an optional companion for Regular/Bold
         italics.
  ttf/   TrueType fonts for local install (documents, editors) if you want it on desktop.

Recommended: for the web, use web/ and the included stylesheet(s). If you need the full
Nerd Font icon set (for terminals and coding), use Planetaire Mono Extended instead.

Web delivery notes:
  - Preload PlanetaireMonoText-Regular-latin.woff2 when Planetaire text appears above
    the fold. Also preload PlanetaireMonoText-Bold-latin.woff2 if bold text appears
    above the fold.
  - Use font-family: var(--planetaire-mono-text-font-stack); after loading the CSS.
    The stylesheet includes a metric-matched local fallback face for stable line height
    during font-display: swap.
  - Serve WOFF2 files from a versioned path or fingerprinted filename with
    Cache-Control: public, max-age=31536000, immutable. Keep CSS cache shorter if font
    URLs inside it are not versioned.

License:
  LICENSE        SIL Open Font License 1.1 (covers this distribution)
  licenses/      Constituent upstream license texts (B612, Hack, Nerd Fonts)

https://github.com/jlevy/planetaire   (SIL Open Font License 1.1)
https://openfontlicense.org
