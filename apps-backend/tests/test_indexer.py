import json
import os
import shutil

import pytest
from music21 import metadata, stream

from app import scores
from app.indexer import clean_path, get_lieder_index, get_score_index, get_score_name


def score_with(**fields):
    score = stream.Score()
    score.metadata = metadata.Metadata(**{"composer": "Bach", **fields})
    return score


@pytest.mark.parametrize("fields,name", [
    ({"title": "Chorale"}, "Bach - Chorale"),
    ({"title": "Suite", "movementNumber": "2"}, "Bach - Suite: 2"),
    ({"title": "Suite", "movementNumber": "2", "movementName": "Allemande"}, "Bach - Suite: 2, Allemande"),
    ({"title": "Suite", "movementName": "Suite"}, "Bach - Suite"),
    ({"movementName": "Allemande"}, "Bach - Allemande"),
    ({"movementName": "Allemande", "movementNumber": "2"}, "Bach - Allemande: 2"),
])
def test_score_name(fields, name):
    assert get_score_name(score_with(**fields)) == name


@pytest.mark.parametrize("fields,name", [
    ({"composer": None, "title": "Chorale"}, "Chorale"),
    ({"title": None}, "Bach"),
])
def test_score_name_leaves_out_missing_metadata(fields, name):
    assert get_score_name(score_with(**fields)) == name


def test_clean_path():
    assert clean_path(" Schubert,_Franz ") == "Schubert, Franz"


# Score index (chorales)


@pytest.fixture
def scores_dir(app, chorale_path):
    path = os.path.join(app.config["SCORE_PATH"], "chorales")
    os.makedirs(path)
    shutil.copy(chorale_path, path)
    return path


def test_score_index_skips_files_that_fail_to_parse(scores_dir):
    with open(os.path.join(scores_dir, "broken.xml"), "w") as f:
        f.write("<not-musicxml/>")
    with open(os.path.join(scores_dir, "notes.txt"), "w") as f:
        f.write("not a score")

    assert list(get_score_index(scores_dir)) == ["bwv66.6.mxl"]


def test_score_index_is_written_in_one_step(scores_dir):
    index = get_score_index(scores_dir)

    with open(os.path.join(scores_dir, "scores.json")) as f:
        assert json.load(f) == index
    assert not [name for name in os.listdir(scores_dir) if name.startswith(".partial-")]


def test_score_index_is_cached(scores_dir):
    with open(os.path.join(scores_dir, "scores.json"), "w") as f:
        json.dump({"cached.xml": "Cached - Score"}, f)

    assert get_score_index(scores_dir) == {"cached.xml": "Cached - Score"}
    assert list(get_score_index(scores_dir, reset=True)) == ["bwv66.6.mxl"]


def test_list_scores_sorts_by_name(scores_dir):
    with open(os.path.join(scores_dir, "scores.json"), "w") as f:
        json.dump({"b.xml": "Bach - Chorale 10", "a.xml": "Bach - Chorale 9", "c.xml": "Anon - Song"}, f)

    assert scores.list_scores("chorales") == [
        ("c.xml", "Anon - Song"),
        ("a.xml", "Bach - Chorale 9"),
        ("b.xml", "Bach - Chorale 10"),
    ]


def test_normalize_score_path(app, scores_dir):
    assert scores.normalizeScorePath("bwv66.6.mxl", subDir="chorales") == os.path.join(scores_dir, "bwv66.6.mxl")

    with pytest.raises(ValueError, match="File not found"):
        scores.normalizeScorePath("missing.mxl", subDir="chorales")


# Lieder index


def test_lieder_index_describes_each_song(app, add_lied, song_path):
    lied = add_lied(song_path, "Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht", files={"template.txt": ""})

    corpus = app.config["LIEDER_CORPUS_PATH"]
    assert lied == {
        "relative_path": "Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/score.mxl",
        "relative_dir": "Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht",
        "dir": os.path.join(corpus, "Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht"),
        "title": "01 Gute Nacht",
        "collection": "Winterreise, D.911",
        "composer": "Schubert, Franz",
        "name": "Schubert, Franz - Winterreise, D.911 - 01 Gute Nacht",
        "files": lied["files"],
    }
    assert sorted(lied["files"]) == ["score.mxl", "template.txt"]


def test_lieder_index_is_read_back_unless_rebuilt(app, add_lied, song_path):
    add_lied(song_path, "A/B/C")
    corpus = app.config["LIEDER_CORPUS_PATH"]
    index_path = app.config["LIEDER_INDEX_PATH"]
    shutil.rmtree(os.path.join(corpus, "A"))

    assert list(get_lieder_index(corpus, index_filename=index_path)) == ["A/B/C"]
    assert get_lieder_index(corpus, index_filename=index_path, rebuild=True) == {}


def test_lieder_index_is_replaced_in_one_step(app, add_lied, song_path):
    add_lied(song_path, "A/B/C")
    corpus = app.config["LIEDER_CORPUS_PATH"]
    index_path = app.config["LIEDER_INDEX_PATH"]
    os.makedirs(os.path.join(corpus, "D/E/F"))
    shutil.copy(song_path, os.path.join(corpus, "D/E/F/score.mxl"))
    before = os.stat(index_path).st_ino

    assert sorted(get_lieder_index(corpus, index_filename=index_path, rebuild=True)) == ["A/B/C", "D/E/F"]

    # A new file, renamed into place, rather than the old one rewritten.
    assert os.stat(index_path).st_ino != before
    assert sorted(get_lieder_index(corpus, index_filename=index_path)) == ["A/B/C", "D/E/F"]
    assert not [name for name in os.listdir(os.path.dirname(index_path)) if name.startswith(".partial-")]


def test_lieder_index_is_built_when_missing(app, add_lied, song_path):
    add_lied(song_path, "A/B/C")
    os.remove(app.config["LIEDER_INDEX_PATH"])

    assert list(scores.list_lieder()) == [("A/B/C", "A - B - C")]
    assert os.path.exists(app.config["LIEDER_INDEX_PATH"])


def test_list_lieder_can_require_files(app, add_lied, song_path):
    add_lied(song_path, "Z/Songs/Plain")
    add_lied(song_path, "A/Songs/Analysable", files={"template.txt": "", "slices.tsv": ""})

    assert scores.list_lieder() == [
        ("A/Songs/Analysable", "A - Songs - Analysable"),
        ("Z/Songs/Plain", "Z - Songs - Plain"),
    ]
    assert scores.list_lieder(require_files=["template.txt", "slices.tsv"]) == [
        ("A/Songs/Analysable", "A - Songs - Analysable"),
    ]


def test_lied_by_dir(app, add_lied, song_path):
    lied = add_lied(song_path, "A/B/C")

    assert scores.lied_by_dir("A/B/C") == lied
    assert scores.lied_by_dir("A/B/missing") is None
