from music21 import clef
from music21 import chord
from music21 import expressions
from music21 import interval
from music21 import layout

from copy import deepcopy
from math import floor


# -------------------------------------------------------------------------------

# CHORALES

def makeCadenceExercise(score,
                        numberOfBeatsToCut: int = 2,
                        Alto: bool = True,
                        Tenor: bool = True,
                        Bass: bool = True,
                        shortScore: bool = False,
                        writeFile: bool = False,
                        outPath='~/Desktop/',
                        title=''):
    """
    Creates cadence exercises by cutting parts out of a chorale at each fermata cadence.
    User chooses:
    number of beats to cut,
    which parts to cut (A, T, B, or a combination), and
    full- or short- score presentation.
    """

    score = deepcopy(score)  # Leave the original alone: parts are removed from it

    # Cut non-SATB parts
    # Possible TODO: return these instrumental parts at the end? (if not shortScore)
    legalList = ['Soprano', 'Alto', 'Tenor', 'Bass']
    if len(score.parts) > 4:
        for i in range(len(score.parts))[::-1]:
            if score.parts[i].partName not in legalList:
                score.remove(score.parts[i])

    # Identify fermataPositions
    fermataPositions = []
    sopNotes = score.parts[0].recurse().notes  # NB leave ties in for tied-to fermata.
    for note in sopNotes:
        if any(isinstance(e, expressions.Fermata) for e in note.expressions):
            uniqueOffsetID = note.getOffsetInHierarchy(score.parts[0])
            fermataPositions.append(uniqueOffsetID)

    # Which to cut
    partsRefs = []
    if Alto:
        partsRefs.append(1)
    if Tenor:
        partsRefs.append(2)
    if Bass:
        partsRefs.append(3)

    # Separate ex and soln
    exercise = deepcopy(score)
    solution = deepcopy(score)

    # Exercise
    for i in partsRefs:
        exPart = exercise.parts[i]
        for noteOrRest in exPart.recurse().notesAndRests:
            noteOrRest.stemDirection = 'unspecified'
            uniqueOffsetID = noteOrRest.getOffsetInHierarchy(exPart)
            for position in fermataPositions:
                if (position-numberOfBeatsToCut) <= uniqueOffsetID <= position:
                    exPart.remove(noteOrRest, recurse=True)

        # Solution (same i references)
        solnPart = solution.parts[i]
        for noteOrRest in solnPart.recurse().notesAndRests:
            noteOrRest.stemDirection = 'unspecified'
            uniqueOffsetID = noteOrRest.getOffsetInHierarchy(solnPart)
            for position in fermataPositions:
                if (position-numberOfBeatsToCut) <= uniqueOffsetID <= position:
                    noteOrRest.style.color = 'red'  # NB Style

    if not title:
        title = score.metadata.title

    # Full or Short Score + writes and returns. Heavy-handed approach to clef.
    firstMeasure = exercise.parts[0].getElementsByClass('Measure')[0].measureNumber
    if shortScore:
        shortEx = exercise.implode()
        shortSoln = solution.implode()
        shortEx.parts[1].measure(firstMeasure).clef = clef.BassClef()
        shortSoln.parts[1].measure(firstMeasure).clef = clef.BassClef()
        if writeFile:
            shortEx.write('mxl', fp=f'{outPath}Exercise-{title}.mxl')
            shortSoln.write('mxl', fp=f'{outPath}Solution-{title}.mxl')
        return shortEx, shortSoln
    else:
        exercise.parts[2].measure(firstMeasure).clef = clef.Treble8vbClef()
        solution.parts[2].measure(firstMeasure).clef = clef.Treble8vbClef()
        if writeFile:
            exercise.write('mxl', fp=f'{outPath}Exercise-{title}.mxl')
            solution.write('mxl', fp=f'{outPath}Solution-{title}.mxl')
        return exercise, solution

    # TODO: write to PDF option, when operational in music21


# -------------------------------------------------------------------------------

# LIEDER

