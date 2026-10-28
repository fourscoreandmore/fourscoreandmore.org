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
