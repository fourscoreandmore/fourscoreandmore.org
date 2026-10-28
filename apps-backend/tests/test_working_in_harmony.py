import io
import os
import re
import urllib.parse

import pytest

from conftest import requires_roman_umpire

ANALYSIS = """Composer: J. S. Bach
Title: Christ unser Herr zum Jordan kam

Time Signature: 4/4

m1 f#: i b2 V b3 i b4 VI
m2 iv b2 V b3 i
"""

TEMPLATE = """Composer: J. S. Bach
Title: Christ unser Herr zum Jordan kam
Analyst:
Proofreader:

Time Signature: 4/4
m1 b1
m2 b1
"""


@pytest.fixture
def lied(add_lied, chorale_path):
    """A stand-in for a lieder corpus entry, using the chorale as its score."""
    return add_lied(chorale_path, "Bach/Chorales/bwv66.6", files={"template.txt": TEMPLATE, "slices.tsv": ""})


@requires_roman_umpire
def test_analysis_produces_feedback_and_score(app, lied, tmp_path):
    from app.routes import _working_in_harmony_process

    out = str(tmp_path / "out")
    with app.app_context():
        errors = _working_in_harmony_process(lied, ANALYSIS, out)

    assert errors == []
    for filename in ("analysis.txt", "feedback.txt", "result.mxl"):
        assert os.path.getsize(os.path.join(out, filename)) > 0


def test_unfilled_template_explains_what_to_do(app, lied, tmp_path):
    """music21 9 crashes on RomanText with no chords; tell the user to fill in the template."""
    from app.roman_text_validator import NO_ROMAN_NUMERALS
    from app.routes import _working_in_harmony_process

    out = tmp_path / "out"
    with app.app_context():
        errors = _working_in_harmony_process(lied, TEMPLATE, str(out))

    assert errors == [NO_ROMAN_NUMERALS]
    assert not out.exists()


SELECTED = "/apps/working-in-harmony/selected/Bach/Chorales/bwv66.6"


def test_selection_lists_only_songs_with_a_template(client, lied, add_lied, song_path):
    add_lied(song_path, "Tester/Songs/No_template")

    response = client.get("/apps/working-in-harmony/")

    assert response.status_code == 200
    assert b"Bach - Chorales - bwv66.6" in response.data
    assert b"No template" not in response.data


def test_selecting_a_song_redirects_to_its_analysis_page(client, add_lied, chorale_path):
    add_lied(chorale_path, "Bach/Chorales/Nr 1", files={"template.txt": "", "slices.tsv": ""})

    response = client.post("/apps/working-in-harmony/", data={"originalScore": "Bach/Chorales/Nr 1"})

    assert response.status_code == 302
    assert response.location == "/apps/working-in-harmony/selected/" + urllib.parse.quote("Bach/Chorales/Nr 1")


def test_analysis_page_starts_with_the_template(client, lied):
    response = client.get(SELECTED)

    assert response.status_code == 200
    assert b"Proofreader:" in response.data
    assert b"/apps/download/Bach/Chorales/bwv66.6/score.mxl" in response.data


def test_analysis_page_reports_a_missing_template(client, add_lied, chorale_path):
    add_lied(chorale_path, "Bach/Chorales/bwv66.6")

    response = client.get(SELECTED)

    assert response.status_code == 200
    assert b"Template file not found" in response.data


def test_unknown_song_redirects_to_the_selection(client, lied):
    response = client.get("/apps/working-in-harmony/selected/Nobody/Nothing")

    assert response.status_code == 302
    assert response.location == "/apps/working-in-harmony"


def test_submitting_the_template_explains_what_to_do(client, lied):
    from app.roman_text_validator import NO_ROMAN_NUMERALS

    response = client.post(SELECTED, data={"analysis": TEMPLATE})

    assert response.status_code == 200
    assert NO_ROMAN_NUMERALS.encode() in response.data.replace(b"&#34;", b'"')


