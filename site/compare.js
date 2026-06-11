const fontData = window.PlanetaireFontData || { fonts: [] };
/** @type {PlanetaireFont[]} */
const fonts = fontData.fonts;
const installedFontFaceIds = new Set();
let backgroundFontLoadStarted = false;

/**
 * @template {HTMLElement} T
 * @param {string} id
 * @returns {T}
 */
function requireElementById(id) {
  const element = document.getElementById(id);
  if (!element) {
    throw new Error(`Missing required element: #${id}`);
  }
  return /** @type {T} */ (element);
}

/**
 * @template {HTMLElement} T
 * @param {string} selector
 * @returns {T}
 */
function requireElement(selector) {
  const element = document.querySelector(selector);
  if (!element) {
    throw new Error(`Missing required element: ${selector}`);
  }
  return /** @type {T} */ (element);
}

function cssString(value) {
  return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function renderFontFace(font, face) {
  const family = face.family || font.family;
  const src = face.sources
    .map((item) => `url("${cssString(item.url)}") format("${cssString(item.format || "woff2")}")`)
    .join(",\n    ");

  return `@font-face {
  font-family: "${cssString(family)}";
  font-style: ${face.style || "normal"};
  font-display: swap;
  font-weight: ${face.weight || 400};
  src:
    ${src};
}`;
}

function fontFaceId(font, face) {
  return [font.id, face.family || font.family, face.style || "normal", face.weight || 400].join(
    "|",
  );
}

function installFontFacesFor(fontList) {
  const rules = [];
  for (const font of fontList) {
    for (const face of font.faces || []) {
      const id = fontFaceId(font, face);
      if (installedFontFaceIds.has(id)) {
        continue;
      }
      installedFontFaceIds.add(id);
      rules.push(renderFontFace(font, face));
    }
  }
  if (!rules.length) {
    return;
  }

  let style = document.getElementById("compare-font-faces");
  if (!style) {
    style = document.createElement("style");
    style.id = "compare-font-faces";
    document.head.appendChild(style);
  }
  style.appendChild(document.createTextNode(`${style.textContent ? "\n" : ""}${rules.join("\n")}`));
}

function currentProofFontSpec() {
  const styles = getComputedStyle(document.documentElement);
  const fontStyle = styles.getPropertyValue("--proof-style").trim() || "normal";
  const fontWeight = styles.getPropertyValue("--proof-weight").trim() || "400";
  const fontSize = styles.getPropertyValue("--proof-size").trim() || "16px";
  return `${fontStyle} ${fontWeight} ${fontSize}`;
}

let fontLoadSyncRun = 0;
function queueRenderedFontSync(fontList) {
  if (!document.fonts || !fontList.length) {
    return;
  }
  const run = ++fontLoadSyncRun;
  const fontSpec = currentProofFontSpec();
  Promise.all(
    fontList.map((font) =>
      document.fonts.load(`${fontSpec} "${cssString(font.family)}"`).catch(() => []),
    ),
  ).then(() => {
    if (run === fontLoadSyncRun) {
      queueProofDimensionSync();
    }
  });
}

function scheduleIdleTask(callback) {
  if ("requestIdleCallback" in window) {
    window.requestIdleCallback(callback, { timeout: 2500 });
    return;
  }
  setTimeout(callback, 900);
}

function scheduleBackgroundFontLoading() {
  if (backgroundFontLoadStarted) {
    return;
  }
  backgroundFontLoadStarted = true;

  const popularIds = new Set(popularFontIds());
  const remainingFonts = fonts.filter((font) => !popularIds.has(font.id));
  let nextIndex = 0;

  const loadNextFont = () => {
    const font = remainingFonts[nextIndex];
    nextIndex += 1;
    if (!font) {
      return;
    }

    installFontFacesFor([font]);
    if (!document.fonts) {
      scheduleIdleTask(loadNextFont);
      return;
    }

    document.fonts
      .load(`${currentProofFontSpec()} "${cssString(font.family)}"`)
      .catch(() => [])
      .then(() => scheduleIdleTask(loadNextFont));
  };

  const startLoading = () => scheduleIdleTask(loadNextFont);
  if (document.readyState === "complete") {
    startLoading();
  } else {
    window.addEventListener("load", startLoading, { once: true });
  }
}

function readTextSource(id) {
  const source = document.getElementById(id);
  return source ? source.textContent.replace(/^\n/, "").replace(/\n$/, "") : "";
}

const microgptSource = readTextSource("microgpt-source");
const rfc1Source = readTextSource("rfc1-source");
const turingFullSource = readTextSource("turing-full-source");

const samples = {
  prose: {
    label: "Alan Turing: Computing Machinery",
    mode: "plain",
    text: turingFullSource,
  },
  rfc1: {
    label: "RFC 1: Host Software",
    mode: "plain",
    text: rfc1Source,
  },
  code: {
    label: "microGPT Source",
    mode: "code",
    text: microgptSource,
  },
  terminal: {
    label: "Terminal",
    mode: "terminal",
    text: `planetaire $ eza -l --icons=always .
drwxr-xr-x@    - levy 15 Feb 23:07 devtools
drwxr-xr-x@    - levy 15 Feb 23:07 docs
drwxr-xr-x@    - levy 15 Feb 23:07 fonts
.rw-r--r--@ 7.6k levy 16 Feb 09:14 LICENSE
.rw-r--r--@ 6.4k levy 15 Feb 23:07 README.md

planetaire $ python -c "print('Hello from Planetaire Mono!')"
Hello from Planetaire Mono!

planetaire $ git log --oneline -3
5bd69c5 Switch B612 source to original polarsys/b612
a1c8e3f Add font comparison and regression detection
e927d01 Refactor merge pipeline for original B612`,
  },
  ligatures: {
    label: "Ligatures",
    mode: "ligatures",
    text: `Common programming ligatures, with raw fallback text:

Arrows       -> <- => <= >= <=> ==> <== --> <-- <->
Equality     == === != !== =/= <= >=
Logic        && || ?? ?. ?: :: ::
Pipes        |> <| |] [| ||| <|| ||>
Math         ++ -- +++ *** ** // /// \\\\ ~= =~
Comments     // /* */ <!-- --> </> /> <tag/>
Assignment   := =: <- -> => ||= &&= ??=
Sequences    www ffi fl tt`,
  },
  confusables: {
    label: "Confusables",
    mode: "plain",
    text: `Il1|  IIl1||  I_l_1_|  file://localhost:8080
O0o   OO00oo   FL350 FL850   10.0.0.1
rn m  rnm  minimum  modern  memory
5S 8B 2Z 6G 9g q9 db pq
{}[]()<>  => -> <= >= != == === !==
.,;:'"\`  -- -_ ~= @#$%^&*+`,
  },
};

const els = {
  cardModeControls: requireElementById("card-mode-controls"),
  cardSize: /** @type {HTMLSelectElement} */ (requireElementById("card-size")),
  checks: requireElementById("font-checks"),
  editor: /** @type {HTMLTextAreaElement} */ (requireElementById("sample-text")),
  fontPickerHeading: requireElementById("font-picker-heading"),
  fontSelect: /** @type {HTMLSelectElement} */ (requireElementById("font-select")),
  fontSelectTip: requireElementById("font-select-tip"),
  fontSelectWrap: requireElementById("font-select-wrap"),
  fontPicker: requireElement(".font-picker"),
  grid: requireElementById("proof-grid"),
  showLabels: /** @type {HTMLInputElement} */ (requireElementById("show-labels")),
  modeTabs: Array.from(
    document.querySelectorAll("[data-view-mode]"),
    (tab) => /** @type {HTMLElement} */ (tab),
  ),
  pickerActions: requireElement(".picker-actions"),
  sample: /** @type {HTMLSelectElement} */ (requireElementById("sample-select")),
  size: /** @type {HTMLInputElement} */ (requireElementById("font-size")),
  fontStyle: /** @type {HTMLSelectElement} */ (requireElementById("font-style")),
  lineHeight: /** @type {HTMLInputElement} */ (requireElementById("line-height")),
  weight: /** @type {HTMLSelectElement} */ (requireElementById("font-weight")),
};

const SIZE_MIN = 2;
const SIZE_MAX = 256;
const LINE_HEIGHT_DEFAULT = 1.5;
let viewMode = "cards";

function escapeHtml(value) {
  return value.replace(
    /[&<>]/g,
    (ch) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
      })[ch],
  );
}

