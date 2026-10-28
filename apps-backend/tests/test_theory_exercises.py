from copy import deepcopy

import pytest
from music21 import chord, clef, corpus, expressions, layout, note, stream
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


@pytest.fixture
def chorale_with_continuo(chorale):
    score = deepcopy(chorale)
    continuo = deepcopy(score.parts[3])
    continuo.partName = "Continuo"
    score.insert(0, continuo)
    return score


def test_cadence_exercise_drops_instrumental_parts(chorale_with_continuo):
    exercise, solution = makeCadenceExercise(chorale_with_continuo)

    assert [p.partName for p in exercise.parts] == ["Soprano", "Alto", "Tenor", "Bass"]
    assert [p.partName for p in solution.parts] == ["Soprano", "Alto", "Tenor", "Bass"]


def test_cadence_exercise_keeps_instrumental_parts_in_the_original(chorale_with_continuo):
    makeCadenceExercise(chorale_with_continuo)

    assert len(chorale_with_continuo.parts) == 5


def test_cadence_exercise_ignores_ornaments_that_are_not_fermatas(chorale):
    with_trill = deepcopy(chorale)
    first_note = with_trill.parts[0].recurse().notes[0]
    assert not first_note.expressions
    first_note.expressions.append(expressions.Trill())

    exercise, _ = makeCadenceExercise(with_trill)
    expected, _ = makeCadenceExercise(chorale)

    for i in (1, 2, 3):
        assert note_offsets(exercise.parts[i]) == note_offsets(expected.parts[i])


# Lieder


def test_lieder_exercise_keeps_the_piano_where_the_voice_rests(song):
    exercise = makeLiederExercise(song)

    assert bars(exercise.parts[0]) == bars(song.parts[0])
    assert bars(exercise.parts[1]) == [["E4"], [], ["F4"], [], [], []]
    assert bars(exercise.parts[2]) == [["C3"], [], ["G2"], [], [], []]


def test_rest_length_sets_what_counts_as_resting(song):
    # Bar 3 has a two-beat rest: not enough when resting means three beats.
    exercise = makeLiederExercise(song, quarterLengthOfRest=3)

    assert bars(exercise.parts[1]) == [["E4"], [], [], [], [], []]


def test_lieder_exercise_can_remove_the_whole_piano_part(song):
    exercise = makeLiederExercise(song, leaveRestBars=False)

    assert bars(exercise.parts[1]) == [[]] * 6
    assert bars(exercise.parts[2]) == [[]] * 6


def test_lieder_exercise_can_keep_the_bass_line(song):
    exercise = makeLiederExercise(song, leaveBassLine=True)

    assert bars(exercise.parts[1]) == [["E4"], [], ["F4"], [], [], []]
    assert bars(exercise.parts[2]) == bars(song.parts[2])


def test_lieder_exercise_cuts_the_final_bar(song):
    exercise = makeLiederExercise(song, leaveRestBars=False)

    assert bars(exercise.parts[1])[-1] == []


def test_transfer_tune_copies_the_melody_into_the_right_hand(song):
    exercise = makeLiederExercise(song, addition="transferTune")

    assert bars(exercise.parts[1]) == [
        ["E4"], ["C5", "E5", "G5"], ["F4"], ["C5", "A4", "F5", "D5"], ["C5"], ["E5"],
    ]
    assert not any(n.lyric for n in exercise.parts[1].recurse().notes)


def renumber(score, numbers, suffixes=None):
    """Give each bar of every part a new measure number, and a suffix by position."""
    for part in score.parts:
        for position, (measure, number) in enumerate(zip(part.getElementsByClass("Measure"), numbers)):
            measure.number = number
            measure.numberSuffix = (suffixes or {}).get(position)
    return score


@pytest.fixture
def pickup_song(song):
    """The song with its first bar as an anacrusis: bars 0 to 5."""
    return renumber(song, range(6))


