// The in-browser apps' page code: runs tasks in worker.js and shows the
// results, as the Flask app's templates do (macros/downloads.html and
// macros/errors.html).
//
// The worker starts loading when the page does. Until it's ready, the form's
// button says so and can't be pressed, and the status line beside it shows the
// loading step; while a task runs, the button shows the form's data-busy
// label (e.g. "Generating exercise…").
var BrowserApps = (function () {
  "use strict";

  var worker = null;
  // "loading", "ready" or "failed", and while loading, the step; or the error.
  var state = { name: "loading", text: "Loading…" };
  var busy = false;
  var tasks = {};
  var nextId = 0;

  // Show the state (or that a task is running) on each app form.
  function render() {
    document.querySelectorAll("form[data-browser-app]").forEach(function (form) {
      var button = form.querySelector("[type=submit]");
      button.dataset.label = button.dataset.label || button.value;
      button.disabled = busy || state.name !== "ready";
      button.value = busy ? form.dataset.busy || "Working…"
        : state.name === "loading" ? "Loading…" : button.dataset.label;

      var status = form.querySelector(".browser-apps-status");
      status.classList.toggle("busy", busy || state.name === "loading");
      status.classList.toggle("error", !busy && state.name === "failed");
      status.textContent = busy ? form.dataset.busy || "Working…"
        : state.name === "loading" ? state.text + " The first time, this downloads about 12 MB, so it can take a while."
        : state.name === "failed" ? "Sorry, the app couldn't load (" + state.text + "). Try reloading the page."
        : "";
      status.hidden = !status.textContent;
    });
  }

  function setState(name, text) {
    state = { name: name, text: text };
    render();
  }

  function startWorker() {
    setState("loading", "Loading…");
    worker = new Worker("/browser-apps/assets/worker.js", { type: "module" });
    worker.onmessage = function (event) {
      var message = event.data;
      if (message.loading) return setState("loading", message.loading);
      if (message.ready) return setState("ready", "");
      if (message.failed) return setState("failed", message.failed);
      var task = tasks[message.id];
      if (!task) return;
      if (message.started) return task.onStarted();
      delete tasks[message.id];
      if (message.error) task.reject(new Error(message.error));
      else task.resolve(message.result);
    };
    worker.onerror = function (event) {
      setState("failed", event.message || "the app's worker failed to start");
      Object.keys(tasks).forEach(function (id) {
        tasks[id].reject(new Error(state.text));
        delete tasks[id];
      });
    };
  }

  // Run apps.py's task on the score at the URL, with args. Resolves with its
  // result, or rejects with an Error whose timedOut is true if it took more
  // than timeLimit seconds (not counting loading), in which case the worker is
  // stopped and a new one started.
  function run(task, score, args, timeLimit) {
    if (!worker) startWorker();
    if (state.name === "failed") return Promise.reject(new Error(state.text));
    var id = ++nextId;
    return new Promise(function (resolve, reject) {
      var timer = null;
      tasks[id] = {
        onStarted: function () {
          timer = setTimeout(function () {
            delete tasks[id];
            worker.terminate();
            startWorker();
            var error = new Error("Took more than " + timeLimit + " seconds");
            error.timedOut = true;
            reject(error);
          }, timeLimit * 1000);
        },
        resolve: function (result) { clearTimeout(timer); resolve(result); },
        reject: function (error) { clearTimeout(timer); reject(error); },
      };
      worker.postMessage({ id: id, task: task, score: new URL(score, location.href).href, args: args });
    });
  }

  function element(tag, attributes, children) {
    var e = document.createElement(tag);
    Object.keys(attributes || {}).forEach(function (name) { e.setAttribute(name, attributes[name]); });
    (children || []).forEach(function (child) {
      e.append(typeof child === "string" ? document.createTextNode(child) : child);
    });
    return e;
  }

  // The URL of the page that shows the MusicXML at url (which can be a blob:
  // URL, while this page is open).
  function viewUrl(url, name) {
    return "/browser-apps/score/?" + new URLSearchParams({ f: url, name: name });
  }

  // A download for each of the result's files, with its data as a blob: URL.
  function downloads(result) {
    return result.files.map(function (file) {
      var url = URL.createObjectURL(new Blob([file.data], { type: "application/vnd.recordare.musicxml+xml" }));
      return { title: file.title, url: url, name: file.name, view: viewUrl(url, file.name) };
    });
  }

  // Show errors and downloads ({title, url, name, view}) in container, as the
  // Flask templates do.
  function show(container, errors, files) {
    container.replaceChildren();
    errors.forEach(function (message) {
      container.append(element("p", { class: "error" }, [message]));
    });
    if (!files.length) return;
    var list = element("ul", { class: "file-downloads" });
    files.forEach(function (file) {
      var item = element("li", {}, [element("a", { href: file.url, download: file.name }, [file.title])]);
      if (file.view) {
        item.append(element("br"), "Alternatively, click ",
          element("a", { href: file.view, target: "_blank" }, ["here to view in browser"]));
      }
      list.append(item);
    });
    container.append(element("div", { class: "result" }, [
      element("h2", {}, [files.length > 1 ? "Downloads" : "Download"]),
      list,
      element("p", { class: "description" }, [
        "Hint: you can open the downloaded files in any notation software (e.g. MuseScore, Sibelius, or Finale). " +
        "If you don't already have a preference, try ",
        element("a", { href: "https://musescore.org/", target: "_blank", rel: "noopener" }, ["MuseScore"]),
        " which is free and open source. " +
        "If you don't want to download files or run notation software, use the 'view in browser' option.",
      ]),
    ]));
  }

  // Handle form's submission with submit(form), a function that returns a
  // promise, showing that it's busy until that settles.
  function onSubmit(form, submit) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (busy || state.name !== "ready") return;
      busy = true;
      render();
      Promise.resolve()
        .then(function () { return submit(form); })
        .finally(function () { busy = false; render(); });
    });
  }

  var lists = {};

  // Resolve with the list (chorales or lieder) that build-browser-apps.py wrote.
  function list(name) {
    lists[name] = lists[name] || fetch("/browser-apps/generated/" + name + ".json").then(function (response) {
      if (!response.ok) throw new Error("Couldn't load the list of " + name);
      return response.json();
    });
    return lists[name];
  }

  // Fill select with an option for each item, and update its Chosen widget.
  function fillSelect(select, items, option) {
    items.forEach(function (item) {
      var attributes = option(item);
      var text = attributes.text;
      delete attributes.text;
      select.append(element("option", attributes, [text]));
    });
    if (window.jQuery) jQuery(select).trigger("chosen:updated");
  }

  // Start loading the app on a page without an app form, so that the files it
  // downloads are in the browser's cache by the time the next page needs them.
  function preload() {
    if (!worker) startWorker();
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector("form[data-browser-app]")) preload();
  });

  return {
    run: run, show: show, downloads: downloads, viewUrl: viewUrl, onSubmit: onSubmit, element: element,
    list: list, fillSelect: fillSelect, preload: preload,
  };
})();
