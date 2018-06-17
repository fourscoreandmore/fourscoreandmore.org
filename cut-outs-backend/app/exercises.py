from app import TheoryExercises
from app.scores import getScoreName
import errno
import music21
import os
import re

def mkdir_simple(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

class ExerciseBase(object):
    def __init__(self, scoreFilename):
        self.score = music21.converter.parse(scoreFilename)
        self._exercise = None
        self._solution = None

    @property
    def score_name(self):
        return getScoreName(self.score)

    @property
    def filename_prefix(self):
        clean = re.compile(r"[^\w]+")

        return re.sub(clean, "_", self.score_name)


class ChoraleExercise(ExerciseBase):
    def __init__(
        self,
        scoreFilename,
        beatsToCut=2,
        partsToCut=["alto", "tenor", "bass"],
        shortScore=False
        ):
        self.beatsToCut = beatsToCut
        self.partsToCut = partsToCut
        self.shortScore = shortScore
        super().__init__(scoreFilename)

    @property
    def exercise(self):
        if not self._exercise:
            (self._exercise, self._solution) = self._generate()

        return self._exercise

    @property
    def solution(self):
        if not self._solution:
            (self._exercise, self._solution) = self._generate()

        return self._solution

    def _generate(self):
        return TheoryExercises.makeCadenceExercise(
            self.score,
            numberOfBeatsToCut=self.beatsToCut,
            Alto="alto" in self.partsToCut,
            Tenor="tenor" in self.partsToCut,
            Bass="bass" in self.partsToCut,
            shortScore=self.shortScore
        )

    @property
    def filename_prefix(self):
        prefix = super().filename_prefix
        prefix += "-cut" + str(self.beatsToCut)
        prefix += "-from" + "".join([p[0].upper() for p in self.partsToCut])
        if self.shortScore:
            prefix += "-short"

        return prefix

    def write(self, directory="/tmp/scores"):
        """
        Writes exercise(s) and solution(s) to files.

        Skips this process if the files already exists.

        Lazily generates the exercise and solution if necessary.

        Returns a list of tuples, containing the description and the aboslute
        file path.
        """
        mkdir_simple(directory)

        files = []
        prefix = os.path.join(directory, self.filename_prefix)

        exercise_xml_path = prefix + "-exercise.xml"
        if not os.path.exists(exercise_xml_path):
            self.exercise.write(fmt="musicxml", fp=exercise_xml_path)
        files.append( (self.score_name + ": Exercise (MusicXML file)", exercise_xml_path) )

        solution_xml_path = prefix + "-solution.xml"
        if not os.path.exists(solution_xml_path):
            self.solution.write(fmt="musicxml", fp=solution_xml_path)
        files.append( (self.score_name + ": Solution (MusicXML file)", solution_xml_path) )

        return files

class LiedExercise(ExerciseBase):
    def __init__(
        self,
        scoreFilename,
        leaveRestBars=True,
        quarterLengthOfRest=2,
        leaveBassLine=False,
        addition=None,
        quarterLength=1
        ):
        self.leaveRestBars = leaveRestBars
        self.quarterLengthOfRest = quarterLengthOfRest
        self.leaveBassLine = leaveBassLine
        self.addition = addition
        self.quarterLength = quarterLength
        super().__init__(scoreFilename)

    @property
    def exercise(self):
        if not self._exercise:
            self._exercise = self._generate()

        return self._exercise

    def _generate(self):
        return TheoryExercises.makeLiederExercise(
            self.score,
            leaveRestBars=self.leaveRestBars,
            quarterLengthOfRest=self.quarterLengthOfRest,
            leaveBassLine=self.leaveBassLine,
            addition=self.addition,
            quarterLength=self.quarterLength
        )

    @property
    def filename_prefix(self):
        prefix = super().filename_prefix
        if self.leaveRestBars:
            prefix += "-rests"
            prefix += str(self.quarterLengthOfRest)
        if self.leaveBassLine:
            prefix += "-withBass"
        if self.addition:
            prefix += "-" + str(self.addition)
            if self.addition == "chordHints":
                prefix += str(self.quarterLength)

        return prefix

    def write(self, directory="/tmp/scores"):
        mkdir_simple(directory)

        files = []
        prefix = os.path.join(directory, self.filename_prefix)

        exercise_xml_path = prefix + "-exercise.xml"
        if not os.path.exists(exercise_xml_path):
            self.exercise.write(fmt="musicxml", fp=exercise_xml_path)
        files.append( (self.score_name + ": Exercise (MusicXML file)", exercise_xml_path) )

        return files
