---
layout: post
title: 'Working in Harmony'
---

What if there were a more interactive way to do harmonic analysis exercises in music notation software that would enable you to listen to the music you are working on?
And what if the exercises you produce while learning could also contribute to projects that would benefit the wider musical community?

'Working in Harmony' sets out a method for realising those goals by bringing together disparate existing resources to create something amazing together. Basically, the idea is to do harmonic analysis directly on scores in music notation packages in a way that will make the pedagogical task more musical than is often the case, and will simultaneously allow harvesting of that those analyses as raw data to unlock the awesome power of machine learning.

NB: This page focusses on instructions for analysts; (let us know if you want to hear more about the motivation and methods for machine learning and the exciting possibilities that opens up!). We assume a basic working knowledge of harmony in general and roman numerals in particular. If there's anyone out there working on this alone, without guidance, and without that prior knowledge then let us know and we'll provide a brief introduction, or links to recommended resources.

## Basic Instructions

Basically, your task is to:
- Choose a score (or download the one you’ve been allocated)
- Open it in a notation software editor (we recommend the free and open source [MuseScore](https://musescore.org/en/download/musescore.dmg)).
- Annotate it according to the instructions in the next section.

## Annotation Instructions

- Decide where each chord change occurs;
- Click on the note in the highest voice at that point (you may need to break up a note or rest into shorter values to add the harmony at the right point);
- Click CTRL+K (Windows) CMD+K (Mac) to start entering a roman numeral.
- Enter a roman numeral in the format described in the next section.

NB: For more on the delicate, interpretative art of harmonic analysis, you might like to have a look at the first, 'philosophy' section of Dmitri Tymoczko's guidelines [here](http://dmitri.tymoczko.com/RNguidelines.pdf).

## Format and list of keys and numerals

- New chord: For each new chord, specify the roman numeral in relation to the prevailing key, for instance 'I' for the tonic.
- New key: For the start of a new key area (including, necessarily, the start of the piece), specify that key with dots on either side, combined with the roman numeral (e.g. '.G.I' for a move to G major and a tonic chord in that key). For a continuation of the prevailing key, there's no need to specify the key: just write in the roman numeral alone ('I').
- Chord quality: don't forget to use upper case for Major (e.g. 'I'), lower case for minor ('i'), and add the symbols for a diminished triad ('o') or augmented triad ('+') as necessary.
- Finally, specify any added notes not in the specified triad with '(+4)', for example (note the parentheses within the figure here to distinguish from augmented).

In summary, enter a roman numeral (that’s required), along with the following any or all of the other annotations (all optional) in the format: '.key.', 'root accidental', 'roman numeral', 'chord form', 'figure', 'additions'.

For instance, the entry ’.a.#viio6(+4)’ indicates:
- a modulation to a minor and
- a chord on the raised seventh degree (#g) …
- that is diminished (so g#, b, d) …
- in first inversion (so with b in the bass, below the g# and d) …
- and with an added 4th (above that bass, so the pitch E).

See [this folder](https://github.com/DCMLab/ABC/blob/master/data/mscx/) for examples scores as produced by [EPFL's DCM lab](https://github.com/DCMLab) in this format.

## Nerdery

For the budding music theorists among you, here is the full list of admissible symbols by category.

* Key symbols: {ab, a, a#, bb, b, b#, cb, c, c#, db, d, d#, eb, e, e#, fb, f, f#, gb, g, g#, Ab, A, A#, Bb, B, B#, Cb, C, C#, Db, D, D#, Eb, E, E#, Fb, F, F#, Gb, G, G#}
* Roman numerals (with possible alterations): {bi, i, #i, bii, ii, #ii, biii, iii, #iii, biv, iv, #iv, bv, v, #v, bvi, vi, #vi, bvii, vii, #vii, bI, I, #I, bII, II, #II, bIII, III, #III, bIV, IV, #IV, bV, V, #V, bVI, VI, #VI, bVII, VII, #VII, Ger, It, Fr}
* Chord forms: {M, %, o, +}
* Figured bass: {6, 64, 7, 65, 43, 2}
* Extensions and suspensions (which can be altered): {2, 4, 6, 7, 9, 11, 13}
* Special characters: {., +, /, \\}

That is, we have
- 42 key possibilities given by the 7 scale degree steps (a,b,c,d,e,f,g); X 3 accidentals (flat, natural, sharp); X 2 (minor / major).
- the same possibilities for chords, with the special addition of German, Italian, and French Augmented 6ths (= 45).
- four additional chord types: M = major seventh, % = half-diminished, o = diminished, and + = augmented.
- added notes that don’t fit in the triad, i.e. everything other than the root (1, 8), third (3, 10), and fifth (5, 12).
- special characters for dealing with how they relate to each other.

For the really insatiable, hardcore music theorists, [click here](https://github.com/MarkGotham/When-in-Rome/tree/master/Lists) for a directory of all possible roman numerals along with the pitches they generate in major (C major) and minor (a minor) contexts as interpreted by music21's automated functions.

## Alternative methods

You may prefer to adopt one of the following alternative, text-based methods, particularly if there isn't an encoded, MuseScore-compatible score available for the piece you want to analyze.

1. Spreadsheet:
Write harmonic analyses directly to spreadsheet files in the same format defined and demonstrated by [EPFL's DCM lab](https://github.com/DCMLab), as exemplified by  [these files](https://github.com/DCMLab/ABC/blob/master/data/tsv/).
This requires you to follow all of the above conventions for roman numerals, but also to specify additional information that would otherwise be extracted automatically from the score (e.g. measure and beat numbers).

2. Plain text:
Write harmonic analyses in plain text documents following the notation style as defined and demonstrated by Dmitri Tymoczko. Dmitri's write-up is [here](http://dmitri.tymoczko.com/RNguidelines.pdf) -- the technical details follow that section on philosophy.
Again, the musical task and the roman numerals are exactly as above, but there are differences of syntax.

All three methods can be fully and automatically integrated with one another so the choice is free from that perspective. On balance, I would suggest the score annotation method as it keeps both score and analysis in one place. You can also listen to the piece (or at least a computer rendered performance of it), and keep your place in the score.
