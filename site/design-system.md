# Design system

The static site’s visual rules, kept deliberately small. The goal: a clean type specimen
where the **font** is the only thing doing the talking. Add a token only when something
genuinely cannot be expressed with the ones below.

The CSS in `style.css` is the implementation; this file is the spec. They must agree —
if you change one, change the other.

## Principle

Two text colors. Four type sizes. Three weights. Two heading levels. Everything else is
either structure (one hairline, one surface tint) or **content** — the specimen demos
(size waterfall, weight ladder, glyph showcases) deliberately render many sizes and all
ten weights, because that *is* what they exist to show. Chrome stays on-system; demos
are free.

## Color

Two colors for all text, full stop:

| Token | Value (light) | Value (dark) | Used for |
| --- | --- | --- | --- |
| `--ink` | `#000` | `#e6edf3` | All main text: body, headings, samples, bold, links |
| `--gray` | `#6e7781` | `#8b949e` | Labels, captions, secondary text only |

Two structural tints (not “colors” — they carry no text):

| Token | Value (light) | Value (dark) | Used for |
| --- | --- | --- | --- |
| `--rule` | `#d7dbdf` | `#30363d` | Hairlines: section underlines, table/box borders |
| `--surface` | `#f6f8fa` | `#161b22` | Background behind code blocks, inline code, table headers |

- **Links are `--ink` + underline** — no link color. Distinguished by the underline
  alone.
- **One exception:** the `.panel` code & terminal blocks carry a syntax palette
  (`--syn-*`) that **follows the page theme** — it maps to the light `--l-*` palette in
  light mode and the dark `--d-*` palette in dark mode (both copied verbatim from
  `pal-light` / `pal-dark` in `content.typ`). So the examples always match the page’s
  current mode rather than being fixed dark/light pairs. Showing the font on
  syntax-colored code is the content, so the color there is justified. Nowhere else.

## Type scale

Four sizes for everything that is chrome (prose, headings, tables, labels):

| Token | Size | Used for |
| --- | --- | --- |
| `--fs-display` | `3.25rem` | Hero wordmark only |
| `--fs-h2` | `1.625rem` | Major section headings |
| `--fs-body` | `1rem` | Body text, h3 sub-headers, tables, buttons |
| `--fs-small` | `0.9rem` | Labels, captions, footer |

The rem scale is **anchored**: `html { font-size: 16px }` and
`body { font-size: var(--fs-body) }`, so `1rem` always equals body text. (Without the
anchor, rem-based chrome like h3 and the toggle would shrink relative to body if the
browser root size weren’t 16px.) Inter-paragraph spacing (`--space-para`) is `1.6rem` =
one line height, so paragraphs are separated by a full blank line, like the specimen.

The **hero/title cluster** is a self-contained brand block echoing the PDF cover, so its
lineage uses a bespoke larger size (`1.3rem`, black bold) rather than a chrome token.
Like the demos, the cover cluster is exempt from the four-size scale.

Base font-size is `16px`. **Reading line-height is one of exactly two** (matching the
PDF specimen): `--lh` (`1.5`) for prose and text samples, `--lh-tight` (`1.4`) for
terminal/code panels. Structural/showcase line-heights (headings, the hero wordmark, the
size-waterfall stack, glyph rows) are exempt — they’re not reading text.

**Demo sizes are exempt.** The size waterfall (8–44px), the weight ladder, and the large
legibility/character glyphs set their own sizes (`--fs-glyph`, `--fs-glyph-sm`,
`--fs-glyph-lg`, or inline px). These are content, not chrome — do not fold them into
the scale.

## Weight

Three weights for chrome:

| Token | Value | Used for |
| --- | --- | --- |
| `--fw-regular` | `400` | Body text |
| `--fw-medium` | `500` | Hero wordmark, **h2 major-section headings** |
| `--fw-bold` | `700` | Bold, h3 sub-headers, labels, buttons |

The weight-ladder demo uses all ten faces (400/500/600/700/800 × upright/italic) — that
is the content of that demo, not a license to use other weights in the chrome.

## Headings

Two levels, mirroring the PDF specimen’s heading roles:

| Level | Looks like | Mirrors (specimen) |
| --- | --- | --- |
| **`h2` — major section** | `--fs-h2`, **medium (500)**, **Title Case**, with a full-width underline rule below | `section()` |
| **`h3` — sub-header** | `--fs-body`, **BOLD CAPS** (uppercase), no rule | `about-heading()` |

Do not introduce an h4 in prose. Field captions inside demos use `.label` (small gray
caps), which reads as a quieter tier than an h3 (body black caps) — black vs gray, body
vs small, exactly the two-color / two-size split.

- The homepage hero title, lineage, tagline/prose, and content headings stay in
  Planetaire Mono Text. The sans-serif UI face is reserved for chrome such as the top
  nav, tabs, buttons, theme switch, footer, and comparison controls.

