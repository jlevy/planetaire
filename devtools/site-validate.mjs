import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import * as parse5 from "parse5";

const HTML_URL_ATTRS = new Map([
  ["a", ["href"]],
  ["img", ["src"]],
  ["link", ["href"]],
  ["script", ["src"]],
  ["source", ["src", "srcset"]],
]);
const JS_SCRIPT_TYPES = new Set([
  "",
  "application/ecmascript",
  "application/javascript",
  "text/javascript",
]);
const SKIP_SCHEMES = new Set(["data:", "http:", "https:", "javascript:", "mailto:", "tel:"]);
const CSS_URL_RE = /url\(\s*(["']?)(?<url>.*?)\1\s*\)/g;

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const site = path.join(root, "site");

function rel(filePath) {
  return path.relative(root, filePath).split(path.sep).join("/");
}

function attrMap(node) {
  return Object.fromEntries((node.attrs || []).map((attr) => [attr.name, attr.value]));
}

function locationLabel(filePath, location) {
  if (!location) {
    return rel(filePath);
  }
  return `${rel(filePath)}:${location.startLine}:${location.startCol}`;
}

function walk(node, visit) {
  visit(node);
  for (const child of node.childNodes || []) {
    walk(child, visit);
  }
}

function parseSrcset(value) {
  return value
    .split(",")
    .map((candidate) => candidate.trim().split(/\s+/, 1)[0])
    .filter(Boolean);
}

function parseLocalUrl(ref) {
  if (!ref || ref.startsWith("#")) {
    return null;
  }

  let url;
  try {
    url = new URL(ref, "https://static.invalid/");
  } catch {
    return { error: `invalid URL reference: ${ref}` };
  }
  // Only refs that carry their own scheme or host are external. A site-local
  // ref also resolves onto the placeholder https: origin, so testing the
  // resolved protocol alone would skip every local ref.
  if (/^[a-z][a-z0-9+.-]*:/i.test(ref) || ref.startsWith("//")) {
    if (SKIP_SCHEMES.has(url.protocol)) {
      return null;
    }
    return { error: `unexpected URL scheme: ${ref}` };
  }
  return { pathname: ref.split(/[?#]/, 1)[0], hash: url.hash };
}

function validateRef({ errors, filePath, htmlIds, ref, source }) {
  const parsed = parseLocalUrl(ref);
  if (!parsed) {
    return;
  }
  if (parsed.error) {
    errors.push(`${source}: ${parsed.error}`);
    return;
  }
  if (!parsed.pathname) {
    return;
  }
  if (parsed.pathname.startsWith("/")) {
    errors.push(`${source}: root-absolute site reference is not portable: ${ref}`);
    return;
  }
  if (parsed.pathname.startsWith("../")) {
    errors.push(`${source}: parent-directory site reference is not allowed: ${ref}`);
    return;
  }

  let target = path.resolve(path.dirname(filePath), decodeURIComponent(parsed.pathname));
  if (!target.startsWith(`${site}${path.sep}`) && target !== site) {
    errors.push(`${source}: reference escapes site/: ${ref}`);
    return;
  }

  // The published URL for a page is its directory ("planetaire/"), never
  // "planetaire/index.html" — keep every internal link on the canonical form.
  if (path.basename(target) === "index.html") {
    errors.push(
      `${source}: link to index.html directly is not allowed; use a trailing-slash directory reference instead: ${ref}`,
    );
    return;
  }
  if (knownDirs.has(target)) {
    target = path.join(target, "index.html");
  }

  if (!knownFiles.has(target)) {
    errors.push(`${source}: missing local site asset: ${ref}`);
    return;
  }

  if (!parsed.hash || path.extname(target) !== ".html") {
    return;
  }

  const fragment = decodeURIComponent(parsed.hash.slice(1));
  if (!htmlIds.get(target)?.has(fragment)) {
    errors.push(`${source}: missing local fragment target #${fragment} in ${rel(target)}`);
  }
}

function collectHtml(document, filePath, htmlIds, htmlRefs, inlineScripts) {
  const ids = new Set();
  const refs = [];

  walk(document, (node) => {
    if (!node.tagName) {
      return;
    }

    const attrs = attrMap(node);
    if (attrs.id) {
      ids.add(attrs.id);
    }

    for (const attrName of HTML_URL_ATTRS.get(node.tagName) || []) {
      const value = attrs[attrName];
      if (!value) {
        continue;
      }
      const values = attrName === "srcset" ? parseSrcset(value) : [value];
      for (const ref of values) {
        refs.push({
          ref,
          source: `${locationLabel(filePath, node.sourceCodeLocation)} ${node.tagName}[${attrName}]`,
        });
      }
    }

    if (node.tagName !== "script" || attrs.src !== undefined) {
      return;
    }

    const type = (attrs.type || "").toLowerCase();
    if (!JS_SCRIPT_TYPES.has(type)) {
      return;
    }
    const code = (node.childNodes || [])
      .filter((child) => child.nodeName === "#text")
      .map((child) => child.value)
      .join("")
      .trim();
    if (code) {
      inlineScripts.push({
        code,
        label: locationLabel(filePath, node.sourceCodeLocation),
      });
    }
  });

  htmlIds.set(filePath, ids);
  htmlRefs.set(filePath, refs);
}

async function readSiteFiles(extension) {
  const { readdir } = await import("node:fs/promises");
  return (await readdir(site, { recursive: true, withFileTypes: true }))
    .filter((entry) => entry.isFile() && entry.name.endsWith(extension))
    .map((entry) => path.join(entry.parentPath, entry.name))
    .sort();
}

async function collectKnownFiles() {
  const { readdir } = await import("node:fs/promises");
  const files = new Set();
  const dirs = new Set([site]);
  for (const entry of await readdir(site, { recursive: true, withFileTypes: true })) {
    const entryPath = path.join(entry.parentPath, entry.name);
    if (entry.isFile()) {
      files.add(entryPath);
    } else if (entry.isDirectory()) {
      dirs.add(entryPath);
    }
  }
  return { files, dirs };
}

async function validateHtmlReferences(errors) {
  const htmlIds = new Map();
  const htmlRefs = new Map();
  const inlineScripts = [];

  for (const filePath of await readSiteFiles(".html")) {
    const text = await readFile(filePath, "utf8");
    const document = parse5.parse(text, { sourceCodeLocationInfo: true });
    collectHtml(document, filePath, htmlIds, htmlRefs, inlineScripts);
  }

  for (const [filePath, refs] of htmlRefs.entries()) {
    for (const { ref, source } of refs) {
      validateRef({ errors, filePath, htmlIds, ref, source });
    }
  }

  return inlineScripts;
}

async function validateCssReferences(errors) {
  for (const filePath of await readSiteFiles(".css")) {
    const text = await readFile(filePath, "utf8");
    for (const match of text.matchAll(CSS_URL_RE)) {
      validateRef({
        errors,
        filePath,
        htmlIds: new Map(),
        ref: match.groups.url.trim(),
        source: `${rel(filePath)} url()`,
      });
    }
  }
}

function checkJavaScriptSyntax(filePaths, inlineScripts) {
  let code = 0;
  for (const filePath of filePaths) {
    code |= runCheck(filePath);
  }

  const tmp = mkdtempSync(path.join(tmpdir(), "planetaire-site-js-"));
  try {
    inlineScripts.forEach((script, index) => {
      const filePath = path.join(tmp, `inline-${index + 1}.js`);
      writeFileSync(filePath, `// ${script.label}\n${script.code}\n`, "utf8");
      code |= runCheck(filePath, script.label);
    });
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
  return code;
}

function runCheck(filePath, label = rel(filePath)) {
  const result = spawnSync(process.execPath, ["--check", filePath], {
    cwd: root,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  if (result.status === 0) {
    return 0;
  }
  process.stderr.write(`\n${label}\n`);
  process.stderr.write(result.stdout);
  process.stderr.write(result.stderr);
  return result.status || 1;
}

let knownFiles = new Set();
let knownDirs = new Set();

async function main() {
  ({ files: knownFiles, dirs: knownDirs } = await collectKnownFiles());
  const errors = [];
  const inlineScripts = await validateHtmlReferences(errors);
  await validateCssReferences(errors);

  const syntaxStatus = checkJavaScriptSyntax(await readSiteFiles(".js"), inlineScripts);
  for (const error of errors) {
    console.error(error);
  }
  return errors.length || syntaxStatus ? 1 : 0;
}

process.exitCode = await main();
