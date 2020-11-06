from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, BooleanField, RadioField, SelectField, SelectMultipleField, SubmitField, widgets, TextAreaField
from wtforms.validators import AnyOf, DataRequired, NumberRange, Length
from app import app
import os


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ChoralesForm(FlaskForm):
    originalScore = SelectField(
        label='Original chorale',
        validators=[DataRequired()],
        description="The chorale used as a base for the exercise.",
    )

    beatsToCut = IntegerField(
        label='Beats to cut',
        default=2,
        validators=[NumberRange(min=1, max=64)],
        description=
        "The number of tactus beats ('crotchet' / 'quarter note') to cut from each phrase, before the pause."
    )

    partsToCut = MultiCheckboxField(
        label="Voices to remove",
        choices=[('alto', 'Alto'), ('tenor', 'Tenor'), ('bass', 'Bass')],
        default=['alto', 'tenor', 'bass'])

    shortScore = RadioField(
        label="Score type",
        choices=[('full', 'Full score (four staves)'),
                 ('short', 'Short score (two staves)')],
        default='full',
    )

    submit = SubmitField(label="Generate exercise")


class LiederForm(FlaskForm):
    originalScore = SelectField(
        label="Original song",
        validators=[DataRequired()],
        description="The song used as a base for the exercise.",
    )

    preserveRestBars = BooleanField(
        label="Preserve piano part in rests",
        default=True,
        description=
        "Preserve the piano part in bars where the voice part is resting.",
    )

    restLength = IntegerField(
        label="Rest length",
        default=2,
        validators=[NumberRange(min=1, max=16)],
        description=
        "What does 'resting' mean? Choose a length (in 'quarter notes' / ‘crotchets') that acts as the benchmark. So, when the combined length of rests in one bar (measure) of the vocal part add up to this value, the piano part will be preserved.",
    )

    preserveBass = BooleanField(
        label="Preserve bass line",
        default=False,
        description=
        "Leave the piano part's left hand intact, and just work on the right hand.",
    )

    addition = SelectField(
        label="Additional features",
        choices=[('none', 'None'), ('transferTune', 'Transfer Tune'),
                 ('chordHints', 'Chord Hints')],
    )

    harmonicRhythm = DecimalField(
        label="Harmonic rhythm for chord hints",
        default=1,
        places=0,
        validators=[AnyOf((0.25, 0.5, 1, 1.5, 2, 3, 4))],
        description=
        "The harmonic rhythm (in 'quarter notes' / 'crotchets') of the chord hints."
    )

    submit = SubmitField(label="Generate exercise")


class WorkingInHarmonyScoreSelectionForm(FlaskForm):
    originalScore = SelectField(
        label="Original song",
        validators=[DataRequired()],
        description="The song used as a base for the exercise.",
    )

    submit = SubmitField(label="Continue")


class WorkingInHarmonyAnalysisForm(FlaskForm):
    analysis = TextAreaField(
        label="Analysis",
        description="Complete the template with your own Roman numeral analysis",
        validators=[
            Length(max=102400) # the analysis can be max 100 KB
        ]
    )

    submit = SubmitField(label="Submit analysis")
