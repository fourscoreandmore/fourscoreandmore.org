'''
For comparisons between a Roman numeral analysis and its corresponding score.
Makes comparisons by pairing up each Roman numeral with the 'vertical' slices that take place during the span in question.
Currently, the comparisons involve simple metrics for:
- the proportion of notes in the score matching the corresponding Roman numeral (weighed by length);
- chord changes at unusally weak metrical positions;

TODO:
- penatly for notes in the RN not used?
- weighting by metrical strength to prioritise those on the beat.
- subtler metrics (set relative weights).
'''

from music21 import common
from music21 import converter
from music21 import corpus
from music21 import chord
from music21 import note
from music21 import pitch
from music21 import roman

import unittest
from copy import deepcopy

# ------------------------------------------------------------------------------

class Slice:
    '''
    A reduction object corresponding to one 'vertical' slice.
    '''

    def __init__(self):

        self.uniqueOffsetID = None
        self.pitches = []
        self.quarterLength = None
        self.measure = None
        self.beat = None
        self.beatStrength = None

# ------------------------------------------------------------------------------

class Comparison:
    '''
    A comparison between a Roman numeral and the corresponding slices for that range.
    '''

    def __init__(self):

        self.figure = None
        self.key = None
        self.bassPitch = None
        self.pitches = []

        self.startUniqueOffsetID = None

        self.slices = []

        self.endUniqueOffsetID = None

# ------------------------------------------------------------------------------

class ScoreAndAnalysis:
    '''
    Class for handling
    - 'ground-truth' score data (in the form of chord and rest slices);
    - Roman numeral analysis either on that score or on a separate Roman text analysis file;
    - comparisons between the two.
    Both the score and the optional separate analysis should be pre-parsed.
    '''

    def __init__(self, score, analysisLocation='On score'):

        self.score = score
        self.metadata = [x[1] for x in self.score.metadata.all()]  # Values

        self.comparisons = []
        self.analysis = analysisLocation
        if self.analysis == 'On score':
            self.getAnalysis()
        else:
            self.getSeparateAnalysis()

        self.prevSlicePitches = None
        self.retrieveSlices()

        self.rnSliceMatchUp()

        self.pitchFeedback = []
        self.metricalPositionFeedback = []
        self.bassFeedback = []

    def retrieveSlices(self):
        '''
        Extracts chord and rest info from scores as self.slices
        '''

        if self.analysis == 'On score':
            noAnalysisScore = deepcopy(self.score)
            noAnalysisScore.remove(noAnalysisScore.parts[-1])
            chordScore = noAnalysisScore.chordify()
        else:
            chordScore = self.score.chordify()

        self.slices = []

        for x in chordScore.recurse():

            if ('Rest' in x.classes) or ('Chord' in x.classes):

                thisEntry = Slice()

                thisEntry.measure = int(x.measureNumber)
                thisEntry.beat = intBeat(x.beat)
                thisEntry.beatStrength = x.beatStrength
                thisEntry.length = float(x.quarterLength)
                thisEntry.startUniqueOffsetID = x.activeSite.offset + x.offset

                if 'Chord' in x.classes:
                    thisEntry.pitches = [p.nameWithOctave for p in x.pitches]
                    self.prevSlicePitches = thisEntry.pitches

                if 'Rest' in x.classes:
                    if self.prevSlicePitches:
                        thisEntry.pitches = self.prevSlicePitches
                    else:
                        print('Did you put a Roman numeral at the start of the piece before any notes?')

                self.slices.append(thisEntry)

    def getAnalysis(self, type='Lyric', partNo=-1):
        '''
        Gets an analysis hosted in the main score,
        as lyrics in one part (the lowest, by default).
        Straight to putative 'comparison' object.
        '''

        self.prevailingKey = 'FAKE KEY'

        for x in self.score.parts[partNo].recurse().notes:
            if x.lyric:

                thisComparison = Comparison()

                thisComparison.measure = int(x.measureNumber)
                thisComparison.beat = intBeat(x.beat)

                thisComparison.beatStrength = x.beatStrength
                thisComparison.length = round(x.quarterLength, 2)
                thisComparison.startUniqueOffsetID = round(x.activeSite.offset + x.offset, 2)

                rn = self.romanFromLyric(x.lyric)
                thisComparison.figure = rn.figure
                thisComparison.key = rn.key
                thisComparison.pitches = [p.name for p in rn.pitches]
                thisComparison.bassPitch = rn.bass().name

                self.comparisons.append(thisComparison)


    def romanFromLyric(self, lyric):
        '''
        Converts lyrics in recognised format into m21 Roman Numeral objects.
        Format: 'Key: Figure' for first entry and all key changes; otherwise just 'Figure'.
        '''

        lyric = lyric.replace(' ', '')  # space
        lyric = lyric.replace('\xa0', '')  # non-breaking space

        if ':' in lyric:
            self.prevailingKey, figure = lyric.split(':')
        else:
            figure = lyric

        asRoman = roman.RomanNumeral(figure, self.prevailingKey)

        return asRoman

    def getSeparateAnalysis(self):
        '''
        Gets an analysis hosted in a separate RNTXT file.
        Straight to putative 'comparison' object.
        '''

        for x in self.analysis.recurse().getElementsByClass('RomanNumeral'):
            thisComparison = Comparison()
            thisComparison.measure = int(x.measureNumber)
            thisComparison.beat = intBeat(x.beat)
            thisComparison.beatStrength = x.beatStrength
            thisComparison.length = round(x.quarterLength, 2)
            thisComparison.startUniqueOffsetID = round(x.activeSite.offset + x.offset, 2)
            thisComparison.figure = x.figure
            thisComparison.key = x.key
            thisComparison.pitches = [pn.name for pn in x.pitches]
            thisComparison.bassPitch = x.bass().name
            self.comparisons.append(thisComparison)

