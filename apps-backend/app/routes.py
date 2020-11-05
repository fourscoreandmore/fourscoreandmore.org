from flask import abort, safe_join, render_template, redirect, request, send_from_directory
from app import app
from app.forms import *
from app import scores, TheoryExercises, exercises
import urllib
import os
import logging


@app.route(app.config["SCORE_DOWNLOAD_URI_PREFIX"] + '<path:filename>')
def custom_static(filename):
    mimetype = None
    if filename.endswith(".xml") or filename.endswith(".musicxml") or filename.endswith(".mxl"):
        mimetype = "application/vnd.recordare.musicxml+xml"

    if os.path.exists(safe_join(app.config["SCORE_DOWNLOAD_PATH"], filename)):
        dir = app.config["SCORE_DOWNLOAD_PATH"]
    elif os.path.exists(safe_join(app.config["CORPUS_DOWNLOAD_PATH"], filename)):
        dir = app.config["CORPUS_DOWNLOAD_PATH"]
    else:
        abort(404)

    # Total hack to give a more useful download filename for WIH.
    name = os.path.basename(filename)
    if name == "score.mxl":
        name = filename.replace("/", "_")

    return send_from_directory(
        dir,
        filename,
        as_attachment=("download" in request.args),
        attachment_filename=name,
        mimetype=mimetype)


@app.route('/apps/score/' + '<path:filename>')
def display_score(filename):
    if os.path.exists(safe_join(app.config["SCORE_DOWNLOAD_PATH"], filename)):
        dir = app.config["SCORE_DOWNLOAD_PATH"]
    elif os.path.exists(safe_join(app.config["CORPUS_DOWNLOAD_PATH"], filename)):
        dir = app.config["CORPUS_DOWNLOAD_PATH"]
    else:
        abort(404)

    url = app.config["SCORE_DOWNLOAD_URI_PREFIX"] + filename

    return render_template(
        "display-music.html", file=url, basename=os.path.basename(filename))


@app.route('/apps/chorales/', methods=['GET', 'POST'])
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
            shortScore=form.shortScore.data == 'short')
        try:
            exercise.parse()
        except:
            logging.error("Failed to parse file: " + filename)
            errors.append(("Failed to parse file: " + form.originalScore.data))
        files = exercise.write(
            directory=os.path.join(app.config["SCORE_DOWNLOAD_PATH"],
                                   "chorales"))
        download = []
        for title, path in files:
            download.append(
                (title,
                 path.replace(app.config["SCORE_DOWNLOAD_PATH"] + "/",
                              app.config["SCORE_DOWNLOAD_URI_PREFIX"]),
                 path.replace(app.config["SCORE_DOWNLOAD_PATH"] + "/", "")))
    elif "partsToCut" not in request.form:
        # TODO: Find a way to set this as the default
        form.partsToCut.data = ['alto', 'tenor', 'bass']

    return render_template('chorales-form.html', form=form, download=download, errors=errors)


@app.route('/apps/lieder/', methods=['GET', 'POST'])
def lieder():
    form = LiederForm(request.form)
    form.originalScore.choices = scores.list_lieder()
    download = []
    errors = []

    if form.validate_on_submit():
        filename = scores.normalizeScorePath(form.originalScore.data, base_path=app.config["LIEDER_CORPUS_PATH"])
        exercise = exercises.LiedExercise(
            filename,
            leaveRestBars=form.preserveRestBars.data,
            leaveBassLine=form.preserveBass.data,
            quarterLengthOfRest=form.restLength.data,
            addition=(None
                      if form.addition.data == "none" else form.addition.data),
            quarterLength=form.harmonicRhythm.data)
        files = []
        try:
            exercise.parse()
            files = exercise.write(
                directory=os.path.join(app.config["SCORE_DOWNLOAD_PATH"], "lieder"))
        except:
            logging.error("Failed to parse file: " + filename)
            errors.append(("Failed to parse file: " + form.originalScore.data))
        for title, path in files:
            download.append(
                (title,
                 path.replace(app.config["SCORE_DOWNLOAD_PATH"] + "/",
                              app.config["SCORE_DOWNLOAD_URI_PREFIX"]),
                 path.replace(app.config["SCORE_DOWNLOAD_PATH"] + "/", "")))
    elif "preserveRestBars" not in request.form:
        # TODO: Find a way to set this as the default
        form.preserveRestBars.data = True

    return render_template('lieder-form.html', form=form, download=download, errors=errors)


@app.route('/apps/working-in-harmony/', methods=['GET', 'POST'])
def working_in_harmony():

    form = WorkingInHarmonyScoreSelectionForm(request.form)
    form.originalScore.choices = scores.list_lieder(require_files=["template.txt", "slices.tsv"])

    download = []
    errors = []

    if form.validate_on_submit():
        return redirect('/apps/working-in-harmony/' + urllib.parse.quote(form.originalScore.data), code=302)

    return render_template('working-in-harmony-selection-form.html', form=form, download=download, errors=errors)


@app.route('/apps/working-in-harmony/<path:score>', methods=['GET', 'POST'])
def working_in_harmony_analysis(score=""):
    if score.strip() == "":
        return redirect('/apps/working-in-harmony', code=302)

    lied = scores.lied_by_path(score)
    if lied is None:
        return redirect('/apps/working-in-harmony', code=302)

    download = []
    errors = []

    filename = scores.normalizeScorePath(score, base_path=app.config["LIEDER_CORPUS_PATH"])
    path = filename
    download.append(
        (lied["name"],
            app.config["SCORE_DOWNLOAD_URI_PREFIX"] + score,
            score)
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
        errors.append("thanks but this is not implemented yet")

    return render_template(
        'working-in-harmony-analysis-form.html',
        song=lied["name"],
        back="/apps/working-in-harmony/",
        form=form,
        download=download,
        errors=errors,
    )
