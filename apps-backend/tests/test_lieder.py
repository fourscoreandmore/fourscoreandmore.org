import os

import music21
import pytest

FORM = {
    "originalScore": "Tester,_A/Songs,_Op.1/1_Test_Song",
    "preserveRestBars": "y",
    "restLength": "2",
    "addition": "none",
    "harmonicRhythm": "1",
}


@pytest.fixture
def lied(add_lied, song_path):
    return add_lied(song_path)


def written(app):
    download_dir = os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "lieder")
    return sorted(os.listdir(download_dir)) if os.path.exists(download_dir) else []


def test_form_lists_songs(client, lied):
    response = client.get("/apps/lieder/")

    assert response.status_code == 200
    assert b"Tester, A - Songs, Op.1 - 1 Test Song" in response.data


@pytest.mark.parametrize("fields,filename", [
    ({}, "Tester_Test_Song-rests2-exercise.xml"),
    ({"preserveRestBars": None, "preserveBass": "y"}, "Tester_Test_Song-withBass-exercise.xml"),
    ({"addition": "transferTune"}, "Tester_Test_Song-rests2-transferTune-exercise.xml"),
    ({"addition": "chordHints", "harmonicRhythm": "2"}, "Tester_Test_Song-rests2-chordHints2-exercise.xml"),
])
def test_generate_exercise(app, client, lied, fields, filename):
    data = {k: v for k, v in {**FORM, **fields}.items() if v is not None}

    response = client.post("/apps/lieder/", data=data)

    assert response.status_code == 200
    assert written(app) == [filename]
    assert b"/apps/download/lieder/" + filename.encode() in response.data
    exercise = music21.converter.parse(os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "lieder", filename))
    assert len(exercise.parts) == 3


def test_unreadable_score_is_reported(app, client, add_lied, tmp_path):
    broken = tmp_path / "broken.mxl"
    broken.write_text("not a score")
    add_lied(str(broken))

    response = client.post("/apps/lieder/", data=FORM)

    assert response.status_code == 200
    assert b"Failed to parse file: Tester,_A/Songs,_Op.1/1_Test_Song/score.mxl" in response.data
    assert written(app) == []


def test_unknown_song_is_rejected(app, client, lied):
    response = client.post("/apps/lieder/", data={**FORM, "originalScore": "Nobody/Nothing/Nowhere"})

    assert response.status_code == 200
    assert b"Not a valid choice" in response.data
    assert written(app) == []


def test_invalid_harmonic_rhythm_is_rejected(app, client, lied):
    response = client.post("/apps/lieder/", data={**FORM, "addition": "chordHints", "harmonicRhythm": "5"})

    assert response.status_code == 200
    assert written(app) == []
