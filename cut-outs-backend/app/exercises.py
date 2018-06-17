from app import TheoryExercises
import errno
import music21
import os
import re

class ExerciseBase(object):
    def __init__(self, scoreFilename):
        self.scoreFilename = scoreFilename
        self._exercise = None
        self._solution = None

    def _generate(self):
        return TheoryExercises.makeCadenceExercise(
            thisScore=music21.converter.parse(self.scoreFilename)
        )

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

    @property
    def filename_prefix(self):
        clean = re.compile(r"\W")

        return re.sub(clean, "_", os.path.basename(self.scoreFilename))

    def write(self, directory="/tmp/scores", skipIfExists=True):
        """
        Writes exercise(s) and solution(s) to files.

        Skips this process if the files already exists.

        Lazily generates the exercise and solution if necessary.

        Returns a list of tuples, containing the description and the aboslute
        file path.
        """

        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        files = []
        prefix = os.path.join(directory, self.filename_prefix)

        exercise_xml_path = prefix + "-exercise.xml"
        if not os.path.exists(exercise_xml_path):
            self.exercise.write(fmt="musicxml", fp=prefix + "-exercise.xml")
        files.append( ("Exercise (MusicXML)", exercise_xml_path) )

        solution_xml_path = prefix + "-solution.xml"
        if not os.path.exists(solution_xml_path):
            self.solution.write(fmt="musicxml", fp=prefix + "-solution.xml")
        files.append( ("Solution (MusicXML)", solution_xml_path) )

        return files


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

    def _generate(self):
        return TheoryExercises.makeCadenceExercise(
            music21.converter.parse(self.scoreFilename),
            numberOfBeatsToCut=self.beatsToCut,
            Alto="alto" in self.partsToCut,
            Tenor="tenor" in self.partsToCut,
            Bass="bass" in self.partsToCut,
            shortScore=self.shortScore
        )

    @property
    def filename_prefix(self):
        prefix = super().filename_prefix
        prefix += "-b" + str(self.beatsToCut)
        prefix += "-p" + "".join([p[0].lower() for p in self.partsToCut])
        if self.shortScore:
            prefix += "-s"

        return prefix


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

    def _generate(self):
        return TheoryExercises.makeLiederExercise(
            music21.converter.parse(self.scoreFilename),
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
            prefix += "-r"
        prefix += "-rl" + str(self.quarterLengthOfRest)
        if self.leaveBassLine:
            prefix += "-b"
        if self.addition:
            prefix += "-" + str(self.addition)
        if self.quarterLength:
            prefix += "-hr" + str(self.quarterLength)

        return prefix
