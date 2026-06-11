# Feature: Mobile Scroll-Through Tabs (Stacked Scrollspy)

**Date:** 2026-06-10

**Author:** jlevy (with Claude Code)

**Status:** Implemented, then unified: after on-device testing, the stacked scrollspy
became the only mode at all widths (plt-use9 resolved Open Question 1), deleting the
tabbed mode entirely. Phase 2 extraction remains open as plt-9uiq.

## Overview

On narrow screens, the index page’s tabs (About, FAQ, Samples, Installation) become
sections of one continuously scrollable document.
The tab bar pins to the top of the viewport once the hero scrolls away, and then serves
two roles: a position indicator (the active tab follows whatever section is under the
reading line, scrolling down or back up) and jump navigation (tapping a tab scrolls to
its section).
Scrolling past the end of one tab flows directly into the next, which opens
with a clean section header, so the whole page reads like a single document.
Desktop keeps the existing show/hide tab behavior.

## Goals

- Reaching the end of a tab on mobile is no longer a dead end: continued scrolling moves
  into the next tab’s content with no extra gesture.
- The tab bar slides into a pinned position at the top of the page and stays there while
  reading; the active indicator moves (for example About to FAQ) so you always know
  where you are.
- The indicator derives from scroll position alone, so scrolling back up reverses it
  with no special casing.
- Tabs stay tappable as jump navigation, and existing `#hash` deep links keep working in
  both modes.
- The mechanism is small, dependency-free, and reusable on other static sites.

## Non-Goals

- **No scroll hijacking.** We never capture overscroll to animate a hidden panel into
  view. That variant fights momentum scrolling, find-in-page, and accessibility (see
  Prior Art).
- Desktop (above 620px) behavior is unchanged in this iteration; unifying the two modes
  is an open question below.
- `compare.html` is out of scope: its tabs switch rendering modes of the same content,
  not document sections.
- No URL scheme changes: hashes remain `#about`, `#faq`, etc., plus the existing
  in-section anchors.

## Background

### Current Implementation

The tab bar is `nav.tabs` with `button.tab-opt` elements (`role="tablist"`/`tab`), and
the panels are `section.tab-panel` elements (`role="tabpanel"`) toggled with the
`hidden` attribute. An inline script in `site/index.html` manages `aria-selected`, the
`hidden` toggles, hash `pushState`, a View Transitions fade, and hash-link delegation so
anchors into hidden panels activate the containing tab.
The site’s mobile breakpoint is 620px.

The mobile pain: the tab bar sits below the hero, so after reading About to the end you
must scroll all the way back to the top to reach another tab.
Hidden panels are also invisible to find-in-page and printing.

### Prior Art

This is a well-established pattern, usually called **scrollspy** (after Bootstrap’s
ScrollSpy component, in wide use since roughly 2012), or a **sticky section nav** or
**anchored tabs**. Mainstream examples:

- **Food-delivery menus** (DoorDash, Uber Eats, Deliveroo): the category tab bar pins
  under the header; scrolling the menu updates the active category in both directions;
  tapping a category jumps to it.
  This is the closest match to what we want.
- **Docs sites and tables of contents** (Bootstrap docs, MDN): a side or top nav
  highlights the section currently in view.
- **Mobile app detail pages** (Google Play app pages, Twitter/X profiles): a tab bar
  pins under a collapsing header.
  Android Material Design ships this as standard CollapsingToolbar-plus-TabLayout
  behavior.

The other variant, literally swapping hidden tab panels when you overscroll
(fullpage.js-style), exists but is widely considered hostile on mobile.
The proven version is the reframe below.

### The Reframe

“Tabs that switch automatically as you scroll” falls out naturally once tabs stop being
views and become anchors into one continuous document.
The next tab’s content literally begins where the previous one ends; the only thing that
“switches” is the indicator.
Both scroll directions work for free because the active tab is computed from scroll
position, not from scroll events or direction.

## Design

### Approach

A small mode controller watches `matchMedia('(max-width: 620px)')` and converts the tabs
to **stacked mode** (and back) when the viewport crosses the breakpoint:

1. **Stack the panels.** Remove `hidden` from all panels; DOM order already matches tab
   order.

2. **Section headers.** Panels after the first get a section-divider header carrying the
   tab’s name, shown only in stacked mode.
   FAQ already opens with an `h2` reading “FAQ”; Samples and Installation need one.
   About needs none: the hero is its header.

3. **Pin the bar.** `.tabs { position: sticky; top: 0; }` with an opaque background and
   a z-index. Pure CSS gives both the slide-into-place and the unpin when scrolling back
   to the top. The bar's existing bottom hairline is the only stuck-state treatment (no
   shadow and no stuck-detection sentinel), per the design system's minimal chrome.
   Gotcha: `html`/`body` used `overflow-x: hidden`, which can defeat
   `position: sticky`; the guard is now `overflow-x: clip`, which clips without
   creating a scroll container.
   Verify sticky early on iOS Safari.

4. **Spy.** The active section is the last one whose top has crossed an activation line
   just below the pinned bar, with one override: at the very bottom of the page, force
   the last tab (a short final section might never reach the line).
   Updates are driven by a rAF-throttled passive scroll listener: with four sections the
   per-frame cost is negligible, and unlike an IntersectionObserver's static
   `rootMargin` it needs no observer rebuild when the bar's height changes (the labels
   can wrap on very narrow screens).
   Conceptual core:

   ```js
   // Active section = last one whose top is above the activation line.
   function activeSection() {
     if (atPageBottom()) return sections.at(-1);
     const line = bar.getBoundingClientRect().bottom + 1;
     return sections.findLast((s) => s.getBoundingClientRect().top <= line) ?? sections[0];
   }
   ```

