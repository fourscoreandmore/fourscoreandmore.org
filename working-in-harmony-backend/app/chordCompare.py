'''
This code provides a kind of 'spell checker' for Roman numeral analysis.

It works by pairing up each Roman numeral with the
'vertical' slices that take place during the span in question
and assessing the fit.

Currently, the comparisons involve simple metrics for the:
- proportion of notes in the score matching the corresponding Roman numeral (weighed by length);
- (unusally weak) metrical positions of chord changes; and
- presence in the score of the bass note asserted by the inversion.

Feedback is available in any or all of those areas, and can be set to flag up either
- all areas that the code finds questionable, or
- only those for which it offers 'constructive' suggestions for replacement.
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

        self.startUniqueOffsetID = None
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

class Feedback:
    '''
    A feedback object for organising what advice to print.
    All types or just some?
    All cases or only where constructive suggestions are on offer?
    '''

    def __init__(self):

        self.message = None  # for all cases
        self.matchStrength = None  # for pitch comparison only
        self.suggestions = []  # where possible

# ------------------------------------------------------------------------------

class ScoreAndAnalysis:
    '''
    Class for handling
    - 'ground-truth' score data (in the form of chord and rest slices);
    - Roman numeral analysis either on that score or on a separate Roman text analysis file;
    - comparisons between the two.
    Both the score and the optional separate analysis should be pre-parsed.
    '''

    def __init__(self, score, analysisLocation='On score', minBeatStrength=0.25, tolerance=0.6):

        self.score = score
        self.analysis = analysisLocation
        self.minBeatStrength = minBeatStrength
        self.tolerance = tolerance

        self.slices = None
        self.prevSlicePitches = None

        self.comparisons = []
        self.pitchFeedback = []
        self.metricalPositionFeedback = []
        self.bassFeedback = []
        self.errorLog = []

        if self.analysis == 'On score':
            self.getAnalysis()
        else:
            self.getSeparateAnalysis()

        self.retrieveSlices()
        self.rnSliceMatchUp()


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

        self.lastBeat = 0
        self.lastMeasure = 0
        self.lastStartUniqueOffsetID = 0

        for x in chordScore.recurse():

            if ('Rest' in x.classes) or ('Chord' in x.classes):

                if not self.checkMonotonicIncrease(x):
                    continue

                thisEntry = Slice()

                thisEntry.measure = int(x.measureNumber)
                thisEntry.beat = intBeat(x.beat)
                thisEntry.beatStrength = x.beatStrength
                thisEntry.quarterLength = round(float(x.quarterLength), 2)
                thisEntry.startUniqueOffsetID = round(x.activeSite.offset + x.offset, 2)

                if 'Chord' in x.classes:
                    thisEntry.pitches = [p.nameWithOctave for p in x.pitches]
                    self.prevSlicePitches = thisEntry.pitches

                if 'Rest' in x.classes:
                    if self.prevSlicePitches:
                        thisEntry.pitches = self.prevSlicePitches
                    else:
                        thisEntry.pitches = []
                        self.errorLog.append(
                        'It looks like there\'s a Roman numeral allocated before the start of any notes.\n' +
                        'Please check and correct if so.'
                        )

                self.lastBeat = thisEntry.beat
                self.lastMeasure = thisEntry.measure
                self.lastStartUniqueOffsetID = thisEntry.startUniqueOffsetID

                self.slices.append(thisEntry)

    def checkMonotonicIncrease(self, x):
        '''
        For checking monotonically increment through the piece.
        if not monotonically increasing, log error, reject element (slice or RN).
        '''

        measure = int(x.measureNumber)
        beat = intBeat(x.beat)
        startUniqueOffsetID = round(x.activeSite.offset + x.offset, 2)

        if startUniqueOffsetID < self.lastStartUniqueOffsetID:
            self.errorLog.append(f'checkMonotonicIncrease fail on startUniqueOffsetID: {startUniqueOffsetID}.')
            return False

        if measure < self.lastMeasure:
            self.errorLog.append(f'checkMonotonicIncrease fail on measure numbers: {measure}.')
            return False

            if measure == self.lastMeasure:
                if beat < self.lastBeat:
                    self.errorLog.append(f'checkMonotonicIncrease fail on beat number (same measure): {beat}.')
                    return False

        return True

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
                thisComparison.quarterLength = round(x.quarterLength, 2)
                thisComparison.startUniqueOffsetID = round(x.activeSite.offset + x.offset, 2)

                try:
                    rn = self.romanFromLyric(x.lyric)
                    thisComparison.figure = rn.figure
                    thisComparison.key = rn.key
                    thisComparison.pitches = [p.name for p in rn.pitches]
                    thisComparison.bassPitch = rn.bass().name
                except:
                    self.errorLog.append(f'Error retrieving a Roman numeral from the lyric {x.lyric} in measure {x.measureNumber} with the prevailing key of {self.prevailingKey}.')

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

        asRoman = roman.RomanNumeral(figure,
                                    self.prevailingKey,
                                    sixthMinor=roman.Minor67Default.CAUTIONARY,
                                    seventhMinor=roman.Minor67Default.CAUTIONARY,
                                    )

        return asRoman

    def getSeparateAnalysis(self):
        '''
        Gets an analysis hosted in a separate RNTXT file.
        Straight to putative 'comparison' object.
        '''

        self.lastBeat = 0
        self.lastMeasure = 0
        self.lastStartUniqueOffsetID = 0

        scoreMeasures = len(self.score.parts[0].getElementsByClass('Measure'))
        analysisMeasures = len(self.analysis.parts[0].getElementsByClass('Measure'))
        if scoreMeasures != analysisMeasures:
            self.errorLog.append(
            f'WARNING: There are {scoreMeasures} measures in the score but {analysisMeasures} in your analysis. '+
            'This is usually a question of either the beginning or end: either\n'+
            '1) The piece reaches its final chord before the final measure (in which case fine), or\n'+
            '2) There\'s an anacrusis in the score without accompanying harmony (i.e. the analysis is missing measure 0). '+
            'In that latter case, the score and analysis will be misaligned, and the comparisons will not work properly. '+
            'Best to put in a chord of some kind for the anacrusis.\n'
            )

        for x in self.analysis.recurse().getElementsByClass('RomanNumeral'):

            if not self.checkMonotonicIncrease(x):
                continue

            thisComparison = Comparison()
            thisComparison.measure = int(x.measureNumber)
            thisComparison.beat = intBeat(x.beat)
            thisComparison.beatStrength = x.beatStrength
            thisComparison.quarterLength = round(x.quarterLength, 2)
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

        # Special case of last one.
        self.comparisons[-1].endUniqueOffsetID = 1000000  # Fake value
        self.singleMatchUp(self.comparisons[-1])

        if self.indexCount != len(self.slices):
            self.errorLog.append(f'Slices missing: {self.indexCount} accounted for of {len(self.slices)} total.')

    def singleMatchUp(self, thisComparison):
        '''
        Comparison and match up of a Roman number with slices (potentially) in that range by position in score.
        Note that harmony changes between slice changes are not supported and may lead to erratic results.
        I.e. chords should change where at least one pitch changes.
        '''

        for thisSlice in self.slices[self.indexCount:]:
            if thisComparison.startUniqueOffsetID <= thisSlice.startUniqueOffsetID < thisComparison.endUniqueOffsetID:
                thisComparison.slices.append(thisSlice)
                self.indexCount += 1
            else:
                break

# ------------------------------------------------------------------------------

# Assesments:

    def metricalPositions(self):
        '''
        Check beatStrengths and returns unlikely choices.
        '''

        for x in self.comparisons:
            if x.beatStrength < self.minBeatStrength:
                # TODO: context comparison e.g.
                # if x.beatStrength < lastBeatStrength

                fb = Feedback()
                fb.message = f'Measure {x.measure}, {x.figure} in {x.key} appears on beat {x.beat}.'
                self.metricalPositionFeedback.append(fb)

                # lastBeatStrength = x.beatStrength

    def comparePitches(self):
        '''
        Single RN-slice comparison for pitches:
        do the chords reflect the pitch content of the score section in question?
        '''

        for comp in self.comparisons:

            overall = 0

            totalLength = sum([round(sl.quarterLength, 2) for sl in comp.slices])  # Avoid division by 0

            for slice in comp.slices:
                pitchesNameNoOctave = [x[:-1] for x in slice.pitches]  # Pitch only, for the comparison only
                proportionSame = proportionSimilarity(comp.pitches, pitchesNameNoOctave)  # NB: Rest slices handled above.
                # weighedSimilarity = proportionSame * slice.beatStrength  # TODO: weight by metrical weight
                overall += slice.quarterLength * proportionSame / totalLength
                overall = round(overall, 2)

            if overall < self.tolerance:
                pl = [pList.pitches for pList in comp.slices]

                # Suggestions
                suggestions = []
                for sl in comp.slices:
                    chd = chord.Chord(sl.pitches)
                    if (chd.isTriad() or chd.isSeventh()):
                        rn = roman.romanNumeralFromChord(chd, comp.key)
                        if rn.figure != comp.figure:
                            suggestions.append([sl.measure, sl.beat, rn.figure, sl.pitches])

                fb = Feedback()
                fb.message = f'Measure {comp.measure}, beat {comp.beat}, {comp.figure} in {comp.key}, indicating the pitches {comp.pitches} accounting for successive slices of {pl}.'
                fb.matchStrength = f'Match strength estimated at {round(overall * 100, 2)}%.'
                fb.suggestions = []

                if len(suggestions) > 0:
                    for s in suggestions:
                        fb.suggestions.append(f'm{s[0]} b{s[1]} {s[2]} for the slice {s[3]}')

                self.pitchFeedback.append(fb)

    def compareBass(self):
        '''
        Single RN-slice comparison for bass / inversion.
        does at least one of the lowest notes during the span in question correspod to the chordal inversion asserted?
        '''

        for comp in self.comparisons:

            bassPitchesWithOctave = [slice.pitches[0] for slice in comp.slices]
            bassPitchesNoOctave = [p[:-1] for p in bassPitchesWithOctave]
            bassPitchesWithOctave = list(set(bassPitchesWithOctave))

            if comp.bassPitch not in bassPitchesNoOctave:

                inversionSuggestions = []

                for bassPitch in bassPitchesNoOctave:
                    if bassPitch in comp.pitches:  # already retrieved
                        suggestedPitches = comp.pitches
                        suggestedPitches.append(bassPitch+'0')  # To ensure it is lowest
                        suggestedChord = chord.Chord(suggestedPitches)
                        rn = roman.romanNumeralFromChord(suggestedChord, comp.key)
                        inversionSuggestions.append(f'm{comp.measure} b{comp.beat} {rn.figure}')

                fb = Feedback()
                fb.message = f'Measure {comp.measure}, beat {comp.beat}, {comp.figure} in {comp.key}, indicating the bass {comp.bassPitch} for lowest note(s) of: {bassPitchesWithOctave}.'
                # fb.matchStrength = N/A
                fb.suggestions = []

                if len(inversionSuggestions) > 0:
                    fb.suggestions = list(set(inversionSuggestions)) # Just once per distinct suggestion

                self.bassFeedback.append(fb)

# ------------------------------------------------------------------------------

# Feedback:

    def printFeedback(self, pitches=True, metre=True, bass=True, constructiveOnly=False):
        '''
        Select feedback to print: any or all of:
        'pitches' for pitch comparisons;
        'metre' for metrical positions; and
        'bass' for bass notes / inversions.
        '''

        allToPrint = []

        if (pitches == False) and (metre == False) and (bass == False):
            allToPrint.append('Please select at least one of pitches, metre, or bass to receive feedback on that / those aspect(s).')
            return

        allToPrint.append('Here are my thoughts. Remember, Roman numeral analysis is highly subjective, and I\'m just a bot so these are suggestions only.\n')

        if pitches == True:
            self.comparePitches()
            allToPrint.append('PITCH COVERAGE =====================\n')  # Whether there's feedback or not
            if len(self.pitchFeedback) == 0:
                allToPrint.append('The pitch coverage looks good: your choice of chords match the corresponding sections of the score well.\n')
            else:  # if len(self.pitchFeedback) > 0:
                allToPrint.append('In these cases, the chord indicated does not seem to capture everything going on:\n')
                for fb in self.pitchFeedback:
                    if len(fb.suggestions) > 0:
                        allToPrint.append(fb.message)
                        allToPrint.append(fb.matchStrength)
                        allToPrint.append('How about:')
                        [allToPrint.append(x) for x in fb.suggestions]
                        allToPrint.append('\n')
                    else:  # no suggestions
                        if constructiveOnly == False:
                            allToPrint.append(fb.message)
                            allToPrint.append(fb.matchStrength)
                            allToPrint.append('Sorry, no suggestions - I can\'t find any triads of sevenths.\n')
                        # if constructiveOnly == True, print nothing

        if metre == True:
            self.metricalPositions()
            allToPrint.append('HARMONIC RHYTHM =====================\n')
            if len(self.metricalPositionFeedback) == 0:
                allToPrint.append('The harmonic rhythm looks good: all the chord changes take place on strong metrical positions.\n')
            else:  # if len(self.metricalPositionFeedback) > 0:
                allToPrint.append('In these cases, the chord change is at an unusually weak metrical position:\n')
                [allToPrint.append(fb.message) for fb in self.metricalPositionFeedback]
                allToPrint.append('\n')

        if bass == True:
            self.compareBass()
            allToPrint.append('BASS / INVERSION =====================\n')
            if len(self.bassFeedback) == 0:
                allToPrint.append('The inversions look good: the bass notes indicated by your Roman numerals do indeed appears at least once in the lowest part during the relevant span.\n')
            else:  # len(self.bassFeedback) > 0:
                allToPrint.append('The following chords look ok, except for the bass note / inversion. (NB: pedals are not currently supported):\n')
                for fb in self.bassFeedback:
                    if len(fb.suggestions) > 0:
                        allToPrint.append(fb.message)
                        allToPrint.append('How about:')
                        [allToPrint.append(x) for x in fb.suggestions]
                        allToPrint.append('\n')
                    else:  # no suggestions
                        if constructiveOnly == False:
                            allToPrint.append(fb.message)
                            allToPrint.append(f'Sorry, no inversion suggestions - none of the bass note(s) are in the chord.\n')
                        # if constructiveOnly == True, print nothing

        if len(self.errorLog) > 0:
            allToPrint.append('WARNINGS =====================\n')
            [allToPrint.append(x) for x in self.errorLog]

        [print(x) for x in allToPrint]

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
    # NOTE: multiplication by the beat strength handled in another function.

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

        scoreFile = 'Prelude_1.mxl'
        analysisFile = 'Prelude_1.txt'
        score = converter.parse(scoreFile)
        analysis = converter.parse(analysisFile, format='romanText')
        testSeparate = ScoreAndAnalysis(score, analysisLocation=analysis)

        testSeparate.comparePitches()
        testSeparate.compareBass()
        testSeparate.metricalPositions()

        self.assertEqual(len(testSeparate.pitchFeedback), 2)
        self.assertEqual(testSeparate.pitchFeedback[0].message[:29], 'Measure 28, beat 1, viio642/v')

        self.assertEqual(len(testSeparate.bassFeedback), 2)
        self.assertEqual(testSeparate.bassFeedback[0].message[:29], 'Measure 28, beat 1, viio642/v')
        # Same measure raises both errors due to the bass.

        self.assertEqual(len(testSeparate.metricalPositionFeedback), 0)

# ------------------------------------------------------------------------------

    def testOnScoreAnalyses(self):

        file = 'Wolf_Hugo_-_Eichendorff-Lieder_Der verzweifelte Liebhaber.mxl'
        score = converter.parse(file)
        onScoreTest = ScoreAndAnalysis(score)

        onScoreTest.comparePitches()
        onScoreTest.compareBass()
        onScoreTest.metricalPositions()

        self.assertEqual(len(onScoreTest.pitchFeedback), 0)

        self.assertEqual(len(onScoreTest.bassFeedback), 1)
        self.assertEqual(onScoreTest.bassFeedback[0].message[:34], 'Measure 0, beat 2.67, i in g minor')

        self.assertEqual(len(onScoreTest.metricalPositionFeedback), 0)

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