def makeLiederExercise(score,
                       leaveRestBars: bool = True,
                       quarterLengthOfRest=2,
                       leaveBassLine: bool = False,
                       addition=None,  # Options: 'transferTune' and 'chordHints'
                       quarterLength=1,
                       writeFile: bool = False,
                       outPath: str = '~/Desktop/',
                       title: str = ''):
    """
    Removes the piano part of an input song to create an exercise.

    Optionally leaves in:
    1. the piano part for bars with a vocal part rest of a specified, minimum length;
    2. the bass line (piano LH);

    Optionally then adds one of the following to the piano RH as a draft solution:
    A. the vocal melody (notes and rests);
    B. new chords based on leaps in the vocal line
    within the harmonic rhythm (rate) specified by quarterLength variable.
    """

    score = deepcopy(score)

    # Bassline line Y / N. i.e. Select both piano parts, or just RH.
    parts = [1]  # For cutting out RH (partNumber[1])
    if not leaveBassLine:
        parts.append(2)  # For also cutting out LH

    topPart = score.parts[0]

    # Work by position in the list of measures, not by measure number: numbers
    # start at 0 in songs with an anacrusis, and split measures repeat a number.
    voiceMeasures = list(topPart.getElementsByClass('Measure'))
    NumMeasures = len(voiceMeasures)

    # Find vocal rests
    restBars = []  # Positions. Remains empty if not leaveRestBars
    if leaveRestBars:
        for listIndex, thisMeasure in enumerate(voiceMeasures):
            count = 0
            for item in thisMeasure.recurse().notesAndRests:
                if item.isRest:
                    count += item.quarterLength
                    if count >= thisMeasure.quarterLength:  # Special case for anacrustic pieces.
                        restBars.append(listIndex)
                        break  # No need to look at this measure any further
                    elif count >= quarterLengthOfRest:
                        restBars.append(listIndex)
                        break  # No need to look at this measure any further

    measuresToDo = [x for x in range(NumMeasures) if x not in restBars]  # Positions

    # Removals
    for partNo in parts:
        pianoMeasures = list(score.parts[partNo].getElementsByClass('Measure'))
        for listIndex in measuresToDo:
            for x in list(pianoMeasures[listIndex].recurse().notesAndRests):
                score.parts[partNo].remove(x, recurse=True)

    # Additions
    validAdditions = [None, 'transferTune', 'chordHints']
    if addition not in validAdditions:
        raise ValueError(f'Invalid addition type: must be one of {validAdditions}.')
    elif addition == 'transferTune':
        tempScore = transferClefs(score, measuresToDo)
        score = transferTune(tempScore, measuresToDo)
    elif addition == 'chordHints':
        tempScore = transferClefs(score, measuresToDo)
        score = addChords(tempScore, quarterLength=quarterLength, measuresToDo=measuresToDo)

    # Scrub lyrics inherited into piano part
    for item in score.parts[1].recurse().notesAndRests:
        if item.lyric:
            item.lyric = None

    if not title:
        title = score.metadata.title

    staffGrouping = layout.StaffGroup([score.parts[1], score.parts[2]],
                                      name='Piano',
                                      abbreviation='Pno.',
                                      symbol='brace')
    staffGrouping.barTogether = 'Mensurstrich'
    score.insert(0, staffGrouping)

    if writeFile:
        score.write('mxl', fp=f'{outPath}Exercise-{title}.mxl')

    return score


# -------------------------------------------------------------------------------

# LIEDER continued: Additions into the score

def clefAt(measure):
    """
    The clef in force at the start of a measure: its own, else the one before it.
    """
    return measure.clef or measure.getContextByClass('Clef')


