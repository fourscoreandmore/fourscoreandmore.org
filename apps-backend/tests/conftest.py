import importlib.util
import os
import sys
import types

import jinja2
import pytest

BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_roman_umpire():
    """Make app.romanUmpire importable, as the Upsun build hook does.

    The build hook copies it from the When-in-Rome submodule. Use that copy if
    it exists, then the submodule itself, else a stub (tests that need it are
    skipped).
    """
    for path in (
        os.path.join(BACKEND, "app", "romanUmpire.py"),
        os.path.join(BACKEND, "When-in-Rome", "Code", "romanUmpire.py"),
    ):
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("app.romanUmpire", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["app.romanUmpire"] = module
            spec.loader.exec_module(module)
            return True
    sys.modules["app.romanUmpire"] = types.ModuleType("app.romanUmpire")
    return False


HAVE_ROMAN_UMPIRE = _load_roman_umpire()

from app import app as flask_app  # noqa: E402

requires_roman_umpire = pytest.mark.skipif(
    not HAVE_ROMAN_UMPIRE, reason="romanUmpire.py not available (When-in-Rome submodule not checked out)"
)


@pytest.fixture(scope="session")
def chorale_path(tmp_path_factory):
    """A Bach chorale bundled with music21, written out as MusicXML."""
    from music21 import corpus

    path = tmp_path_factory.mktemp("corpus") / "bwv66.6.mxl"
    corpus.parse("bach/bwv66.6").write("mxl", fp=str(path))
    return str(path)


@pytest.fixture
def app(tmp_path):
    """The Flask app with its Upsun mounts replaced by temporary directories."""
    original_config = dict(flask_app.config)
    original_loader = flask_app.jinja_loader
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SCORE_PATH=str(tmp_path / "scores"),
        SCORE_DOWNLOAD_PATH=str(tmp_path / "download"),
        LIEDER_CORPUS_PATH=str(tmp_path / "lieder"),
        LIEDER_INDEX_PATH=str(tmp_path / "lieder.jsonl"),
        WIH_WRITABLE_PATH=str(tmp_path / "wih-writable"),
    )
    # writable/base.html is fetched from the Jekyll site at deploy time.
    flask_app.jinja_loader = jinja2.ChoiceLoader([
        jinja2.DictLoader({"writable/base.html": "<html><body>{% block content %}{% endblock %}</body></html>"}),
        original_loader,
    ])
    flask_app.jinja_env.cache = {}
    yield flask_app
    flask_app.config.clear()
    flask_app.config.update(original_config)
    flask_app.jinja_loader = original_loader
    flask_app.jinja_env.cache = {}


@pytest.fixture
def client(app):
    return app.test_client()
