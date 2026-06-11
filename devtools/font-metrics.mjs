// Measure the real rendered glyph metrics of every comparator font and print a
// FONT_METRICS table for site/compare-fonts.js.
//
// The numbers can't be read from the source files: they depend on each font's
// actual outlines, so we render the live @font-face faces in headless Chrome and
// read them back with canvas measureText. For each font we report em-relative
// ratios (measured at a large reference size, then divided by it):
//   advance  - monospace character advance width / em  (drives "Normalize Metrics")
//   cap      - ink height of "H" / em
//   xHeight  - ink height of "x" / em
//
// Usage: node devtools/font-metrics.mjs
// Requires Google Chrome installed; loads the @font-face sources over the network.
import { spawn } from "node:child_process";
import { dirname, resolve } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const COMPARE_HTML = resolve(here, "../site/compare.html");
const CHROME =
  process.env.CHROME_BIN || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = Number(process.env.CHROME_PORT || 9337);
const URL = `file://${COMPARE_HTML}`;

const proc = spawn(
  CHROME,
  [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    `--remote-debugging-port=${PORT}`,
    "--user-data-dir=/tmp/chrome-fontmetrics",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "about:blank",
  ],
  { stdio: ["ignore", "pipe", "pipe"] },
);
proc.stderr.on("data", () => {});

async function getJson(path) {
  const r = await fetch(`http://127.0.0.1:${PORT}${path}`);
  return r.json();
}

let version;
for (let i = 0; i < 100; i++) {
  try {
    version = await getJson("/json/version");
    break;
  } catch {
    await sleep(100);
  }
}
if (!version) {
  console.error("Chrome devtools endpoint never came up");
  proc.kill();
  process.exit(1);
}

const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((res, rej) => {
  ws.onopen = res;
  ws.onerror = rej;
});

let msgId = 0;
const pending = new Map();
const eventWaiters = [];
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) {
    const { res, rej } = pending.get(m.id);
    pending.delete(m.id);
    if (m.error) {
      rej(new Error(JSON.stringify(m.error)));
    } else {
      res(m.result);
    }
  } else {
    for (const w of eventWaiters.slice()) {
      w(m);
    }
  }
};
function send(method, params = {}, sessionId) {
  const id = ++msgId;
  const msg = { id, method, params };
  if (sessionId) {
    msg.sessionId = sessionId;
  }
  ws.send(JSON.stringify(msg));
  return new Promise((res, rej) => pending.set(id, { res, rej }));
}
function waitEvent(pred) {
  return new Promise((res) => {
    const w = (m) => {
      if (pred(m)) {
        const i = eventWaiters.indexOf(w);
        if (i >= 0) {
          eventWaiters.splice(i, 1);
        }
        res(m);
      }
    };
    eventWaiters.push(w);
  });
}

const { targetId } = await send("Target.createTarget", { url: "about:blank" });
const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
await send("Page.enable", {}, sessionId);
await send("Runtime.enable", {}, sessionId);
const loaded = waitEvent((m) => m.method === "Page.loadEventFired" && m.sessionId === sessionId);
await send("Page.navigate", { url: URL }, sessionId);
await loaded;
await sleep(400);

async function measureFn() {
  const REF = 200;
  const round = (n) => Math.round(n * 1000) / 1000;
  const data = window.PlanetaireFontData;
  if (!data) {
    return { error: "no PlanetaireFontData" };
  }
  const cssEsc = (v) => String(v).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  const pickFace = (font) => {
    const faces = font.faces || [];
    return faces.find((f) => (f.style || "normal") === "normal") || faces[0];
  };
  let style = document.getElementById("measure-faces");
  if (!style) {
    style = document.createElement("style");
    style.id = "measure-faces";
    document.head.appendChild(style);
  }
  const rules = [];
  for (const font of data.fonts) {
    const face = pickFace(font);
    if (!face) {
      continue;
    }
    const fam = face.family || font.family;
    const src = face.sources
      .map((s) => `url("${cssEsc(s.url)}") format("${cssEsc(s.format || "woff2")}")`)
      .join(",");
    rules.push(
      `@font-face{font-family:"${cssEsc(fam)}";font-style:normal;font-weight:${face.weight || 400};font-display:block;src:${src};}`,
    );
  }
  style.textContent = rules.join("\n");

  const ctx = document.createElement("canvas").getContext("2d");
  const out = [];
  for (const font of data.fonts) {
    const face = pickFace(font);
    const fam = face ? face.family || font.family : font.family;
    let loaded = false;
    try {
      await document.fonts.load(`400 ${REF}px "${fam}"`);
      loaded = document.fonts.check(`400 ${REF}px "${fam}"`);
    } catch {}
    ctx.font = `400 ${REF}px "${fam}", monospace`;
    out.push({
      id: font.id,
      name: font.name,
      loaded,
      advance: round(ctx.measureText("0000000000").width / 10 / REF),
      cap: round(ctx.measureText("H").actualBoundingBoxAscent / REF),
      xHeight: round(ctx.measureText("x").actualBoundingBoxAscent / REF),
    });
  }
  return { ref: REF, fonts: out };
}

const expr = `(${measureFn.toString()})()`;
const { result, exceptionDetails } = await send(
  "Runtime.evaluate",
  { expression: expr, awaitPromise: true, returnByValue: true },
  sessionId,
);
proc.kill();
if (exceptionDetails) {
  console.error("EXCEPTION", JSON.stringify(exceptionDetails, null, 2));
  process.exit(1);
}
const value = result.value;
const failed = value.fonts.filter((f) => !f.loaded).map((f) => f.id);
if (failed.length) {
  console.error(`WARNING: fonts failed to load: ${failed.join(", ")}`);
}

const lines = value.fonts.map((f) => {
  const key = /^[a-z][\w-]*$/i.test(f.id) && !f.id.includes("-") ? f.id : `"${f.id}"`;
  return `    ${key}: { advance: ${f.advance}, cap: ${f.cap}, xHeight: ${f.xHeight} },`;
});
console.log("  const FONT_METRICS = {");
console.log(lines.join("\n"));
console.log("  };");
process.exit(0);