function highlightWithPatterns(text, patterns) {
  const matches = [];
  for (const pattern of patterns) {
    for (const match of text.matchAll(pattern.regex)) {
      matches.push({
        start: match.index,
        end: match.index + match[0].length,
        value: match[0],
        className: pattern.className,
      });
    }
  }
  matches.sort((a, b) => a.start - b.start || b.end - a.end);

  const chosen = [];
  let lastEnd = -1;
  for (const match of matches) {
    if (match.start < lastEnd) {
      continue;
    }
    chosen.push(match);
    lastEnd = match.end;
  }

  let html = "";
  let cursor = 0;
  for (const match of chosen) {
    html += escapeHtml(text.slice(cursor, match.start));
    html += `<span class="${match.className}">${escapeHtml(match.value)}</span>`;
    cursor = match.end;
  }
  html += escapeHtml(text.slice(cursor));
  return html;
}

function renderCode(text) {
  return highlightWithPatterns(text, [
    { regex: /#[^\n]*/g, className: "tok-comment" },
    { regex: /"""[\s\S]*?"""|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'/g, className: "tok-string" },
    {
      regex:
        /\b(import|from|as|def|return|if|elif|else|for|while|in|class|try|except|with|lambda)\b/g,
      className: "tok-keyword",
    },
    {
      regex: /\b(float|dict|tuple|list|set|int|str|bool|None|True|False)\b/g,
      className: "tok-type",
    },
    { regex: /\b(?:0x[0-9a-fA-F]+|\d[\d_]*(?:\.\d+)?(?:e[+-]?\d+)?)\b/g, className: "tok-number" },
  ]);
}

function renderTerminalLine(line) {
  const prompt = line.match(/^([\w.-]+)(\s+\$\s+)(.*)$/u);
  if (prompt) {
    return `<span class="term-prompt">${escapeHtml(prompt[1])}</span><strong>${escapeHtml(prompt[2])}</strong><span class="term-command">${escapeHtml(prompt[3])}</span>`;
  }

  return highlightWithPatterns(line, [
    { regex: /^([.d-][rwx-]+@?)/gu, className: "term-dim" },
    { regex: /\b([0-9a-f]{7,})\b/gu, className: "term-hash" },
    { regex: /\b(\d{1,2}\s+[A-Z][a-z]{2}\s+\d{2}:\d{2})\b/gu, className: "term-date" },
    { regex: /\b(\d+(?:\.\d+)?k?)\b/gu, className: "term-size" },
    { regex: /\b(levy)\b/gu, className: "term-user" },
    { regex: /\b(devtools|docs|fonts|README\.md|LICENSE)\b/gu, className: "term-path" },
  ]);
}

function renderTerminal(text) {
  return text.split("\n").map(renderTerminalLine).join("\n");
}

function selectedFontIds() {
  return Array.from(els.checks.querySelectorAll("input[type='checkbox']:checked")).map(
    (input) => /** @type {HTMLInputElement} */ (input).value,
  );
}

function sameIdSet(left, right) {
  if (left.length !== right.length) {
    return false;
  }
  const selected = new Set(left);
  return right.every((id) => selected.has(id));
}

function popularFontIds() {
  return fonts.filter((font) => font.default).map((font) => font.id);
}

function allFontIds() {
  return fonts.map((font) => font.id);
}

function syncFontActionState() {
  const selected = selectedFontIds();
  document.querySelectorAll("[data-font-action]").forEach((button) => {
    const actionButton = /** @type {HTMLElement} */ (button);
    let pressed = false;
    if (actionButton.dataset.fontAction === "popular") {
      pressed = sameIdSet(selected, popularFontIds());
    }
    if (actionButton.dataset.fontAction === "all") {
      pressed = sameIdSet(selected, allFontIds());
    }
    actionButton.setAttribute("aria-pressed", String(pressed));
  });
}

function formatNpmDownloads(downloads) {
  if (!Number.isFinite(downloads)) {
    return "";
  }
  if (downloads >= 1000000) {
    return `${(downloads / 1000000).toFixed(1)}M npm/mo`;
  }
  if (downloads >= 1000) {
    return `${Math.round(downloads / 1000)}k npm/mo`;
  }
  return `${downloads} npm/mo`;
}

function formatAvailability(value) {
  const labels = {
    free: "free",
    "free-private": "free private",
    paid: "paid",
    restricted: "restricted",
    private: "private",
  };
  return labels[value] || value || "";
}

function fontLicenseLabel(font) {
  const availability = formatAvailability(font.availability || font.license?.availability);
  const license = font.license?.shortName || font.license?.spdx || font.license?.name || "";
  if (!availability && !license) {
    return "";
  }
  if (availability && license) {
    return `${availability} ${license}`;
  }
  return availability || license;
}

function fontInfo(font) {
  const details = [font.source];
  const downloads = formatNpmDownloads(font.npmDownloadsLastMonth);
  const license = fontLicenseLabel(font);
  if (downloads) {
    details.push(downloads);
  }
  if (license) {
    details.push(license);
  }
  return `${font.description} (${details.join("; ")})`;
}

function currentSample() {
  return samples[els.sample.value] || samples.prose;
}

function renderSample(text, mode) {
  if (mode === "code") {
    return renderCode(text);
  }
  if (mode === "terminal") {
    return renderTerminal(text);
  }
  return escapeHtml(text);
}

function resolveCssLength(value, dimension = "width") {
  const probe = document.createElement("div");
  probe.style.position = "absolute";
  probe.style.visibility = "hidden";
  probe.style.pointerEvents = "none";
  probe.style[dimension] = value;
  document.body.appendChild(probe);
  const rect = probe.getBoundingClientRect();
  probe.remove();
  return dimension === "height" ? rect.height : rect.width;
}

function cssVarPx(name, dimension = "width") {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return resolveCssLength(value, dimension);
}

/**
 * @param {HTMLElement} sampleEl
 */
function measureSampleContent(sampleEl) {
  const clone = /** @type {HTMLElement} */ (sampleEl.cloneNode(true));
  clone.style.position = "absolute";
  clone.style.left = "-10000px";
  clone.style.top = "0";
  clone.style.visibility = "hidden";
  clone.style.pointerEvents = "none";
  clone.style.width = "max-content";
  clone.style.height = "auto";
  clone.style.maxHeight = "var(--proof-max-height)";
  clone.style.overflow = "hidden";
  document.body.appendChild(clone);
  const rect = clone.getBoundingClientRect();
  clone.remove();
  return {
    height: rect.height,
    width: rect.width + 2,
  };
}

function maxCardWidthForMode(gridWidth) {
  const mode = els.cardSize?.value || "large";
  const gap = Number.parseFloat(getComputedStyle(els.grid).columnGap) || 0;
  if (mode === "small") {
    return Math.max(0, (gridWidth - gap * 3) / 4);
  }
  if (mode === "medium") {
    return Math.max(0, (gridWidth - gap) / 2);
  }
  return gridWidth;
}

function syncProofDimensions() {
  if (viewMode !== "cards") {
    return;
  }
  const samplesEls = Array.from(
    els.grid.querySelectorAll(".proof-sample"),
    (sampleEl) => /** @type {HTMLElement} */ (sampleEl),
  );
  if (!samplesEls.length) {
    return;
  }

  els.grid.style.removeProperty("--proof-card-width");
  els.grid.style.removeProperty("--proof-sample-height");

  const gridWidth = els.grid.clientWidth || cssVarPx("--proof-max-width");
  const maxWidth = Math.min(maxCardWidthForMode(gridWidth), gridWidth);
  const maxHeight = cssVarPx("--proof-max-height", "height");
  const minWidth = Math.min(160, maxWidth);

  let naturalWidth = 0;
  let naturalHeight = 0;
  for (const sampleEl of samplesEls) {
    const measured = measureSampleContent(sampleEl);
    naturalWidth = Math.max(naturalWidth, measured.width);
    naturalHeight = Math.max(naturalHeight, measured.height);
  }

  const mode = els.cardSize?.value || "large";
  const useFullLargeWidth = mode === "large" && naturalWidth > maxWidth * 0.5;
  const sharedWidth = Math.ceil(
    useFullLargeWidth ? maxWidth : Math.min(Math.max(naturalWidth, minWidth), maxWidth),
  );
  const sharedHeight = Math.ceil(Math.min(naturalHeight, maxHeight));
  els.grid.style.setProperty("--proof-card-width", `${sharedWidth}px`);
  els.grid.style.setProperty("--proof-sample-height", `${sharedHeight}px`);
  applyPanToCards();
}

let proofSyncFrame = 0;
function queueProofDimensionSync() {
  if (viewMode !== "cards") {
    els.grid.style.removeProperty("--proof-card-width");
    els.grid.style.removeProperty("--proof-sample-height");
    return;
  }
  if (proofSyncFrame) {
    cancelAnimationFrame(proofSyncFrame);
  }
  proofSyncFrame = requestAnimationFrame(() => {
    proofSyncFrame = 0;
    syncProofDimensions();
  });
}

// ---- Synchronized drag-to-pan (card view) --------------------------------
// In card view the proof text is clipped, not scrollable, so the wheel/trackpad
// scrolls the page instead of fighting a scroll trap inside each card. To look
// closer you drag any card, and every card pans by the same horizontal and
// vertical offset — so the same slice of text lines up across all fonts for
// piece-by-piece comparison. Pointer Events cover mouse, touch, and pen; the
// cards keep overflow:hidden, which still honors programmatic scrollLeft/Top,
// so the pan is just a shared scroll offset re-applied to every card.
const DRAG_THRESHOLD = 3; // px of movement before a click becomes a drag
let panX = 0;
let panY = 0;
/** @type {{pointerId: number, target: HTMLElement, startX: number, startY: number, originX: number, originY: number, active: boolean} | null} */
let panDrag = null;

function proofSampleEls() {
  return Array.from(
    els.grid.querySelectorAll(".proof-sample"),
    (el) => /** @type {HTMLElement} */ (el),
  );
}

function applyPanToCards() {
  if (viewMode !== "cards") {
    return;
  }
  const samples = proofSampleEls();
  let maxX = 0;
  let maxY = 0;
  for (const el of samples) {
    maxX = Math.max(maxX, el.scrollWidth - el.clientWidth);
    maxY = Math.max(maxY, el.scrollHeight - el.clientHeight);
  }
  panX = Math.min(Math.max(panX, 0), maxX);
  panY = Math.min(Math.max(panY, 0), maxY);
  for (const el of samples) {
    el.scrollLeft = panX;
    el.scrollTop = panY;
  }
}

function endProofPan() {
  if (!panDrag) {
    return;
  }
  if (panDrag.target.hasPointerCapture?.(panDrag.pointerId)) {
    panDrag.target.releasePointerCapture(panDrag.pointerId);
  }
  els.grid.classList.remove("is-panning");
  panDrag = null;
  updateActiveTip();
}

function onProofPointerDown(event) {
  if (viewMode !== "cards" || event.button !== 0) {
    return;
  }
  const sample = /** @type {HTMLElement} */ (event.target).closest(".proof-sample");
  if (!sample) {
    return;
  }
  panDrag = {
    pointerId: event.pointerId,
    target: /** @type {HTMLElement} */ (sample),
    startX: event.clientX,
    startY: event.clientY,
    originX: panX,
    originY: panY,
    active: false,
  };
}

function onProofPointerMove(event) {
  if (!panDrag || event.pointerId !== panDrag.pointerId) {
    return;
  }
  const dx = event.clientX - panDrag.startX;
  const dy = event.clientY - panDrag.startY;
  if (!panDrag.active) {
    // Wait for real movement so a plain click still focuses the card.
    if (Math.abs(dx) < DRAG_THRESHOLD && Math.abs(dy) < DRAG_THRESHOLD) {
      return;
    }
    panDrag.active = true;
    panDrag.target.setPointerCapture(panDrag.pointerId);
    els.grid.classList.add("is-panning");
    updateActiveTip();
  }
  panX = panDrag.originX - dx;
  panY = panDrag.originY - dy;
  applyPanToCards();
  event.preventDefault();
}

// ---- Single card-name overlay (card view) --------------------------------
// In overlay-label mode exactly one card shows its name tip at a time. Hover or
// keyboard focus (tabbing through cards) can set the active card; hover wins
// over focus, and a drag clears the tip while panning. One source of truth —
// the .is-tip class on a single card — is what keeps two tips from ever showing
// together; CSS :hover + :focus could light up two cards at once.
/** @type {HTMLElement | null} */
let tipHover = null;
/** @type {HTMLElement | null} */
let tipFocus = null;

function proofFromEventTarget(target) {
  return target instanceof Element
    ? /** @type {HTMLElement | null} */ (target.closest(".proof"))
    : null;
}

function activeTipProof() {
  if (viewMode !== "cards" || panDrag?.active) {
    return null;
  }
  return tipHover || tipFocus;
}

function updateActiveTip() {
  const active = activeTipProof();
  els.grid.querySelectorAll(".proof").forEach((proof) => {
    proof.classList.toggle("is-tip", proof === active);
  });
}

function onProofPointerOver(event) {
  const proof = proofFromEventTarget(event.target);
  if (proof !== tipHover) {
    tipHover = proof;
    updateActiveTip();
  }
}

function onProofPointerOut(event) {
  // relatedTarget is where the pointer is heading: another card, or off the grid.
  const proof = proofFromEventTarget(event.relatedTarget);
  if (proof !== tipHover) {
    tipHover = proof;
    updateActiveTip();
  }
}

function onProofFocusIn(event) {
  tipFocus = proofFromEventTarget(event.target);
  updateActiveTip();
}

function onProofFocusOut(event) {
  tipFocus = proofFromEventTarget(event.relatedTarget);
  updateActiveTip();
}

function currentFullFont() {
  return fonts.find((font) => font.id === els.fontSelect.value) || fonts[0];
}

function renderFullProof(sample, sampleHtml) {
  const font = currentFullFont();
  els.grid.classList.remove("labels-overlay", "is-empty");
  els.grid.classList.add("is-full-page");
  els.grid.innerHTML = "";

  if (!font) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "Choose a font to render the full-page proof.";
    els.grid.appendChild(empty);
    return;
  }

  installFontFacesFor([font]);

  const section = document.createElement("section");
  section.className = "proof proof-full";
  section.dataset.family = font.family;
  section.tabIndex = 0;
  section.setAttribute("aria-label", `${font.name} full-page proof`);
  section.setAttribute("aria-describedby", "font-select-tip");
  section.addEventListener("keydown", (event) => {
    const step = fullProofKeyStep(event);
    if (!step) {
      return;
    }
    event.preventDefault();
    changeFullFont(step);
  });

  const pre = document.createElement("pre");
  pre.className = `proof-sample is-${sample.mode}`;
  pre.style.setProperty("--proof-font", `"${font.family}"`);
  pre.tabIndex = 0;
  pre.setAttribute("aria-describedby", "font-select-tip");
  pre.innerHTML = sampleHtml;

  section.appendChild(pre);
  els.grid.appendChild(section);
  queueRenderedFontSync([font]);
}

function renderProofs() {
  const sample = currentSample();
  const text = els.editor.value;
  const sampleHtml = renderSample(text, sample.mode);

  if (viewMode === "full") {
    renderFullProof(sample, sampleHtml);
    return;
  }

  const ids = new Set(selectedFontIds());
  const selectedFonts = fonts.filter((font) => ids.has(font.id));
  installFontFacesFor(selectedFonts);

  els.grid.classList.remove("is-full-page");
  els.grid.classList.toggle("labels-overlay", !els.showLabels?.checked);
  els.grid.classList.toggle("is-empty", !selectedFonts.length);
  els.grid.innerHTML = "";
  if (!selectedFonts.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "Select at least one font to render comparison proofs.";
    els.grid.appendChild(empty);
  }

  for (const font of selectedFonts) {
    const section = document.createElement("section");
    section.className = "proof";
    section.dataset.family = font.family;
    section.tabIndex = 0;

    const pre = document.createElement("pre");
    pre.className = `proof-sample is-${sample.mode}`;
    pre.style.setProperty("--proof-font", `"${font.family}"`);
    pre.innerHTML = sampleHtml;

    const foot = document.createElement("div");
    foot.className = "proof-foot";
    foot.innerHTML = `
      <div class="proof-title">${escapeHtml(font.name)}</div>
      <div class="proof-meta">${escapeHtml(fontInfo(font))}</div>`;

    section.append(pre, foot);
    els.grid.appendChild(section);
  }

  queueProofDimensionSync();
  queueRenderedFontSync(selectedFonts);
}

function renderFontPicker() {
  els.checks.innerHTML = "";
  els.fontSelect.innerHTML = "";

  const preventMultiClickTextSelection = (event) => {
    if (event.detail > 1) {
      event.preventDefault();
    }
  };

  const makeFontOption = (font) => {
    const label = document.createElement("label");
    label.className = "font-option";
    label.innerHTML = `
      <input type="checkbox" value="${font.id}"${font.default ? " checked" : ""}>
      <span>
        <span class="font-name">${escapeHtml(font.name)}</span>
        <span class="font-note">${escapeHtml(fontInfo(font))}</span>
      </span>`;
    label.addEventListener("mousedown", preventMultiClickTextSelection);
    return label;
  };

  const makeFontGroup = (title, groupFonts, options = {}) => {
    const collapsible = Boolean(options.collapsible);
    const section = document.createElement("section");
    section.className = "font-group";
    if (options.kind) {
      section.classList.add(`font-group-${options.kind}`);
    }
    if (collapsible) {
      section.classList.add("is-collapsible");
    }
    if (options.expanded) {
      section.classList.add("is-expanded");
    }

    const heading = collapsible ? document.createElement("button") : document.createElement("h3");
    heading.className = collapsible ? "font-group-toggle" : "font-group-title";
    heading.textContent = title;
    if (heading instanceof HTMLButtonElement) {
      heading.type = "button";
      heading.setAttribute("aria-expanded", String(Boolean(options.expanded)));
    }

    const grid = document.createElement("div");
    grid.className = "font-group-grid";
    if (collapsible) {
      grid.id = `${options.kind}-fonts-grid`;
      heading.setAttribute("aria-controls", grid.id);
      heading.addEventListener("click", () => {
        setFontGroupExpanded(options.kind, !section.classList.contains("is-expanded"));
      });
    }
    for (const font of groupFonts) {
      grid.appendChild(makeFontOption(font));
    }

    section.append(heading, grid);
    return section;
  };

  const popularFonts = fonts.filter((font) => font.default);
  const moreFonts = fonts.filter((font) => !font.default);

  els.checks.appendChild(
    makeFontGroup("Popular Fonts", popularFonts, {
      collapsible: true,
      expanded: true,
      kind: "popular",
    }),
  );

  if (moreFonts.length) {
    els.checks.appendChild(
      makeFontGroup("More Fonts", moreFonts, {
        collapsible: true,
        expanded: false,
        kind: "more",
      }),
    );
    syncMoreFontsExpansion();
  }

  for (const font of fonts) {
    const option = document.createElement("option");
    option.value = font.id;
    option.textContent = font.name;
    els.fontSelect.appendChild(option);
  }

  els.fontSelect.value = fonts.find((font) => font.default)?.id || fonts[0]?.id || "";
  els.checks.addEventListener("change", () => {
    syncMoreFontsExpansion();
    syncFontActionState();
    renderProofs();
  });
  els.fontSelect.addEventListener("change", renderProofs);
  syncFontActionState();
}

function renderSampleOptions() {
  els.sample.innerHTML = Object.entries(samples)
    .map(([id, sample]) => `<option value="${id}">${escapeHtml(sample.label)}</option>`)
    .join("");
}

function formatSizeValue(value) {
  return Number.isInteger(value) ? String(value) : String(value).replace(/\.?0+$/, "");
}

function formatDecimalValue(value) {
  return String(value).replace(/\.?0+$/, "");
}

function coerceSize(value) {
  const parsed = Number.parseFloat(value);
  if (!Number.isFinite(parsed)) {
    return null;
  }
  return Math.min(Math.max(parsed, SIZE_MIN), SIZE_MAX);
}

function coerceLineHeight(value) {
  const parsed = Number.parseFloat(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return null;
  }
  return parsed;
}

function applySize(value, { syncInput = false } = {}) {
  const size = coerceSize(value);
  if (size === null) {
    return null;
  }
  const formatted = formatSizeValue(size);
  document.documentElement.style.setProperty("--proof-size", `${formatted}px`);
  if (syncInput) {
    els.size.value = formatted;
  }
  return size;
}

function applyLineHeight(value, { syncInput = false } = {}) {
  const lineHeight = coerceLineHeight(value);
  if (lineHeight === null) {
    return null;
  }
  const formatted = formatDecimalValue(lineHeight);
  document.documentElement.style.setProperty("--proof-line-height", formatted);
  if (syncInput) {
    els.lineHeight.value = formatted;
  }
  return lineHeight;
}

function applyWeight(value) {
  document.documentElement.style.setProperty("--proof-weight", value);
}

function applyFontStyle(value) {
  document.documentElement.style.setProperty("--proof-style", value);
}

function setChecked(ids, options = {}) {
  const selected = new Set(ids);
  els.checks.querySelectorAll("input[type='checkbox']").forEach((input) => {
    const checkbox = /** @type {HTMLInputElement} */ (input);
    checkbox.checked = selected.has(checkbox.value);
  });
  if (options.expandPopular) {
    setFontGroupExpanded("popular", true);
  }
  if (options.collapseMore) {
    setFontGroupExpanded("more", false);
  } else {
    setMoreFontsExpanded(moreFontsHaveSelection());
  }
  syncFontActionState();
  renderProofs();
}

function moreFontsHaveSelection() {
  return Boolean(els.checks.querySelector(".font-group-more input[type='checkbox']:checked"));
}

function setFontGroupExpanded(kind, expanded) {
  const section = els.checks.querySelector(`.font-group-${kind}`);
  if (!section) {
    return;
  }
  section.classList.toggle("is-expanded", expanded);
  const button = section.querySelector(".font-group-toggle");
  if (button) {
    button.setAttribute("aria-expanded", String(expanded));
  }
}

function setMoreFontsExpanded(expanded) {
  setFontGroupExpanded("more", expanded);
}

function syncMoreFontsExpansion() {
  if (moreFontsHaveSelection()) {
    setMoreFontsExpanded(true);
  }
}

/**
 * @param {HTMLSelectElement} select
 */
function moveSelectOption(select, delta) {
  const count = select.options.length;
  if (!count) {
    return;
  }
  select.selectedIndex = (select.selectedIndex + delta + count) % count;
}

function changeFullFont(delta) {
  if (viewMode !== "full") {
    return false;
  }
  const proofHadFocus = document.activeElement && els.grid.contains(document.activeElement);
  moveSelectOption(els.fontSelect, delta);
  renderProofs();
  if (proofHadFocus) {
    const proof =
      els.grid.querySelector(".proof-full .proof-sample") || els.grid.querySelector(".proof-full");
    if (proof) {
      /** @type {HTMLElement} */ (proof).focus({ preventScroll: true });
    }
  }
  return true;
}

function fullProofKeyStep(event) {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
    return 0;
  }
  if (event.key === "ArrowRight") {
    return 1;
  }
  if (event.key === "ArrowLeft") {
    return -1;
  }
  return 0;
}

