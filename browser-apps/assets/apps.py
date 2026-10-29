"""The in-browser apps' Python, run by worker.js in Pyodide.

Each function takes the path of a score (which worker.js has fetched) and the
form's values, and returns a dict of "errors", "files" (each with a "title"
and a "path" to send back to the page) and, for Working in Harmony,
"feedback". They do what the Flask app's routes do (apps-backend/app/routes.py),
with the same app modules.
"""
import logging
import os

from app import exercises, romanUmpire
from app.roman_text_validator import validate_roman_text

OUT = "/tmp/out"


def _files(written):
    return [{"title": title, "path": path} for title, path in written]


def chorale(path, name, beats_to_cut, parts_to_cut, short_score):
    exercise = exercises.ChoraleExercise(
        path,
        beatsToCut=beats_to_cut,
        partsToCut=list(parts_to_cut),
        shortScore=short_score,
    )
    try:
        exercise.parse()
        files = exercise.write(directory=os.path.join(OUT, "chorales"))
    except Exception:
        logging.exception("Failed to parse file: " + path)
        return {"errors": ["Failed to parse file: " + name], "files": []}
    return {"errors": [], "files": _files(files)}


def lied(path, name, preserve_rest_bars, rest_length, preserve_bass, addition, harmonic_rhythm):
    exercise = exercises.LiedExercise(
        path,
        leaveRestBars=preserve_rest_bars,
        leaveBassLine=preserve_bass,
        quarterLengthOfRest=rest_length,
        addition=None if addition == "none" else addition,
        quarterLength=harmonic_rhythm,
    )
    try:
        exercise.parse()
        files = exercise.write(directory=os.path.join(OUT, "lieder"))
    except Exception:
        logging.exception("Failed to parse file: " + path)
        return {"errors": ["Failed to parse file: " + name], "files": []}
    return {"errors": [], "files": _files(files)}


def working_in_harmony(path, analysis):
    """As _working_in_harmony_process in routes.py."""
    def failed(message):
        return {"errors": [message], "files": [], "feedback": ""}

    try:
        validate_roman_text(analysis)
    except ValueError as e:
        return failed(str(e))

    directory = os.path.join(OUT, "working-in-harmony")
    os.makedirs(directory, exist_ok=True)
    romantext_filename = os.path.join(directory, "analysis.txt")
    with open(romantext_filename, "w") as romantext_file:
        romantext_file.write(analysis)

    try:
        result = romanUmpire.ScoreAndAnalysis(
            scoreOrData=path, analysisLocation=romantext_filename
        )
    except Exception:
        logging.exception("Failed to load analysis or score")
        return failed("Failed to load analysis or score")

    try:
        result.printFeedback(outPath=directory, outFile="feedback")
    except Exception:
        logging.exception("Failed to write feedback file")
        return failed("Failed to write feedback file")

    try:
        result.writeScoreWithAnalysis(outPath=directory, outFile="result")
    except Exception:
        logging.exception("Failed to write analysis to a score")
        return failed("Failed to write analysis to a score")

    with open(os.path.join(directory, "feedback.txt")) as feedback_file:
        feedback = feedback_file.read()
    files = [{"title": "Score with added analysis", "path": os.path.join(directory, "result.mxl")}]
    return {"errors": [], "files": files, "feedback": feedback}
