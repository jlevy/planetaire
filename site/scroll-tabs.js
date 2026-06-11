/* Scroll-through tabs: the tab bar is a sticky scrollspy over one continuous
 * document, at every width.
 *
 * All panels render stacked in tab order. The bar pins to the viewport top
 * (position: sticky in CSS) and the active tab derives from scroll position
 * alone, so scrolling down and back up both move it with no direction logic,
 * and there is never any scroll hijacking. Tapping a tab smooth-scrolls to
 * its section; anchors and deep links are plain native hash navigation.
 *
 * Reusable contract:
 * - A bar (".section-tabs") of buttons (".tab-opt") with
 *   data-tab-set="<panel-id>". Plain ".tabs" rows (page/view tabs) are
 *   deliberately not matched; only section tabs scroll-spy.
 * - Panels (".tab-panel") whose ids match, in the same DOM order as the tabs.
 * - CSS pins the bar and offsets anchors with
 *   scroll-margin-top: var(--tabbar-h), measured here (the bar's height
 *   changes when its labels wrap on narrow screens).
 *
 * See site/design-system.md ("Tabs and scrolling") for the UX rules.
 */
(function () {
  const bar = /** @type {HTMLElement | null} */ (document.querySelector(".section-tabs"));
  const tabs = /** @type {HTMLButtonElement[]} */ (
    Array.from(document.querySelectorAll(".section-tabs .tab-opt"))
  );
  const panels = /** @type {HTMLElement[]} */ (Array.from(document.querySelectorAll(".tab-panel")));
  if (!bar || !tabs.length || !panels.length) {
    return;
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  let currentName = "";
  let suppressSpy = false;
  let scrollQueued = false;

  /* Hash bookkeeping is cosmetic; some contexts (file:// previews, sandboxed
     iframes) forbid history updates, and the tabs must keep working there. */
  const setHash = (hash) => {
    try {
      history.replaceState(null, "", hash);
    } catch (_e) {
      /* The URL just won't reflect position. */
    }
  };

  /* jsdom (the smoke tests) has no scrollIntoView; guard rather than crash. */
  const scrollToElement = (element, behavior) => {
    if (typeof element.scrollIntoView === "function") {
      element.scrollIntoView({ behavior, block: "start" });
    }
  };

  /* The active tab reflects scroll position only: the last section whose top
     has crossed an activation line just below the pinned bar, except at the
     very bottom of the page, which always counts as the last section (a short
     final section might never reach the line). */
  const activePanel = () => {
    const scrollBottom = window.scrollY + window.innerHeight;
    if (scrollBottom >= document.documentElement.scrollHeight - 2) {
      return panels[panels.length - 1];
    }
    const line = bar.getBoundingClientRect().bottom + 1;
    for (let i = panels.length - 1; i >= 0; i--) {
      if (panels[i].getBoundingClientRect().top <= line) {
        return panels[i];
      }
    }
    return panels[0];
  };

  const setCurrent = (name) => {
    if (name === currentName) {
      return false;
    }
    currentName = name;
    tabs.forEach((tab) => {
      if (tab.dataset.tabSet === name) {
        tab.setAttribute("aria-current", "true");
      } else {
        tab.removeAttribute("aria-current");
      }
    });
    return true;
  };

  /* Scrolling rewrites the hash with replaceState only (no history spam), and
     a clean URL stays clean while you are still in the first section. */
  const updateHashFor = (name) => {
    if (!location.hash && name === panels[0].id) {
      return;
    }
    if (location.hash !== `#${name}`) {
      setHash(`#${name}`);
    }
  };

  const onScroll = () => {
    if (scrollQueued) {
      return;
    }
    scrollQueued = true;
    requestAnimationFrame(() => {
      scrollQueued = false;
      /* Depth cue: the bar casts a small shadow only while it is actually
         pinned with content scrolling underneath (tracked even during a
         tap-glide, when the spy itself is suppressed). */
      bar.classList.toggle("is-stuck", bar.getBoundingClientRect().top <= 0);
      if (suppressSpy) {
        return;
      }
      const panel = activePanel();
      if (setCurrent(panel.id)) {
        updateHashFor(panel.id);
      }
    });
  };

  /* Anchors must land below the pinned bar; the bar's height is dynamic (the
     labels can wrap on very narrow screens), so measure it into a custom
     property that scroll-margin-top uses. */
  const measureBar = () => {
    document.documentElement.style.setProperty("--tabbar-h", `${bar.offsetHeight}px`);
  };

  const onResize = () => {
    measureBar();
    onScroll();
  };

  /* Tap = jump. The indicator updates immediately and the spy stays quiet
     until the glide ends so intermediate tabs don't flash. */
  const jumpTo = (panel) => {
    setCurrent(panel.id);
    setHash(`#${panel.id}`);
    suppressSpy = true;
    let released = false;
    const release = () => {
      if (released) {
        return;
      }
      released = true;
      suppressSpy = false;
      onScroll();
    };
    if ("onscrollend" in window) {
      window.addEventListener("scrollend", release, { once: true });
    }
    window.setTimeout(release, 900);
    scrollToElement(panel, reduceMotion.matches ? "auto" : "smooth");
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const panel = panels.find((candidate) => candidate.id === tab.dataset.tabSet);
      if (panel) {
        jumpTo(panel);
      }
    });
  });

  measureBar();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onResize);

  /* Deep links: every target is in the document, so the browser handles the
     initial #hash itself; re-scroll once after --tabbar-h is set so the
     target lands below the pinned bar. */
  if (location.hash) {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target) {
      requestAnimationFrame(() => scrollToElement(target, "auto"));
    }
  }
  onScroll();
})();
