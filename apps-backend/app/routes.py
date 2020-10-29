from flask import abort, safe_join, render_template, request, send_from_directory
from app import app
from app.forms import ChoralesForm, LiederForm
from app import scores, TheoryExercises, exercises
import os
import logging


@app.route(app.config["SCORE_DOWNLOAD_URI_PREFIX"] + '<path:filename>')
def custom_static(filename):
    mimetype = None
    if filename.endswith(".xml") or filename.endswith(".musicxml") or filename.endswith(".mxl"):
        mimetype = "application/vnd.recordare.musicxml+xml"

    return send_from_directory(
        app.config["SCORE_DOWNLOAD_PATH"],
        filename,
        as_attachment=("download" in request.args),
        mimetype=mimetype)


@app.route('/apps/score/' + '<path:filename>')
def display_score(filename):
    if not os.path.exists(
            safe_join(app.config["SCORE_DOWNLOAD_PATH"], filename)):
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