@requires_roman_umpire
def test_submitted_analysis_shows_feedback_and_the_annotated_score(client, lied):
    response = client.post(SELECTED, data={"analysis": ANALYSIS})

    assert response.status_code == 200
    assert b'class="feedback"' in response.data
    with client.session_transaction() as session:
        wih_id = session["wih_id"]
    match = re.search(rb'href="(/apps/working-in-harmony/download/Bach_Chorales_bwv66\.6/\w+/result\.mxl)', response.data)
    assert match

    download = client.get(match.group(1).decode())

    assert download.status_code == 200
    assert download.data[:2] == b"PK"  # a compressed MusicXML file
    assert download.mimetype == "application/vnd.recordare.musicxml+xml"
    assert os.path.isdir(os.path.join(client.application.config["WIH_WRITABLE_PATH"], wih_id))

    view_url = match.group(1).decode().replace("/download/", "/view/")
    assert f'href="{view_url}"'.encode() in response.data
    view = client.get(view_url)

    assert view.status_code == 200
    assert f'href="{match.group(1).decode()}?download=1"'.encode() in view.data


def test_downloads_need_a_session(client):
    response = client.get("/apps/working-in-harmony/download/x/result.mxl")

    assert response.status_code == 302
    assert response.location == "/working-in-harmony/"


def test_viewing_needs_a_session(client):
    response = client.get("/apps/working-in-harmony/view/x/result.mxl")

    assert response.status_code == 302
    assert response.location == "/working-in-harmony/"


def test_viewing_a_missing_result_is_not_found(client):
    with client.session_transaction() as session:
        session["wih_id"] = "test"

    assert client.get("/apps/working-in-harmony/view/x/result.mxl").status_code == 404


UPLOAD = "/apps/working-in-harmony/upload/"


@pytest.fixture
def analysed_song(song):
    """The test song with an analysis on a new, lowest part."""
    from music21 import clef, meter, note, stream

    part = stream.Part()
    part.partName = "Analysis"
    for number, lyric in enumerate(["C: I", "I", "V", "IV", "I", "I"], 1):
        measure = stream.Measure(number=number)
        if number == 1:
            measure.append(clef.BassClef())
            measure.append(meter.TimeSignature("4/4"))
        n = note.Note("C3", quarterLength=4)
        n.lyric = lyric
        measure.append(n)
        part.append(measure)
    song.insert(0, part)
    return song


def score_bytes(score, tmp_path, fmt="mxl", extension=".mxl"):
    path = tmp_path / ("upload" + extension)
    score.write(fmt, fp=str(path))
    return path.read_bytes()


def upload(client, data, filename="song.mxl"):
    return client.post(
        UPLOAD,
        data={"score": (io.BytesIO(data), filename)},
        content_type="multipart/form-data",
    )


def test_selection_links_to_the_upload(client):
    response = client.get("/apps/working-in-harmony/")

    assert f'href="{UPLOAD}"'.encode() in response.data


def test_upload_page_has_a_file_form(client):
    response = client.get(UPLOAD)

    assert response.status_code == 200
    assert b'enctype="multipart/form-data"' in response.data
    assert b'type="file"' in response.data


@requires_roman_umpire
@pytest.mark.parametrize("fmt, filename", [
    ("mxl", "song.mxl"),
    ("musicxml", "song.musicxml"),
    ("musicxml", "Song.XML"),
])
def test_uploaded_analysis_shows_feedback_and_the_annotated_score(client, analysed_song, tmp_path, fmt, filename):
    data = score_bytes(analysed_song, tmp_path, fmt, "." + filename.split(".")[-1].lower())

    response = upload(client, data, filename)

    assert response.status_code == 200
    assert b'class="error"' not in response.data
    assert b'class="feedback"' in response.data
    assert b"PITCH COVERAGE" in response.data
    match = re.search(rb'href="(/apps/working-in-harmony/download/upload/\w+/result\.mxl)\?download=1"', response.data)
    assert match
    download = client.get(match.group(1).decode())
    assert download.status_code == 200
    assert download.data[:2] == b"PK"
    view_url = match.group(1).decode().replace("/download/", "/view/")
    assert f'href="{view_url}"'.encode() in response.data
    assert client.get(view_url).status_code == 200


