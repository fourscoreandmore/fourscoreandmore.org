from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired, ValidationError
from app import app
import os
import re


def cleanPath(path):
    return path.strip("/.")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ChoralesForm(FlaskForm):

    csrf_enabled = False
    originalScore = StringField(
        label='Original chorale score',
        validators=[DataRequired()],
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


    def validate_originalScore(form, field):
        base_path=app.config["SCORE_PATH"]
        path=os.path.abspath(base_path + "/" + field.data)

        if not os.path.exists(path):
            raise ValidationError("File not found: " + field.data)