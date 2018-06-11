from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired, ValidationError
from app import app
import copy
import os
import re

def normalizeScorePath(path):
    base_path=app.config["SCORE_PATH"]
    abs=os.path.join(base_path, os.path.basename(path))

    if not os.path.isfile(abs):
        raise ValidationError("File not found: " + path)

    return abs


def validateScorePath(form, field):
    normalizeScorePath(copy.copy(field.data))


def cleanPath(path):
    return path.strip("/.")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ChoralesForm(FlaskForm):
    originalScore = StringField(
        label='Original chorale score',
        validators=[DataRequired(), validateScorePath],
        filters=[cleanPath],
        default="bwv256.mxl",
        description="The chorale score (in MusicXML format) used as a base for the exercise.",
        )

    beatsToCut = IntegerField(
        label='Beats to cut',
        default=2,
        )

    partsToCut = MultiCheckboxField(
        label="Voices to cut",
        choices=[('alto', 'Alto'), ('bass', 'Bass'), ('tenor', 'Tenor')],
        )

    shortScore = BooleanField(
        label="Short score",
        default=False
        )

    submit = SubmitField(
        label="Generate exercise"
        )


class LiederForm(FlaskForm):
    originalScore = StringField(
        label="Song",
        validators=[DataRequired(), validateScorePath],
        filters=[cleanPath],
        default="Schumann_Robert_-_Dichterliebe_Op.48_No.1_-_Im_wunderschonen_Monat_Mai.mxl",
        description="The original score (in MusicXML format) used as a base for the exercise.",
       )

    preserveRestBars = BooleanField(
        label="Preserve piano part in rests",
        default=True,
        description="Choose whether or not to leave the piano part in for the bars where the voice part is resting.",
        )

    restLength = IntegerField(
        label="Rest length",
        default=2,
        description="What does 'resting' mean? Chose a length (in 'quarter notes' / ‘crotchets') that acts as the benchmark. So, when the combined length of rests in one bar (measure) of the vocal part add up to this value, the 'Preserve piano part in rests' option will be activated (if selected).",
        )

    preserveBass = BooleanField(
        label="Preserve bass line",
        default=False,
        description="Whatever else is going on, leave the left hand piano part intact and just work on the right hand.",
        )

    addition = SelectField(
        label="Additional features",
        choices=[('transferTune', 'Transfer Tune'), ('chordHints', 'Chord Hints')],
        )

    harmonicRhythm = IntegerField(
        label="Harmonic rhythm for chord hints",
        default=1,
        )

    submit = SubmitField(
        label="Generate exercise"
        )