- **`h3` sits in the regular paragraph rhythm** — the gap above and below it equals the
  one paragraph gap (`--space-para`), shared with `<p>`, for a traditional manuscript
  feel (same as the specimens). No extra heading space.

## Spacing

- Page: max width `720px`, centered, with `8px` top padding and `96px` bottom padding.
  The shared nav can expand to the wider `--nav-max` measure on large screens.
- One paragraph gap, `--space-para` (`1.6rem`), is shared by `<p>` and `h3`.
- **Hero** mirrors the specimen cover’s generous vertical rhythm: wide planet frame (max
  `940px`), ample space below it, and one shared `--hero-stack-gap` between the title,
  lineage, intro, CTAs, and theme switch. The hero intro is a single bold statement,
  slightly larger than body text and constrained by character measure so it wraps
  intentionally. When in doubt, give the title more room, not less.
- Section headings (`h2`): `4.25rem` above, `1.3rem` below.

## Components

All button text is **CAPS** (via `text-transform`, authored mixed-case).

- **Chrome dimensions:** form controls, segmented controls, and ordinary buttons share
  `--control-height` / `--button-height` (`2.1rem`). Compact button rows, such as
  compare page font preset actions, use `--compact-button-height` (`1.75rem`). Heights
  are tokens, not ad hoc padding math, so buttons and widgets line up.
- **Chrome borders:** UI chrome uses one thin border token:
  `--chrome-border-width: 1px`. Active/selected states may change fill or text color,
  but they must not increase border width, add a second inset border, or change the
  element’s height. If a selected button needs emphasis, use a gray fill rather than a
  thicker outline; dark-mode selected fills should sit visibly above hover while staying
  softer than an inverse button. Tab indicators are the one explicit exception and use
  `--tab-indicator-width`.
- **Tabs:** tab labels use shared block and inline padding tokens so hover backgrounds
  have even top/bottom space and a small left/right cushion. The active underline is the
  tab’s own bottom border (`--tab-indicator-width`), so it always matches the hover
  background width.
- **Top nav:** a minimal gray caps row above the hero. Planetaire and Compare are page
  tabs, left-aligned on a hairline rule and using the same active underline as the main
  About / Samples / Installation tabs. The nav expands to the shared wide compare-page
  width on large screens while the homepage content remains on its narrower reading
  column. GitHub is an external link, separated at right with an arrow and no active-tab
  state.
- **Compare page header:** a compact utility-page title in the sans-serif UI face, with
  optional italic gray supporting copy below it. Keep this lighter than the homepage
  hero so the controls and proofs remain the primary interface.
- **Buttons:** two in the hero — *Download Fonts* (latest GitHub release) and *Specimen
  PDF →* (opens the PDF in a new tab). Identical style: `--ink` border, transparent
  fill, invert on hover. No primary/secondary distinction.
- **Theme switch:** a centered Light/Dark control directly below the CTAs (not a corner
  toggle) — seeing the font on both backgrounds is a primary way to evaluate it. Two
  **equal-width** segments; the **current** theme is the filled (emphasized) segment,
  the other muted gray, so the fill alone shows the position (no label). Flips
  `data-theme` on `<html>`, persists to a **1-year cookie** (`plt-theme`, with a
  `localStorage` fallback) so the choice sticks on revisit, and defaults to the OS
  preference on first visit.
- **Main tabs:** a centered About / Samples / Installation row below the hero. Tabs are
  caps labels on a hairline rule, with the current tab marked by an `--ink` underline,
  and switch between the three content panels without changing the content text.
- **Theme transition:** light↔dark eases gently — a single global transition on
  themeable properties (`background-color`, `border-color`, `color`, `fill`, `filter`),
  `360ms`, disabled under `prefers-reduced-motion`.
- **Dark-mode planet:** the SVG is black line art, so dark mode inverts it
  (`filter: invert(1)`) to keep it visible.
- **Tables / spec grid / code panels / glyph rows:** styled once in `style.css`; reuse
  the classes rather than adding inline styles.
- **Narrow tables:** tables may self-scroll horizontally below the small-screen
  breakpoint so multi-column release/config data remains reachable while page-level
  overflow stays clipped for the hero planet.
- **Keyboard focus:** links and buttons use a visible `--ink` focus outline. Segmented
  theme buttons draw the outline inside the control so it is not clipped by the group.

## Checklist before adding anything

1. Can an existing token express it? Use that.
2. Is it chrome or content? Chrome must stay on the scale; only demos get free sizes.
3. Does it need a new color? Almost certainly no — try `--ink`, `--gray`, weight, or
   size.
4. If you truly need a token, add it here **and** in `style.css`, with a one-line
   reason.