function setViewMode(mode) {
  viewMode = mode === "full" ? "full" : "cards";

  els.modeTabs.forEach((tab) => {
    const selected = tab.dataset.viewMode === viewMode;
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
  });

  const fullMode = viewMode === "full";
  els.fontPickerHeading.textContent = fullMode ? "Font" : "Fonts";
  els.fontPicker.classList.toggle("is-full-mode", fullMode);
  els.pickerActions.hidden = fullMode;
  els.checks.hidden = fullMode;
  els.fontSelectWrap.hidden = !fullMode;
  els.fontSelectTip.hidden = !fullMode;
  els.cardModeControls.hidden = fullMode;
  els.cardModeControls.classList.toggle("is-disabled", fullMode);
  els.cardModeControls.setAttribute("aria-disabled", String(fullMode));
  els.cardSize.disabled = fullMode;
  els.showLabels.disabled = fullMode;

  if (fullMode) {
    const checked = selectedFontIds()[0];
    if (checked) {
      els.fontSelect.value = checked;
    }
  }

  renderProofs();
}

renderSampleOptions();
renderFontPicker();
els.editor.value = currentSample().text;
applySize(els.size.value);
applyFontStyle(els.fontStyle.value);
applyWeight(els.weight.value);
applyLineHeight(els.lineHeight.value);
setViewMode("cards");
scheduleBackgroundFontLoading();

