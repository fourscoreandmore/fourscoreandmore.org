# apps-backend

The Flask app behind [fourscoreandmore.org/apps](https://fourscoreandmore.org/apps):
the chorale and lieder exercise generators ([Cut Outs](https://fourscoreandmore.org/cut-outs))
and [Working in Harmony](https://fourscoreandmore.org/working-in-harmony).

It uses Python 3.14 and [uv](https://docs.astral.sh/uv/), on Upsun
(`.platform.app.yaml`) and in CI (`.github/workflows/apps-backend.yml`).

## Tests

```bash
uv sync
scripts/fetch-roman-umpire.sh   # optional: without it, Working in Harmony tests are skipped
uv run pytest
uv run ruff check .
```

`romanUmpire.py` comes from the [When-in-Rome](https://github.com/MarkGotham/When-in-Rome)
submodule. If the submodule is checked out, the tests use it from there.

## Dependencies

Add or upgrade with `uv add <package>` or `uv lock --upgrade-package <package>`, and
commit `uv.lock`. Dependabot opens weekly grouped updates.

## Checking score rendering

The "view in browser" links open `app/templates/display-music.html`, which draws
MusicXML with [OpenSheetMusicDisplay](https://opensheetmusicdisplay.org/) (OSMD,
from `package.json`; the build hook copies it into `app/static/`). Before
upgrading OSMD or changing that template, screenshot some scores with the old and
new versions and compare them by eye. CI doesn't check rendering.

```bash
pnpm install --frozen-lockfile
# Bach chorales and the app's exercises made from them, plus lieder exercises
# from any Lieder Corpus score.mxl files given:
uv run python scripts/make-sample-scores.py /tmp/samples
# The version to compare against:
(mkdir -p /tmp/osmd-old && cd /tmp/osmd-old && npm install opensheetmusicdisplay@1.9.9)
node scripts/render-scores.js --out /tmp/render \
  --osmd /tmp/osmd-old/node_modules/opensheetmusicdisplay/build/opensheetmusicdisplay.min.js \
  --osmd node_modules/opensheetmusicdisplay/build/opensheetmusicdisplay.min.js \
  /tmp/samples/*
```

`render-scores.js` needs Playwright with Chromium. It renders each score at
desktop and phone widths, writes `*.compare.png` side by side when given two
builds, and fails if a score doesn't render or logs an error. Re-rendering the
same build gives identical images, but between versions the layout shifts, so
pixel diffs flag everything: look at the images, and check a change against the
MusicXML before calling it a regression (OSMD often starts drawing what the file
actually says).

For real songs, take a few `score.mxl` files from the Lieder Corpus in the
When-in-Rome submodule without checking it all out:

```bash
git clone --filter=blob:none --no-checkout https://github.com/MarkGotham/When-in-Rome.git /tmp/wir
sha=$(git ls-tree HEAD When-in-Rome | awk '{print $3}')
git -C /tmp/wir ls-tree -r --name-only "$sha" Corpus/OpenScore-LiederCorpus | grep 'score.mxl$'
git -C /tmp/wir show "$sha:Corpus/OpenScore-LiederCorpus/<composer>/<set>/<song>/score.mxl" > /tmp/song.mxl
```