def transferClefs(score,
                  measuresToDo):
    """
    Adjusts clefs to accommodate the new part (transferTune or chordHints).
    Optionally also does the transferTune while it's at it:
    """  # TODO: integrate with leaveRestBars.

    if not measuresToDo:  # Nothing added
        return score

    voiceMeasures = list(score.parts[0].getElementsByClass('Measure'))
    pianoMeasures = list(score.parts[1].getElementsByClass('Measure'))

    startAdditions = [measuresToDo[0]]  # First in measuresToDo definitely a startAddition
    startGaps = []
    for index in range(1, len(measuresToDo)):
        oneMoreThanLastEntry = measuresToDo[index-1] + 1
        if measuresToDo[index] != oneMoreThanLastEntry:
            startGaps.append(oneMoreThanLastEntry)
            startAdditions.append(measuresToDo[index])

    if measuresToDo[-1] != len(voiceMeasures) - 1:  # No final gap if additions run to the end
        finalGap = measuresToDo[-1] + 1
        startGaps.append(finalGap)

    for index in range(len(startAdditions)):  # Either
        vClefAdd = clefAt(voiceMeasures[startAdditions[index]])
        pClefAdd = clefAt(pianoMeasures[startAdditions[index]])
        if vClefAdd is not None and vClefAdd != pClefAdd:
            if index < len(startGaps):
                gapMeasure = pianoMeasures[startGaps[index]]
                pClefGap = clefAt(gapMeasure)
                if gapMeasure.clef is None and pClefGap is not None:  # Else it has its own
                    gapMeasure.insert(0, deepcopy(pClefGap))
            pianoMeasures[startAdditions[index]].clef = deepcopy(vClefAdd)  # Replaces any there

    return score


def transferTune(score, measuresToDo):
    """
    Transfers the melody line from a top part (voice) to the piano right hand.
    (Duplicates the above for running separately, without transfer clefs).
    """

    topPartCopy = deepcopy(score.parts[0])
    voiceMeasures = list(topPartCopy.getElementsByClass('Measure'))
    pianoMeasures = list(score.parts[1].getElementsByClass('Measure'))

    for listIndex in measuresToDo:  # Positions, not measure numbers

        whereFrom = voiceMeasures[listIndex]
        whereTo = pianoMeasures[listIndex]

        # Notes, and voices (with their notes) in bars with more than one.
        for e in list(whereFrom.notesAndRests) + list(whereFrom.voices):
            whereTo.insert(e.getOffsetBySite(whereFrom), e)

    return score


def addChords(score,
              quarterLength=1,
              measuresToDo=None):
    """
    Inputs provisional chords based on leaps in the melodic line,
    in the measures at the positions in measuresToDo (default: all).
    """

    # Raise exception for illegal beatStrengths
    validQuarterLengths = {4, 3, 2, 1.5, 1, 0.5, 0.25}
    if quarterLength not in validQuarterLengths:
        raise ValueError(f'Invalid quarter length: must be one of {validQuarterLengths}.')

    # Work by position in the list of measures, as makeLiederExercise does.
    voiceMeasures = list(score.parts[0].getElementsByClass('Measure'))
    pianoMeasures = list(score.parts[1].getElementsByClass('Measure'))
    if measuresToDo is None:
        measuresToDo = range(len(voiceMeasures))
    positions = {id(m): listIndex for listIndex, m in enumerate(voiceMeasures)}

    # Prepare dict of (measure position, beat) and corresponding lists of pitches
    chordDict = {}
    vpr = score.parts[0].recurse()
    for i in range(1, len(vpr.notesAndRests)): # starting pair index = [1] and [0]
        note2 = vpr.notesAndRests[i]
        measure = note2.getContextByClass('Measure')  # Not activeSite, which may be a Voice
        offset = note2.getOffsetInHierarchy(measure)
        adjustedBeatPosition = floor(offset / quarterLength) * quarterLength
        # i.e. floor(x * accuracy) / accuracy # signs reversed as < 1
        if adjustedBeatPosition != offset:  # metrically weak enough
            if 'Note' in note2.classes:  # Not a rest, nor a chord (e.g. divisi)
                note1 = vpr.notesAndRests[i-1]
                if 'Note' in note1.classes:
                    if abs(interval.notesToGeneric(note1, note2).directed) > 2: # a leap
                        listIndex = positions.get(id(measure))
                        if listIndex in measuresToDo:  # Not where the piano part is kept
                            key = (listIndex, adjustedBeatPosition)
                            chordDict.setdefault(key, []).extend([note1.pitch, note2.pitch])

    # Prepare and insert chords
    for (listIndex, adjustedBeatPosition), pitches in chordDict.items():
        noDuplicatesChord = chord.Chord(list(set(pitches)))
        restOfBar = voiceMeasures[listIndex].quarterLength - adjustedBeatPosition
        noDuplicatesChord.quarterLength = min(quarterLength, restOfBar)  # Not past the barline
        pianoMeasures[listIndex].insert(adjustedBeatPosition, noDuplicatesChord)

    return score
