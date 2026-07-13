# Design system

The static site’s visual rules, kept deliberately small.
The goal: a clean type specimen where the **font** is the only thing doing the talking.
Add a token only when something genuinely cannot be expressed with the ones below.

The CSS in `style.css` and the tab/scroll behavior in `scroll-tabs.js` are the
implementation; this file is the spec.
They must agree — if you change one, change the other.

## Principle

Two text colors. Four type sizes.
Three weights. Two heading levels.
Everything else is either structure (one hairline, one surface tint) or **content** —
the specimen demos (size waterfall, weight ladder, glyph showcases) deliberately render
many sizes and all ten weights, because that *is* what they exist to show.
Chrome stays on-system; demos are free.

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

- **Links are `--ink` + underline** — no link color.
  Distinguished by the underline alone.
- **One exception:** the `.panel` code & terminal blocks carry a syntax palette
  (`--syn-*`) that **follows the page theme** — it maps to the light `--l-*` palette in
  light mode and the dark `--d-*` palette in dark mode (both copied verbatim from
  `pal-light` / `pal-dark` in `content.typ`). So the examples always match the page’s
  current mode rather than being fixed dark/light pairs.
  Showing the font on syntax-colored code is the content, so the color there is
  justified. Nowhere else.

## Type scale

Four sizes for everything that is chrome (prose, headings, tables, labels):

| Token | Size | Used for |
| --- | --- | --- |
| `--fs-display` | `3.25rem` | Hero wordmark only |
| `--fs-h2` | `1.625rem` | Major section headings |
| `--fs-body` | `1rem` | Body text, h3 sub-headers, tables, buttons |
| `--fs-small` | `0.9rem` | Labels, captions, footer |

The rem scale is **anchored**: `html { font-size: 16px }` and
`body { font-size: var(--fs-body) }`, so `1rem` always equals body text.
(Without the anchor, rem-based chrome like h3 and the toggle would shrink relative to
body if the browser root size weren’t 16px.) Inter-paragraph spacing (`--space-para`) is
`1.6rem` = one line height, so paragraphs are separated by a full blank line, like the
specimen.

The **hero/title cluster** is a self-contained brand block echoing the PDF cover, so its
lineage uses a bespoke larger size (`1.3rem`, black bold) rather than a chrome token.
Like the demos, the cover cluster is exempt from the four-size scale.

Base font-size is `16px`. **Reading line-height is one of exactly two** (matching the
PDF specimen): `--lh` (`1.5`) for prose and text samples, `--lh-tight` (`1.4`) for
terminal/code panels.
Structural/showcase line-heights (headings, the hero wordmark, the size-waterfall stack,
glyph rows) are exempt — they’re not reading text.

**Demo sizes are exempt.** The size waterfall (8–44px), the weight ladder, and the large
legibility/character glyphs set their own sizes (`--fs-glyph`, `--fs-glyph-sm`,
`--fs-glyph-lg`, or inline px).
These are content, not chrome — do not fold them into the scale.

## Weight

Three weights for chrome:

| Token | Value | Used for |
| --- | --- | --- |
| `--fw-regular` | `400` | Body text |
| `--fw-medium` | `500` | Hero wordmark, **h2 major-section headings**; on compare, **widget input values** and **chrome hint labels** (see Components → Compare-page labels) |
| `--fw-bold` | `700` | Bold, h3 sub-headers, **widget field labels** (caps gray), buttons |

The weight-ladder demo uses all ten faces (400/500/600/700/800 × upright/italic) — that
is the content of that demo, not a license to use other weights in the chrome.

## Headings

Two levels, mirroring the PDF specimen’s heading roles:

| Level | Looks like | Mirrors (specimen) |
| --- | --- | --- |
| **`h2` — major section** | `--fs-h2`, **medium (500)**, **Title Case**, with a full-width underline rule below | `section()` |
| **`h3` — sub-header** | `--fs-body`, **BOLD CAPS** (uppercase), no rule | `about-heading()` |

Do not introduce an h4 in prose.
Field captions inside demos use `.label` (small gray caps), which reads as a quieter
tier than an h3 (body black caps) — black vs gray, body vs small, exactly the two-color
/ two-size split.

- The homepage hero title, lineage, tagline/prose, and content headings stay in
  Planetaire Mono Text.
  The sans-serif UI face is reserved for chrome such as the top nav, tabs, buttons,
  theme switch, footer, and comparison controls.