els.sample.addEventListener("change", () => {
  els.editor.value = currentSample().text;
  renderProofs();
});

els.modeTabs.forEach((tab) => {
  tab.addEventListener("click", () => setViewMode(tab.dataset.viewMode));
  tab.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") {
      return;
    }
    event.preventDefault();
    const current = els.modeTabs.indexOf(tab);
    const dir = event.key === "ArrowRight" ? 1 : -1;
    const next = els.modeTabs[(current + dir + els.modeTabs.length) % els.modeTabs.length];
    next.focus();
    setViewMode(next.dataset.viewMode);
  });
});

els.editor.addEventListener("input", renderProofs);
els.cardSize.addEventListener("change", queueProofDimensionSync);
els.fontSelect.addEventListener("keydown", (event) => {
  const keySteps = {
    ArrowDown: 1,
    ArrowRight: 1,
    Enter: 1,
    ArrowUp: -1,
    ArrowLeft: -1,
  };
  const step = keySteps[event.key];
  if (!step) {
    return;
  }
  event.preventDefault();
  moveSelectOption(els.fontSelect, step);
  renderProofs();
});

els.size.addEventListener("keydown", (event) => {
  if (event.key !== "ArrowUp" && event.key !== "ArrowDown") {
    return;
  }
  event.preventDefault();
  const fallback =
    coerceSize(getComputedStyle(document.documentElement).getPropertyValue("--proof-size")) || 16;
  const current = coerceSize(els.size.value) || fallback;
  const step = Number.parseFloat(els.size.step) || 1;
  const next = current + (event.key === "ArrowUp" ? step : -step);
  if (applySize(next, { syncInput: true }) !== null) {
    queueProofDimensionSync();
  }
});

