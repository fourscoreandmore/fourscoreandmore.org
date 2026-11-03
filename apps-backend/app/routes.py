from flask import (
    abort,
    render_template,
    redirect,
    request,
    send_from_directory,
    session,
)
from app import app
from app.forms import *
from app import scores, TheoryExercises, exercises, romanUmpire
from app.roman_text_validator import validate_roman_text
from app.time_limit import TimeLimitExceeded, run_with_time_limit
from werkzeug.utils import safe_join
import fcntl
import hashlib
import shutil
import tempfile
import uuid
import urllib
import os
import logging


def _download_dir(filename):
    """Return the download directory containing filename, or abort with a 404."""
    for dir in (app.config["SCORE_DOWNLOAD_PATH"], app.config["CORPUS_DOWNLOAD_PATH"]):
        # safe_join returns None for paths that would escape the directory.
        path = safe_join(dir, filename)
        if path is not None and os.path.exists(path):
            return dir
    abort(404)


@app.route(app.config["SCORE_DOWNLOAD_URI_PREFIX"] + "<path:filename>")
def custom_static(filename):
    mimetype = None
    if (
        filename.endswith(".xml")
        or filename.endswith(".musicxml")
        or filename.endswith(".mxl")
    ):
        mimetype = "application/vnd.recordare.musicxml+xml"

    dir = _download_dir(filename)

    # Total hack to give a more useful download filename for WIH.
    name = os.path.basename(filename)
    if name == "score.mxl":
        name = filename.replace("/", "_")

    return send_from_directory(
        dir,
        filename,
        as_attachment=("download" in request.args),
        download_name=name,
        mimetype=mimetype,
    )


def _view_url(filename):
    """Return the URL to view a score in the browser, or "" if it isn't MusicXML."""
    if filename.endswith((".xml", ".musicxml", ".mxl")):
        return "/apps/score/" + filename
    return ""


@app.route("/apps/score/" + "<path:filename>")
def display_score(filename):
    _download_dir(filename)  # 404 unless the score exists

    url = app.config["SCORE_DOWNLOAD_URI_PREFIX"] + filename

    return render_template(
        "display-music.html", file=url, basename=os.path.basename(filename)
    )


@app.route("/apps/chorales/", methods=["GET", "POST"])
def chorales():
    form = ChoralesForm(request.form)
    form.originalScore.choices = scores.list_scores(subDir="chorales")
    download = []
    errors = []

    if form.validate_on_submit():
        filename = scores.normalizeScorePath(form.originalScore.data, subDir="chorales")
        exercise = exercises.ChoraleExercise(
            filename,
            beatsToCut=form.beatsToCut.data,
            partsToCut=form.partsToCut.data,
            shortScore=form.shortScore.data == "short",
        )
        files = []
        try:
            exercise.parse()
            files = exercise.write(
                directory=os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "chorales")
            )
        except:
            logging.error("Failed to parse file: " + filename)
            errors.append(("Failed to parse file: " + form.originalScore.data))
        for title, path in files:
            download.append(
                (
                    title,
                    path.replace(
                        app.config["SCORE_DOWNLOAD_PATH"] + "/",
                        app.config["SCORE_DOWNLOAD_URI_PREFIX"],
                    ),
                    _view_url(
                        path.replace(app.config["SCORE_DOWNLOAD_PATH"] + "/", "")
                    ),
                )
            )
    elif "partsToCut" not in request.form:
        # TODO: Find a way to set this as the default
        form.partsToCut.data = ["alto", "tenor", "bass"]

    return render_template(
        "chorales-form.html", form=form, download=download, errors=errors
    )