# ------------------------------------------------------------------------------

    def rnSliceMatchUp(self):
        '''
        Compares a score-analysis pair.
        Currently using a simple metric for proportion of notes the same and of time.
        '''

        self.indexCount = 0

        for index in range(len(self.comparisons) - 1):

            self.comparisons[index].endUniqueOffsetID = self.comparisons[index + 1].startUniqueOffsetID
            self.singleMatchUp(self.comparisons[index])

        # Special case of last one. TODO: get actual end of piece and smarten this up?
        self.comparisons[-1].endUniqueOffsetID = 1000000
        self.singleMatchUp(self.comparisons[-1])

        if self.indexCount != len(self.slices):
            print(f'Slices missing: {self.indexCount} accounted for of {len(self.slices)} total.')

    def singleMatchUp(self, thisComparison):
        '''Single comparison of rn vs slices in range.'''
        # TODO case of harmony change between slice changes. Or set error to explicitly reject that possibility?

        for thisSlice in self.slices[self.indexCount:]:
            if thisComparison.startUniqueOffsetID <= thisSlice.startUniqueOffsetID < thisComparison.endUniqueOffsetID:
                thisComparison.slices.append(thisSlice)
                self.indexCount += 1
            else:
                break

# ------------------------------------------------------------------------------

# Assesments:

    def metricalPositions(self, minBeatStrength=0.25):
        '''
        Check beatStrengths and returns unlikely choices.
        '''

        for x in self.comparisons:
            if x.beatStrength < minBeatStrength:
                # TODO: context comparison e.g.
                # if x.beatStrength < lastBeatStrength
                feedback = f'Measure {x.measure}, {x.figure} in {x.key} appears on beat {x.beat}.'
                self.metricalPositionFeedback.append(feedback)
                lastBeatStrength = x.beatStrength

    def comparePitches(self, tolerance=0.75):
        '''
        Single RN-slice comparison for pitches.
        '''

        for comp in self.comparisons:

            overall = 0

            totalLength = sum([round(sl.length, 2) for sl in comp.slices])  # Avoid division by 0

            for slice in comp.slices:
                pitchesNameNoOctave = [x[:-1] for x in slice.pitches]  # Pitch only, for the comparison only
                proportionSame = proportionSimilarity(comp.pitches, pitchesNameNoOctave)  # NB: Rest slices handled above.
                # weighedSimilarity = proportionSame * slice.beatStrength  # TODO: weight by metrical weight
                overall += round(slice.length * proportionSame / totalLength, 2)

            if overall < tolerance:
                pl = [pList.pitches for pList in comp.slices]
                feedback = [f'Measure {comp.measure}, beat {comp.beat}, {comp.figure} in {comp.key}, indicating the pitches {comp.pitches} accounting for successive slices of {pl}.']

                # Suggestions
                suggestions = []
                for sl in comp.slices:
                    chd = chord.Chord(sl.pitches)
                    if (chd.isTriad() or chd.isSeventh()):
                        rn = roman.romanNumeralFromChord(chd, comp.key)
                        if rn.figure != comp.figure:
                            suggestions.append([rn.figure, sl.pitches, sl.beat])

                if len(suggestions) > 0:
                    feedback.append('How about:')
                    for s in suggestions:
                        feedback.append(f'{s[0]} for {s[1]} on beat {s[2]}')

                [self.pitchFeedback.append(x) for x in feedback]
                self.pitchFeedback.append('\n')

            else:  # overall => tolerance:
                bassPitchesWithOctave = [slice.pitches[0] for slice in comp.slices]
                bassPitchesNoOctave = [p[:-1] for p in bassPitchesWithOctave]

                if comp.bassPitch not in bassPitchesNoOctave:
                    self.bassFeedback.append(f'Measure {comp.measure}, beat {comp.beat}, {comp.figure} in {comp.key}, indicating the bass {comp.bassPitch} for successive lowest notes of: {bassPitchesWithOctave}.')

    def printFeedback(self, types='all'):

        allPossibleTypes = ['metricalPositions', 'comparePitches']

        if types == 'all':
            types = allPossibleTypes
        elif any(x not in allPossibleTypes for x in markingTypes):
            raise Exception(f'Type not supported, must be one of {types}')

        if 'metricalPositions' in types:
            self.metricalPositions()

        if 'comparePitches' in types:
            self.comparePitches()

        print('Here are some suggestions. Remember, Roman numeral analysis is highly subjective, and I\'m just a bot so these are suggestions only.\n')

        if len(self.pitchFeedback) > 0:
            print('In the following cases, the chord indicated doesn\'t seem to capture everything going on:\n')
            [print(x) for x in self.pitchFeedback]
            print('\n')

        if len(self.metricalPositionFeedback) > 0:
            print('In these cases, the chord change is at an unusually weak metrical position:\n')
            [print(x) for x in self.metricalPositionFeedback]
            print('\n')

        if len(self.bassFeedback) > 0:
            print('Finally, these chords seem fine, except the bass note (inversion):\n')
            [print(x) for x in self.bassFeedback]
            print('\n')

