const fontData = window.PlanetaireFontData || { fonts: [] };
const fonts = fontData.fonts;

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

function installFontFaces() {
  const style = document.createElement("style");
  style.id = "compare-font-faces";
  style.textContent = fonts
    .flatMap((font) => (font.faces || []).map((fontFace) => renderFontFace(font, fontFace)))
    .join("\n");
  document.head.appendChild(style);
}

installFontFaces();

function readTextSource(id) {
  const source = document.getElementById(id);
  return source ? source.textContent.replace(/^\n/, "").replace(/\n$/, "") : "";
}

const microgptSource = readTextSource("microgpt-source");
const turingFullSource = readTextSource("turing-full-source");

const samples = {
  prose: {
    label: "Alan Turing: Computing Machinery",
    mode: "plain",
    text: turingFullSource,
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
  cardModeControls: document.getElementById("card-mode-controls"),
  cardSize: document.getElementById("card-size"),
  checks: document.getElementById("font-checks"),
  editor: document.getElementById("sample-text"),
  fontPickerHeading: document.getElementById("font-picker-heading"),
  fontSelect: document.getElementById("font-select"),
  fontSelectWrap: document.getElementById("font-select-wrap"),
  grid: document.getElementById("proof-grid"),
  showLabels: document.getElementById("show-labels"),
  modeTabs: Array.from(document.querySelectorAll("[data-view-mode]")),
  pickerActions: document.querySelector(".picker-actions"),
  sample: document.getElementById("sample-select"),
  size: document.getElementById("font-size"),
  fontStyle: document.getElementById("font-style"),
  weight: document.getElementById("font-weight"),
};

const SIZE_MIN = 2;
const SIZE_MAX = 256;
let viewMode = "cards";

function escapeHtml(value) {
  return value.replace(/[&<>]/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
  })[ch]);
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
    if (match.start < lastEnd) continue;
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
    { regex: /\b(import|from|as|def|return|if|elif|else|for|while|in|class|try|except|with|lambda)\b/g, className: "tok-keyword" },
    { regex: /\b(float|dict|tuple|list|set|int|str|bool|None|True|False)\b/g, className: "tok-type" },
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
  return Array.from(els.checks.querySelectorAll("input[type='checkbox']:checked"))
    .map((input) => input.value);
}

function formatNpmDownloads(downloads) {
  if (!Number.isFinite(downloads)) return "";
  if (downloads >= 1000000) return `${(downloads / 1000000).toFixed(1)}M npm/mo`;
  if (downloads >= 1000) return `${Math.round(downloads / 1000)}k npm/mo`;
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
  if (!availability && !license) return "";
  if (availability && license) return `${availability} ${license}`;
  return availability || license;
}

function fontInfo(font) {
  const details = [font.source];
  const downloads = formatNpmDownloads(font.npmDownloadsLastMonth);
  const license = fontLicenseLabel(font);
  if (downloads) details.push(downloads);
  if (license) details.push(license);
  return `${font.description} (${details.join("; ")})`;
}

function currentSample() {
  return samples[els.sample.value] || samples.prose;
}