5. **Tap to jump.** `scrollIntoView({ behavior: "smooth" })`, instant under
   `prefers-reduced-motion`; update the hash with `replaceState`; suppress the spy until
   `scrollend` (timeout fallback where unsupported) so intermediate tabs don’t flash
   during the glide.

6. **Anchors.** Set `scroll-margin-top` (roughly bar height plus breathing room) on
   panels and in-section `[id]` targets so native anchor navigation lands below the
   pinned bar. In stacked mode the hash-activation JS stands down; the browser’s own
   anchor handling does the work.

7. **ARIA.** Stacked mode is navigation, not tabs: drop the `tablist`/`tab`/`tabpanel`
   roles and switch `aria-selected` to `aria-current`. The CSS indicator keys on either
   attribute. This is also an accessibility improvement: all content is reachable, in
   reading order, with no tab interaction required.

8. **URL.** When the active tab changes by scrolling, `replaceState` the panel hash so
   reload and share reflect position without polluting history.

### Components

- **`site/scroll-tabs.js` (new):** the mode controller, spy, and jump logic, roughly 150
  lines, no dependencies.
  Must pass the existing `biome` and `tsc` site checks.
  The current inline tab script moves here so desktop and stacked logic live together.
- **`site/index.html`:** stacked section headers; replace the inline tab script with a
  `<script src>` tag (cache-busted like the other site scripts).
- **`site/style.css`:** roughly 30 lines inside the 620px media query (sticky bar, stuck
  state, stacked headers, `scroll-margin-top`), plus the `overflow-x: clip` change.

### Reusable Contract

The module generalizes to any page shaped like “a nav bar of in-page links plus
sections”: configuration is the bar element, the section list (derived from the tabs’
targets), the breakpoint, and the top offset.
Everything else (sticky pinning, spy, jump, ARIA swap) is behavior.
Document the contract in the file header so it can be copied to other sites (ojoshe.com
pages are natural candidates).

Platform note: CSS scroll-driven animations and the proposed `::scroll-marker` features
point toward a no-JS version of this pattern eventually, but as of mid-2026 they are not
reliably cross-browser, so IntersectionObserver remains the portable choice.

### Edge Cases

- **Bar wraps to two lines** on very narrow screens: measure the bar’s height for the
  activation line and `scroll-margin-top` rather than hardcoding it.
- **Short final section:** covered by the bottom-of-page override.
- **Programmatic scroll:** spy suppressed until `scrollend`, with a timeout fallback.
- **iOS dynamic toolbar:** viewport height changes as the toolbar collapses; avoid
  vh-based math (the activation line is computed from the bar’s rect, which is immune).
- **Find-in-page and print get better,** not worse: stacked mode has all content in the
  document.

## Implementation Plan

### Phase 1: Ship Stacked Scrollspy on index.html

- [x] Extract the inline tab controller to `site/scroll-tabs.js` with desktop behavior
  unchanged (pure refactor, verified before the next step).
- [x] Change the `overflow-x` guard to `clip` and add stacked-mode CSS: sticky bar,
  stuck state, section headers, `scroll-margin-top`.
- [x] Add the mode controller (matchMedia), panel unhiding, and ARIA swap.
- [x] Add the spy with bottom override, tap-to-jump with spy suppression, and hash
  `replaceState`.
- [x] Bump cache-bust queries; pass `npm run site:lint`; run the manual checklist.

### Phase 2: Extract as a Reusable Pattern (after Phase 1 settles)

- [ ] Generalize the `scroll-tabs.js` configuration and document the HTML contract in
  the file header.
- [ ] Consider adoption on other ojoshe.com pages, and whether `compare.html` wants any
  of it.

## Testing Strategy

- `npm run site:lint` (biome format, tsc, html-validate, link integrity, smoke) stays
  green.
- Manual at 620px and below: scroll down through all three boundaries (About to FAQ to
  Samples to Installation) and back up, confirming the indicator follows in both
  directions; tap each tab; load fresh with `#terminal` and `#faq` deep links; use
  back/forward; check `prefers-reduced-motion` jumps instantly; rotate and resize across
  the breakpoint in both directions; check light and dark themes.
- Desktop: tab behavior and the View Transitions fade are unchanged.
- Optionally extend `devtools/site-smoke.mjs` to assert the stacked DOM (no `hidden`
  panels) at a narrow viewport.

## Open Questions

1. **Unify on stacked mode for desktop too?** Resolved 2026-06-10 (plt-use9): yes.
   After testing the stacked mode, scrollspy became the only mode at all widths,
   deleting the tabbed mode, the View Transitions fade, and the matchMedia mode
   controller. Traditional tabs remain the right pattern for the *other* tab kinds
   (page tabs in the top nav, view tabs on compare); see design-system.md, "Tabs and
   scrolling", for the taxonomy.
2. **Hash updates on scroll:** recommended yes (replaceState only, at tab boundaries),
   but easy to drop if it feels noisy.
3. **Header titles** for Samples and Installation in stacked mode: reuse the tab labels
   or fuller titles ("Type Samples", “Install and Configure”)?

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
