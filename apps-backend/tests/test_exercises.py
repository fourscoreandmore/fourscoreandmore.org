import os

import music21
import pytest

from app import exercises
from app.exercises import ChoraleExercise, LiedExercise


@pytest.mark.parametrize("kwargs,suffix", [
    ({}, "-cut2-fromATB"),
    ({"beatsToCut": 3, "partsToCut": ["tenor"]}, "-cut3-fromT"),
    ({"partsToCut": ["alto", "bass"], "shortScore": True}, "-cut2-fromAB-short"),
])
def test_chorale_filename_prefix(chorale_path, kwargs, suffix):
    exercise = ChoraleExercise(chorale_path, **kwargs)

    # The chorale's metadata names music21 and the file it was written to.
    assert exercise.score_name == "Music21 - bwv66.6.mxl"
    assert exercise.filename_prefix == "Music21_bwv66_6_mxl" + suffix


@pytest.mark.parametrize("kwargs,suffix", [
    ({}, "-rests2"),
    ({"leaveRestBars": False}, ""),
    ({"quarterLengthOfRest": 4, "leaveBassLine": True}, "-rests4-withBass"),
    ({"addition": "transferTune"}, "-rests2-transferTune"),
    ({"addition": "chordHints", "quarterLength": 2}, "-rests2-chordHints2"),
])
def test_lied_filename_prefix(song_path, kwargs, suffix):
    exercise = LiedExercise(song_path, **kwargs)

    assert exercise.score_name == "Tester - Test Song"
    assert exercise.filename_prefix == "Tester_Test_Song" + suffix


def test_chorale_exercise_writes_exercise_and_solution(chorale_path, tmp_path):
    files = ChoraleExercise(chorale_path).write(str(tmp_path / "out"))

    assert [title for title, _ in files] == [
        "Music21 - bwv66.6.mxl: Exercise (MusicXML file)",
        "Music21 - bwv66.6.mxl: Solution (MusicXML file)",
    ]
    exercise_path, solution_path = (path for _, path in files)
    assert exercise_path.endswith("-cut2-fromATB-exercise.xml")
    assert solution_path.endswith("-cut2-fromATB-solution.xml")
    exercise = music21.converter.parse(exercise_path)
    solution = music21.converter.parse(solution_path)
    assert len(exercise.parts[1].recurse().notes) < len(solution.parts[1].recurse().notes)


def test_lied_exercise_writes_exercise(song_path, tmp_path):
    files = LiedExercise(song_path, addition="transferTune").write(str(tmp_path / "out"))

    ((title, path),) = files
    assert title == "Tester - Test Song: Exercise (MusicXML file)"
    assert path == str(tmp_path / "out" / "Tester_Test_Song-rests2-transferTune-exercise.xml")
    exercise = music21.converter.parse(path)
    assert [n.nameWithOctave for n in exercise.parts[1].measure(2).notes] == ["C5", "E5", "G5"]


def test_saved_files_are_reused_until_the_code_changes(song_path, tmp_path):
    ((_, path),) = LiedExercise(song_path).write(str(tmp_path))
    with open(path, "w") as f:
        f.write("saved")

    LiedExercise(song_path).write(str(tmp_path))
    with open(path) as f:
        assert f.read() == "saved"

    # Files older than exercises.py were made by an older version of the code.
    old = os.path.getmtime(exercises.__file__) - 60
    os.utime(path, (old, old))
    LiedExercise(song_path).write(str(tmp_path))
    with open(path) as f:
        assert f.read() != "saved"


def test_saved_files_are_remade_when_the_exercise_generators_change(song_path, tmp_path, monkeypatch):
    ((_, path),) = LiedExercise(song_path).write(str(tmp_path))
    with open(path, "w") as f:
        f.write("saved")

    # TheoryExercises.py changes after the file was saved.
    generators = tmp_path / "TheoryExercises.py"
    generators.touch()
    newer = os.path.getmtime(path) + 60
    os.utime(generators, (newer, newer))
    monkeypatch.setattr(exercises.TheoryExercises, "__file__", str(generators))

    LiedExercise(song_path).write(str(tmp_path))
    with open(path) as f:
        assert f.read() != "saved"


def test_write_musicxml_replaces_the_file_in_one_step(tmp_path):
    path = tmp_path / "exercise.xml"
    path.write_text("old")

    exercises.write_musicxml(music21.stream.Score([music21.stream.Part([music21.note.Note()])]), str(path))

    assert path.read_text().startswith("<?xml")
    assert os.listdir(tmp_path) == ["exercise.xml"]


def test_write_musicxml_leaves_the_old_file_if_writing_fails(tmp_path):
    path = tmp_path / "exercise.xml"
    path.write_text("old")

    class Broken:
        def write(self, fmt, fp):
            with open(fp, "w") as f:
                f.write("<?xml half")
            raise RuntimeError("music21 failed")

    with pytest.raises(RuntimeError):
        exercises.write_musicxml(Broken(), str(path))

    assert path.read_text() == "old"
    assert os.listdir(tmp_path) == ["exercise.xml"]
