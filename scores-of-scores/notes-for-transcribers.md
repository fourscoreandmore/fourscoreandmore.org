---
layout: post
title: 'Notes for Transcribers'
---

_Part of [Scores of Scores](/scores-of-scores)._

---

For score download (in multiple formats including MuseScore and PDF), head to:
- [this page for the lieder](https://fourscoreandmore.org/openscore/lieder/)
- [this page for the quartets](https://fourscoreandmore.org/openscore/stringquartets/).

This page provides some additional information for transcribers
and doubles as a reference guide to the editorial interventions we have made.

Welcome and thanks for participating in this very exciting encoding project.

On this page, we aim to answer some of the most frequently asked questions (FAQs)
and common issues encountered in transcribing for this project and/or using the scores.
We hope you find it useful!

## Contents

| Code                                  | Section                                        |
|---------------------------------------|------------------------------------------------|
| [G](#g-general)                       | General                                        |
| [M](#m-metadata)                      | Metadata: Score and Online                     |
| [L](#l-layout)                        | Layout: System and Page breaks                 |
| [T](#t-time)                          | Time: Time Signatures, Beaming, Tuplets, Tempo |
| [O](#o-ornaments)                     | Ornaments including Grace Notes                |
| [K](#k-key)                           | Key: Key Signatures and Accidentals            |
| [C](#c-clefs-and-stems)               | Clefs                                          |
| [D](#d-dynamics-and-lines)            | Dynamics (Cresc.) and Lines (Rit.)             |
| [S](#s-ties-and-slurs)                | Ties and Slurs                                 |
| [B](#b-editorial-brackets)            | Brackets                                       |
| [P](#p-playing-instructions)          | Playing Instructions                           |
| [W](#w-workflow-during-transcription) | Workflow: During Transcription                 |   

We also include some notes [about this page](#about-this-page).

## G: General

1. Aim to produce as **exact** a copy of the source edition as possible.
2. Use MuseScore **defaults** wherever possible so that as much information is transferred as effectively as possible to the parts and when converted into other formats like MusicXML.
3. Where these two are in conflict (G1 exact copy vs G2 MuseScore defaults), the MuseScore defaults take priority. (More detailed notes follow below.)
4. Aim to produce a score with strong internal **consistency**:
if a motive recurs exactly, it should probably be edited similarly;
if all parts have the same material, and one has divergent articulation,
it should probably be edited to match. 
5. Keep recognised musical terms like "cresc.", "andante" etc. in the source **language**;
provide a translation for anything non-standard.
6. Edition of manuscript sources is often more complicated and introduces more exceptions to the guidance here.
7. If in doubt, ask your reviewer and/or the team via Signal.

## M: Metadata

1. **Title** and **composer** should already be present in their respective fields of the 'score properties' box and displayed on the score.
Likewise, the **lyricist** in the case of the lieder.
The naming convention on musescore.com should likewise have been handled by the reviewer/central team.
Let us know if you spot any errors (do not make changes unless agreed with your reviewer).
2. **Dedication:** We use a separate 'Vertical Frame', above the main 'Title frame' with text centred, italic, 9pt.
Again, this is handled at the templating stage.
3. **Dates:** Birth and death dates are not shown for anyone (composer, lyricist or dedicatee).
Some of that data is stored separately (not on the scores, but within the project data.)
4. **Date of composition:** not shown in the title frame.
A date and place of composition may be shown at the end of the score if it appears on the source edition.

## L: Layout

1. **System breaks and page breaks:** Follow the system breaks and page breaks used by the source edition where possible in that order (system being the more important).
   1. _Exception:_ Never attempt to replicate the splitting of measures across a system or page break (i.e., with part before and part after).
   2. _Exception:_ Dispense with all system breaks and page breaks in extreme cases,
   e.g., of a source with very small pages, and/or in transcribing from parts (from which there is no consistent stave/page break to follow).
2. **Above / below stave:** In general, use the default settings provided in the template 
   1. Above: Tempo marks; playing instructions such as `pizz.` and `arco`:
       1. _Exception (quartets):_ where there are two voices, one arco and one pizz. In this case they should be placed above/below as appropriate for the voice in question.
   2. Below: All dynamics, hairpins and expression text.
      1. _Exception (all):_ given multiple expressive markings all at once, it can be useful to flip some to other side. 
      2. _Exception (lieder):_ dynamics in the vocal parts for the lieder go above.

## T: Time

1. **Time signatures:** Always reproduce time signature symbols as shown in the source edition, e.g., common time, cut common time (_alla breve_), and 4/4 are all to be treated as different even though they refer to the same duration and (arguably) beam groupings.
2. **Beaming:** We usually enter the notes with default beaming for …
   1. Placement: above _or_ below – not a combination of both
      1. _Exception:_ We do not use crossing combinations of notes both above and below the beam in string parts, but we do sometimes need to copy that notation in the lieder piano parts, e.g., when crossing between treble and bass of the grand stave. Please discuss with your reviewer.
   1. Grouping: typically follows the pre-set time signature defaults (cf G2).
   E.g., editorial conventions for 6/8 time vary.
      1. This is partly for consistency (cf G4).
      2. _Exception:_ Composers sometimes use a deviation from the normal beaming pattern for a specific passage within a longer work.
      Do copy this except where it means beaming across barlines at line breaks: there is no MuseScore provision for this, so separate the beam groupings there.
3. **Rest grouping**: As for beam grouping, use the pre-set time signature defaults (cf G2).
This can lead to extensive visual divergence from the source, as long as it is consistent.
4. **Tuplets:** Use only the MuseScore default bracket (right-angle corners) whatever the source uses.
   1. The settings in the Inspector for tuplets should be: `Direction = Auto`; `Number type = Number`; `Bracket type = Auto`
   2. In longer passages consistently in the same tuplet,
   provide the first tuplet marking for that long group, and make the rest invisible.
5. **Tremolo:** Measured tremolo can be notated with any markings that are semantical equivalent.

## O: Ornaments

1. Copy the source edition including noting the difference between:
   1. the presence (acciaccatura) or absence (appoggiatura) of a slash through the note.
   2. positioning before / after the main note (MuseScore defaults support both).
2. Use MuseScore defaults for the exact placement (e.g., before/after the barline, where relevant).
3. Triplet (or other tuplet) grace notes cannot be entered into MuseScore. Enter them as grace notes of the appropriate type and use staff text to enter the appropriate number.

## K: Key

1. **Key signatures:** Include all key signatures exactly as given, except for …
   1. **Cancelling naturals:** Never show cancelling naturals on a change of key signature (again, use the MuseScore default).
Likewise, never use the "Natural-flat" or "Natural-sharp" symbols for individual accidental cancellation in adjacent measures.
2. **Accidentals:** Any accidentals that need to be introduced (which were not present in the source) should be enclosed in square brackets `[]` to indicate an editorial change.

## C: Clefs and Stems

1. Generally, most of our work is set out in two clefs: treble and bass.
2. Additional clefs to preserve in our editions:
   1. Lieder: many songs use the treble clef with `8` beneath it to indicate down one octave.
   This is typical for the tenor voice in modern editions (for both solo and choral repertoire).
   2. Viola parts are (mostly) in alto clef, with occasional passages in treble clef (then and now).
   Preserve both, though note C.3.
   3. 'Cello parts: in addition to the bass clef, these may well have passages in tenor and treble clefs.
   Preserve all three, though note C.3 and the following exception.
      1. _Exception_: Do use cello treble clef, but notate at the sounding octave, per modern convention.
      Some sources (Dvorak, Beethoven, ...) use a _de facto_ "treble clef an octave lower".
      We avoid this relatively rare and confusing practice. 
3. Omit or adapt brief clef changes in some extreme cases.
For example, we sometimes see very brief use of a clef change
in a source that seems to prioritise page space over part readability.
We prioritise part readability and adjust accordingly.
As a rule of thumb for viola and cello parts,
only change clef if you would need more than 2 leger lines
and the passage stays high for long enough to be useful to the player. 
4. Adapt any other clefs to their nearest modern equivalent.
E.g., we often convert cello treble clef to tenor per modern conventions.
5. Almost never use manual adjustment (flip) of a note's stem direction.
This is partly due to the clef issues above and related use cases such as transposition.

Notes:
- Some transcribers prefer to use original clefs during transcription to make direct proofreading easier
(e.g., comparing a notehead on the same line or space).
Reviewers will then change the clefs to standard when review is complete before release.
- For a more robust (algorithmic) approach to modern clef choice, see the
[Species](../species) corpus.
We may move to formalise in this way in future.


## D: Dynamics and Lines

1. Use 'real' lines (that affect playback and are exported) wherever possible.
2. **Terms:** Copy the source (cf. G1)
   1. _Exception_ where there is an alternative that is clearly both 1) equivalent and 2) more standard today (cf G2).
   E.g., use `diminuendo` or `dim.` in place of `decrescendo`.
3. **Abbreviations:** Use any that are recognised standards including
`cresc.` and `dim.`;
`rit.`, `rall.`, and `accel`.
Please spell out anything even slightly ambiguous and/or adapt to one of these (D2.1).
4. Some older sources break these instructions into separate syllables over multiple measures or even multiple systems.
For example: `cre - - - scen - - - do`. Do not attempt to copy this manually.
Instead, use a wide-dashed line (`Line Thickness = 0.12sp`, `Dash Line Length = 5`, and `Dash Gap Width = 20`),
with standard `Begin text` - and with `Continue text` in parentheses at the start of each system e.g., _(dim.)_.
5. We use the `ritardando` since it was added to MuseScore (v4). 
For earlier scores we had to use a `System text` entry instead.
We may update these in due course.

## S: Ties and Slurs

1. Make sure to include all ties as ties and slurs as slurs without mixing (they are not equivalent).
2. Ties across barlines: Accidentals are not repeated at the beginning of the second (or subsequent) bar, even if it is a system or page break.
If the note is repeated later in the bar, the accidental is shown (this is MuseScore default.)

## B: Editorial Brackets

1. Brackets around a note or accidental or similar in the source indicate their editorial intervention.
2. Square brackets in our files indicate our editorial interventions.
3. As such, where there are brackets in the source (whether square brackets or curved),
the enclosed element should be included in our transcription, without the brackets.


## P: Playing instructions

1. Use the `pizz.` and `arco` instructions from the Text palette (see comments above about placement).
2. Include instructions for harmonics (from the articulations palette, the symbol looks similar to `o`)
3. Include any instructions indicating the string to be used (e.g., `sul A` or `IV`).
4. Fingerings are generally not included.
   1. _Exception_: Fingering sometimes acts as an implicit string instruction. P3 overrides P4.
5. For mutes use 'con sord.' and 'senza sord.',
in place of whatever language the source uses (cf G5).

## W: Workflow: During Transcription

In addition to direct communication,
transcribers are also encouraged to use staff text with the colour set to red to explain intentional deviations from the source edition.
This includes any such edit including 'obvious' corrections.
The reviewers will make the final decision on these deviations and delete all red text prior to uploading the score.

## About this page

Last Updated: October 2026

The rule numbering is our own, created for want of an existing standard.
There are practical style guides (e.g., MOLA, IMSLP) and books (e.g., Gould _Behind Bars_)
but none has a clear codification for use in a case like this.
The closest parallel seems to be bibliographic metadata, (e.g., MCRM(M): Descriptive Cataloguing Rules for Music).
We are happy to move to a standard if/as/when one emerges.

Contributors:
- [Mark Gotham](https://markgotham.github.io/), Principal Investigator
- Peter Jonas ([shoogle on MuseScore](https://musescore.com/shoogle)), MuseScore.
- Mike Nelson † ([mike320](https://musescore.com/mike320))
- Maureen Redbond ([ashmoggs](https://musescore.com/user/27968710)), OSQ Manager
- Dan Rootham ([DanielR](https://musescore.com/danielr)), Former OSLC Manager


If you find anything unclear, or would like any other questions answered here, then please do let us know via your reviewer.
You may also find useful these [general tips](https://musescore.com/shoogle/scores/3434266)
which Peter prepared at the very beginning of OpenScore.

Many thanks for being a part of this initiative. Here’s to a great encoded corpus in the making!
