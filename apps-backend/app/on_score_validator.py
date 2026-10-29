"""Checks on analyses entered on the score, before romanUmpire reads them.

romanUmpire reads Roman numerals from lyrics in the score's last part. It
crashes with unhelpful errors (an IndexError, or a music21 exception about
"FAKE KEY") when that part has no lyrics, the first lyric has no key, or a
lyric isn't a Roman numeral. These checks find those problems and say where.
"""
from music21 import roman

TOO_FEW_PARTS = (
    "The score has only one part. Add your analysis as lyrics on a new, "
    "lowest part (e.g. press 'i' in MuseScore to add an instrument)."
)
NO_LYRICS = (
    "No analysis found: the score's lowest part has no lyrics. Add a new, "
    "lowest part and enter your Roman numerals as lyrics on its notes."
)
NO_FIRST_KEY = (
    'The first Roman numeral ("{lyric}", in measure {measure}) needs a key, '
    'e.g. "C: I" or "a: i".'
)
NOT_A_ROMAN_NUMERAL = (
    'Measure {measure}: "{lyric}" could not be read as a Roman numeral.'
)
MAX_ERRORS = 20


def normalize_lyric(lyric):
    """Make the same substitutions as romanUmpire's _romanFromLyric.

    As of the When-in-Rome commit the submodule pins. Later versions also split
    lyrics at "//" (alternative or pivot chords) and newlines: follow them here
    when the submodule is updated.
    """
    lyric = lyric.replace(" ", "").replace("\xa0", "")
    lyric = lyric.replace("-", "b")
    lyric = lyric.replace("(", "[").replace(")", "]")
    if "sus" in lyric:
        lyric = lyric.replace("sus", "[add") + "]"
    return lyric


def find_on_score_errors(score):
    """Return messages for the user about problems in an on-score analysis."""
    if len(score.parts) < 2:
        return [TOO_FEW_PARTS]

    errors = []
    key = None
    found = False
    for n in score.parts[-1].recurse().notes:
        if not n.lyric:
            continue
        found = True
        lyric = normalize_lyric(n.lyric)
        if lyric.count(":") > 1:
            errors.append(NOT_A_ROMAN_NUMERAL.format(measure=n.measureNumber, lyric=n.lyric))
            continue
        if ":" in lyric:
            new_key, figure = lyric.split(":")
        elif key is None:
            # Unless the first lyric had a key that couldn't be read.
            if not errors:
                errors.append(NO_FIRST_KEY.format(measure=n.measureNumber, lyric=n.lyric))
            break
        else:
            new_key, figure = key, lyric
        try:
            if not roman.RomanNumeral(figure, new_key).figure:
                raise ValueError(figure)
        except Exception:
            errors.append(NOT_A_ROMAN_NUMERAL.format(measure=n.measureNumber, lyric=n.lyric))
            continue
        key = new_key

    if not found:
        return [NO_LYRICS]
    if len(errors) > MAX_ERRORS:
        errors = errors[:MAX_ERRORS] + [f"... and {len(errors) - MAX_ERRORS} more."]
    return errors
