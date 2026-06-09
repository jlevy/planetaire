/* Consolidated font metadata for the comparison tool.

   This file is intentionally plain browser JavaScript so the static site can
   load it without a build step. Keep the visible comparator shortlist, CDN
   @font-face sources, brand cross-references, and popularity snapshot together
   here instead of spreading them across CSS and rendering code. */
(function () {
  const FONTSOURCE_CDN = "https://cdn.jsdelivr.net/fontsource/fonts";
  const NPM_WINDOW = {
    start: "2026-05-04",
    end: "2026-06-02",
    source: "https://api.npmjs.org/downloads/point/last-month/<package>",
  };
  const NERD_FONTS_ECOSYSTEM = {
    snapshot: "2026-06-09",
    sourceUrl: "https://www.nerdfonts.com/",
    downloadsUrl: "https://www.nerdfonts.com/font-downloads",
    githubUrl: "https://github.com/ryanoasis/nerd-fonts",
    icons: "10390+",
    patchedFonts: "68+",
    githubStars: 63300,
    githubForks: 3900,
    githubWatchers: 402,
    githubReleases: 38,
    latestRelease: "v3.4.0",
    latestReleaseDate: "2025-04-24",
  };

  function license({ availability = "free", name, spdx = null, shortName = null, url, notes = "" }) {
    return { availability, name, spdx, shortName, url, notes };
  }

  const LICENSES = {
    ofl: license({
      name: "SIL Open Font License 1.1",
      spdx: "OFL-1.1",
      url: "https://openfontlicense.org/",
      notes: "Free/open font license; allows web embedding, bundling, modification, and redistribution under OFL conditions.",
    }),
    planetaire: license({
      name: "SIL Open Font License 1.1",
      spdx: "OFL-1.1",
      url: "https://github.com/jlevy/planetaire/blob/main/LICENSE",
      notes: "Final Planetaire font files are OFL-1.1; upstream components include B612, Hack, and Nerd Fonts license obligations.",
    }),
    hack: license({
      name: "MIT License plus Bitstream Vera License",
      shortName: "MIT + Bitstream Vera",
      url: "https://github.com/source-foundry/Hack/blob/master/LICENSE.md",
      notes: "Hack includes Source Foundry MIT terms, public-domain DejaVu work, and Bitstream Vera reserved-name conditions.",
    }),
    commercialEula: license({
      availability: "paid",
      name: "Commercial EULA",
      shortName: "Paid commercial EULA",
      url: null,
      notes: "Requires vendor purchase/license review before use or embedding.",
    }),
    privateUseEula: license({
      availability: "free-private",
      name: "Private-use license / commercial publishing license",
      shortName: "Free private use; paid publishing",
      url: null,
      notes: "Free for private/unpublished use; public-facing or commercial publishing requires a paid license.",
    }),
    appleRestricted: license({
      availability: "restricted",
      name: "Apple font license",
      shortName: "Restricted Apple license",
      url: "https://developer.apple.com/fonts/",
      notes: "Apple developer font license is limited to Apple-platform UI mockups and forbids embedding/redistribution.",
    }),
    privateCustom: license({
      availability: "private",
      name: "Private/custom font",
      shortName: "Private/custom",
      url: null,
      notes: "Observed in product CSS but not publicly licensed as a reusable font.",
    }),
  };

  function localPlanetaireFile(styleName) {
    return `fonts/PlanetaireMonoText-${styleName}.woff2`;
  }

  function face({ style = "normal", weight, sources, family }) {
    return { family, style, weight, sources };
  }

  function source(url, format = "woff2") {
    return { url, format };
  }

  function nerdFont({ name, version, notes = "" }) {
    return {
      ecosystem: "Nerd Fonts",
      available: true,
      name,
      version,
      notes,
      sourceUrl: NERD_FONTS_ECOSYSTEM.downloadsUrl,
    };
  }

  function fontsourceVariable(slug, file = "latin-wght-normal.woff2", format = "woff2-variations") {
    return source(`${FONTSOURCE_CDN}/${slug}:vf@latest/${file}`, format);
  }

  function fontsourceStatic(slug, weight = 400, style = "normal") {
    return source(`${FONTSOURCE_CDN}/${slug}@latest/latin-${weight}-${style}.woff2`);
  }

  function planetaireFace(style, weight, styleName) {
    return face({
      style,
      weight,
      sources: [source(localPlanetaireFile(styleName))],
    });
  }

  const fonts = [
    {
      id: "planetaire",
      name: "Planetaire Mono",
      family: "Planetaire Mono Compare",
      source: "local WOFF2",
      sourceKind: "local",
      sourceUrl: "https://github.com/jlevy/planetaire",
      description: "B612 letters, Hack punctuation, dotted zero",
      default: true,
      license: LICENSES.planetaire,
      notes: "Primary project font. Built from B612 Mono plus Hack Nerd Font-derived assets.",
      faces: [
        planetaireFace("normal", 400, "Regular"),
        planetaireFace("italic", 400, "Italic"),
        planetaireFace("normal", 500, "Medium"),
        planetaireFace("italic", 500, "MediumItalic"),
        planetaireFace("normal", 600, "SemiBold"),
        planetaireFace("italic", 600, "SemiBoldItalic"),
        planetaireFace("normal", 700, "Bold"),
        planetaireFace("italic", 700, "BoldItalic"),
        planetaireFace("normal", 800, "ExtraBold"),
        planetaireFace("italic", 800, "ExtraBoldItalic"),
      ],
    },
    {
      id: "hack",
      name: "Hack",
      family: "Hack Compare",
      source: "jsDelivr",
      sourceKind: "npm",
      sourceUrl: "https://github.com/source-foundry/Hack",
      npmPackage: "hack-font",
      npmDownloadsLastMonth: 11080,
      description: "Source-code workhorse, Nerd Font base",
      default: true,
      license: LICENSES.hack,
      notes: "Useful baseline because Planetaire uses Hack-derived punctuation and Nerd Font material.",
      nerdFont: nerdFont({ name: "Hack", version: "3.003" }),
      faces: [
        face({
          style: "normal",
          weight: 400,
          sources: [source("https://cdn.jsdelivr.net/npm/hack-font@3/build/web/fonts/hack-regular-subset.woff2")],
        }),
        face({
          style: "normal",
          weight: 700,
          sources: [source("https://cdn.jsdelivr.net/npm/hack-font@3/build/web/fonts/hack-bold-subset.woff2")],
        }),
      ],
    },
    {
      id: "fira-code",
      name: "Fira Code",
      family: "Fira Code Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/tonsky/FiraCode",
      npmPackage: "@fontsource/fira-code",
      npmDownloadsLastMonth: 418992,
      description: "Programming ligatures, Fira lineage",
      default: true,
      brandRefs: ["Nerd Fonts"],
      nerdFont: nerdFont({ name: "FiraCode", version: "6.2" }),
      faces: [face({ style: "normal", weight: "300 700", sources: [fontsourceVariable("fira-code")] })],
    },
    {
      id: "ibm-plex",
      name: "IBM Plex Mono",
      family: "IBM Plex Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/IBM/plex",
      npmPackage: "@fontsource/ibm-plex-mono",
      npmDownloadsLastMonth: 1168591,
      description: "IBM Plex family",
      default: true,
      nerdFont: nerdFont({ name: "BlexMono", version: "2.004 (6.4.0)" }),
      faces: [face({ style: "normal", weight: 400, sources: [fontsourceStatic("ibm-plex-mono")] })],
    },
    {
      id: "jetbrains",
      name: "JetBrains Mono",
      family: "JetBrains Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/JetBrains/JetBrainsMono",
      npmPackage: "@fontsource/jetbrains-mono",
      npmDownloadsLastMonth: 1627414,
      description: "Developer-focused IDE face",
      default: true,
      brandRefs: ["JetBrains", "Perplexity docs shell"],
      nerdFont: nerdFont({ name: "JetBrainsMono", version: "2.304" }),
      faces: [face({ style: "normal", weight: "100 800", sources: [fontsourceVariable("jetbrains-mono")] })],
    },
    {
      id: "geist",
      name: "Geist Mono",
      family: "Geist Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://vercel.com/font",
      npmPackage: "@fontsource/geist-mono",
      npmDownloadsLastMonth: 404907,
      description: "Vercel and OpenAI developer UI face",
      default: true,
      brandRefs: ["OpenAI developer docs", "Vercel"],
      nerdFont: nerdFont({ name: "GeistMono", version: "1.401" }),
      faces: [face({ style: "normal", weight: "100 900", sources: [fontsourceVariable("geist-mono")] })],
    },
    {
      id: "source-code-pro",
      name: "Source Code Pro",
      family: "Source Code Pro Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/adobe-fonts/source-code-pro",
      npmPackage: "@fontsource/source-code-pro",
      npmDownloadsLastMonth: 250853,
      description: "Adobe source family, neutral coding face",
      brandRefs: ["Nerd Fonts"],
      nerdFont: nerdFont({ name: "SauceCodePro", version: "2.042", notes: "Nerd Fonts distribution uses a renamed Source Code Pro family." }),
      faces: [face({ style: "normal", weight: "200 900", sources: [fontsourceVariable("source-code-pro")] })],
    },
    {
      id: "pt-mono",
      name: "PT Mono",
      family: "PT Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/google/fonts/tree/main/ofl/ptmono",
      npmPackage: "@fontsource/pt-mono",
      npmDownloadsLastMonth: 43044,
      description: "Upright, serif-like monospace flavor",
      faces: [face({ style: "normal", weight: 400, sources: [fontsourceStatic("pt-mono")] })],
    },
    {
      id: "inconsolata",
      name: "Inconsolata",
      family: "Inconsolata Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/google/fonts/tree/main/ofl/inconsolata",
      npmPackage: "@fontsource/inconsolata",
      npmDownloadsLastMonth: 98216,
      description: "Humanist coding classic",
      nerdFont: nerdFont({ name: "Inconsolata", version: "3.000" }),
      faces: [face({ style: "normal", weight: "200 900", sources: [fontsourceVariable("inconsolata")] })],
    },
    {
      id: "cascadia",
      name: "Cascadia Code",
      family: "Cascadia Code Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/microsoft/cascadia-code",
      npmPackage: "@fontsource/cascadia-code",
      npmDownloadsLastMonth: 23478,
      description: "Windows Terminal and Visual Studio lineage",
      brandRefs: ["Microsoft"],
      nerdFont: nerdFont({ name: "CaskaydiaCove", version: "2407.24", notes: "Cascadia Code patched family; CaskaydiaMono covers Cascadia Mono without ligatures." }),
      faces: [face({ style: "normal", weight: "200 700", sources: [fontsourceVariable("cascadia-code")] })],
    },
    {
      id: "iosevka",
      name: "Iosevka",
      family: "Iosevka Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/be5invis/Iosevka",
      npmPackage: "@fontsource/iosevka",
      npmDownloadsLastMonth: 11044,
      description: "Narrow, highly configurable coding face",
      brandRefs: ["Nerd Fonts"],
      nerdFont: nerdFont({ name: "Iosevka", version: "33.2.1", notes: "Nerd Fonts patched-source version; IosevkaTerm and IosevkaTermSlab are also patched distributions." }),
      faces: [face({ style: "normal", weight: 400, sources: [fontsourceStatic("iosevka")] })],
    },
    {
      id: "monaspace",
      name: "Monaspace Neon",
      family: "Monaspace Neon Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/githubnext/monaspace",
      npmPackage: "@fontsource/monaspace-neon",
      npmDownloadsLastMonth: 7422,
      description: "GitHub Next texture-healing family",
      brandRefs: ["GitHub Next"],
      nerdFont: nerdFont({ name: "Monaspice", version: "1.200", notes: "Nerd Fonts patched-source version; covers the Monaspace family under the Monaspice name." }),
      faces: [face({ style: "normal", weight: 400, sources: [fontsourceStatic("monaspace-neon")] })],
    },
    {
      id: "roboto-mono",
      name: "Roboto Mono",
      family: "Roboto Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/googlefonts/RobotoMono",
      npmPackage: "@fontsource/roboto-mono",
      npmDownloadsLastMonth: 556697,
      description: "Google/Android-era monospace baseline",
      brandRefs: ["Google ecosystem"],
      nerdFont: nerdFont({ name: "RobotoMono", version: "3.0" }),
      faces: [face({ style: "normal", weight: "100 700", sources: [fontsourceVariable("roboto-mono")] })],
    },
    {
      id: "google-sans-code",
      name: "Google Sans Code",
      family: "Google Sans Code Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/googlefonts/googlesans-code",
      npmPackage: "@fontsource/google-sans-code",
      npmDownloadsLastMonth: 5108,
      description: "Google developer-docs code face",
      brandRefs: ["Google Developers", "Gemini"],
      notes: "OFL-1.1 font; Google, Google Sans, and Google Sans Code are Google trademarks.",
      faces: [face({ style: "normal", weight: "300 800", sources: [fontsourceVariable("google-sans-code")] })],
    },
    {
      id: "intel-one-mono",
      name: "Intel One Mono",
      family: "Intel One Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/intel/intel-one-mono",
      npmPackage: "@fontsource/intel-one-mono",
      npmDownloadsLastMonth: 5823,
      description: "Low-vision-informed developer face",
      nerdFont: nerdFont({ name: "IntoneMono", version: "1.4.0", notes: "Nerd Fonts distribution uses a renamed Intel One Mono family." }),
      faces: [face({ style: "normal", weight: 400, sources: [fontsourceStatic("intel-one-mono")] })],
    },
    {
      id: "atkinson-hyperlegible-mono",
      name: "Atkinson Hyperlegible Mono",
      family: "Atkinson Hyperlegible Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/googlefonts/atkinson-hyperlegible-next-mono",
      npmPackage: "@fontsource/atkinson-hyperlegible-mono",
      npmDownloadsLastMonth: 9426,
      description: "Accessibility-first mono family",
      nerdFont: nerdFont({ name: "AtkynsonMono", version: "2.001", notes: "Nerd Fonts distribution uses a renamed Atkinson Hyperlegible Mono family." }),
      faces: [face({ style: "normal", weight: "200 800", sources: [fontsourceVariable("atkinson-hyperlegible-mono")] })],
    },
    {
      id: "commit-mono",
      name: "Commit Mono",
      family: "Commit Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/eigilnikolajsen/commit-mono",
      npmPackage: "@fontsource/commit-mono",
      npmDownloadsLastMonth: 29859,
      description: "Neutral coding face with smart kerning",
      nerdFont: nerdFont({ name: "CommitMono", version: "1.143" }),
      faces: [face({ style: "normal", weight: 400, sources: [fontsourceStatic("commit-mono")] })],
    },
    {
      id: "martian-mono",
      name: "Martian Mono",
      family: "Martian Mono Compare",
      source: "Fontsource",
      sourceKind: "fontsource",
      sourceUrl: "https://github.com/evilmartians/mono",
      npmPackage: "@fontsource/martian-mono",
      npmDownloadsLastMonth: 2612,
      description: "Variable mono for devtool branding",
      nerdFont: nerdFont({ name: "MartianMono", version: "1.1.0" }),
      faces: [face({ style: "normal", weight: "100 800", sources: [fontsourceVariable("martian-mono")] })],
    },
  ].map((font) => {
    const fontLicense = font.license || LICENSES.ofl;
    return {
      availability: font.availability || fontLicense.availability,
      license: fontLicense,
      ...font,
    };
  });

  const trackedFonts = [
    {
      id: "recursive",
      name: "Recursive",
      availability: "free",
      license: LICENSES.ofl,
      sourceUrl: "https://github.com/arrowtype/recursive",
      status: "track",
      nerdFont: nerdFont({ name: "RecMono", version: "1.085", notes: "Nerd Fonts distribution covers Recursive Mono." }),
      reason: "Useful variable-axis experiment, but needs deliberate mono/casual/linear axis handling before comparator inclusion.",
    },
    {
      id: "victor-mono",
      name: "Victor Mono",
      availability: "free",
      license: LICENSES.ofl,
      sourceUrl: "https://github.com/rubjo/victor-mono",
      status: "track",
      nerdFont: nerdFont({ name: "VictorMono", version: "1.5.6" }),
      reason: "Distinct cursive italic and ligature personality; lower-priority comparator candidate.",
    },
    {
      id: "berkeley-mono",
      name: "Berkeley Mono",
      availability: "paid",
      license: { ...LICENSES.commercialEula, url: "https://usgraphics.com/products/berkeley-mono" },
      status: "paid-reference",
      reason: "High-quality professional coding font with visible AI/product-brand adoption; not loadable in a public comparator without a license.",
    },
    {
      id: "monolisa",
      name: "MonoLisa",
      availability: "paid",
      license: { ...LICENSES.commercialEula, url: "https://www.monolisa.dev/" },
      status: "paid-reference",
      reason: "Well-known paid coding font with trial, webfont, variable, and commercial licensing options.",
    },
    {
      id: "operator-mono",
      name: "Operator Mono",
      availability: "paid",
      license: { ...LICENSES.commercialEula, url: "https://www.typography.com/fonts/operator/overview" },
      status: "paid-reference",
      reason: "Influential commercial coding font from Hoefler/Monotype; track as historical paid reference.",
    },
    {
      id: "pragmata-pro",
      name: "PragmataPro",
      availability: "paid",
      license: { ...LICENSES.commercialEula, url: "https://fsd.it/shop/fonts/pragmatapro/" },
      status: "paid-reference",
      reason: "Dense paid coding font with very broad symbol coverage and long-running developer following.",
    },
    {
      id: "gt-standard-mono",
      name: "GT Standard Mono",
      availability: "paid",
      license: { ...LICENSES.commercialEula, url: "https://www.grillitype.com/typeface/gt-standard" },
      status: "paid-reference",
      reason: "Perplexity docs use GT Standard Mono; track as a commercial brand/reference mono.",
    },
    {
      id: "input-mono",
      name: "Input Mono",
      availability: "free-private",
      license: { ...LICENSES.privateUseEula, url: "https://input.djr.com/download/" },
      status: "conditional-reference",
      reason: "Free for private/unpublished coding use, but public-facing publishing uses paid Type Network licensing.",
    },
    {
      id: "sf-mono",
      name: "SF Mono",
      availability: "restricted",
      license: LICENSES.appleRestricted,
      status: "system-reference",
      reason: "Important macOS/iOS developer reference, but Apple license restrictions make it unsuitable for bundled public web comparison.",
    },
    {
      id: "anthropic-mono",
      name: "anthropicMono",
      availability: "private",
      license: { ...LICENSES.privateCustom, url: "https://platform.claude.com/docs/en/intro" },
      status: "brand-reference",
      reason: "Observed in Anthropic docs CSS; not publicly distributed as a reusable font.",
    },
  ];

  const brandUsage = [
    {
      brand: "OpenAI Developers",
      observedMono: "Geist Mono",
      evidence: "developers.openai.com API reference page defines --stl-typography-font-mono using Geist Mono.",
      sourceUrl: "https://developers.openai.com/api/reference/overview",
      confidence: "high",
    },
    {
      brand: "Anthropic Claude Platform",
      observedMono: "anthropicMono",
      evidence: "platform.claude.com docs CSS defines --font-anthropic-mono and applies it to code/pre/kbd/samp.",
      sourceUrl: "https://platform.claude.com/docs/en/intro",
      confidence: "high",
    },
    {
      brand: "Perplexity API Docs",
      observedMono: "GT Standard Mono",
      evidence: "docs.perplexity.ai page CSS sets .font-mono to GT Standard Mono; the page shell also includes a JetBrains Mono variable class.",
      sourceUrl: "https://docs.perplexity.ai/docs/getting-started/overview",
      confidence: "high",
    },
    {
      brand: "GitHub Product UI",
      observedMono: "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace",
      evidence: "Primer CSS typography variables define the mono stack.",
      sourceUrl: "https://github.com/primer/css/blob/163a19f3e8afa29e2ffc3e688b5ac17b2717fbdb/src/support/variables/typography.scss",
      confidence: "high",
    },
    {
      brand: "Google Developers",
      observedMono: "Google Sans Code",
      evidence: "developers.google.com sets --gfd-font-family-code and --devsite-code-font-family to Google Sans Code.",
      sourceUrl: "https://developers.google.com/",
      confidence: "high",
    },
    {
      brand: "Vercel",
      observedMono: "Geist Mono",
      evidence: "Vercel publishes Geist Mono as part of the Geist family and licenses it under OFL.",
      sourceUrl: "https://vercel.com/font",
      confidence: "high",
    },
    {
      brand: "Microsoft developer tools",
      observedMono: "Cascadia Code",
      evidence: "Cascadia Code is bundled with Windows Terminal and is the default font in Visual Studio.",
      sourceUrl: "https://github.com/microsoft/cascadia-code",
      confidence: "high",
    },
    {
      brand: "JetBrains IDEs",
      observedMono: "JetBrains Mono",
      evidence: "JetBrains Mono is described as the default editor font in JetBrains IDEs.",
      sourceUrl: "https://www.jetbrains.com/lp/mono/",
      confidence: "high",
    },
  ];

  window.PlanetaireFontData = {
    updated: "2026-06-09",
    npmDownloadWindow: NPM_WINDOW,
    nerdFontsEcosystem: NERD_FONTS_ECOSYSTEM,
    fonts,
    trackedFonts,
    brandUsage,
  };
})();
