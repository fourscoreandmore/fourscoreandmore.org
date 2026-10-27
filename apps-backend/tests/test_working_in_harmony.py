import os
import shutil

import pytest

from conftest import requires_roman_umpire

pytestmark = requires_roman_umpire

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
def lied(app, chorale_path):
    """A stand-in for a lieder corpus entry, using the chorale as its score."""
    song_dir = os.path.join(app.config["LIEDER_CORPUS_PATH"], "Bach", "bwv66.6")
    os.makedirs(song_dir)
    shutil.copy(chorale_path, os.path.join(song_dir, "score.mxl"))
    return {"relative_path": "Bach/bwv66.6/score.mxl"}


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
