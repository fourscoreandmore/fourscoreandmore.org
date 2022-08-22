---
layout: post
title: 'Notes for Transcribers'
---

_Part of [Scores of Scores](/scores-of-scores)._

---

Welcome and thanks for participating in this very exciting encoding project.

On this page, we seek to answer some of the most frequently asked questions (FAQs) and common issues encountered in transcribing for this project.
We hope you find it useful!

## General

- We aim to produce as exact a copy of the source edition as possible.
- We also use MuseScore defaults wherever possible so that as much information is transferred as effectively as possible to the parts and when converted into other formats like musicXML.
- Where these two are in conflict (exact copy vs MuseScore defaults), the MuseScore defaults take priority. (More detailed notes follow below.)
- Edition of manuscript sources is often more complicated: please get in touch to discuss individual cases.
- If in doubt, ask your reviewer!

## Metadata' text on the score and online

- **Title, composer, and lyricist** (for lieder) should already be present in their respective fields of the 'score properties' box and displayed on the score. The naming convention on musescore.com should likewise have been handled by the reviewer/central team. Let us know if you spot any errors (do not make changes unless agreed with your reviewer).
- **Dedication:** We use a separate 'Vertical Frame', above the main 'Title frame' with text centred, italic, 9pt. Again, please leave this as it is.
- **Dates:** Birth and death dates are not shown for anyone (composer, lyricist or dedicatee).
- **Date of composition:** not shown in the title frame. A date and place of composition may be shown at the end of the score if it appears on the source edition.

## Layout

- **System breaks and page breaks:** Follow the system breaks and page breaks used by the source edition where possible in that order (system being the more important).
  - _Exception:_ Do not attempt to replicate the splitting of measures (with part before and part after) a system or page break.
- **Above / below stave:** In general, use the default settings provided in the template

  - Above: Tempo marks; playing instructions such as `pizz.` and `arco`:
    - _Exception:_ where there are 2 voices, one arco and one pizz. In this case they should be placed above/below as appropriate for the voice in question.
  - Below: All dynamics, hairpins and expression text.
    - _Exception:_ dynamics in the vocal parts for the lieder go above.

## Metre: time signatures, beaming, tuplets

- **Time signatures:** Always reproduce time signature symbol as shown in the source edition, e.g., common time, cut common time (_alla breve_), and 4/4 are all to be treated as different even though they refer to the same duration and (arguably) beam groupings.
- **Beaming:** usually, we enter the notes with default beaming for …
  - **P** lacement: above _or_ below – not a combination of both
    - _Exception:_ We do not use crossing combinations of notes both above and below the beam in string parts, but we do sometimes need to copy that notation in the lieder piano parts, e.g., when crossing between treble and bass of the grand stave. Please discuss with your reviewer.
  - Grouping: typically follows the pre-set time signature defaults.
    - _Exception:_ Composers sometimes use a deviation from the normal beaming pattern for a specific passage within a longer work. Do copy this except where it means beaming across barlines at line breaks: there is no MuseScore provision for this, so separate the beam groupings there.
- **Tuplets:** Use only the MuseScore default bracket (right-angle corners) whatever the source uses.
  - The settings in the Inspector for tuplets should be: **`** Direction = Auto`; `Number type = Number` **; `** Bracket type = Auto`
  - Tuplet indication is left visible if it is included in the source edition, otherwise these should be made invisible.
    - _Exception_ – if no indication is given for the first instance of a tuplet, and it could be confusing without it, then make that first instance (only) visible.

**Grace notes**

- Copy the source edition including noting the difference between:
  - the presence (acciaccatura) or absence (appoggiatura) of a slash through the note.
  - positioning before / after the main note (MuseScore defaults support both).
- Use MuseScore defaults for the exact placing (e.g., before/after the barline, where relevant).
- Triplet (or other tuplet) grace notes cannot be entered into MuseScore. Enter them as grace notes of the appropriate type and use staff text to enter the appropriate number.

## Key signatures and accidentals

- **Key signatures:** Include all (of course!) exactly as given, except for …
- **Cancelling naturals:** Never show cancelling naturals on a change of key signature (again, use the MuseScore default). Likewise, never use the "Natural-flat" or "Natural-sharp" symbols for individual accidental cancellation in adjacent measures.
- **Accidentals:** Any accidentals that need to be introduced (which were not present in the source) should be enclosed in square brackets `[]` to indicate an editorial change.

## Clefs

- Generally, most of our work is set out in two clefs: treble and bass.
- Exceptions to preserve in our editions:
  - Lieder: many songs use the treble clef with `8` beneath it to indicate down one octave. This is typical for the tenor voice in modern editions (for both solo and choral repertoire).
  - Quartet viola parts are (mostly) in alto clef, with occasional passages in treble.
  - Quartet 'cello parts: in addition to the bass clef, these may well have passages in tenor and treble clefs.
- All other clefs are to be converted to the nearest modern equivalent. E.g., the treble clef is the only 'G' clef in common use: convert any other G clefs into a treble clef.
  - _Exception:_ You may wish to use the original clef during transcription to make proofreading easier. Reviewers will then change the clefs to standard when review is complete. Do not make any manual adjustments to the stem direction in this case.

## Crescendo, diminuendo, ritardando

- Use 'real' lines (that affect playback and are exported) wherever possible.
- **Terms:** Copy the source except where there is a now-more-standard equivalent. E.g., use ` diminuendo` in place of `decrescendo`.
- **Abbreviations:** only `cresc.`, `dim.` and `rit.`., please spell anything else out in full and/or adapt to one of these.
- Some older sources break these instructions into separate syllables over multiple measures or even multiple systems. For example: `cre - - - scen - - - do`. Do not attempt to copy this. Instead use a wide-dashed line (`Line Thickness = 0.12sp`, `Dash Line Length = 5`, and `Dash Gap Width = 20`), with standard `Begin text` - and with `Continue text` in parentheses at the start of each system e.g., _(dim.)_.

## Ties

- Make sure to include all ties … as ties … not as slurs!!
- Ties across barlines: Accidentals are not repeated at the beginning of the second (or subsequent) bar, even if it is a system or page break. If the note is repeated later in the bar the accidental is shown (this is MuseScore default.)

## Playing instructions

- Use the `pizz.` and `arco` instructions from the Text palette (see comments above about placement).
- Do include instructions for harmonics (i.e., usually the `o` symbol)
- Do include the Roman numerals indicating which string to be used (e.g., `IV`).
- Indication of fingering is not generally included. If in doubt, ask your reviewer.

## During transcription:

- In addition to direct communication, transcribers are also encouraged to use staff text with the colour set to red to explain intentional deviations from the source edition including 'obvious' corrections. The reviewers will make the final decision on these deviations and delete all red text prior to uploading the score.

## About this page

Last Updated: August 2022

Contributors:
- Mark Gotham ([here](/people/MG_bio.md) and [on musescore](https://musescore.com/user/8641586)) - Principal Investigator
- Peter Jonas ([shoogle](https://musescore.com/shoogle)) - MuseScore / OpenScore Manager
- Dan Rootham ([DanielR](https://musescore.com/danielr))
- Mike Nelson ([mike320](https://musescore.com/mike320))
- Maureen Redbond ([ashmoggs](https://musescore.com/user/27968710))

If you find anything unclear, or would like any other questions answered here, then please do let us know via your reviewer.
You may also find these [general tips](https://musescore.com/shoogle/scores/3434266) useful.

Many thanks for being a part of this initiative. Here’s to a great encoded corpus in the making!
