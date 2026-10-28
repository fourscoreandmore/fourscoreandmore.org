import pytest
from music21 import note, stream

from app.on_score_validator import (
    MAX_ERRORS,
    NO_FIRST_KEY,
    NO_LYRICS,
    NOT_A_ROMAN_NUMERAL,
    TOO_FEW_PARTS,
    find_on_score_errors,
)


def with_analysis(song, lyrics):
    """Add a lowest part to song with one note per bar, carrying lyrics."""
    part = stream.Part()
    for number, lyric in enumerate(lyrics, 1):
        measure = stream.Measure(number=number)
        n = note.Note("C3", quarterLength=4)
        if lyric:
            n.lyric = lyric
        measure.append(n)
        part.append(measure)
    song.insert(0, part)
    return song


VALID = {
    "keys and numerals": ["C: I", "IV", "V7", "I", "a: i", "V"],
    "spaces, brackets and flats as in notation software": ["C : I", "ii 6 5", "V(no5)", "-VI", "Vsus4", "I"],
    "chords on some bars only": ["C: I", None, "V", None, None, "I"],
}


@pytest.mark.parametrize("lyrics", VALID.values(), ids=VALID.keys())
def test_accepts_roman_numerals(song, lyrics):
    assert find_on_score_errors(with_analysis(song, lyrics)) == []


def test_rejects_a_score_with_one_part():
    part = stream.Part()
    part.append(note.Note())
    score = stream.Score([part])

    assert find_on_score_errors(score) == [TOO_FEW_PARTS]


def test_rejects_a_score_without_lyrics_in_the_lowest_part(song):
    """The song's voice part has lyrics, but that isn't an analysis."""
    assert find_on_score_errors(song) == [NO_LYRICS]


def test_the_first_numeral_needs_a_key(song):
    errors = find_on_score_errors(with_analysis(song, [None, "I", "V"]))

    assert errors == [NO_FIRST_KEY.format(measure=2, lyric="I")]


def test_reports_each_lyric_that_is_not_a_roman_numeral(song):
    errors = find_on_score_errors(with_analysis(song, ["C: I", "la", "V", "Q: I", "C: I:V", "I"]))

    assert errors == [
        NOT_A_ROMAN_NUMERAL.format(measure=2, lyric="la"),
        NOT_A_ROMAN_NUMERAL.format(measure=4, lyric="Q: I"),
        NOT_A_ROMAN_NUMERAL.format(measure=5, lyric="C: I:V"),
    ]


def test_a_bad_first_key_is_reported_once(song):
    errors = find_on_score_errors(with_analysis(song, ["Q: I", "V"]))

    assert errors == [NOT_A_ROMAN_NUMERAL.format(measure=1, lyric="Q: I")]


def test_limits_the_number_of_errors(song):
    errors = find_on_score_errors(with_analysis(song, ["C: I"] + ["la"] * (MAX_ERRORS + 5)))

    assert len(errors) == MAX_ERRORS + 1
    assert errors[-1] == "... and 5 more."