@requires_roman_umpire
def test_feedback_points_out_wrong_chords(client, analysed_song, tmp_path):
    """Bar 2 has C major in the piano, not ii."""
    analysed_song.parts[-1].measure(2).notes[0].lyric = "ii"

    response = upload(client, score_bytes(analysed_song, tmp_path))

    assert b'class="feedback"' in response.data
    assert b"Total cases: 1" in response.data


@requires_roman_umpire
def test_uploading_the_same_score_again_reuses_the_result(client, analysed_song, tmp_path, monkeypatch):
    data = score_bytes(analysed_song, tmp_path)
    first = upload(client, data)
    monkeypatch.setattr("app.routes._write_feedback", lambda *a, **k: pytest.fail("analysed again"))

    second = upload(client, data)

    assert second.data == first.data


def test_upload_reports_a_missing_analysis(client, song, tmp_path):
    from app.on_score_validator import NO_LYRICS

    response = upload(client, score_bytes(song, tmp_path))

    assert response.status_code == 200
    assert NO_LYRICS.encode() in response.data.replace(b"&#39;", b"'")
    assert b'class="feedback"' not in response.data


def test_upload_reports_bad_lyrics(client, analysed_song, tmp_path):
    from app.on_score_validator import NOT_A_ROMAN_NUMERAL

    analysed_song.parts[-1].measure(3).notes[0].lyric = "la"

    response = upload(client, score_bytes(analysed_song, tmp_path))

    message = NOT_A_ROMAN_NUMERAL.format(measure=3, lyric="la")
    assert message.encode() in response.data.replace(b"&#34;", b'"')


def test_upload_needs_a_file(client):
    response = client.post(UPLOAD, data={}, content_type="multipart/form-data")

    assert response.status_code == 200
    assert b"field-error" in response.data


def test_upload_rejects_other_file_types(client):
    response = upload(client, b"m1 C: I\n", "analysis.txt")

    assert b"Upload a MusicXML file" in response.data
    assert b'class="feedback"' not in response.data


@pytest.mark.parametrize("data, filename, message", [
    (b"not a zip", "song.mxl", b"not a compressed MusicXML"),
    (b"<not musicxml", "song.musicxml", b"could not be read as MusicXML"),
])
def test_upload_rejects_unreadable_files(client, data, filename, message):
    response = upload(client, data, filename)

    assert response.status_code == 200
    assert message in response.data


def test_upload_rejects_a_score_that_unzips_too_large(app, client, analysed_song, tmp_path):
    app.config["WIH_MAX_UNZIPPED_SIZE"] = 1000

    response = upload(client, score_bytes(analysed_song, tmp_path))

    assert b"The score is too large." in response.data


def test_upload_rejects_a_file_over_the_limit(app, client):
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

    response = upload(client, b"x" * (1024 * 1024 + 1))

    assert response.status_code == 413
    assert b"The file is too large: the limit is 1 MB." in response.data
    assert b'type="file"' in response.data


WOLF_EXAMPLE = os.path.join(
    os.path.dirname(__file__), "..", "..", "working-in-harmony-backend", "app",
    "Wolf_Hugo_-_Eichendorff-Lieder_Der verzweifelte Liebhaber.mxl",
)


@requires_roman_umpire
def test_the_example_from_the_analysis_notes(client):
    """The on-score example linked from working-in-harmony/analysis.md."""
    with open(WOLF_EXAMPLE, "rb") as f:
        response = upload(client, f.read(), os.path.basename(WOLF_EXAMPLE))

    assert b'class="error"' not in response.data
    assert b'class="feedback"' in response.data