def test_lieder_exercise_handles_a_pickup_bar(pickup_song):
    exercise = makeLiederExercise(pickup_song)

    assert [m.number for m in exercise.parts[1].getElementsByClass("Measure")] == list(range(6))
    # The voice rests in bars 0 and 2.
    assert bars(exercise.parts[1]) == [["E4"], [], ["F4"], [], [], []]
    assert bars(exercise.parts[2]) == [["C3"], [], ["G2"], [], [], []]


def test_lieder_exercise_cuts_a_pickup_bar_where_the_voice_sings(pickup_song):
    exercise = makeLiederExercise(pickup_song, leaveRestBars=False)

    assert bars(exercise.parts[1]) == [[]] * 6


def test_lieder_exercise_handles_a_split_bar(song):
    # As music21 parses a bar split across a system break: 1, 2, 2X1, 3, 4, 5.
    renumber(song, [1, 2, 2, 3, 4, 5], suffixes={2: "X1"})

    exercise = makeLiederExercise(song, addition="transferTune")

    assert bars(exercise.parts[1]) == [
        ["E4"], ["C5", "E5", "G5"], ["F4"], ["C5", "A4", "F5", "D5"], ["C5"], ["E5"],
    ]
    assert bars(exercise.parts[2]) == [["C3"], [], ["G2"], [], [], []]


def test_transfer_tune_lines_up_with_a_pickup_bar(pickup_song):
    exercise = makeLiederExercise(pickup_song, addition="transferTune")

    assert bars(exercise.parts[1]) == [
        ["E4"], ["C5", "E5", "G5"], ["F4"], ["C5", "A4", "F5", "D5"], ["C5"], ["E5"],
    ]


def test_chord_hints_line_up_with_a_pickup_bar(pickup_song):
    exercise = makeLiederExercise(pickup_song, addition="chordHints", quarterLength=1)

    assert bars(exercise.parts[1]) == [["E4"], [], ["F4"], ["chord"], [], []]
    chord = exercise.parts[1].measure(3).recurse().getElementsByClass("Chord")[0]
    assert sorted(p.nameWithOctave for p in chord.pitches) == ["A4", "F5"]


@pytest.mark.parametrize("numbers", [range(1, 7), range(6)])
def test_transferred_tune_brings_the_voice_clef_up_to_the_last_bar(song, numbers):
    renumber(song, numbers)
    rh = song.parts[1].getElementsByClass("Measure")[0]
    rh.replace(rh.getElementsByClass("Clef")[0], clef.BassClef())

    exercise = makeLiederExercise(song, addition="transferTune")

    clefs = [
        [c.name for c in m.getElementsByClass("Clef")]
        for m in exercise.parts[1].getElementsByClass("Measure")
    ]
    # Treble while the right hand has the tune (bars 2, 4 to 6), bass in bar 3.
    assert clefs == [["bass"], ["treble"], ["bass"], ["treble"], [], []]


def rh_clefs(score):
    return [
        [c.name for c in m.getElementsByClass("Clef")]
        for m in score.parts[1].getElementsByClass("Measure")
    ]


def test_transferred_tune_brings_the_voice_clef_into_the_first_bar(song):
    rh = song.parts[1].getElementsByClass("Measure")[0]
    rh.replace(rh.getElementsByClass("Clef")[0], clef.BassClef())

    exercise = makeLiederExercise(song, leaveRestBars=False, addition="transferTune")

    # The clef is replaced, not joined by a second one.
    assert rh_clefs(exercise) == [["treble"], [], [], [], [], []]


def test_transferred_tune_keeps_an_octave_clef(song):
    voice = song.parts[0].getElementsByClass("Measure")[0]
    voice.replace(voice.getElementsByClass("Clef")[0], clef.Treble8vbClef())

    exercise = makeLiederExercise(song, addition="transferTune")

    (added,) = exercise.parts[1].measure(2).getElementsByClass("Clef")
    assert added.octaveChange == -1


def test_transferred_tune_keeps_a_clef_change_in_the_piano_part(song):
    # The right hand changes to the bass clef in bar 3, where the voice rests.
    rh = song.parts[1]
    rh.measure(1).replace(rh.measure(1).getElementsByClass("Clef")[0], clef.BassClef())
    rh.measure(3).insert(0, clef.BassClef())

    exercise = makeLiederExercise(song, addition="transferTune")

    assert rh_clefs(exercise) == [["bass"], ["treble"], ["bass"], ["treble"], [], []]


