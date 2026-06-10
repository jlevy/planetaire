/* Main tabs: About / FAQ / Samples / Installation. Hash links activate the
   panel containing their target so existing anchors keep working. */
(function () {
  const tabs = /** @type {HTMLButtonElement[]} */ (
    Array.from(document.querySelectorAll(".tab-opt"))
  );
  const panels = /** @type {HTMLElement[]} */ (Array.from(document.querySelectorAll(".tab-panel")));
  const content = document.querySelector(".tab-content");
  if (!tabs.length || !panels.length) {
    return;
  }

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
    } else if (content && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
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
    const panelName = panels.some((panel) => panel.id === name) ? name : "about";
    tabs.forEach((tab) => {
      const selected = tab.dataset.tabSet === panelName;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    panels.forEach((panel) => {
      panel.hidden = panel.id !== panelName;
    });
    if (options.push) {
      history.pushState(null, "", `#${panelName}`);
    }
  };

  const activateForHash = (hash, options = {}) => {
    const panelName = panelForHash(hash) || "about";
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
          target.scrollIntoView();
        }
      });
    }
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      transition(() => activate(tab.dataset.tabSet, { push: true }));
    });
    tab.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") {
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

  document.addEventListener("click", (event) => {
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
    history.pushState(null, "", hash);
    activateForHash(hash, { scroll: true, transition: true });
  });

  window.addEventListener("popstate", () =>
    activateForHash(location.hash, { scroll: true, transition: true }),
  );
  activateForHash(location.hash);
})();
