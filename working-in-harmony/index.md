---
layout: post
title: 'Working in Harmony'
---

What if there were a more interactive way to do harmonic analysis exercises?
And what if the work you do for class or private study could contribute to something bigger than itself?

Welcome to 'Working in Harmony' — a radical initiative which addresses these goals.
Through this course, we will simultaneously reinvigorate harmony teaching and harness the power of the classroom for wider projects through crowdsourcing datasets for machine learning.

## Instructions

Basically, your task is to:
- Choose a score (or download the one you’ve been allocated)
- Open it in a notation software editor (we recommend the free and open source [MuseScore](https://musescore.org/en/download/musescore.dmg)).
- Annotate it according to the instructions below:

## Annotation Instructions
<!-- NB: We are starting with roman numeral analysis. A broader range of tasks and instructions will follow soon. -->

- Pick the moment where the chord changes
- Click on the note in the highest voice at that point
- Click CTRL+K (Windows) CMD+K (Mac) to enter a roman numeral.
- Enter a roman numeral in the format described below:

## Format and list of keys and numerals

Very basically, you need to decide what key the passage is in (e.g. G), and what each chord is in relation to that key.
So for instance, you might start with '.G.' and then have a tonic chord 'I'.
In that case, you write ‘.G.I’.
If the next chord is still in G, say a 'V' chord, then just 'V' will do
(there's no need to specify the key unless it changes).

There are, of course, more  more For more

In summary, you enter a roman numeral (that’s required), along with the following other options (all optional) in the format:
key: root accidental, roman numeral, chord form, figure, additions.

For instance. ’a: #viio6(+5)’ indicates
- a modulation to a minor,
- a chord on the raised seventh degree (#g) …
- that is diminished (so g#, b, d) …
- in first inversion (so b in the bass)
- with an added 5th (above that bass, so F#).

Here is the full list of admissible symbols by category.

* Key symbols: {ab, a, a#, bb, b, b#, cb, c, c#, db, d, d#, eb, e, e#, fb, f, f#, gb, g, g#, Ab, A, A#, Bb, B, B#, Cb, C, C#, Db, D, D#, Eb, E, E#, Fb, F, F#, Gb, G, G#}
* Roman numerals (with possible alterations): {bi, i, #i, bii, ii, #ii, biii, iii, #iii, biv, iv, #iv, bv, v, #v, bvi, vi, #vi, bvii, vii, #vii, bI, I, #I, bII, II, #II, bIII, III, #III, bIV, IV, #IV, bV, V, #V, bVI, VI, #VI, bVII, VII, #VII, Ger, It, Fr}
* Chord forms: {M, %, o, +}
* Figured bass: {6, 64, 7, 65, 43, 2}
* Extensions and suspensions (possibly altered): {2, 4, 6, 7, 9, 11, 13}
* Special characters: {., +, /, \\}

Click [here](***) for a directory of all possible roman numerals along with the pitches they generate in major (C major) and minor (a minor) contexts.

That is, we have
- 42 key possibilities given by the 7 scale degree steps (a,b,c,d,e,f,g); X 3 accidentals (flat, natural, sharp); X 2 (minor / major).
- the same possibilities for chords, with the special addition of German, Italian, and French Augmented 6ths (= 45).
- four additional chord types: M = major seventh, % = half-diminished, o = diminished, and + = augmented.
- added notes that don’t fit in the triad, i.e. everything other than the root (1, 8), third (3, 10), and fifth (5, 12).
- special characters for dealing with how they relate to each other.

Click [here](***) (or attend your class!) for an introduction to roman numeral and analysis.

## Alternative methods

You may prefer to adopt one of the following alternative, text-based methods, particularly if there isn't an encoded, MuseScore-compatible score available for the piece you want to analyze.

1. Spreadsheet:
Write harmonic analyses directly to spreadsheet files in [this](https://github.com/DCMLab/ABC/blob/master/data/tsv/op.%2018%20No.%201/op18_no1_mov1.tsv) format, as defined and demonstrated by [EPFL's DCM lab](https://github.com/DCMLab).
This requires you to follow all of the above conventions for roman numerals, but also to specify additional information that would otherwise be extracted automatically from the score (e.g. measure and beat numbers).

2. Plain text:
Write harmonic analyses in plain text documents following the notation style as defined and demonstrated by Dmitri Tymoczko. Dmitri's write-up is [here](http://dmitri.tymoczko.com/RNguidelines.pdf) -- there's a section of the philosophy first before the technical details.
Again, the musical task and the roman numerals are exactly as above, but the there are necessarily differences of syntax.

All three methods can be fully and automatically integrated with one another so the choice is free from that perspective. On balance, I would suggest the score annotation method as it keeps both score and analysis in one place. You can also listen to the piece (or at least a computer rendered performance of it), and keep your place in the score ... which can't hurt.

## Submitting your work

If you're working in a formal class then follow your instructors' instructions for submission.
For lone wolves, please submit your files (whether annotated score, spreadsheets, or .rntxt files) via this dropbox:
