import os

import pytest


def test_routes_are_registered(app):
    rules = {rule.rule for rule in app.url_map.iter_rules()}

    assert {
        "/apps/chorales/",
        "/apps/lieder/",
        "/apps/working-in-harmony/",
        "/apps/working-in-harmony/selected/<path:score>",
    } <= rules


@pytest.mark.parametrize("url", [
    "/apps/download/../../app/config.py",
    "/apps/score/../../app/config.py",
    "/apps/working-in-harmony/download/../../../app/config.py",
    "/apps/working-in-harmony/view/../../../app/config.py",
])
def test_path_traversal_is_not_found(client, url):
    with client.session_transaction() as session:
        session["wih_id"] = "test"

    assert client.get(url).status_code == 404


def test_missing_download_is_not_found(client):
    assert client.get("/apps/download/nope.xml").status_code == 404


@pytest.fixture
def generated_score(app):
    path = os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "chorales", "ex.xml")
    os.makedirs(os.path.dirname(path))
    with open(path, "w") as f:
        f.write("<score-partwise/>")
    return "chorales/ex.xml"


def test_download_serves_generated_scores_as_musicxml(client, generated_score):
    response = client.get("/apps/download/" + generated_score)

    assert response.status_code == 200
    assert response.data == b"<score-partwise/>"
    assert response.mimetype == "application/vnd.recordare.musicxml+xml"
    assert "attachment" not in response.headers.get("Content-Disposition", "")


def test_download_can_be_an_attachment(client, generated_score):
    response = client.get("/apps/download/" + generated_score + "?download=1")

    assert response.headers["Content-Disposition"] == "attachment; filename=ex.xml"


def test_download_names_corpus_scores_after_the_song(client, add_lied, song_path):
    lied = add_lied(song_path, "A/B/C")

    response = client.get("/apps/download/" + lied["relative_path"] + "?download=1")

    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=A_B_C_score.mxl"


def test_display_score_page_links_to_the_download(client, generated_score):
    response = client.get("/apps/score/" + generated_score)

    assert response.status_code == 200
    assert b'href="/apps/download/chorales/ex.xml?download=1"' in response.data


def test_display_missing_score_is_not_found(client):
    assert client.get("/apps/score/chorales/nope.xml").status_code == 404