- **`h3` sits in the regular paragraph rhythm** — the gap above and below it equals the
  one paragraph gap (`--space-para`), shared with `<p>`, for a traditional manuscript
  feel (same as the specimens).
  No extra heading space.

## Spacing

- Page: max width `720px`, centered, with `8px` top padding and `96px` bottom padding.
  The shared nav can expand to the wider `--nav-max` measure on large screens.
- One paragraph gap, `--space-para` (`1.6rem`), is shared by `<p>` and `h3`.
- **Hero** mirrors the specimen cover’s generous vertical rhythm: wide planet frame (max
  `940px`), ample space below it, and one shared `--hero-stack-gap` between the title,
  lineage, intro, CTAs, and theme switch.
  The hero intro is a single bold statement, slightly larger than body text and
  constrained by character measure so it wraps intentionally.
  When in doubt, give the title more room, not less.
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
  softer than an inverse button.
  Tab indicators are the one explicit exception and use `--tab-indicator-width`.
- **Checkboxes:** one global `input[type="checkbox"]` style (`style.css`) for every box
  on the site. The box is a `--gray` outline on a transparent fill; checking it fills
  with `--soft-selected-bg` — the same gray as an active/pressed button — so a checked
  box and a selected button read as one selected state. The tick is drawn thicker than
  the box border via its own `--checkmark-stroke-width` (`2px` vs `--chrome-border-width`
  `1px`), the one place a glyph stroke outweighs the chrome border.
  `--soft-selected-bg` is a shared color token: `#e8eaed` light, a translucent gray dark.
- **Tabs:** tab labels use shared block and inline padding tokens so hover backgrounds
  have even top/bottom space and a small left/right cushion.
  The active underline is the tab’s own bottom border (`--tab-indicator-width`), so it
  always matches the hover background width.
