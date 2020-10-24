from music21 import clef
from music21 import chord
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
        if note.expressions:  # TODO expressions.Fermata() not working
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

    NumMeasures = len(score.parts[0].getElementsByClass('Measure'))

    # Find vocal rests
    restBars = []  # Remains empty if not leaveRestBars
    if leaveRestBars:
        for listIndex in range(0, NumMeasures - 1):  # NB list is 0 to N; measures is 1 to (N-1)
            count = 0
            thisMeasure = topPart.getElementsByClass('Measure')[listIndex]  # NB Above
            for item in thisMeasure.recurse().notesAndRests:
                if item.isRest:
                    count += item.quarterLength
                    if count >= thisMeasure.quarterLength:  # Special case for anacrustic pieces.
                        restBars.append(listIndex + 1)  # = measure number
                        break  # No need to look at this measure any further
                    elif count >= quarterLengthOfRest:
                        restBars.append(listIndex + 1)  # = measure number
                        break  # No need to look at this measure any further

    measuresToDo = [x for x in range(1, NumMeasures) if x not in restBars]

    # Removals
    for measureNumber in measuresToDo:
        for partNo in parts:
            for x in score.parts[partNo].measure(measureNumber).recurse().notesAndRests:
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
        score = addChords(tempScore, quarterLength=quarterLength)

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

def transferClefs(score,
                  measuresToDo):
    """
    Adjusts clefs to accommodate the new part (transferTune or chordHints).
    Optionally also does the transferTune while it's at it:
    """  # TODO: integrate with leaveRestBars.

    startAdditions = [measuresToDo[0]]  # First in measuresToDo definitely a startAddition
    startGaps = []
    for index in range(1, len(measuresToDo)):
        oneMoreThanLastEntry = measuresToDo[index-1] + 1
        if measuresToDo[index] != oneMoreThanLastEntry:
            startGaps.append(oneMoreThanLastEntry)
            startAdditions.append(measuresToDo[index])

    if measuresToDo[-1] != len(score.parts[0]):
        finalGap = measuresToDo[-1] + 1
        startGaps.append(finalGap)

    for index in range(len(startAdditions)):  # Either
        vClefAdd = score.parts[0].measure(startAdditions[index]).getContextByClass('Clef')
        pClefAdd = score.parts[1].measure(startAdditions[index]).getContextByClass('Clef')
        # vClefGap = score.parts[0].measure(startGaps[index]).getContextByClass('Clef')
        pClefGap = score.parts[1].measure(startGaps[index]).getContextByClass('Clef')
        if vClefAdd != pClefAdd:
            AddClef = vClefAdd.sign + str(vClefAdd.line)  # TODO simplify?
            GapClef = pClefGap.sign + str(pClefGap.line)
            score.parts[1].measure(startAdditions[index]).insert(0, clef.clefFromString(AddClef))
            score.parts[1].measure(startGaps[index]).insert(0, clef.clefFromString(GapClef))

    return score


def transferTune(score, measuresToDo):
    """
    Transfers the melody line from a top part (voice) to the piano right hand.
    (Duplicates the above for running separately, without transfer clefs).
    """

    for measureNumber in measuresToDo:

        topPartCopy = deepcopy(score.parts[0])

        whereFrom = topPartCopy.measure(measureNumber)
        whereTo = score.parts[1].measure(measureNumber)

        for e in whereFrom.recurse().notesAndRests:  # m.getElementsByClass():
            whereTo.insert(e.getOffsetBySite(whereFrom), e)

    return score


def addChords(score,
              quarterLength=1):
    """
    Inputs provisional chords based on leaps in the melodic line.
    """

    # Raise exception for illegal beatStrengths
    validQuarterLengths = {4, 3, 2, 1.5, 1, 0.5, 0.25}
    if quarterLength not in validQuarterLengths:
        raise ValueError(f'Invalid quarter length: must be one of {validQuarterLengths}.')

    # Prepare dict of offsets and corresponding lists of pitches
    chordDict = {}
    vpr = score.parts[0].recurse()
    for i in range(1, len(vpr.notesAndRests)): # starting pair index = [1] and [0]
        note2 = vpr.notesAndRests[i]
        adjustedBeatPosition = floor(note2.offset / quarterLength) * quarterLength
        # i.e. floor(x * accuracy) / accuracy # signs reversed as < 1
        if adjustedBeatPosition != note2.offset:  # metrically weak enough
            if 'NotRest' in note2.classes:
                note1 = vpr.notesAndRests[i-1]
                if 'NotRest' in note1.classes:
                    if abs(interval.notesToGeneric(note1, note2).directed) > 2: # a leap
                        measureOffset = note2.activeSite.offset
                        offset = measureOffset + adjustedBeatPosition # combined unique value
                        if offset in chordDict.keys():  # Add to existing
                            tempList = [x for x in chordDict[offset][0]]
                            tempList.append(note1.pitch)
                            tempList.append(note2.pitch)
                            chordDict[offset][0] = tempList
                        else:  # Create new entry
                            chordDict[offset] = [[note1.pitch, note2.pitch],
                                                 measureOffset,
                                                 adjustedBeatPosition
                                                 ]

    # Prepare and insert chords
    for x in chordDict.keys():
        noDuplicatesChord = chord.Chord(list(set([y for y in chordDict[x][0]])))
        noDuplicatesChord.quarterLength = quarterLength
        measureOffset = round(chordDict[x][1], 2)  # NB not int
        adjustedBeatPosition = chordDict[x][2]
        finalStep = score.parts[1].getElementsByClass('Measure').getElementsByOffset(measureOffset)[0]
        finalStep.insert(adjustedBeatPosition, noDuplicatesChord)

    return score
