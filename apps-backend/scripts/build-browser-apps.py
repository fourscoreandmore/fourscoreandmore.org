#!/usr/bin/env python3
"""Prepare the files for the in-browser apps (browser-apps/ in the Jekyll site).

The in-browser apps run this app's music21 code in the browser with Pyodide,
instead of on a server. Run this before `jekyll build`, from anywhere:

    python3 apps-backend/scripts/build-browser-apps.py

It writes, all gitignored:

- browser-apps/generated/: Python wheels (pinned in uv.lock), this app's music
  code, the chorale and lieder scores, and the static files the pages share.
- _data/generated/lieder.json: the songs, for the pages' song lists.

It uses only the standard library, because it runs in the Jekyll (Ruby)
container. Downloads are checked against the hashes in uv.lock and
pnpm-lock.yaml, and cached in $PLATFORM_CACHE_DIR if that's set.
"""
import base64
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
SITE = BACKEND.parent
OUT = SITE / "browser-apps" / "generated"
DATA_OUT = SITE / "_data" / "generated"
CACHE = Path(os.environ.get("PLATFORM_CACHE_DIR") or BACKEND / ".cache") / "browser-apps"
LIEDER_CORPUS = BACKEND / "When-in-Rome" / "Corpus" / "OpenScore-LiederCorpus"

# Pure-Python wheels to serve, from uv.lock. music21's other requirements are
# either Pyodide packages (requests) or not needed by these apps (numpy and
# matplotlib, for analysis and graphs; chardet and joblib are optional).
WHEELS = ["music21", "jsonpickle", "webcolors", "more-itertools", "jsonlines"]

# This app's modules that the browser runs (see browser-apps/assets/apps.py).
APP_MODULES = ["TheoryExercises.py", "exercises.py", "indexer.py", "roman_text_validator.py"]

# Static files shared with the Flask app's pages, so the forms look the same.
STATIC_FILES = ["main.css", "forms.js", "lieder-form.js"]

# Files of music21's that the apps don't need: most of its corpus (the chorales
# are served separately) and some large test data.
MUSIC21_DROP = re.compile(r"^music21/(corpus/.*(?<!\.py)|audioSearch/.*\.wav|omr/.*\.xml)$")


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.rmtree(DATA_OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    DATA_OUT.mkdir(parents=True)

    wheels = [write_wheel(name) for name in WHEELS]
    copy_app_code()
    copy_static_files()
    write_osmd()
    lieder = write_lieder()
    modules = sorted(p.name for p in (OUT / "app").iterdir())
    write_json(OUT / "manifest.json", {"wheels": wheels, "modules": modules, "songs": len(lieder)})
    print("Wrote the in-browser apps' files to " + str(OUT.relative_to(SITE)))


def uv_lock_wheel(name):
    """Return the (url, sha256) of package name's pure-Python wheel in uv.lock."""
    lock = (BACKEND / "uv.lock").read_text(encoding="utf-8")
    for block in lock.split("[[package]]"):
        if re.search(r'^name = "%s"$' % re.escape(name), block, re.M):
            match = re.search(r'url = "([^"]+-py3-none-any\.whl)", hash = "sha256:([0-9a-f]+)"', block)
            if match:
                return match.group(1), match.group(2)
    sys.exit("No pure-Python wheel for %s in uv.lock" % name)


def download(url, check):
    """Return the content at url, cached, after check(content) passes."""
    path = CACHE / hashlib.sha256(url.encode()).hexdigest()
    if path.exists():
        content = path.read_bytes()
        if check(content):
            return content
    print("Downloading " + url)
    with urllib.request.urlopen(url, timeout=60) as response:
        content = response.read()
    if not check(content):
        sys.exit("Downloaded file doesn't match its lockfile hash: " + url)
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return content


def write_wheel(name):
    url, sha256 = uv_lock_wheel(name)
    content = download(url, lambda c: hashlib.sha256(c).hexdigest() == sha256)
    filename = url.rsplit("/", 1)[1]
    if name == "music21":
        content = trim_music21(content)
    (OUT / "wheels").mkdir(exist_ok=True)
    (OUT / "wheels" / filename).write_bytes(content)
    return filename


def trim_music21(content):
    """Return the music21 wheel without the files in MUSIC21_DROP.

    Also writes the chorales that _data/chorales.json lists, from music21's
    corpus, to chorales/.
    """
    chorales = json.loads((SITE / "_data" / "chorales.json").read_text(encoding="utf-8"))
    wanted = {"music21/corpus/bach/" + c["file"]: c["file"] for c in chorales}
    (OUT / "chorales").mkdir()
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(content)) as source, \
            zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as trimmed:
        for info in source.infolist():
            if info.filename in wanted:
                (OUT / "chorales" / wanted.pop(info.filename)).write_bytes(source.read(info))
            if MUSIC21_DROP.match(info.filename):
                continue
            data = source.read(info)
            if info.filename.endswith(".dist-info/RECORD"):
                lines = data.decode().splitlines(True)
                data = "".join(line for line in lines if not MUSIC21_DROP.match(line.split(",", 1)[0])).encode()
            trimmed.writestr(info, data)
    if wanted:
        sys.exit("Chorales not found in music21's corpus: " + ", ".join(sorted(wanted.values())))
    return out.getvalue()