def test_chord_hints_follow_leaps_in_the_melody(song):
    exercise = makeLiederExercise(song, addition="chordHints", quarterLength=1)

    assert bars(exercise.parts[1]) == [["E4"], [], ["F4"], ["chord"], [], []]
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


def test_chord_hints_leave_bars_where_the_piano_is_kept(song):
    # With a two-beat harmonic rhythm, bar 3's D5-B4 (beat 4) is a weak leap,
    # but the voice rests in bar 3, so its piano part is kept as it is.
    exercise = makeLiederExercise(song, addition="chordHints", quarterLength=2)

    assert bars(exercise.parts[1]) == [["E4"], ["chord"], ["F4"], ["chord"], [], []]


def test_chord_hints_can_fill_every_bar(song):
    exercise = makeLiederExercise(song, leaveRestBars=False, addition="chordHints", quarterLength=2)

    assert bars(exercise.parts[1]) == [[], ["chord"], ["chord"], ["chord"], [], []]


def test_chord_hints_stop_at_the_barline(song):
    # An off-beat leap on beat 4 (E5-A5 at 3.5): the hint starts at 3, but has
    # only one beat of the bar left, not the full 1.5.
    bar = song.parts[0].measure(2)
    for n in list(bar.notes):
        bar.remove(n)
    for pitch, length in [("C5", 3), ("E5", 0.5), ("A5", 0.5)]:
        bar.append(note.Note(pitch, quarterLength=length))

    exercise = makeLiederExercise(song, addition="chordHints", quarterLength=1.5)

    (hint,) = exercise.parts[1].measure(2).getElementsByClass("Chord")
    assert hint.offset == 3
    assert hint.quarterLength == 1


@pytest.mark.parametrize("addition", ["transferTune", "chordHints"])
def test_additions_when_the_voice_rests_in_every_bar(song, addition):
    for bar in song.parts[0].getElementsByClass("Measure"):
        for n in list(bar.notesAndRests):
            bar.remove(n)
        bar.append(note.Rest(quarterLength=1))
        bar.append(note.Note("C5", quarterLength=3))

    exercise = makeLiederExercise(song, quarterLengthOfRest=1, addition=addition)

    assert bars(exercise.parts[1]) == bars(song.parts[1])


def with_voices(measure):
    """Move a bar's notes into a music21 Voice, as for a bar with two voices."""
    voice = stream.Voice()
    for n in list(measure.notesAndRests):
        measure.remove(n)
        voice.append(n)
    measure.insert(0, voice)


def test_transfer_tune_copies_bars_with_voices(song, tmp_path):
    with_voices(song.parts[0].measure(2))

    exercise = makeLiederExercise(song, addition="transferTune")

    rh = exercise.parts[1].measure(2)
    assert [n.nameWithOctave for n in rh.recurse().notes] == ["C5", "E5", "G5"]
    assert not any(n.lyric for n in rh.recurse().notes)
    exercise.write("musicxml", fp=str(tmp_path / "exercise.xml"))


def test_chord_hints_follow_leaps_in_bars_with_voices(song):
    with_voices(song.parts[0].measure(4))

    exercise = makeLiederExercise(song, addition="chordHints", quarterLength=1)

    assert bars(exercise.parts[1]) == [["E4"], [], ["F4"], ["chord"], [], []]


def test_chord_hints_skip_chords_in_the_vocal_line(song):
    # Two notes at once in the voice part, e.g. a divisi: A4 and C5 in bar 4.
    bar = song.parts[0].measure(4)
    bar.replace(bar.notes[1], chord.Chord(["A4", "C5"], quarterLength=0.5))

    exercise = makeLiederExercise(song, leaveRestBars=False, addition="chordHints", quarterLength=1)

    assert bars(exercise.parts[1]) == [[]] * 6


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