function renderSample(text, mode) {
  if (mode === "code") return renderCode(text);
  if (mode === "terminal") return renderTerminal(text);
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

function measureSampleContent(sampleEl) {
  const clone = sampleEl.cloneNode(true);
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
  if (mode === "small") return Math.max(0, (gridWidth - gap * 3) / 4);
  if (mode === "medium") return Math.max(0, (gridWidth - gap) / 2);
  return gridWidth;
}

function syncProofDimensions() {
  if (viewMode !== "cards") return;
  const samplesEls = Array.from(els.grid.querySelectorAll(".proof-sample"));
  if (!samplesEls.length) return;

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
  const sharedWidth = Math.ceil(useFullLargeWidth ? maxWidth : Math.min(Math.max(naturalWidth, minWidth), maxWidth));
  const sharedHeight = Math.ceil(Math.min(naturalHeight, maxHeight));
  els.grid.style.setProperty("--proof-card-width", `${sharedWidth}px`);
  els.grid.style.setProperty("--proof-sample-height", `${sharedHeight}px`);
}

let proofSyncFrame = 0;
function queueProofDimensionSync() {
  if (viewMode !== "cards") {
    els.grid.style.removeProperty("--proof-card-width");
    els.grid.style.removeProperty("--proof-sample-height");
    return;
  }
  if (proofSyncFrame) cancelAnimationFrame(proofSyncFrame);
  proofSyncFrame = requestAnimationFrame(() => {
    proofSyncFrame = 0;
    syncProofDimensions();
  });
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

  const section = document.createElement("section");
  section.className = "proof proof-full";
  section.dataset.family = font.family;
  section.setAttribute("aria-label", `${font.name} full-page proof`);

  const pre = document.createElement("pre");
  pre.className = `proof-sample is-${sample.mode}`;
  pre.style.setProperty("--proof-font", `"${font.family}"`);
  pre.tabIndex = 0;
  pre.innerHTML = sampleHtml;

  section.appendChild(pre);
  els.grid.appendChild(section);
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

  els.grid.classList.remove("is-full-page");
  els.grid.classList.toggle("labels-overlay", !Boolean(els.showLabels?.checked));
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
}

function renderFontPicker() {
  els.checks.innerHTML = "";
  els.fontSelect.innerHTML = "";

  const preventMultiClickTextSelection = (event) => {
    if (event.detail > 1) event.preventDefault();
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
    const section = document.createElement("section");
    section.className = "font-group";
    if (options.kind) section.classList.add(`font-group-${options.kind}`, "is-collapsible");
    if (options.expanded) section.classList.add("is-expanded");

    const heading = options.kind ? document.createElement("button") : document.createElement("h3");
    heading.className = options.kind ? "font-group-toggle" : "font-group-title";
    heading.textContent = title;
    if (options.kind) {
      heading.type = "button";
      heading.setAttribute("aria-expanded", String(Boolean(options.expanded)));
    }

    const grid = document.createElement("div");
    grid.className = "font-group-grid";
    if (options.kind) {
      grid.id = `${options.kind}-fonts-grid`;
      heading.setAttribute("aria-controls", grid.id);
      heading.addEventListener("click", () => {
        setFontGroupExpanded(options.kind, !section.classList.contains("is-expanded"));
      });
    }
    for (const font of groupFonts) grid.appendChild(makeFontOption(font));

    section.append(heading, grid);
    return section;
  };

  const popularFonts = fonts.filter((font) => font.default);
  const moreFonts = fonts.filter((font) => !font.default);

  els.checks.appendChild(makeFontGroup("Popular Fonts", popularFonts, {
    expanded: true,
    kind: "popular",
  }));

  if (moreFonts.length) {
    els.checks.appendChild(makeFontGroup("More Fonts", moreFonts, {
      expanded: false,
      kind: "more",
    }));
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
    renderProofs();
  });
  els.fontSelect.addEventListener("change", renderProofs);
}

function renderSampleOptions() {
  els.sample.innerHTML = Object.entries(samples).map(([id, sample]) => (
    `<option value="${id}">${escapeHtml(sample.label)}</option>`
  )).join("");
}

function formatSizeValue(value) {
  return Number.isInteger(value) ? String(value) : String(value).replace(/\.?0+$/, "");
}

function coerceSize(value) {
  const parsed = Number.parseFloat(value);
  if (!Number.isFinite(parsed)) return null;
  return Math.min(Math.max(parsed, SIZE_MIN), SIZE_MAX);
}

