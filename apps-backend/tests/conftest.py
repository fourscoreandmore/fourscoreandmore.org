import importlib.util
import os
import shutil
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


SONG = {
    # Bar 1 and 3 have vocal rests, so their piano part is kept by default.
    # Bar 4 has an off-beat leap (A4-F5), which gets a chord hint.
    "Voice": ["r w", "C5 h E5 q G5 q", "r h D5 q B4 q", "C5 q A4 e F5 e D5 h", "C5 w", "E5 w"],
    "Piano RH": ["E4 w", "E4 w", "F4 w", "F4 w", "E4 w", "C4 w"],
    "Piano LH": ["C3 w", "C3 w", "G2 w", "F2 w", "C3 w", "C3 w"],
}
DURATIONS = {"w": 4, "h": 2, "q": 1, "e": 0.5}


def make_song():
    """A short song for voice and piano: three parts of six 4/4 bars."""
    from music21 import clef, metadata, meter, note, stream

    score = stream.Score()
    score.metadata = metadata.Metadata(title="Test Song", composer="Tester")
    for name, bars in SONG.items():
        part = stream.Part()
        part.partName = name
        for number, bar in enumerate(bars, 1):
            measure = stream.Measure(number=number)
            if number == 1:
                measure.append(clef.BassClef() if name == "Piano LH" else clef.TrebleClef())
                measure.append(meter.TimeSignature("4/4"))
            tokens = bar.split()
            for pitch, duration in zip(tokens[::2], tokens[1::2]):
                if pitch == "r":
                    n = note.Rest(quarterLength=DURATIONS[duration])
                else:
                    n = note.Note(pitch, quarterLength=DURATIONS[duration])
                    if name == "Voice":
                        n.lyric = "la"
                measure.append(n)
            part.append(measure)
        score.insert(0, part)
    return score


@pytest.fixture
def song():
    return make_song()


@pytest.fixture(scope="session")
def song_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("song") / "score.mxl"
    make_song().write("mxl", fp=str(path))
    return str(path)


@pytest.fixture
def add_lied(app):
    """Add a song to the lieder corpus, laid out as in When-in-Rome.

    Returns the song's index entry once the index has been rebuilt.
    """
    from app.indexer import get_lieder_index

    def add(score_path, relative_dir="Tester,_A/Songs,_Op.1/1_Test_Song", files=()):
        song_dir = os.path.join(app.config["LIEDER_CORPUS_PATH"], relative_dir)
        os.makedirs(song_dir)
        shutil.copy(score_path, os.path.join(song_dir, "score.mxl"))
        for filename, contents in dict(files).items():
            with open(os.path.join(song_dir, filename), "w") as f:
                f.write(contents)
        open(app.config["LIEDER_INDEX_PATH"], "a").close()
        index = get_lieder_index(
            app.config["LIEDER_CORPUS_PATH"],
            index_filename=app.config["LIEDER_INDEX_PATH"],
            rebuild=True,
        )
        return index[relative_dir]

    return add


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
        CORPUS_DOWNLOAD_PATH=str(tmp_path / "lieder"),
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
