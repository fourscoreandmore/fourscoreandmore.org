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
    assert os.listdir(tmp_path / "song") == ["hash"]


def test_an_incomplete_result_from_before_is_replaced(app, tmp_path):
    from app.routes import _run_analysis

    directory = str(tmp_path / "song" / "hash")
    os.makedirs(directory)
    open(os.path.join(directory, "feedback.txt"), "w").close()

    assert _run_analysis(lambda directory: write_result(directory) or [], directory) == []
    assert open(os.path.join(directory, "feedback.txt")).read() == "Feedback"
    assert os.listdir(tmp_path / "song") == ["hash"]