function applySize(value, { syncInput = false } = {}) {
  const size = coerceSize(value);
  if (size === null) return null;
  const formatted = formatSizeValue(size);
  document.documentElement.style.setProperty("--proof-size", `${formatted}px`);
  if (syncInput) els.size.value = formatted;
  return size;
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
    input.checked = selected.has(input.value);
  });
  if (options.expandPopular) setFontGroupExpanded("popular", true);
  if (options.collapseMore) setFontGroupExpanded("more", false);
  else setMoreFontsExpanded(moreFontsHaveSelection());
  renderProofs();
}

function moreFontsHaveSelection() {
  return Boolean(els.checks.querySelector(".font-group-more input[type='checkbox']:checked"));
}

function setFontGroupExpanded(kind, expanded) {
  const section = els.checks.querySelector(`.font-group-${kind}`);
  if (!section) return;
  section.classList.toggle("is-expanded", expanded);
  const button = section.querySelector(".font-group-toggle");
  if (button) button.setAttribute("aria-expanded", String(expanded));
}

function setMoreFontsExpanded(expanded) {
  setFontGroupExpanded("more", expanded);
}

function syncMoreFontsExpansion() {
  if (moreFontsHaveSelection()) setMoreFontsExpanded(true);
}

function moveSelectOption(select, delta) {
  const count = select.options.length;
  if (!count) return;
  select.selectedIndex = (select.selectedIndex + delta + count) % count;
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
  els.pickerActions.hidden = fullMode;
  els.checks.hidden = fullMode;
  els.fontSelectWrap.hidden = !fullMode;
  els.cardModeControls.classList.toggle("is-disabled", fullMode);
  els.cardModeControls.setAttribute("aria-disabled", String(fullMode));
  els.cardSize.disabled = fullMode;
  els.showLabels.disabled = fullMode;

  if (fullMode) {
    const checked = selectedFontIds()[0];
    if (checked) els.fontSelect.value = checked;
  }

  renderProofs();
}

renderSampleOptions();
renderFontPicker();
els.editor.value = currentSample().text;
applySize(els.size.value);
applyFontStyle(els.fontStyle.value);
applyWeight(els.weight.value);
setViewMode("cards");

els.sample.addEventListener("change", () => {
  els.editor.value = currentSample().text;
  renderProofs();
});

els.modeTabs.forEach((tab) => {
  tab.addEventListener("click", () => setViewMode(tab.dataset.viewMode));
  tab.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
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
  if (!step) return;
  event.preventDefault();
  moveSelectOption(els.fontSelect, step);
  renderProofs();
});

els.size.addEventListener("keydown", (event) => {
  if (event.key !== "ArrowUp" && event.key !== "ArrowDown") return;
  event.preventDefault();
  const fallback = coerceSize(getComputedStyle(document.documentElement).getPropertyValue("--proof-size")) || 16;
  const current = coerceSize(els.size.value) || fallback;
  const step = Number.parseFloat(els.size.step) || 1;
  const next = current + (event.key === "ArrowUp" ? step : -step);
  if (applySize(next, { syncInput: true }) !== null) queueProofDimensionSync();
});

els.size.addEventListener("input", () => {
  const parsed = Number.parseFloat(els.size.value);
  const size = applySize(els.size.value);
  if (size !== null) {
    if (parsed > SIZE_MAX) els.size.value = formatSizeValue(size);
    queueProofDimensionSync();
  }
});

els.size.addEventListener("change", () => {
  if (applySize(els.size.value, { syncInput: true }) === null) {
    els.size.value = formatSizeValue(coerceSize(getComputedStyle(document.documentElement).getPropertyValue("--proof-size")) || 16);
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

document.querySelectorAll("[data-font-action]").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.fontAction === "all") {
      setChecked(fonts.map((font) => font.id), { expandPopular: true });
    }
    if (button.dataset.fontAction === "clear") {
      setChecked([], { expandPopular: true });
    }
    if (button.dataset.fontAction === "popular") {
      setChecked(fonts.filter((font) => font.default).map((font) => font.id), {
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
