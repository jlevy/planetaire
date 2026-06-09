const fontDescriptions = {
  planetaire: "B612 letters, Hack punctuation, dotted zero",
  hack: "Source-code workhorse, Nerd Font base",
  "fira-code": "Programming ligatures, Fira lineage",
  "ibm-plex": "IBM Plex family",
  jetbrains: "Developer-focused IDE face",
  geist: "Vercel developer UI face",
  "source-code-pro": "Adobe source family, neutral coding face",
  "pt-mono": "Upright, serif-like monospace flavor",
  inconsolata: "Humanist coding classic",
  cascadia: "Windows Terminal and Visual Studio lineage",
  iosevka: "Narrow, highly configurable coding face",
  monaspace: "GitHub Next texture-healing family",
};

const fonts = [
  {
    id: "planetaire",
    name: "Planetaire Mono",
    family: "Planetaire Mono Compare",
    source: "local WOFF2",
    description: fontDescriptions.planetaire,
    default: true,
  },
  {
    id: "hack",
    name: "Hack",
    family: "Hack Compare",
    source: "jsDelivr",
    description: fontDescriptions.hack,
    default: true,
  },
  {
    id: "fira-code",
    name: "Fira Code",
    family: "Fira Code Compare",
    source: "Fontsource",
    description: fontDescriptions["fira-code"],
    default: true,
  },
  {
    id: "ibm-plex",
    name: "IBM Plex Mono",
    family: "IBM Plex Mono Compare",
    source: "Fontsource",
    description: fontDescriptions["ibm-plex"],
    default: true,
  },
  {
    id: "jetbrains",
    name: "JetBrains Mono",
    family: "JetBrains Mono Compare",
    source: "Fontsource",
    description: fontDescriptions.jetbrains,
    default: true,
  },
  {
    id: "geist",
    name: "Geist Mono",
    family: "Geist Mono Compare",
    source: "Fontsource",
    description: fontDescriptions.geist,
  },
  {
    id: "source-code-pro",
    name: "Source Code Pro",
    family: "Source Code Pro Compare",
    source: "Fontsource",
    description: fontDescriptions["source-code-pro"],
  },
  {
    id: "pt-mono",
    name: "PT Mono",
    family: "PT Mono Compare",
    source: "Fontsource",
    description: fontDescriptions["pt-mono"],
  },
  {
    id: "inconsolata",
    name: "Inconsolata",
    family: "Inconsolata Compare",
    source: "Fontsource",
    description: fontDescriptions.inconsolata,
  },
  {
    id: "cascadia",
    name: "Cascadia Code",
    family: "Cascadia Code Compare",
    source: "Fontsource",
    description: fontDescriptions.cascadia,
  },
  {
    id: "iosevka",
    name: "Iosevka",
    family: "Iosevka Compare",
    source: "Fontsource",
    description: fontDescriptions.iosevka,
  },
  {
    id: "monaspace",
    name: "Monaspace Neon",
    family: "Monaspace Neon Compare",
    source: "Fontsource",
    description: fontDescriptions.monaspace,
  },
];

const samples = {
  prose: {
    label: "Prose",
    mode: "plain",
    text: [
      "ALAN TURING \u00B7 \u201CCOMPUTING MACHINERY AND INTELLIGENCE\u201D (1950)",
      "",
      "I propose to consider the question, \u201CCan machines think?\u201D This should",
      "begin with definitions of the meaning of the terms \u201Cmachine\u201D and",
      "\u201Cthink.\u201D The definitions might be framed so as to reflect so far as",
      "possible the normal use of the words, but this attitude is dangerous.",
      "If the meaning of the words \u201Cmachine\u201D and \u201Cthink\u201D are to be found",
      "by examining how they are commonly used it is difficult to escape the",
      "conclusion that the meaning and the answer to the question, \u201CCan",
      "machines think?\u201D is to be sought in a statistical survey such as a",
      "Gallup poll. But this is absurd.",
    ].join("\n"),
  },
  code: {
    label: "Python Source",
    mode: "code",
    text: `import math

def analyze_trajectory(altitude: float, velocity: float) -> dict:
    """Calculate orbital parameters."""

    G = 6.674e-11  # gravitational constant
    M = 5.972e24

    if altitude > 400_000:
        orbit_type = "LEO"
    elif altitude > 35_786_000:
        orbit_type = "GEO"
    else:
        orbit_type = "SUBORBITAL"

    period = 2 * math.pi * math.sqrt(altitude**3 / (G * M))
    return {"type": orbit_type, "period": period, "v": velocity}`,
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
  cardSize: document.getElementById("card-size"),
  checks: document.getElementById("font-checks"),
  editor: document.getElementById("sample-text"),
  grid: document.getElementById("proof-grid"),
  hideLabels: document.getElementById("hide-labels"),
  sample: document.getElementById("sample-select"),
  size: document.getElementById("font-size"),
  fontStyle: document.getElementById("font-style"),
  weight: document.getElementById("font-weight"),
};

const SIZE_MIN = 2;
const SIZE_MAX = 256;

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

function fontInfo(font) {
  return `${font.description} (${font.source})`;
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
  clone.style.maxHeight = "none";
  clone.style.overflow = "visible";
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
  if (proofSyncFrame) cancelAnimationFrame(proofSyncFrame);
  proofSyncFrame = requestAnimationFrame(() => {
    proofSyncFrame = 0;
    syncProofDimensions();
  });
}

function renderProofs() {
  const ids = new Set(selectedFontIds());
  const selectedFonts = fonts.filter((font) => ids.has(font.id));
  const sample = currentSample();
  const text = els.editor.value;
  const sampleHtml = renderSample(text, sample.mode);

  els.grid.classList.toggle("labels-overlay", Boolean(els.hideLabels?.checked));
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
  for (const font of fonts) {
    const label = document.createElement("label");
    label.className = "font-option";
    label.innerHTML = `
      <input type="checkbox" value="${font.id}"${font.default ? " checked" : ""}>
      <span>
        <span class="font-name">${escapeHtml(font.name)}</span>
        <span class="font-note">${escapeHtml(fontInfo(font))}</span>
      </span>`;
    els.checks.appendChild(label);
  }

  els.checks.addEventListener("change", renderProofs);
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

function setChecked(ids) {
  const selected = new Set(ids);
  els.checks.querySelectorAll("input[type='checkbox']").forEach((input) => {
    input.checked = selected.has(input.value);
  });
  renderProofs();
}

renderSampleOptions();
renderFontPicker();
els.editor.value = currentSample().text;
applySize(els.size.value);
applyFontStyle(els.fontStyle.value);
applyWeight(els.weight.value);
renderProofs();

els.sample.addEventListener("change", () => {
  els.editor.value = currentSample().text;
  renderProofs();
});

els.editor.addEventListener("input", renderProofs);
els.cardSize.addEventListener("change", queueProofDimensionSync);
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

els.hideLabels.addEventListener("change", renderProofs);
window.addEventListener("resize", queueProofDimensionSync);

document.querySelectorAll("[data-font-action]").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.fontAction === "all") setChecked(fonts.map((font) => font.id));
    if (button.dataset.fontAction === "clear") setChecked([]);
    if (button.dataset.fontAction === "default") setChecked(fonts.filter((font) => font.default).map((font) => font.id));
  });
});

if (document.fonts) {
  document.fonts.ready.then(() => {
    queueProofDimensionSync();
  });
}
