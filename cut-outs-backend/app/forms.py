from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, RadioField, SelectField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired, ValidationError, NumberRange
from app import app
import copy
import os
import re

def normalizeScorePath(path, subDir=""):
    base_path=app.config["SCORE_PATH"]
    prefixed=os.path.join(subDir, cleanPath(path))
    abs=os.path.join(base_path, prefixed)

    if not os.path.isfile(abs):
        raise ValidationError("File not found: " + prefixed)

    return abs


def validateLiedPath(form, field):
    normalizeScorePath(copy.copy(field.data), subDir="lieder")


def validateChoralePath(form, field):
    normalizeScorePath(copy.copy(field.data), subDir="chorales")


def cleanPath(path):
    return path.strip("/.")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ChoralesForm(FlaskForm):
    originalScore = StringField(
        label='Original chorale score',
        validators=[DataRequired(), validateChoralePath],
        filters=[cleanPath],
        default="BWV 369.xml",
        description="The chorale score (in MusicXML format) used as a base for the exercise.",
        )

    beatsToCut = IntegerField(
        label='Beats to cut',
        default=2,
        validators=[NumberRange(min=1, max=16)],
        description="Decide on a number of tactus beats ('crotchet' / 'quarter note') to cut from each phrase."
        )

    partsToCut = MultiCheckboxField(
        label="Voices to cut",
        choices=[('alto', 'Alto'), ('bass', 'Bass'), ('tenor', 'Tenor')],
        description="Choose which voices to remove."
        )

    shortScore = RadioField(
        label="Score type",
        choices=[('full', 'Full score (four staves)'), ('short', 'Short score (two staves)')],
        default='full',
        )

    submit = SubmitField(
        label="Generate exercise"
        )


class LiederForm(FlaskForm):
    originalScore = StringField(
        label="Song",
        validators=[DataRequired(), validateLiedPath],
        filters=[cleanPath],
        default="Hensel_Fanny_Mendelssohn_-_5_Lieder_Op.10_No.5_-_Bergeslust.mxl",
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
        validators=[NumberRange(min=1, max=16)],
        description="What does 'resting' mean? Choose a length (in 'quarter notes' / ‘crotchets') that acts as the benchmark. So, when the combined length of rests in one bar (measure) of the vocal part add up to this value, the 'Preserve piano part in rests' option will be activated (if selected).",
        )

    preserveBass = BooleanField(
        label="Preserve bass line",
        default=False,
        description="Whatever else is going on, leave the left hand piano part intact and just work on the right hand.",
        )

    addition = SelectField(
        label="Additional features",
        choices=[('none', 'None'), ('transferTune', 'Transfer Tune'), ('chordHints', 'Chord Hints')],
        )

    harmonicRhythm = IntegerField(
        label="Harmonic rhythm for chord hints",
        default=1,
        validators=[NumberRange(min=1, max=16)],
        description="If you chose the Chord Hints feature, what harmonic rhythm should these be based on? Please specify the length in 'quarter notes' ('crotchets') of that harmonic rhythm."
        )

    submit = SubmitField(
        label="Generate exercise"
        )
