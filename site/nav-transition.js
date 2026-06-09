(function () {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  document.addEventListener("click", (event) => {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.altKey || event.ctrlKey || event.shiftKey) return;

    const link = event.target.closest("a.site-nav-tab");
    if (!link || link.target || link.hasAttribute("download")) return;

    const nextUrl = new URL(link.href, window.location.href);
    const currentUrl = new URL(window.location.href);
    if (nextUrl.origin !== currentUrl.origin) return;

    const samePage =
      nextUrl.pathname === currentUrl.pathname &&
      nextUrl.search === currentUrl.search &&
      nextUrl.hash === currentUrl.hash;
    if (samePage || link.getAttribute("aria-current") === "page") {
      event.preventDefault();
      return;
    }

    if (reduceMotion.matches) return;

    event.preventDefault();
    root.classList.add("is-page-leaving");
    window.setTimeout(() => {
      window.location.href = nextUrl.href;
    }, 45);
  });

  window.addEventListener("pageshow", () => {
    root.classList.remove("is-page-leaving");
  });
})();
