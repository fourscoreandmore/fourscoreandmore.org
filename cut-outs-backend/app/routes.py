from flask import send_file, render_template, redirect, request
from app import app
from app.forms import ChoralesForm, LiederForm
from app import scores, TheoryExercises
from music21 import converter
import json
import os

@app.route('/apps/')
def index():
    return redirect('/cut-outs/', code=302)


@app.route('/apps/chorales/', methods=['GET', 'POST'])
def chorales():
    form=ChoralesForm(request.form)
    form.originalScore.choices = scores.list_scores(subDir="chorales");

    if form.validate_on_submit():
        return generate_chorale_exercise(form)

    return render_template('chorales-form.html', form=form)


@app.route('/apps/lieder/', methods=['GET', 'POST'])
def lieder():
    form=LiederForm(request.form)
    form.originalScore.choices = scores.list_scores(subDir="lieder");
    if form.validate_on_submit():
        return generate_lieder_exercise(form)

    return render_template('lieder-form.html', form=form)


@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    return response


def generate_chorale_exercise(form):
    path = scores.normalizeScorePath(form.originalScore.data, subDir="chorales")

    # makeCadenceExercise returns two Music21 scores.
    (exercise, solution) = TheoryExercises.makeCadenceExercise(
        converter.parse(path),
        numberOfBeatsToCut=form.beatsToCut.data,
        Alto="alto" in form.partsToCut.data,
        Tenor="tenor" in form.partsToCut.data,
        Bass="bass" in form.partsToCut.data,
        shortScore=form.shortScore.data is "short",
        writeFile=False)

    # Construct the filename for the generated exercise.
    (name, _) = os.path.splitext(os.path.basename(path))
    name = name or "chorale"
    exercise_filename=name + "-exercise.xml"

    # Write the exercise to a temp file and "send" it to the browser as an
    # attachment.
    temp_filename=exercise.write()
    data=send_file(temp_filename, as_attachment=True, attachment_filename=exercise_filename)
    os.remove(temp_filename)

    return data


def generate_lieder_exercise(form):
    path = scores.normalizeScorePath(form.originalScore.data, subDir="lieder")

    # makeLiederExercise returns two Music21 scores.
    (exercise, solution) = TheoryExercises.makeLiederExercise(
        converter.parse(path),
        leaveRestBars=form.preserveRestBars.data,
        leaveBassLine=form.preserveBass.data,
        quarterLengthOfRest=form.restLength.data,
        addition=None if form.addition.data is "none" else form.addition.data,
        quarterLength=form.harmonicRhythm.data,
        writeFile=False)

    # Construct the filename for the generated exercise.
    (name, _) = os.path.splitext(os.path.basename(path))
    name = name or "chorale"
    exercise_filename=name + "-exercise.xml"

    # Write the exercise to a temp file and "send" it to the browser as an
    # attachment.
    temp_filename=exercise.write()
    data=send_file(temp_filename, as_attachment=True, attachment_filename=exercise_filename)
    os.remove(temp_filename)

    return data