def copy_app_code():
    (OUT / "app").mkdir()
    for module in APP_MODULES:
        shutil.copy(BACKEND / "app" / module, OUT / "app" / module)
    # As in the Upsun build hook, or from scripts/fetch-roman-umpire.sh.
    for path in (BACKEND / "When-in-Rome" / "Code" / "romanUmpire.py", BACKEND / "app" / "romanUmpire.py"):
        if path.exists():
            shutil.copy(path, OUT / "app" / "romanUmpire.py")
            return
    print("Warning: romanUmpire.py not found, so Working in Harmony won't work"
          " (check out the When-in-Rome submodule)")


def copy_static_files():
    (OUT / "static").mkdir()
    for filename in STATIC_FILES:
        shutil.copy(BACKEND / "app" / "static" / filename, OUT / "static" / filename)


def write_osmd():
    """Write OpenSheetMusicDisplay, the version in pnpm-lock.yaml (as the Flask app uses)."""
    lock = (BACKEND / "pnpm-lock.yaml").read_text(encoding="utf-8")
    match = re.search(r"^  opensheetmusicdisplay@([^:]+):\n    resolution: \{integrity: sha512-([^}]+)\}", lock, re.M)
    if not match:
        sys.exit("No opensheetmusicdisplay in pnpm-lock.yaml")
    version, integrity = match.groups()
    url = "https://registry.npmjs.org/opensheetmusicdisplay/-/opensheetmusicdisplay-%s.tgz" % version
    content = download(url, lambda c: base64.b64encode(hashlib.sha512(c).digest()).decode() == integrity)
    with tarfile.open(fileobj=io.BytesIO(content)) as tar:
        build = tar.extractfile("package/build/opensheetmusicdisplay.min.js").read()
    (OUT / "static" / "opensheetmusicdisplay.min.js").write_bytes(build)


def utf8(path):
    """Return path as a str, decoded as UTF-8 whatever the locale.

    Without a UTF-8 locale (as in some build containers), Python decodes
    non-ASCII filenames with surrogate escapes, which can't be written out.
    """
    return os.fsencode(str(path)).decode("utf-8")


def clean_path(name):
    # As app/indexer.py does.
    return utf8(name).replace("_", " ").strip()


def natural_key(text):
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r"(\d+)", text)]


def write_lieder():
    """Copy each song's score (and Working in Harmony template), and write the index.

    The songs are those that app/indexer.py's get_lieder_index finds, with the
    same names.
    """
    lieder = []
    if not LIEDER_CORPUS.is_dir():
        print("Warning: the Lieder Corpus isn't checked out, so the lieder apps have no songs"
              " (check out the When-in-Rome submodule)")
    else:
        for score in LIEDER_CORPUS.rglob("score.mxl"):
            song = score.parent
            relative_dir = utf8(song.relative_to(LIEDER_CORPUS).as_posix())
            files = os.listdir(song)
            parts = [clean_path(song.parent.parent.name), clean_path(song.parent.name), clean_path(song.name)]
            lieder.append({
                "dir": relative_dir,
                # Where the song's files are copied to: an ASCII name, as Jekyll
                # fails on some non-ASCII filenames.
                "id": hashlib.sha256(relative_dir.encode()).hexdigest()[:16],
                "name": " - ".join(p for p in parts if p),
                # As the Flask app requires for Working in Harmony.
                "wih": "template.txt" in files and "slices.tsv" in files,
            })
            destination = OUT / "lieder" / lieder[-1]["id"]
            destination.mkdir(parents=True)
            shutil.copy(score, destination / "score.mxl")
            if lieder[-1]["wih"]:
                shutil.copy(song / "template.txt", destination / "template.txt")
    lieder.sort(key=lambda song: natural_key(song["name"]))
    write_json(DATA_OUT / "lieder.json", lieder)
    write_json(OUT / "lieder.json", lieder)
    print("Indexed %d songs" % len(lieder))
    return lieder


def write_json(path, data):
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
