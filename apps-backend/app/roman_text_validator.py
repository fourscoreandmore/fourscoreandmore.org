"""Checks on submitted RomanText analyses, before music21 parses them.

music21 9 crashes with an AttributeError ('NoneType' object has no attribute
'quarterLength') when translating RomanText that has no Roman numerals, such
as an unfilled Working in Harmony template.
"""
from music21.romanText import rtObjects

NO_ROMAN_NUMERALS = (
    "The analysis contains no Roman numerals. "
    "If this is the template, fill it in before analysing: "
    'add at least one Roman numeral (e.g. "m1 b1 C: I").'
)


def validate_roman_text(text):
    """Raise ValueError with a message for the user if text can't be analysed.

    Uses music21's own RomanText tokenizer, so it accepts exactly the syntax
    music21 does (e.g. "m1 I" with the beat omitted).
    """
    try:
        handler = rtObjects.RTFile().readstr(text)
    except rtObjects.RomanTextException as e:
        raise ValueError(f"The analysis could not be read: {e}") from e

    for token in handler.tokens:
        if isinstance(token, rtObjects.RTMeasure) and any(
            isinstance(atom, rtObjects.RTChord) for atom in token.atoms
        ):
            return

    raise ValueError(NO_ROMAN_NUMERALS)
