from flask import send_file, render_template, request
from app import app
from app.forms import ChoralesForm
from app import TheoryExercises
from music21 import converter
import os

@app.route('/apps')
def index():
    return ''


@app.route('/apps/chorales', methods=['GET', 'POST'])
def chorales():
    form=ChoralesForm(request.form)
    if form.validate_on_submit():
        return generate_exercise(form)

    return render_template('chorales-form.html', form=form)


def generate_exercise(form):
    # The originalScore should already be validated, but we also check it here.
    basename=os.path.basename(form.originalScore.data)
    path=os.path.abspath(
        os.path.join(app.config["SCORE_PATH"], basename)
        )
    if not os.path.isfile(path):
        raise ValueError("File not found: " + path)

    # makeCadenceExercise returns two Music21 scores.
    (exercise, solution) = TheoryExercises.makeCadenceExercise(
        converter.parse(path),
        numberOfBeatsToCut=form.beatsToCut.data,
        Alto="alto" in form.partsToCut.data,
        Tenor="tenor" in form.partsToCut.data,
        Bass="bass" in form.partsToCut.data,
        shortScore=form.shortScore.data,
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
