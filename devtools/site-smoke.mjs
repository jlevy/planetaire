import path from "node:path";
import { pathToFileURL } from "node:url";
import { JSDOM, VirtualConsole } from "jsdom";

const root = path.resolve(import.meta.dirname, "..");
const site = path.join(root, "site");
const OPTIONAL_EXTERNAL_STYLESHEETS = ["https://cdn.jsdelivr.net/gh/jlevy/planetaire@"];

const pages = [
  {
    file: "index.html",
    checks(window) {
      const document = window.document;
      assertText(document.querySelector("h1"), "Planetaire Mono", "homepage h1");
      assertCount(document.querySelectorAll(".tab-opt"), 3, "homepage tabs");
      assertCount(document.querySelectorAll(".tab-panel"), 3, "homepage tab panels");
      assertCount(document.querySelectorAll("#qa-upper .cell"), 26, "homepage QA uppercase cells");
      assertPressedThemeButtons(document);
    },
  },
  {
    file: "compare.html",
    checks(window) {
      const document = window.document;
      assertText(document.querySelector("h1"), "What Monospace Font is Best?", "compare h1");
      assertAtLeast(
        document.querySelectorAll("#font-checks input[type='checkbox']").length,
        6,
        "font choices",
      );
      assertAtLeast(document.querySelectorAll("#sample-select option").length, 5, "sample choices");
      assertAtLeast(
        document.querySelectorAll("#proof-grid .proof").length,
        1,
        "rendered proof cards",
      );
      assertAtLeast(
        document.querySelectorAll("#compare-font-faces").length,
        1,
        "installed font faces",
      );
      assertPressedThemeButtons(document);
    },
  },
];

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function assertText(element, expected, label) {
  assert(element, `${label}: missing element`);
  assert(element.textContent.trim() === expected, `${label}: expected "${expected}"`);
}

function assertCount(items, expected, label) {
  assert(items.length === expected, `${label}: expected ${expected}, found ${items.length}`);
}

function assertAtLeast(value, expected, label) {
  assert(value >= expected, `${label}: expected at least ${expected}, found ${value}`);
}

function assertPressedThemeButtons(document) {
  const buttons = [...document.querySelectorAll(".ts-opt")];
  assert(buttons.length === 2, "theme switch: expected light and dark buttons");
  assert(
    buttons.some((button) => button.getAttribute("aria-pressed") === "true"),
    "theme switch: no active theme",
  );
}

function waitForLoad(window) {
  return new Promise((resolve) => {
    if (window.document.readyState === "complete") {
      resolve();
      return;
    }
    window.addEventListener("load", resolve, { once: true });
  });
}

async function nextFrame(window) {
  await new Promise((resolve) => window.requestAnimationFrame(resolve));
}

async function smokePage(page) {
  const errors = [];
  const virtualConsole = new VirtualConsole();
  virtualConsole.on("error", (message) => errors.push(`console.error: ${message}`));
  virtualConsole.on("jsdomError", (error) => {
    if (isOptionalExternalStylesheetError(error.message)) {
      return;
    }
    errors.push(`jsdom: ${error.message}`);
  });

  const fileUrl = pathToFileURL(path.join(site, page.file)).href;
  const dom = await JSDOM.fromURL(fileUrl, {
    beforeParse(window) {
      window.matchMedia = (query) => ({
        matches: false,
        media: query,
        onchange: null,
        addEventListener() {},
        removeEventListener() {},
        addListener() {},
        removeListener() {},
        dispatchEvent() {
          return false;
        },
      });
    },
    pretendToBeVisual: true,
    resources: "usable",
    runScripts: "dangerously",
    virtualConsole,
  });

  try {
    await waitForLoad(dom.window);
    await nextFrame(dom.window);
    await nextFrame(dom.window);
    page.checks(dom.window);
  } catch (error) {
    errors.push(error.message);
  } finally {
    dom.window.close();
  }

  if (errors.length) {
    throw new Error(`${page.file}\n${errors.map((error) => `  - ${error}`).join("\n")}`);
  }
  console.log(`ok ${page.file}`);
}

function isOptionalExternalStylesheetError(message) {
  return OPTIONAL_EXTERNAL_STYLESHEETS.some((prefix) =>
    message.startsWith(`Could not load link: "${prefix}`),
  );
}

const failures = [];
for (const page of pages) {
  try {
    await smokePage(page);
  } catch (error) {
    failures.push(error.message);
  }
}

if (failures.length) {
  console.error(failures.join("\n\n"));
  process.exitCode = 1;
}