els.size.addEventListener("input", () => {
  const parsed = Number.parseFloat(els.size.value);
  const size = applySize(els.size.value);
  if (size !== null) {
    if (parsed > SIZE_MAX) {
      els.size.value = formatSizeValue(size);
    }
    queueProofDimensionSync();
  }
});

els.size.addEventListener("change", () => {
  if (applySize(els.size.value, { syncInput: true }) === null) {
    els.size.value = formatSizeValue(
      coerceSize(getComputedStyle(document.documentElement).getPropertyValue("--proof-size")) || 16,
    );
  }
  queueProofDimensionSync();
});

els.lineHeight.addEventListener("input", () => {
  if (applyLineHeight(els.lineHeight.value) !== null) {
    queueProofDimensionSync();
  }
});

els.lineHeight.addEventListener("change", () => {
  if (applyLineHeight(els.lineHeight.value, { syncInput: true }) === null) {
    els.lineHeight.value = formatDecimalValue(
      coerceLineHeight(
        getComputedStyle(document.documentElement).getPropertyValue("--proof-line-height"),
      ) || LINE_HEIGHT_DEFAULT,
    );
  }
  queueProofDimensionSync();
});

els.weight.addEventListener("change", () => {
  applyWeight(els.weight.value);
  queueProofDimensionSync();
});

