/* Scroll-through tabs: one tab bar, two modes.
 *
 * Tabbed (wide screens): classic tabs. One panel visible at a time, panels
 * toggled with [hidden], tablist/tab/tabpanel roles, hash pushState, and a
 * View Transitions fade. Hash links into a hidden panel activate that panel.
 *
 * Stacked (narrow screens): all panels stack in tab order into one continuous
 * document. The bar pins to the viewport top (position: sticky in CSS) and
 * becomes a scrollspy: the active tab derives from scroll position alone, so
 * scrolling down and back up both move it with no direction logic, and there
 * is never any scroll hijacking. Tapping a tab smooth-scrolls to its section.
 *
 * Reusable contract:
 * - A bar (".tabs") of buttons (".tab-opt") with data-tab-set="<panel-id>".
 * - Panels (".tab-panel") whose ids match, in the same DOM order as the tabs.
 * - CSS keys stacked styles off body.tabs-stacked (set here, only below the
 *   breakpoint) and offsets anchors with scroll-margin-top: var(--tabbar-h)
 *   (measured here). The breakpoint lives only in STACKED_MQ.
 *
 * See site/design-system.md ("Tabs, scrolling, and mobile") for the UX rules.
 */
(function () {
  /* Must match the site's single mobile breakpoint (see design-system.md). */
  const STACKED_MQ = "(max-width: 620px)";

  const bar = /** @type {HTMLElement | null} */ (document.querySelector(".tabs"));
  const tabs = /** @type {HTMLButtonElement[]} */ (
    Array.from(document.querySelectorAll(".tab-opt"))
  );
  const panels = /** @type {HTMLElement[]} */ (Array.from(document.querySelectorAll(".tab-panel")));
  const content = document.querySelector(".tab-content");
  if (!bar || !tabs.length || !panels.length) {
    return;
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const stackedQuery = window.matchMedia(STACKED_MQ);
  let stacked = false;

  /* Hash bookkeeping is cosmetic; some contexts (file:// previews, sandboxed
     iframes) forbid history updates, and the tabs must keep working there. */
  const setHash = (hash, options = {}) => {
    try {
      if (options.push) {
        history.pushState(null, "", hash);
      } else {
        history.replaceState(null, "", hash);
      }
    } catch (_e) {
      /* The URL just won't reflect position. */
    }
  };

  /* ---- Tabbed mode (classic tabs) ---------------------------------------- */

  let transitionTimer = null;

  const transition = (update) => {
    if (document.startViewTransition) {
      try {
        const viewTransition = document.startViewTransition(update);
        if (viewTransition.ready) {
          viewTransition.ready.catch(() => {});
        }
        if (viewTransition.updateCallbackDone) {
          viewTransition.updateCallbackDone.catch(() => {});
        }
        if (viewTransition.finished) {
          viewTransition.finished.catch(() => {});
        }
      } catch (_e) {
        update();
      }
    } else if (content && !reduceMotion.matches) {
      clearTimeout(transitionTimer);
      content.classList.add("is-transitioning");
      transitionTimer = setTimeout(() => {
        update();
        requestAnimationFrame(() => content.classList.remove("is-transitioning"));
      }, 80);
    } else {
      update();
    }
  };

  const panelForHash = (hash) => {
    if (!hash || hash === "#") {
      return null;
    }
    const id = decodeURIComponent(hash.slice(1));
    const direct = panels.find((panel) => panel.id === id);
    if (direct) {
      return direct.id;
    }
    const target = document.getElementById(id);
    const panel = target?.closest(".tab-panel");
    return panel ? panel.id : null;
  };

  const activate = (name, options = {}) => {
    const panelName = panels.some((panel) => panel.id === name) ? name : panels[0].id;
    tabs.forEach((tab) => {
      const selected = tab.dataset.tabSet === panelName;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    panels.forEach((panel) => {
      panel.hidden = panel.id !== panelName;
    });
    if (options.push) {
      setHash(`#${panelName}`, { push: true });
    }
  };

  const activateForHash = (hash, options = {}) => {
    const panelName = panelForHash(hash) || panels[0].id;
    const update = () => activate(panelName, options);
    if (options.transition) {
      transition(update);
    } else {
      update();
    }
    if (options.scroll && hash && hash !== `#${panelName}`) {
      requestAnimationFrame(() => {
        const target = document.getElementById(decodeURIComponent(hash.slice(1)));
        if (target) {
          scrollToElement(target, "auto");
        }
      });
    }
  };

  /* ---- Stacked mode (one document + scrollspy) ---------------------------- */

  let currentName = "";
  let suppressSpy = false;
  let scrollQueued = false;

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
    if (scrollQueued || suppressSpy) {
      return;
    }
    scrollQueued = true;
    requestAnimationFrame(() => {
      scrollQueued = false;
      if (suppressSpy || !stacked) {
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

  const enterStacked = (options = {}) => {
    document.body.classList.add("tabs-stacked");
    bar.removeAttribute("role");
    tabs.forEach((tab) => {
      tab.removeAttribute("role");
      tab.removeAttribute("aria-selected");
      tab.tabIndex = 0;
    });
    panels.forEach((panel) => {
      panel.removeAttribute("role");
      panel.hidden = false;
    });
    measureBar();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize);
    currentName = "";
    if (options.scrollToHash && location.hash) {
      const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) {
        requestAnimationFrame(() => scrollToElement(target, "auto"));
      }
    }
    onScroll();
  };

  const exitStacked = () => {
    window.removeEventListener("scroll", onScroll);
    window.removeEventListener("resize", onResize);
    document.body.classList.remove("tabs-stacked");
    document.documentElement.style.removeProperty("--tabbar-h");
    bar.setAttribute("role", "tablist");
    tabs.forEach((tab) => {
      tab.setAttribute("role", "tab");
      tab.removeAttribute("aria-current");
    });
    panels.forEach((panel) => {
      panel.setAttribute("role", "tabpanel");
    });
    currentName = "";
    activateForHash(location.hash);
  };

  /* ---- Wiring -------------------------------------------------------------- */

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const name = tab.dataset.tabSet;
      if (stacked) {
        const panel = panels.find((candidate) => candidate.id === name);
        if (panel) {
          jumpTo(panel);
        }
        return;
      }
      transition(() => activate(name, { push: true }));
    });
    tab.addEventListener("keydown", (event) => {
      /* Roving arrows belong to tablist semantics; stacked tabs are plain
         buttons in the normal tab order. */
      if (stacked || (event.key !== "ArrowLeft" && event.key !== "ArrowRight")) {
        return;
      }
      event.preventDefault();
      const current = tabs.indexOf(tab);
      const dir = event.key === "ArrowRight" ? 1 : -1;
      const next = tabs[(current + dir + tabs.length) % tabs.length];
      next.focus();
      transition(() => activate(next.dataset.tabSet, { push: true }));
    });
  });

  /* In tabbed mode, hash links into a hidden panel must activate it first. In
     stacked mode every target is already in the document, so native anchor
     behavior (plus scroll-margin-top) does everything. */
  document.addEventListener("click", (event) => {
    if (stacked) {
      return;
    }
    const target = event.target;
    if (!(target instanceof Element)) {
      return;
    }
    const link = target.closest('a[href^="#"]');
    if (!link) {
      return;
    }
    const hash = link.getAttribute("href");
    const panelName = panelForHash(hash);
    if (!panelName) {
      return;
    }
    event.preventDefault();
    setHash(hash, { push: true });
    activateForHash(hash, { scroll: true, transition: true });
  });

  window.addEventListener("popstate", () => {
    if (stacked) {
      return; /* native anchor/back behavior; the spy follows the scroll */
    }
    activateForHash(location.hash, { scroll: true, transition: true });
  });

  stackedQuery.addEventListener("change", () => {
    stacked = stackedQuery.matches;
    if (stacked) {
      enterStacked();
    } else {
      exitStacked();
    }
  });

  stacked = stackedQuery.matches;
  if (stacked) {
    enterStacked({ scrollToHash: true });
  } else {
    activateForHash(location.hash);
  }
})();
