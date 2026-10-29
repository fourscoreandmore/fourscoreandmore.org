// Runs the in-browser apps' Python (apps.py) in Pyodide, off the page's main
// thread. apps.js starts this worker, and stops it if a task takes too long.
//
// Messages in: {id, task, score, args}: fetch the score (a URL), then run
// apps.<task>(score path, ...args). Messages out: {loading} with each step of
// loading, then {ready: true} or {failed}; and for each task, {id, started:
// true} when it starts, then {id, result} or {id, error}.
// Each result file comes back with its "data" (bytes) and "name".
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs";

const GENERATED = new URL("../generated/", import.meta.url);

async function fetchOk(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`Couldn't load ${url} (${response.status})`);
  return response;
}

async function start() {
  postMessage({ loading: "Loading Python…" });
  // Fresh, as it names this build's files (see build-browser-apps.py).
  const manifest = await (await fetchOk(new URL("manifest.json", GENERATED), { cache: "no-cache" })).json();
  const pyodide = await loadPyodide();
  postMessage({ loading: "Loading music21…" });
  // requests (for music21) and attrs (for jsonlines) are Pyodide packages; the
  // other wheels are pinned in uv.lock (see build-browser-apps.py).
  await pyodide.loadPackage(
    ["requests", "attrs", ...manifest.wheels.map((wheel) => new URL("wheels/" + wheel, GENERATED).href)],
    { messageCallback() {} },
  );

  // The app modules as a package named app, as in the Flask app (but without
  // Flask: app/__init__.py is empty here).
  const home = "/home/pyodide";
  pyodide.FS.mkdirTree(home + "/app");
  pyodide.FS.writeFile(home + "/app/__init__.py", "");
  for (const module of manifest.modules) {
    const source = await (await fetchOk(new URL("app/" + module + "?v=" + manifest.version, GENERATED))).text();
    pyodide.FS.writeFile(home + "/app/" + module, source);
  }
  const apps = await (await fetchOk(new URL("apps.py", import.meta.url))).text();
  pyodide.FS.writeFile(home + "/browser_apps.py", apps);
  pyodide.FS.mkdirTree("/tmp/scores");
  postMessage({ loading: "Starting music21…" });
  return { FS: pyodide.FS, apps: pyodide.pyimport("browser_apps") };
}

const ready = start();
ready.then(
  () => postMessage({ ready: true }),
  (error) => postMessage({ failed: error.message || String(error) }),
);

let scoreNumber = 0;

onmessage = async ({ data: { id, task, score, args } }) => {
  try {
    const { FS, apps } = await ready;
    const bytes = new Uint8Array(await (await fetchOk(score)).arrayBuffer());
    const extension = new URL(score, location.href).pathname.match(/\.\w+$/)?.[0] ?? "";
    const path = `/tmp/scores/${++scoreNumber}${extension}`;
    FS.writeFile(path, bytes);
    postMessage({ id, started: true });
    const run = apps[task];
    const proxy = run(path, ...args);
    const result = proxy.toJs({ dict_converter: Object.fromEntries });
    proxy.destroy();
    run.destroy();
    for (const file of result.files) {
      file.data = FS.readFile(file.path);
      file.name = file.path.split("/").pop();
    }
    postMessage({ id, result }, result.files.map((file) => file.data.buffer));
  } catch (error) {
    postMessage({ id, error: String(error) });
  }
};
