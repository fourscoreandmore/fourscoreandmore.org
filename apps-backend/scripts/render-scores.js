#!/usr/bin/env node
// Screenshot MusicXML files as the "view in browser" page shows them
// (app/templates/display-music.html), at desktop and phone widths, with one
// or more builds of OpenSheetMusicDisplay. With two builds it also writes
// side-by-side images for comparing an upgrade.
//
//   node scripts/render-scores.js --out DIR [--osmd BUILD.js ...] SCORE...
//
// --osmd defaults to the locked version in node_modules. Exits non-zero if
// any score fails to render or logs an error. Needs Playwright with Chromium.
const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

const BACKEND = path.dirname(__dirname);
const VIEWPORTS = { desktop: { width: 1280, height: 900 }, mobile: { width: 390, height: 844 } };

const args = process.argv.slice(2);
const builds = [], scores = [];
let out = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--osmd") builds.push(path.resolve(args[++i]));
  else if (args[i] === "--out") out = path.resolve(args[++i]);
  else scores.push(path.resolve(args[i]));
}
if (!out || scores.length === 0) {
  console.error("Usage: node scripts/render-scores.js --out DIR [--osmd BUILD.js ...] SCORE...");
  process.exit(2);
}
if (builds.length === 0) {
  builds.push(path.join(BACKEND, "node_modules/opensheetmusicdisplay/build/opensheetmusicdisplay.min.js"));
}

// The template with its Jinja placeholders filled in for this server.
let page = fs.readFileSync(path.join(BACKEND, "app/templates/display-music.html"), "utf8")
  .replace(/{{ url_for\('static', filename='([^']+)'\) }}/g, "static/$1")
  .replace(/"{{ file }}"/g, 'new URLSearchParams(location.search).get("f")')
  .replace(/{{ file }}|{{ basename }}/g, "");
if (page.includes("{{") || page.includes("{%")) {
  console.error("display-music.html has Jinja this script doesn't fill in; update render-scores.js");
  process.exit(2);
}

// /page/<build>/ is the page with that OSMD build as its static file.
const server = http.createServer((req, res) => {
  const parts = decodeURIComponent(new URL(req.url, "http://localhost").pathname).split("/");
  let file;
  if (parts[1] === "page" && parts[3] === "") return res.end(page);
  if (parts[1] === "page" && parts[4] === "opensheetmusicdisplay.min.js") file = builds[Number(parts[2])];
  else if (parts[1] === "page" && parts[3] === "static") file = path.join(BACKEND, "app/static", parts[4]);
  else if (parts[1] === "score") file = scores[Number(parts[2])];
  else if (parts[1] === "shot") file = path.join(out, ...parts.slice(2));
  fs.readFile(file || "", (err, data) => {
    if (err) { res.statusCode = 404; return res.end(); }
    res.end(data);
  });
});

(async () => {
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  let failures = 0;

  for (const [vname, viewport] of Object.entries(VIEWPORTS)) {
    const context = await browser.newContext({ viewport, deviceScaleFactor: 1 });
    for (const [s, score] of scores.entries()) {
      const shots = [];
      for (const b of builds.keys()) {
        const tab = await context.newPage();
        const errors = [];
        tab.on("pageerror", (e) => errors.push(e.message));
        tab.on("console", (m) => m.type() === "error" && errors.push(m.text()));
        const start = Date.now();
        await tab.goto(`${base}/page/${b}/?f=${encodeURIComponent(`/score/${s}/${path.basename(score)}`)}`);
        try {
          await tab.waitForSelector("#container svg", { timeout: 30000 });
        } catch {
          errors.push("nothing rendered");
        }
        // Rendering is done once the page stops growing.
        for (let last = -1, i = 0; i < 20; i++) {
          await tab.waitForTimeout(250);
          const height = await tab.evaluate(() => document.body.scrollHeight);
          if (height === last) break;
          last = height;
        }
        const name = `${vname}/${path.basename(score)}.${builds.length > 1 ? `osmd${b}.` : ""}png`;
        fs.mkdirSync(path.join(out, vname), { recursive: true });
        await tab.screenshot({ path: path.join(out, name), fullPage: true });
        shots.push(name);
        const height = await tab.evaluate(() => document.body.scrollHeight);
        console.log(`${errors.length ? "FAIL" : "ok  "} ${name} ${height}px ${Date.now() - start}ms`);
        for (const e of new Set(errors)) console.log(`     ${e}`);
        if (errors.length) failures++;
        await tab.close();
      }
      if (builds.length > 1) {
        const tab = await context.newPage();
        await tab.setViewportSize({ width: viewport.width * builds.length + 20, height: 600 });
        await tab.setContent(`<body style="margin:0;display:flex;gap:20px;align-items:flex-start;background:#ccc;font:12px sans-serif">${
          shots.map((shot, b) => `<div><div style="padding:4px">${builds[b]}</div><img src="${base}/shot/${shot}"></div>`).join("")}</body>`);
        await tab.waitForLoadState("networkidle");
        await tab.screenshot({ path: path.join(out, `${vname}/${path.basename(score)}.compare.png`), fullPage: true });
        await tab.close();
      }
    }
    await context.close();
  }

  await browser.close();
  server.close();
  console.log(`Screenshots in ${out}`);
  process.exit(failures ? 1 : 0);
})();