# ------------------------------------------------------------------------------

# Static

def proportionSimilarity(reference, query):
    '''
    Approximate measures of similarity between a
    reference (Roman numeral) and query (actual slice in score).

    Proportion of score pitches accounted for,
    multiplied by the beat strength (externally - not in this function).
    '''
    # TODO: Penatly for notes in the RN not used? Not here, only overall.
    # NOTE: multiplied by the beat strength = external (not in this function).

    intersection = [x for x in query if x in reference]  # Not distinct pitches: better score for multiple tonics, for instance
    proportion = len(intersection) / len(query)
    return proportion

def intBeat(beat):
    '''Beats as integers, or rounded decimals'''
    if int(beat) == beat:
        return int(beat)
    else:
        return round(float(beat), 2)

# ------------------------------------------------------------------------------

class Test(unittest.TestCase):
    '''
    Test two cases: on score and separate analyses.
    '''

    def testSeparateAnalysis(self):

        print('SEPARATE ANALYSIS: Bach ===========================')
        scoreFile = 'Prelude_1.mxl'
        analysisFile = 'Prelude_1.txt'
        score = converter.parse(scoreFile)
        analysis = converter.parse(analysisFile, format='romanText')
        testSeparate = ScoreAndAnalysis(score, analysisLocation=analysis)
        testSeparate.printFeedback()

        self.assertEqual(len(testSeparate.bassFeedback), 0)
        self.assertEqual(testSeparate.pitchFeedback[-2][:28], 'Measure 34, beat 1, V65 in C')


# ------------------------------------------------------------------------------

    def testOnScoreAnalyses(self):

        print('ON SCORE ANALYSIS: Wolf ===========================')
        file = 'Wolf_Hugo_-_Eichendorff-Lieder_Der verzweifelte Liebhaber.mxl'
        score = converter.parse(file)
        onScoreTest = ScoreAndAnalysis(score)
        onScoreTest.printFeedback()

        self.assertEqual(onScoreTest.bassFeedback[0], 'Measure 0, beat 2.67, i in g minor, indicating the bass G for successive lowest notes of: [\'D5\'].')
        self.assertEqual(onScoreTest.pitchFeedback[-2][:27], 'Measure 33, beat 2, V7 in G')

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
