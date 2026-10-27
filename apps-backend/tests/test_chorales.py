import json
import os
import shutil

import music21
import pytest

from app.indexer import get_score_index


@pytest.fixture
def chorales_dir(app, chorale_path):
    path = os.path.join(app.config["SCORE_PATH"], "chorales")
    os.makedirs(path)
    shutil.copy(chorale_path, path)
    return path


def test_score_index_is_built_when_missing(chorales_dir):
    index = get_score_index(chorales_dir)

    assert list(index) == ["bwv66.6.mxl"]
    with open(os.path.join(chorales_dir, "scores.json")) as f:
        assert json.load(f) == index


def test_form_lists_chorales(client, chorales_dir):
    response = client.get("/apps/chorales/")

    assert response.status_code == 200
    assert b"bwv66.6.mxl" in response.data


@pytest.mark.parametrize("score_type,staves", [("full", 4), ("short", 2)])
def test_generate_exercise(app, client, chorales_dir, score_type, staves):
    response = client.post("/apps/chorales/", data={
        "originalScore": "bwv66.6.mxl",
        "beatsToCut": "2",
        "partsToCut": ["alto", "tenor", "bass"],
        "shortScore": score_type,
    })

    assert response.status_code == 200
    assert b"Failed to parse" not in response.data
    download_dir = os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "chorales")
    written = sorted(os.listdir(download_dir))
    assert any(f.endswith("-exercise.xml") for f in written)
    assert any(f.endswith("-solution.xml") for f in written)
    for filename in written:
        assert filename.encode() in response.data
        score = music21.converter.parse(os.path.join(download_dir, filename))
        if filename.endswith("-exercise.xml"):
            assert len(score.parts) == staves