@app.route("/apps/lieder/", methods=["GET", "POST"])
def lieder():
    form = LiederForm(request.form)
    form.originalScore.choices = scores.list_lieder()
    download = []
    errors = []

    if form.validate_on_submit():
        lied = scores.lied_by_dir(form.originalScore.data)
        if lied is None:
            return redirect("/apps/lieder", code=302)
        filename = scores.normalizeScorePath(
            lied["relative_path"], base_path=app.config["LIEDER_CORPUS_PATH"]
        )
        exercise = exercises.LiedExercise(
            filename,
            leaveRestBars=form.preserveRestBars.data,
            leaveBassLine=form.preserveBass.data,
            quarterLengthOfRest=form.restLength.data,
            addition=(None if form.addition.data == "none" else form.addition.data),
            quarterLength=form.harmonicRhythm.data,
        )
        files = []
        try:
            exercise.parse()
            files = exercise.write(
                directory=os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "lieder")
            )
        except:
            logging.error("Failed to parse file: " + filename)
            errors.append(("Failed to parse file: " + lied["relative_path"]))
        for title, path in files:
            download.append(
                (
                    title,
                    path.replace(
                        app.config["SCORE_DOWNLOAD_PATH"] + "/",
                        app.config["SCORE_DOWNLOAD_URI_PREFIX"],
                    ),
                    _view_url(
                        path.replace(app.config["SCORE_DOWNLOAD_PATH"] + "/", "")
                    ),
                )
            )
    elif "preserveRestBars" not in request.form:
        # TODO: Find a way to set this as the default
        form.preserveRestBars.data = True

    return render_template(
        "lieder-form.html", form=form, download=download, errors=errors
    )


@app.route("/apps/working-in-harmony/", methods=["GET", "POST"])
def working_in_harmony():

    form = WorkingInHarmonyScoreSelectionForm(request.form)
    form.originalScore.choices = scores.list_lieder(
        require_files=["template.txt", "slices.tsv"]
    )

    download = []
    errors = []

    if form.validate_on_submit():
        return redirect(
            "/apps/working-in-harmony/selected/"
            + urllib.parse.quote(form.originalScore.data),
            code=302,
        )

    return render_template(
        "working-in-harmony-selection-form.html",
        form=form,
        download=download,
        errors=errors,
    )


def _wih_file(filename):
    """Return the path of a file in this session's Working in Harmony directory.

    Returns None if there is no session; aborts with a 404 if the file doesn't exist.
    """
    if session.get("wih_id", "") == "":
        return None
    abs_filename = safe_join(
        app.config["WIH_WRITABLE_PATH"], session.get("wih_id"), filename
    )
    if abs_filename is None or not os.path.isfile(abs_filename):
        abort(404)
    return abs_filename


@app.route("/apps/working-in-harmony/download/<path:filename>")
def wih_download(filename):
    abs_filename = _wih_file(filename)
    if abs_filename is None:
        return redirect("/working-in-harmony/", code=302)

    mimetype = None
    if (
        filename.endswith(".xml")
        or filename.endswith(".musicxml")
        or filename.endswith(".mxl")
    ):
        mimetype = "application/vnd.recordare.musicxml+xml"

    return send_from_directory(
        os.path.dirname(abs_filename),
        os.path.basename(abs_filename),
        as_attachment=("download" in request.args),
        download_name=filename.replace("/", "_"),
        mimetype=mimetype,
    )


@app.route("/apps/working-in-harmony/view/<path:filename>")
def wih_display_score(filename):
    if _wih_file(filename) is None:
        return redirect("/working-in-harmony/", code=302)

    return render_template(
        "display-music.html",
        file="/apps/working-in-harmony/download/" + filename,
        basename=filename.replace("/", "_"),
    )


