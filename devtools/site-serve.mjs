import { createReadStream, statSync } from "node:fs";
import { createServer } from "node:http";
import path from "node:path";
import process from "node:process";

const root = path.resolve(import.meta.dirname, "..");
const site = path.join(root, "site");
const port = Number(process.env.PORT || 8765);
const host = process.env.HOST || "127.0.0.1";

const mimeTypes = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".svg", "image/svg+xml"],
  [".woff2", "font/woff2"],
]);

function resolvePath(urlPath) {
  const decoded = decodeURIComponent(urlPath);
  const relative = decoded === "/" ? "index.html" : decoded.replace(/^\/+/, "");
  const filePath = path.resolve(site, relative);
  if (!filePath.startsWith(`${site}${path.sep}`)) {
    return null;
  }
  return filePath;
}

const server = createServer((request, response) => {
  const url = new URL(request.url || "/", `http://${host}:${port}`);
  const filePath = resolvePath(url.pathname);
  if (!filePath) {
    response.writeHead(403).end("Forbidden");
    return;
  }

  try {
    const stat = statSync(filePath);
    if (!stat.isFile()) {
      response.writeHead(404).end("Not found");
      return;
    }
  } catch {
    response.writeHead(404).end("Not found");
    return;
  }

  response.setHeader(
    "Content-Type",
    mimeTypes.get(path.extname(filePath)) || "application/octet-stream",
  );
  createReadStream(filePath).pipe(response);
});

server.listen(port, host, () => {
  console.log(`Serving ${site} at http://${host}:${port}/`);
});