els.fontStyle.addEventListener("change", () => {
  applyFontStyle(els.fontStyle.value);
  queueProofDimensionSync();
});

els.showLabels.addEventListener("change", renderProofs);
window.addEventListener("resize", queueProofDimensionSync);

els.grid.addEventListener("pointerdown", onProofPointerDown);
els.grid.addEventListener("pointermove", onProofPointerMove);
els.grid.addEventListener("pointerup", endProofPan);
els.grid.addEventListener("pointercancel", endProofPan);
els.grid.addEventListener("pointerover", onProofPointerOver);
els.grid.addEventListener("pointerout", onProofPointerOut);
els.grid.addEventListener("focusin", onProofFocusIn);
els.grid.addEventListener("focusout", onProofFocusOut);

document.querySelectorAll("[data-font-action]").forEach((button) => {
  const actionButton = /** @type {HTMLElement} */ (button);
  actionButton.addEventListener("click", () => {
    if (actionButton.dataset.fontAction === "all") {
      setChecked(allFontIds(), { expandPopular: true });
    }
    if (actionButton.dataset.fontAction === "clear") {
      setChecked([], { expandPopular: true });
    }
    if (actionButton.dataset.fontAction === "popular") {
      setChecked(popularFontIds(), {
        collapseMore: true,
        expandPopular: true,
      });
    }
  });
});

if (document.fonts) {
  document.fonts.ready.then(() => {
    queueProofDimensionSync();
  });
}
