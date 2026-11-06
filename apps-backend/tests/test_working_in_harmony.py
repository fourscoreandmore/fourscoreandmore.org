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


def test_an_analysis_that_takes_too_long_is_stopped(app, client, lied, monkeypatch):
    import time

    def slow(lied, analysis, directory):
        open(os.path.join(directory, "feedback.txt"), "w").close()
        time.sleep(5)
        return []

    monkeypatch.setattr("app.routes._working_in_harmony_process", slow)
    app.config["WIH_TIME_LIMIT"] = 0.5

    response = client.post(SELECTED, data={"analysis": ANALYSIS})

    assert response.status_code == 200
    assert b"the analysis took too long (over 0.5 seconds)" in response.data
    assert b'class="feedback"' not in response.data
    # The half-finished result is deleted, so it isn't reused next time.
    with client.session_transaction() as session:
        wih_dir = os.path.join(app.config["WIH_WRITABLE_PATH"], session["wih_id"])
    assert not any(files for _, _, files in os.walk(wih_dir))


def write_result(directory, feedback="Feedback"):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "feedback.txt"), "w") as f:
        f.write(feedback)
    with open(os.path.join(directory, "result.mxl"), "w") as f:
        f.write("score")


def test_a_finished_result_is_reused(app, tmp_path):
    from app.routes import _run_analysis

    directory = str(tmp_path / "song" / "hash")
    write_result(directory)

    assert _run_analysis(lambda directory: pytest.fail("analysed again"), directory) == []


def test_a_failed_analysis_leaves_nothing_behind(app, tmp_path):
    """Even if it wrote all its files before failing."""
    from app.routes import _run_analysis

    def fails(directory):
        write_result(directory)
        return ["Failed to write analysis to a score"]

    errors = _run_analysis(fails, str(tmp_path / "song" / "hash"))

    assert errors == ["Failed to write analysis to a score"]
    assert os.listdir(tmp_path / "song") == []


def test_an_identical_submission_that_finished_first_is_kept(app, tmp_path):
    from app.routes import _run_analysis

    directory = str(tmp_path / "song" / "hash")

    def other_request_finishes_first(directory_arg):
        write_result(directory, "First")
        write_result(directory_arg, "Second")
        return []

    assert _run_analysis(other_request_finishes_first, directory) == []
    assert open(os.path.join(directory, "feedback.txt")).read() == "First"
    assert sorted(os.listdir(tmp_path / "song")) == ["hash", "hash.lock"]


def test_an_incomplete_result_from_before_is_replaced(app, tmp_path):
    from app.routes import _run_analysis

    directory = str(tmp_path / "song" / "hash")
    os.makedirs(directory)
    open(os.path.join(directory, "feedback.txt"), "w").close()

    assert _run_analysis(lambda directory: write_result(directory) or [], directory) == []
    assert open(os.path.join(directory, "feedback.txt")).read() == "Feedback"
    assert sorted(os.listdir(tmp_path / "song")) == ["hash", "hash.lock"]


def test_an_upload_that_takes_too_long_is_stopped(app, client, monkeypatch):
    import time

    def slow(data, extension, directory):
        write_result(directory)
        time.sleep(5)
        return []

    monkeypatch.setattr("app.routes._working_in_harmony_upload_process", slow)
    app.config["WIH_TIME_LIMIT"] = 0.5

    response = upload(client, b"PK not really", "song.mxl")

    assert b"the analysis took too long (over 0.5 seconds)" in response.data
    assert b'class="feedback"' not in response.data
    with client.session_transaction() as session:
        wih_dir = os.path.join(app.config["WIH_WRITABLE_PATH"], session["wih_id"])
    assert not any(files for _, _, files in os.walk(wih_dir))


@requires_roman_umpire
def test_an_uploaded_score_is_not_given_a_piano_brace(client, tmp_path):
    """romanUmpire braces parts 2 and 3 of 4 as a piano, for the lieder."""
    from music21 import converter, layout, meter, note, stream

    score = stream.Score()
    for name, pitches, lyrics in [
        ("Violin", ["E5", "F5", "D5", "E5"], None),
        ("Viola", ["G4", "A4", "B4", "G4"], None),
        ("Cello", ["C3", "F2", "G2", "C3"], None),
        ("Analysis", ["C3"] * 4, ["C: I", "IV", "V", "I"]),
    ]:
        part = stream.Part()
        part.partName = name
        for number, pitch in enumerate(pitches, 1):
            measure = stream.Measure(number=number)
            if number == 1:
                measure.append(meter.TimeSignature("4/4"))
            n = note.Note(pitch, quarterLength=4)
            if lyrics:
                n.lyric = lyrics[number - 1]
            measure.append(n)
            part.append(measure)
        score.insert(0, part)

    response = upload(client, score_bytes(score, tmp_path))

    match = re.search(rb'href="(/apps/working-in-harmony/download/upload/\w+/result\.mxl)\?download=1"', response.data)
    result = tmp_path / "result.mxl"
    result.write_bytes(client.get(match.group(1).decode()).data)
    assert list(converter.parse(str(result)).recurse().getElementsByClass(layout.StaffGroup)) == []
