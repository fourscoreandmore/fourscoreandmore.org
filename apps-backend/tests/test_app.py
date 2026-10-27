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
])
def test_path_traversal_is_not_found(client, url):
    with client.session_transaction() as session:
        session["wih_id"] = "test"

    assert client.get(url).status_code == 404


def test_missing_download_is_not_found(client):
    assert client.get("/apps/download/nope.xml").status_code == 404
