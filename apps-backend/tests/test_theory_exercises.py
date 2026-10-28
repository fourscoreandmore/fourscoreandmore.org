import pytest
from music21 import corpus, layout
from music21.pitch import Pitch

from app.TheoryExercises import addChords, makeCadenceExercise, makeLiederExercise


def bars(part):
    """The pitches (or "chord") in each bar of a part, ignoring rests."""
    return [
        ["chord" if n.isChord else n.nameWithOctave for n in m.notes]
        for m in part.getElementsByClass("Measure")
    ]


# Chorales


@pytest.fixture(scope="module")
def chorale():
    return corpus.parse("bach/bwv66.6")


def fermata_offsets(score):
    soprano = score.parts[0]
    return [n.getOffsetInHierarchy(soprano) for n in soprano.recurse().notes if n.expressions]


def note_offsets(part):
    return [n.getOffsetInHierarchy(part) for n in part.recurse().notes]


def test_cadence_exercise_cuts_selected_parts_before_each_fermata(chorale):
    fermatas = fermata_offsets(chorale)
    assert fermatas  # the test is meaningless without cadences

    exercise, solution = makeCadenceExercise(chorale, numberOfBeatsToCut=2, Tenor=False, Bass=False)

    original_alto = note_offsets(chorale.parts[1])
    remaining_alto = note_offsets(exercise.parts[1])
    cut = [o for o in original_alto if o not in remaining_alto]
    assert cut
    assert all(any(f - 2 <= o <= f for f in fermatas) for o in cut)
    assert all(not any(f - 2 <= o <= f for f in fermatas) for o in remaining_alto)

    # Uncut parts are left alone.
    for i in (0, 2, 3):
        assert note_offsets(exercise.parts[i]) == note_offsets(chorale.parts[i])


def test_cadence_solution_marks_the_cut_notes_in_red(chorale):
    exercise, solution = makeCadenceExercise(chorale, numberOfBeatsToCut=2)

    for i in (1, 2, 3):
        original = chorale.parts[i].recurse().notesAndRests
        removed = len(original) - len(exercise.parts[i].recurse().notesAndRests)
        red = [n for n in solution.parts[i].recurse().notesAndRests if n.style.color == "red"]
        assert len(solution.parts[i].recurse().notesAndRests) == len(original)
        assert len(red) == removed > 0
    assert not any(n.style.color for n in solution.parts[0].recurse().notesAndRests)


def test_more_beats_cuts_more_notes(chorale):
    two, _ = makeCadenceExercise(chorale, numberOfBeatsToCut=2)
    four, _ = makeCadenceExercise(chorale, numberOfBeatsToCut=4)

    assert len(four.parts[1].recurse().notes) < len(two.parts[1].recurse().notes)


@pytest.mark.parametrize("short_score,staves", [(False, 4), (True, 2)])
def test_cadence_exercise_score_type(chorale, short_score, staves):
    exercise, solution = makeCadenceExercise(chorale, shortScore=short_score)

    assert len(exercise.parts) == len(solution.parts) == staves


def test_cadence_exercise_leaves_the_original_score_alone(chorale):
    before = [note_offsets(p) for p in chorale.parts]

    makeCadenceExercise(chorale)

    assert [note_offsets(p) for p in chorale.parts] == before


# Lieder


def test_lieder_exercise_keeps_the_piano_where_the_voice_rests(song):
    exercise = makeLiederExercise(song)

    assert bars(exercise.parts[0]) == bars(song.parts[0])
    assert bars(exercise.parts[1])[:5] == [["E4"], [], ["F4"], [], []]
    assert bars(exercise.parts[2])[:5] == [["C3"], [], ["G2"], [], []]


def test_rest_length_sets_what_counts_as_resting(song):
    # Bar 3 has a two-beat rest: not enough when resting means three beats.
    exercise = makeLiederExercise(song, quarterLengthOfRest=3)

    assert bars(exercise.parts[1])[:5] == [["E4"], [], [], [], []]


def test_lieder_exercise_can_remove_the_whole_piano_part(song):
    exercise = makeLiederExercise(song, leaveRestBars=False)

    assert bars(exercise.parts[1])[:5] == [[]] * 5
    assert bars(exercise.parts[2])[:5] == [[]] * 5


def test_lieder_exercise_can_keep_the_bass_line(song):
    exercise = makeLiederExercise(song, leaveBassLine=True)

    assert bars(exercise.parts[1])[:5] == [["E4"], [], ["F4"], [], []]
    assert bars(exercise.parts[2]) == bars(song.parts[2])


@pytest.mark.xfail(strict=True, reason="The final bar is never cut unless the score has an anacrusis")
def test_lieder_exercise_cuts_the_final_bar(song):
    exercise = makeLiederExercise(song, leaveRestBars=False)

    assert bars(exercise.parts[1])[-1] == []


def test_transfer_tune_copies_the_melody_into_the_right_hand(song):
    exercise = makeLiederExercise(song, addition="transferTune")

    assert bars(exercise.parts[1])[:5] == [
        ["E4"], ["C5", "E5", "G5"], ["F4"], ["C5", "A4", "F5", "D5"], ["C5"],
    ]
    assert not any(n.lyric for n in exercise.parts[1].recurse().notes)


def test_chord_hints_follow_leaps_in_the_melody(song):
    exercise = makeLiederExercise(song, addition="chordHints", quarterLength=1)

    assert bars(exercise.parts[1])[:5] == [["E4"], [], ["F4"], ["chord"], []]
    chord = exercise.parts[1].measure(4).recurse().getElementsByClass("Chord")[0]
    assert chord.offset == 1
    assert chord.quarterLength == 1
    assert sorted(p.nameWithOctave for p in chord.pitches) == ["A4", "F5"]


@pytest.mark.parametrize("pitch,hint", [
    ("C5", ["A4", "C5"]),  # a third is a leap
    ("B4", None),  # a step is not
])
def test_chord_hints_need_a_leap_of_at_least_a_third(song, pitch, hint):
    # Replace the off-beat F5 in bar 4 (after A4).
    song.parts[0].measure(4).notes[2].pitch = Pitch(pitch)

    exercise = makeLiederExercise(song, addition="chordHints", quarterLength=1)

    chords = exercise.parts[1].measure(4).recurse().getElementsByClass("Chord")
    if hint is None:
        assert not chords
    else:
        assert sorted(p.nameWithOctave for p in chords[0].pitches) == hint


def test_chord_hints_reject_unsupported_harmonic_rhythms(song):
    with pytest.raises(ValueError, match="Invalid quarter length"):
        addChords(song, quarterLength=0.75)


def test_lieder_exercise_rejects_unknown_additions(song):
    with pytest.raises(ValueError, match="Invalid addition type"):
        makeLiederExercise(song, addition="romanNumerals")


def test_lieder_exercise_groups_the_piano_staves(song):
    exercise = makeLiederExercise(song)

    (group,) = exercise.getElementsByClass(layout.StaffGroup)
    assert group.name == "Piano"
    assert group.symbol == "brace"
    assert list(group) == [exercise.parts[1], exercise.parts[2]]


def test_lieder_exercise_leaves_the_original_score_alone(song):
    before = [bars(p) for p in song.parts]

    makeLiederExercise(song, addition="transferTune")

    assert [bars(p) for p in song.parts] == before
