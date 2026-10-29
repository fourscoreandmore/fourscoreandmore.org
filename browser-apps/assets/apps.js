// The in-browser apps' page code: runs tasks in worker.js and shows the
// results, as the Flask app's templates do (macros/downloads.html and
// macros/errors.html).
//
// The worker starts loading when the page does, so it's often ready by the
// time the form is submitted.
var BrowserApps = (function () {
  "use strict";

  var worker = null;
  var loadFailure = null;
  var tasks = {};
  var nextId = 0;

  function status(text) {
    document.querySelectorAll(".browser-apps-status").forEach(function (element) {
      element.textContent = text;
      element.hidden = !text;
    });
  }

  function startWorker() {
    loadFailure = null;
    worker = new Worker("/browser-apps/assets/worker.js", { type: "module" });
    worker.onmessage = function (event) {
      var message = event.data;
      if ("status" in message) {
        if (message.failed) loadFailure = message.failed;
        status(message.status);
        return;
      }
      var task = tasks[message.id];
      if (!task) return;
      if (message.started) {
        task.onStarted();
        return;
      }
      delete tasks[message.id];
      if (message.error) task.reject(new Error(message.error));
      else task.resolve(message.result);
    };
    worker.onerror = function (event) {
      loadFailure = event.message || "The app's worker failed to start";
      Object.keys(tasks).forEach(function (id) {
        tasks[id].reject(new Error(loadFailure));
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
    if (loadFailure) return Promise.reject(new Error(loadFailure));
    var id = ++nextId;
    return new Promise(function (resolve, reject) {
      var timer = null;
      tasks[id] = {
        onStarted: function () {
          status("Working…");
          timer = setTimeout(function () {
            delete tasks[id];
            worker.terminate();
            startWorker();
            var error = new Error("Took more than " + timeLimit + " seconds");
            error.timedOut = true;
            reject(error);
          }, timeLimit * 1000);
        },
        resolve: function (result) { clearTimeout(timer); status(""); resolve(result); },
        reject: function (error) { clearTimeout(timer); status(""); reject(error); },
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
  // promise, disabling the form's button until it settles.
  function onSubmit(form, submit) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var button = form.querySelector("[type=submit]");
      button.disabled = true;
      Promise.resolve()
        .then(function () { return submit(form); })
        .finally(function () { button.disabled = false; });
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

  document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector("form[data-browser-app]")) startWorker();
  });

  return {
    run: run, show: show, downloads: downloads, viewUrl: viewUrl, onSubmit: onSubmit, element: element,
    list: list, fillSelect: fillSelect,
  };
})();
