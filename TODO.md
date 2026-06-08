# Planetaire Mono TODO

Work is tracked in detail with [`tbd`](https://github.com/jlevy/tbd) (beads); run
`tbd list` for live status.
This file is the human-readable summary of the open follow-ups, ordered by priority.

## P1

- **License/copyright compliance in the distribution** (`plt-idxx`): the shipped fonts
  and release archives are not yet fully OFL-compliant.
  The font name table carries only Hack’s copyright (nameID 0/13/14), not B612’s nor the
  project’s OFL-1.1 and Joshua Levy copyright, and the release archives bundle only
  `ttf/`, `web/`, and `README.txt` with no LICENSE or constituent license texts.
  Fix: have the build set nameID 0 (combined copyright), 13 (OFL-1.1 description noting
  the constituent licenses), and 14 (project OFL URL), and bundle a LICENSE/OFL.txt plus
  the constituent license texts (B612 OFL+EPL, Hack MIT, Nerd Fonts MIT) into `dist/`
  and the tar/zip archives.

## P2

- **Spindly apostrophe in the specimen** (`plt-uuag`): the straight ASCII apostrophe
  (U+0027) in prose such as “B612’s unusual character” renders thin via a DejaVu Sans
  Mono fallback, while the curly apostrophe (U+2019, e.g. “Ryan McIntyre’s” in the
  credits) renders correctly from Planetaire/Hack.
  Confirm whether U+0027 survives into the built font’s cmap, prefer typographic
  apostrophes in prose, and stop the fallback so it is fixed wherever the origin is.
- **Italic stroke-weight unevenness** (`plt-3h7p`): `normalize_monospace` horizontally
  condenses any glyph wider than the cell, thinning the widest italic letters (for
  example italic `y`/`x`/`m`) by about 18 percent so they read lighter than narrow
  glyphs. Fix: for letter and text glyphs, set the uniform advance and recenter the ink
  but let it overhang the cell rather than horizontal-scaling, keeping strict
  cell-fitting only for box-drawing, powerline, and icon glyphs.
- **Italic spacing review in the specimen** (`plt-q10u`): the Spacing Review page shows
  the standard coding characters at true cell widths only upright; add the same
  true-cell-width review for italics so italic overhang/condensing is visible against
  the advance rules (supports verifying `plt-3h7p`).
- **About-page paragraph spacing** (`plt-mqgd`): make the gaps between paragraphs (and
  around the bulleted list) true full blank monospace lines, man-page style, rather than
  the current partial Typst paragraph spacing.
- **“Families” -> “Packages”** (`plt-072i`): Text and Extended are not different font
  families, they are the same typeface in different packagings (Extended adds
  icons/Powerline for terminal/local use; Text is a lightweight web subset; they also
  differ by format). Rename “Families” to “Packages” across the specimen, README, and
  site, keeping the OpenType nameID family names unchanged.
- **Terminal examples as separate dark/light pairs** (`plt-he4k`): the README packs the
  Python function and the terminal session into one combined image with mismatched font
  sizes and a different code sample than the specimen.
  Keep them as two separate images (Python example; terminal example), each shown as a
  dark/light pair, the same way in both the README and the specimen.
- **Full-fidelity SemiBold logos** (`plt-ddjw`): the shipped SemiBold masters cap
  emboldening at 500 points, so about 49 ultra-dense Nerd Font logo glyphs (for example
  `dev-ohmyzsh`, 4,676 points) sit at base weight.
  FontForge `changeWeight` is pathologically slow on these (a full-font pass ran over
  two hours without finishing).
  The difference is visually imperceptible, since those glyphs appear in no specimen or
  README page, but for true full fidelity they should eventually be emboldened to 600.
  Options to explore: parallel-embolden just the capped glyphs across cores and merge
  them into the masters, a faster stroke or overlap method, or interpolation from Medium
  and Bold. Then drop or raise the cap.

## P3

- **Drop the ASCII character table** (`plt-923j`): remove the man-page “ASCII CHARACTER
  TABLE (HEXADECIMAL)” block from the specimen; it does not add much.
- **Two Families page web-block cleanup** (`plt-cpas`): drop the poorly formatted “For
  the web” CSS snippet, and make the inline `@font-face` mention match the surrounding
  text size (different color is fine).
  Also covered by the “Families” -> “Packages” rename (`plt-072i`).
- **Cohesive specimen identity** (`plt-n561`): a consistent document ID and date, an
  accent color, and a unified footer across the specimen.
- **Version stamp** (`plt-makk`): keep the specimen PDF and title current with the
  release version.
- **OTF (CFF) output** (`plt-8cyc`): emit OTF alongside TTF for both families (deferred
  until the specimen and packaging work above is settled).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