- **Top nav:** a minimal gray caps row above the hero.
  A back-link (`← ojoshe.com`) sits flush left, the Planetaire and Compare page tabs are
  centered, and GitHub (an external arrow link, no active-tab state) sits flush right.
  Planetaire and Compare are page tabs using the same active underline as the main
  section tabs.
  **Bar alignment rule** (shared by the nav and all tab rows): the hairline always
  spans the wide bar measure (`--bar-width`, built from `--nav-max` and
  `--page-gutter`, the body side padding that compare widens past the phone layout),
  and the labels are **centered at every width**.
  A three-column grid (`1fr auto 1fr`) holds the page tabs in the centered middle
  column regardless of font size or which side label is wider, so the nav reads the
  same when toggling between pages whose text columns differ (`--max` vs
  `--compare-max`).
  On **very narrow screens** (below `520px`, where the four items stop fitting on one
  line) the row splits in two: back-link and GitHub flush to the edges on the top
  line, page tabs centered below, with the per-label vertical padding trimmed so the
  two rows hug (like the tab bar's wrapped line) instead of stacking tall.
- **Compare page header:** a compact utility-page title in the sans-serif UI face, with
  optional italic gray supporting copy below it.
  Keep this lighter than the homepage hero so the controls and proofs remain the primary
  interface.
- **Compare-page labels (two kinds, deliberately distinct):** all the chrome on the
  compare page uses the sans UI face and `--gray`, but text splits into two tiers by role:
  - **Widget field labels** — the *official* name of an input: **CAPS, bold
    (`--fw-bold`), letter-spaced**. These name a control (`TEXT SAMPLE`, `FONT SIZE`,
    `STYLE`, `FONT WEIGHT`, `LINE HEIGHT`, `CARD SIZE`, `FONTS`). They anchor each control,
    so they stay the heaviest gray tier.
  - **Hints / extra detail** — secondary chrome that isn't a control's name:
    **mixed case, medium (`--fw-medium`)**. This covers checkbox labels (*Show Font
    Names*), font-group titles (*Popular Fonts*), group toggles, and the arrow-key tip.
    Lower case and lighter than a field label, but the **same weight as a widget value**,
    so detail and values read as one quieter tier under the bold field labels.
  - **Widget values** — the selected setting *inside* each input (the chosen
    sample / size / style / weight / line-height / card-size / font): same sans face at
    **medium (`--fw-medium`)**, a touch more prominent than plain body and balanced
    against the bold field labels.
  Buttons (`Popular` / `All` / `Clear`, the view tabs) stay **bold caps**; the Light/Dark
  switch is unchanged; the sample-text editor keeps the monospace `--editor-font`, off this
  scale. All weights are the `--fw-*` tokens — no literal weights in `compare.css`.
- **Buttons:** hero actions use identical style: `--ink` border, transparent fill, and
  invert on hover. No primary/secondary distinction.
  Keep the Compare Fonts CTA as its own centered row directly above the theme switch.
- **Theme switch:** a centered Light/Dark control below the hero CTAs (not a corner
  toggle) — seeing the font on both backgrounds is a primary way to evaluate it.
  Two **equal-width** segments; the **current** theme is the filled (emphasized)
  segment, the other muted gray, so the fill alone shows the position (no label).
  Flips `data-theme` on `<html>`, persists to a **1-year cookie** (`plt-theme`, with a
  `localStorage` fallback) so the choice sticks on revisit, and defaults to the OS
  preference on first visit.
- **Main tabs:** the About / FAQ / Samples / Installation row below the hero, **centered
  at every width** like the top nav, per the bar alignment rule above. Tabs are caps
  labels on a hairline rule, with the current tab marked by an
  `--ink` underline. When the row wraps on very narrow screens, the wrapped line hugs
  the first (small row gap), and arrowed labels like GitHub never break between text
  and arrow (`white-space: nowrap`). These are *section tabs*: a pinned scrollspy over
  one stacked document at every width — see “Tabs and scrolling” below for the three
  tab kinds and their rules.
- **Theme transition:** light↔dark eases gently in a **tiered cascade** rather than
  one flat fade. Every themeable property (`background-color`, `border-color`, `color`,
  `fill`, `filter`) starts easing at the same instant on toggle, but finishes at one of
  three durations, so the change ripples down the page: **fast** (`--fade-fast`, the
  controls and the page background, which also drives chrome hover feedback),
  **medium** (`--fade-medium`, the hero cluster: wordmark, lineage, tagline, and the
  planet's invert), and **slow** (`--fade-slow`, the page default for everything else).
  The slow tier is set once on `*`; the fast tier rides on `--ui-transition`; the medium
  tier is a dedicated rule on the hero leaves. All three durations collapse to `0` under
  `prefers-reduced-motion` (set on `:root`, so even the higher-specificity tier rules
  resolve to no motion).
- **Dark-mode planet:** the SVG is black line art, so dark mode inverts it
  (`filter: invert(1)`) to keep it visible.
- **Star separator (`.starsep`):** a centered row of three distinct stars copied
  verbatim from the cover graphic (`assets/little-planet.svg`), from the cluster left of
  the planet — two hollow sparkles flanking a plump outline star, with their original
  paths and stroke widths kept so the row echoes the cover exactly (no redrawn or
  normalized geometry).
  It marks the lead-in above the section tabs (`--lead`) and the break between stacked
  panels (`--section`), where it supplies the boundary air the panels would otherwise get
  from the tab-boundary gap.
  The shapes live once in the `#plt-star-*` SVG sprite (each `<symbol>` carries the
  star's own cover-coordinate `viewBox`) and are reused via `<use>`.
  Each star gets a small, different `translateY` so the trio reads as hand-placed and
  slightly accidental rather than a ruler-straight row (visual only — transforms don't
  reflow, so the separator height is unchanged).
  Decorative, so the row is `aria-hidden` (the headings carry the structure) and the
  stars are full `--ink`, echoing the planet line art and inverting with the theme via
  `currentColor` rather than a new color token.
- **Tables / spec grid / code panels / glyph rows:** styled once in `style.css`; reuse
  the classes rather than adding inline styles.
- **Narrow tables:** tables may self-scroll horizontally below the small-screen
  breakpoint so multi-column release/config data remains reachable while page-level
  overflow stays clipped for the hero planet.
- **Compare cards pan, they don’t scroll:** in the compare page’s card view each proof’s
  text is clipped (`overflow: hidden`), so the wheel/trackpad always scrolls the page —
  no scroll trap inside a card (the “never hijack scrolling” rule). To look closer you
  **drag** any card (grab → grabbing cursor); every card pans by the **same** horizontal
  and vertical offset, so the same slice of text lines up across all fonts for
  piece-by-piece comparison. `compare.js` drives this with Pointer Events (one path for
  mouse/touch/pen) by re-applying a shared `scrollLeft`/`scrollTop` to every card. The
  full-page view is the real-size proof and keeps native scroll + text selection.
- **One card-name overlay at a time:** when labels are overlaid (Show Labels off), the
  name tip appears for the single card that is hovered or keyboard-focused, never two at
  once. `compare.js` owns one `.is-tip` card: hover sets it and wins over focus (so a
  focused card’s tip clears the moment you hover another), tabbing through cards shows it
  for keyboard users, and a drag clears it for the duration of the pan. A single-source
  class is deliberate — CSS `:hover` + `:focus` would light up two tips at once.
- **Keyboard focus:** links and buttons use a visible `--ink` focus outline.
  Segmented theme buttons draw the outline inside the control so it is not clipped by
  the group.

## Tabs and scrolling

The site has **three kinds of tabs**, distinguished by what switching them means.
They share one look (`.tab-opt` caps labels, `--ink` underline indicator on a hairline
rule) but deliberately different behavior:

| Kind | Example | Switching means | Active state |
| --- | --- | --- | --- |
| **Page tabs** | Planetaire / Compare (top nav) | navigating to another page | `aria-current="page"` |
| **View tabs** | Card View / Page View (compare) | re-rendering the same content | `aria-selected` |
| **Section tabs** | About / FAQ / Samples / Installation | moving within one document | `aria-current="true"` |

Pick by use: separate apps or pages get page tabs; alternate renderings of the same
content get view tabs (classic show/hide switchers); sections of one readable document
get section tabs. Do not turn view or page tabs into scrollspies — they switch context,
not position. In CSS, `.tabs` is only the shared row look; the pinning and breakout
live on the `.section-tabs` modifier (and `scroll-tabs.js` matches only
`.section-tabs`), so view and page tab rows can never inherit scrollspy behavior.

**Section tabs** are a sticky **scrollspy** (the pattern in food-delivery menu
categories and docs-site tables of contents) over panels stacked in tab order, at every
width. `scroll-tabs.js` owns the behavior and `style.css` the look; this section is the
spec for both.

**Scrolling UX rules:**

- **Never hijack scrolling.** No overscroll capture, no scroll-snap between sections, no
  animated panel swaps.
  Momentum scrolling stays native.
- **The indicator derives from scroll position alone:** the active tab is the last
  section whose top has crossed the activation line just under the pinned bar (page
  bottom counts as the last section).
  Position, not direction, so scrolling back up reverses it for free.
- **Tap = jump:** smooth scroll to the section, instant under `prefers-reduced-motion`.
  While a tap-scroll glides, the spy is suppressed so intermediate tabs don’t flash.
- **History stays clean:** the hash is rewritten with `replaceState` only, never
  `pushState`. A clean URL stays clean while you are in the first section; crossing a
  boundary writes `#faq` etc., so reload and share reflect position.
- **Anchors land below the bar** via `scroll-margin-top: var(--tabbar-h)`; the JS
  measures the bar (its labels can wrap on very narrow screens) instead of hardcoding a
  height.

**Look and feel:**

- The pinned bar is opaque `--bg` with the existing hairline rule as its bottom edge.
  **One depth cue:** a small drop shadow appears only while content actually scrolls
  underneath the pinned bar (`is-stuck`, toggled by `scroll-tabs.js` from the bar's
  position); in normal flow the bar stays flat, per the minimal chrome principle.
- The bar follows the bar alignment rule (see Top nav): it breaks out to the wide
  `--bar-width` measure so its hairline reads as a full-width rule when pinned, with
  labels centered at every width.
- **Tab boundaries get extra air:** `--space-tab-boundary` (`6.5rem`) above the first
  heading of each panel after the first, versus the normal `4.25rem` h2 gap, so one
  tab’s section clearly ends before the next begins while scrolling.
- Every panel after the first opens with a tab-boundary heading (a normal `h2`; the
  `.stacked-heading` class marks the ones added purely as boundaries), so the page reads
  like one continuous document.
  The hero is the About panel’s header; an `h2` directly after a boundary heading sits
  closer (`2rem`) since the boundary already provides the break.

**Accessibility and structure:**

- Section tabs are navigation, not ARIA tabs: no `tablist`/`tab`/`tabpanel` roles, the
  active tab is `aria-current`, and the buttons sit in the normal tab order.
  All content is in the document, in reading order, so find-in-page and print see
  everything.
- `html`/`body` overflow guards must stay `overflow-x: clip`, never `hidden`: `hidden`
  creates a scroll container, which silently defeats the sticky bar.

## Checklist before adding anything

1. Can an existing token express it?
   Use that.
2. Is it chrome or content?
   Chrome must stay on the scale; only demos get free sizes.
3. Does it need a new color?
   Almost certainly no — try `--ink`, `--gray`, weight, or size.
4. If you truly need a token, add it here **and** in `style.css`, with a one-line
   reason.