@app.route("/apps/working-in-harmony/selected/<path:score>", methods=["GET", "POST"])
def working_in_harmony_analysis(score=""):
    if score.strip() == "":
        return redirect("/apps/working-in-harmony", code=302)

    lied = scores.lied_by_dir(score)
    if lied is None:
        return redirect("/apps/working-in-harmony", code=302)

    download = []
    errors = []
    feedback = ""

    download.append(
        (
            lied["name"],
            app.config["SCORE_DOWNLOAD_URI_PREFIX"] + lied["relative_path"],
            _view_url(lied["relative_path"]),
        )
    )

    form = WorkingInHarmonyAnalysisForm(request.form)

    # Get the template as the default.
    if "analysis" not in request.form:
        template_file = os.path.join(lied["dir"], "template.txt")
        if not os.path.exists(template_file):
            errors.append("Template file not found")
        else:
            with open(template_file) as f:
                template_contents = f.read()
            form.analysis.data = template_contents

    if form.validate_on_submit():
        relative_directory = (
            lied["relative_dir"].replace("/", "_")
            + "/"
            + hashlib.sha512(form.analysis.data.encode("utf-8")).hexdigest()[:16]
        )
        session["wih_id"] = session.get("wih_id", str(uuid.uuid4()))
        directory = os.path.join(
            app.config["WIH_WRITABLE_PATH"], session.get("wih_id"), relative_directory
        )
        errors = _run_analysis(
            _working_in_harmony_process, lied, form.analysis.data, directory
        )
        if errors == []:
            with open(os.path.join(directory, "feedback.txt"), "r") as feedback_file:
                feedback = feedback_file.read()
            result = os.path.join(relative_directory, "result.mxl")
            download.append(
                (
                    "Score with added analysis",
                    "/apps/working-in-harmony/download/" + result,
                    "/apps/working-in-harmony/view/" + result,
                )
            )

    return render_template(
        "working-in-harmony-analysis-form.html",
        song=lied["name"],
        back="/apps/working-in-harmony/",
        form=form,
        download=download,
        errors=errors,
        feedback=feedback,
    )


def _run_analysis(process, *args):
    """Run a Working in Harmony process(*args, directory) under a time limit.

    Returns its errors. The process writes to a new temporary directory, which
    is renamed to directory only if it succeeds. So directory either holds a
    finished result or doesn't exist, even if the process fails, is stopped, or
    runs at the same time as an identical submission (e.g. a double click).
    """
    *args, directory = args
    if _has_result(directory):
        return []

    parent = os.path.dirname(directory)
    os.makedirs(parent, exist_ok=True)
    work_directory = tempfile.mkdtemp(prefix=".partial-", dir=parent)
    seconds = app.config["WIH_TIME_LIMIT"]
    try:
        errors = run_with_time_limit(seconds, process, *args, work_directory)
    except TimeLimitExceeded:
        logging.warning("Working in Harmony analysis stopped after %s seconds", seconds)
        errors = [
            f"Sorry, the analysis took too long (over {seconds} seconds) and was stopped."
        ]
    except RuntimeError:
        logging.exception("Working in Harmony analysis failed")
        errors = ["Failed to analyse the score"]

    if errors == []:
        # Lock so that identical submissions can't publish at the same time.
        with open(directory + ".lock", "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            # If an identical submission finished first, use its result.
            if not _has_result(directory):
                # Files left by a failure before results were written this way.
                shutil.rmtree(directory, ignore_errors=True)
                os.rename(work_directory, directory)
    shutil.rmtree(work_directory, ignore_errors=True)
    return errors


def _has_result(directory):
    return all(
        os.path.isfile(os.path.join(directory, filename))
        for filename in ("feedback.txt", "result.mxl")
    )


def _working_in_harmony_process(lied, analysis, directory):
    errors = []

    filename = scores.normalizeScorePath(
        lied["relative_path"], base_path=app.config["LIEDER_CORPUS_PATH"]
    )

    try:
        validate_roman_text(analysis)
    except ValueError as e:
        errors.append(str(e))
        return errors

    os.makedirs(directory, exist_ok=True)
    romantext_filename = os.path.join(directory, "analysis.txt")
    with open(romantext_filename, "w") as romantext_file:
        romantext_file.write(analysis)

    try:
        analysis = romanUmpire.ScoreAndAnalysis(
            scoreOrData=filename, analysisLocation=romantext_filename
        )
    except:
        logging.exception("Failed to load analysis or score")
        errors.append("Failed to load analysis or score")
        return errors

    try:
        analysis.printFeedback(outPath=directory, outFile="feedback")
    except:
        logging.exception("Failed to write feedback file")
        errors.append("Failed to write feedback file")
        return errors

    try:
        analysis.writeScoreWithAnalysis(outPath=directory, outFile="result")
    except:
        logging.exception("Failed to write analysis to a score")
        errors.append("Failed to write analysis to a score")

    return errors
