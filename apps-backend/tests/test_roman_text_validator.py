import music21
import pytest

from app.roman_text_validator import NO_ROMAN_NUMERALS, validate_roman_text

VALID = {
    "beat and key": "Time Signature: 4/4\nm1 b1 C: I\n",
    "beat omitted": "Time Signature: 4/4\nm1 I\nm2 V\n",
    "template with one chord filled in": "Time Signature: 4/4\nm1 b1 C: I\nm2 b1\n",
    "Windows line endings": "Time Signature: 4/4\r\nm1 b1 C: I\r\n",
}

NO_NUMERALS = {
    "unfilled template": "Composer: Test\nAnalyst: \n\nTime Signature: 4/4\nm1 b1\nm2 b1\n",
    "repeat line only": "Time Signature: 4/4\nm1 b1\nm2 b1\nm3-4 = m1-2\n",
    "key only": "Time Signature: 4/4\nm1 C:\n",
    "Windows line endings": "Time Signature: 4/4\r\nm1 b1\r\nm2 b1\r\n",
}


@pytest.mark.parametrize("text", VALID.values(), ids=VALID.keys())
def test_accepts_what_music21_parses(text):
    validate_roman_text(text)

    music21.converter.parse(text, format="romantext")


@pytest.mark.parametrize("text", NO_NUMERALS.values(), ids=NO_NUMERALS.keys())
def test_rejects_what_music21_crashes_on(text):
    with pytest.raises(ValueError, match="no Roman numerals") as e:
        validate_roman_text(text)
    assert str(e.value) == NO_ROMAN_NUMERALS

    with pytest.raises(Exception):
        music21.converter.parse(text, format="romantext")


@pytest.mark.parametrize("text", ["", "hello world\n"], ids=["empty", "not RomanText"])
def test_rejects_unreadable_text(text):
    with pytest.raises(ValueError, match="could not be read"):
        validate_roman_text(text)
