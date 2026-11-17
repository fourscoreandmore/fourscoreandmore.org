---
layout: post
title: 'Notes for Transcribers plus Editorial Conventions'
---

_Part of [Scores of Scores](/scores-of-scores)._

---

To download scores (in multiple formats including MuseScore and PDF), head to:
- [this page for the lieder](https://fourscoreandmore.org/openscore/lieder/)
- [this page for the quartets](https://fourscoreandmore.org/openscore/stringquartets/).

This page provides some additional information for transcribers
and doubles as a reference guide to the limited editorial interventions we have made.
On this page, we aim to answer some of the most frequently asked questions (FAQs)
and common issues encountered in transcribing for this project and/or using the scores.
More generally, this serves as a blueprint for the question:
"what does it mean to transcribe a source faithfully but pragmatically in a modern app".

We hope you find it useful!

## Contents

| Code                                  | Section                                               |
|---------------------------------------|-------------------------------------------------------|
| [G](#g-general)                       | General                                               |
| [M](#m-metadata)                      | Metadata: Storing the data, vs rendering in the score |
| [L](#l-layout)                        | Layout: System and Page breaks                        |
| [T](#t-time)                          | Time: Time Signatures, Beaming, Tuplets, Tempo        |
| [O](#o-ornaments)                     | Ornaments including Grace Notes                       |
| [K](#k-key)                           | Key: Key Signatures and Accidentals                   |
| [C](#c-clefs-and-stems)               | Clefs                                                 |
| [D](#d-dynamics-and-lines)            | Dynamics (Cresc.) and Lines (Rit.)                    |
| [S](#s-ties-and-slurs)                | Ties and Slurs                                        |
| [B](#b-editorial-brackets)            | Brackets                                              |
| [P](#p-playing-instructions)          | Playing Instructions                                  |
| [W](#w-workflow-during-transcription) | Workflow: During Transcription                        |   

We also include some notes [about this page](#about-this-page).
This includes the cross-reference convention.

## G: General

1. Aim to produce as **exact** a copy of the source edition as possible.
2. Use the app's **defaults** wherever possible so that as much information is transferred as effectively as possible
when converting into other formats, and/or making parts etc.
Apps come and go, and even different versions of the same app introduce breaking changes.
3. Where these two are in conflict (G1 exact copy vs G2 defaults), the latter (defaults) take priority.
(More detailed notes follow below.)
4. Aim to produce a score with strong internal **consistency**:
if a motive recurs exactly, it should probably be edited similarly;
if all parts have the same material, and one has divergent articulation,
it should probably be edited to match.
5. Keep recognised musical **terms** like "cresc.", "andante" etc. in the source **language**;
provide a translation for anything non-standard.
6. Transcription from **manuscripts**, parts, and/or multiple sources pose more complications and
introduce more exceptions to the guidance here.
7. All else being equal, it is better to include than not.
It is generally easier to remove unwanted information than the reverse.
For example, if it practical to include the source's systems breaks (discussed below)
we do so, and users can easily remove all such markings for use cases where they are net negative
(e.g., variable flow across different page/screen sizes).
8. **Report** any deviation from the source that are covered by explicit rule here.
See [section R](#r-reporting-editorial-changes).

## M: Metadata

In most cases, "more is more" for metadata.
Specific inclusion of this data in the visual rendering of a score is more project specific.
Our projects handle this at the templating stage; here, for reference, are our defaults:

1. **Title** and **composer** should be present in their respective fields of the 'score properties'
and displayed on the score:
title at the top of the page, centered;
composer at the right hard side, just below the title.
In the case of songs, the **lyricist** is given on the left hard side,
just below the title, roughly in line with the composer.
2. **Dedication:** We use a separate 'Vertical Frame', above the main 'Title frame' also centred, and italicised.
Again, this is handled at the templating stage.
3. **Dates:** Birth and death dates are not shown for anyone (composer, lyricist or dedicatee).
Some of that data is stored separately (not visually rendered in the score, but at least in the whole-project data.)
4. **Date of composition:** not shown in the title frame.
A date and place of composition may be shown at the end of the score if it appears on the source edition.

## L: Layout

1. **System breaks and page breaks:**
Follow the system breaks and page breaks used by the source edition where possible in that order (system being the more important).
Sources have often considered carefully where to place these breaks to assist musicians,
and preserving them further supports side-by-side comparison.
   1. _Exception:_ Never attempt to replicate the splitting of measures across a system or page break (i.e., with part before and part after).
   2. _Exception:_ Dispense with all system breaks and page breaks in extreme cases,
   e.g., of a source with very small pages, and/or in transcribing from parts (from which there is no consistent stave/page break to follow).
2. **Above / below stave:** In general, use the default settings provided in the template 
   1. Above: Tempo marks; playing instructions such as `pizz.` and `arco`:
       1. _Exception (strings):_ where there are two voices, one arco and one pizz.
       In this case they should be placed above/below as appropriate for the voice in question.
   2. Below: All dynamics, hairpins and expression text.
      1. _Exception (all):_ given multiple expressive markings all at once, it can be useful to flip some to other side.
      2. _Exception (lieder):_ dynamics in the vocal parts for the lieder go above.

## T: Time

1. **Time signatures:** Always reproduce time signature symbols as shown in the source edition, e.g., common time, cut common time (_alla breve_), and 4/4 are all to be treated as different even though they refer to the same duration and (arguably) beam groupings.
2. **Beaming:** Use default beaming (G2) with exceptions as noted below.
   1. Placement: above _or_ below – not a combination of both
      1. _Exception:_ Do not use crossing combinations of notes both above and below the beam in string parts,
      but do follow that notation in piano parts, e.g., when crossing between two upper and lower parts of the grand stave.
   2. Grouping: typically follows the pre-set time signature defaults (cf G2).
   E.g., editorial conventions for 6/8 time vary.
      1. This is partly for consistency (cf G4).
      2. _Exception:_ Composers sometimes use a deviation from the normal beaming pattern for a specific passage within a longer work.
      Do copy this where it seems to carry compositional intent (e.g., Bartok).
      Exceptions to this exception include beaming across barlines at stave/page breaks.
      As long as there is no reliable in-app provision for this; separate the beam groupings there.
3. **Rest grouping**: As for beam grouping, use the pre-set time signature defaults (cf G2).
This can lead to extensive visual divergence from the source, as long as it is consistent.
4. **Tuplets:** Use only the default bracket (right-angle corners) whatever the source uses.
   1. The settings in the Inspector for tuplets should be: `Direction = Auto`; `Number type = Number`; `Bracket type = Auto`
   2. In longer passages consistently in the same tuplet,
   provide the first tuplet marking for that long group, and make the rest invisible (they stay in the file, so playback and export are unaffected).
5. **Tremolo:** Measured tremolo can be notated with any marking that is semantically equivalent;
prefer the app's default form (cf G2).
6. **Tempo:** Include tempo marks as in the source, including metronome marks, above the stave (L2.1).
Keep tempo terms in the source language (G5), with a bracketed translation for non-standard ones (G5.2).
Gradual tempo changes (`rit.`, `accel.`) are lines (see section D).

## O: Ornaments

1. Copy the source edition including noting the difference between:
   1. the presence (acciaccatura) or absence (appoggiatura) of a slash through the note.
   2. positioning before / after the main note (where the app supports both).
2. Use defaults for the exact placement (e.g., before/after the barline, where relevant).
3. Details such as tuplet grace notes with a specific number of beams may not be possible to enter exactly.
Use the nearest available (acciaccatura vs appoggiatura first, correct number of beams second, tuplet indication last with staff text (optional)).

## K: Key

1. **Key signatures:** Include all key signatures exactly as given, except for …
   1. **Cancelling naturals:** Never show cancelling naturals on a change of key signature (again, use the default).
Likewise, never use the "Natural-flat" or "Natural-sharp" symbols for individual accidental cancellation in adjacent measures.
2. **Accidentals:** Any accidentals that need to be introduced (which were not present in the source) should be enclosed in square brackets `[]` to indicate an editorial change.

## C: Clefs and Stems

1. Most of our work is set out in two clefs: treble and bass.
2. Additional clefs to preserve in our editions:
   1. Lieder: many songs use the treble clef with `8` beneath it to indicate down one octave.
   This is typical for the tenor voice in modern editions (for both solo and choral repertoire).
   2. Viola parts are (mostly) in alto clef, with occasional passages in treble clef (then and now).
   Preserve both, though note C3.
   3. 'Cello parts: in addition to the bass clef, these may well have passages in tenor and treble clefs.
   Preserve all three, though note C3 and the following exception.
      1. _Exception_: Do use cello treble clef, but notate at the sounding octave, per modern convention.
      Some sources (Dvořák, Beethoven, …) use a _de facto_ "treble clef an octave lower".
      We avoid this relatively rare and confusing practice.
3. Omit or adapt brief clef changes in some extreme cases.
For example, we sometimes see very brief use of a clef change
in a source that seems to prioritise page space over part readability.
We prioritise part readability and adjust accordingly.
As a rule of thumb for viola and cello parts,
only change clef if you would need more than 2 leger lines
and the passage stays high for long enough to be useful to the player.
Where you do adapt a clef, use the clef a modern player would expect, and report it (R1).
4. Adapt any other clef, i.e., one not listed in C2 (e.g., soprano, mezzo-soprano or baritone clefs, or the French violin clef), to its nearest modern equivalent.
This does not apply to the cello clefs in C2.3, which are preserved.
5. Almost never use manual adjustment (flip) of a note's stem direction.
This is partly due to the clef issues above and related use cases such as transposition.

Notes:
- Summary of the decision order for viola and cello parts:
(a) keep the source clef where C2 lists it; (b) apply the leger-line test in C3 to brief changes; (c) use C4 for any clef not listed in C2.
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
3. **Abbreviations:** Use any that are recognised standards, including `cresc.` and `dim.`; `rit.`, `rall.`, and `accel.`.
Please spell out anything even slightly ambiguous and/or adapt to one of these (D2.1).
4. Some older sources break these instructions into separate syllables over multiple measures or even multiple systems.
For example: `cre - - - scen - - - do`.
Do not attempt to copy this manually.
Instead, use a wide-dashed line (`Line Thickness = 0.12sp`, `Dash Line Length = 5`, and `Dash Gap Width = 20`), with standard `Begin text` and with `Continue text` in parentheses at the start of each system, e.g., _(dim.)_.
5. For `ritardando`, use the app's built-in line where it exists.
Earlier scores used a `System text` entry instead; we may update these in due course.
Record the app and version used in the editorial report (R3), since line behaviour can differ between versions.

## S: Ties and Slurs

1. Make sure to include all ties as ties and slurs as slurs without mixing (they are not equivalent).
2. Ties across barlines: Accidentals are not repeated at the beginning of the second (or subsequent) bar, even if it is a system or page break.
If the same pitch recurs later in the bar, the accidental is shown (this is both a default and worth keeping).

## B: Editorial Brackets

1. Brackets around a note or accidental or similar in the source indicate their editorial intervention.
2. Square brackets in our files indicate our editorial interventions.
They mark only what we add (accidentals, K2; translations, G5.2).
Every other intervention is reported, not marked (R).
3. As such, where there are brackets in the source (whether square brackets or curved),
the enclosed element should be included in our transcription, without the brackets.
4. Because B3 removes the source's own brackets, record each case in the editorial report (R1) so the information is not lost.


## P: Playing instructions

1. Use the `pizz.` and `arco` instructions from the Text palette (see comments above about placement).
2. Include instructions for harmonics (from the articulations palette, the symbol looks similar to `o`).
3. Include any instructions indicating the string to be used (e.g., `sul A` or `IV`).
4. Fingerings are generally not included.
   1. _Exception_: Fingering sometimes acts as an implicit string instruction.
   In that case, include it (this overrides P4).
5. For mutes use `con sord.` and `senza sord.`, in place of whatever language the source uses (cf G5.1).
Where a preparation instruction is given ahead of the change include this, with translation in square brackets as needed
(e.g., 'Dämpfer auf [mute]'),
and still include the 'con sord.' at the point where playing with mute begins.

## W: Workflow: During Transcription

1. In addition to direct communication, transcribers are also encouraged to use staff text with the colour set to red to explain intentional deviations from the source edition.
This includes any such edit including 'obvious' corrections.
The reviewers will make the final decision on these deviations and delete all red text prior to uploading the score.
2. Before deleting the red text, reviewers move anything that still applies into the editorial report (R).
Red text is the working draft of that report.

## R: Reporting editorial changes

The score itself stays clean for playing and conversion.
We aim to work towards reporting editorial changes for those interested, separately.

1. **What is reported.** Any deviation from the source that is not visibly marked in the score, including:
   1. consistency edits (G4);
   2. normalised terms and abbreviations (G5.1, D2, D3, P5);
   3. source brackets removed (B3, B4);
   4. accidentals added (K2), although these are also bracketed in the score;
   5. clef changes and modernisation (C3, C4);
   6. composer-led vs house-style beaming decisions that were not obvious (T2.2.1);
   7. source errors corrected, or deliberately preserved (W1);
   8. system and page breaks dispensed with (L1.2);
   9. ornaments or details entered as the nearest available form (O3).
2. **Systematic vs specific.**
Systematic differences caused by app defaults (rest grouping T3, tuplet brackets T4, cancelling naturals K1.1, omitted fingerings P4, normalised beaming T2.2) are stated once, in a general note, not bar by bar.
Specific interventions get one line each: bar number, part or staff, the source reading, our reading, the reason, and the rule code (for example, `b. 34, Vc.: source mf, ours p, to match parallel passage in Vn. I (G4)`).
3. **Header.** Source edition and where it was obtained, transcriber, reviewer, date, and the app and version used.
4. **Purpose.** The report is for readers who need to know how the score differs from its source (performers, editors, researchers).
It should be possible to read the score without the report, and to recover the source reading from the two together.

## N: Not yet covered

The following are not yet codified.
Until they are, ask your reviewer (G7) and record the decision (R1):

- Lyrics: underlay, hyphenation, melismas, translations.
- Piano pedalling.
- Articulations, fermatas, repeats and voltas.
- Rehearsal marks, bar numbering, multi-bar rests.
- Hairpins (beyond their placement in L2.2).
- Ornaments other than grace notes (trills, turns, mordents).
- Courtesy accidentals already in the source.

## About this page

Last updated: November 2026.
The rule numbering is our own, created for want of an existing standard.
Internal **cross-references** use the section letter followed by the rule number, with further dots for sub-items, in list order: `G2`, `L2.1`, `T2.2.1`, `C3`.
Sections are written "section R" or "R".

There are practical style guides (e.g., MOLA, IMSLP) and books (e.g., Gould, _Behind Bars_) but none has a clear codification for use in a case like this.
The closest parallel seems to be bibliographic metadata (e.g., MCRM(M): Descriptive Cataloguing Rules for Music).
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

Many thanks for being a part of this initiative.
Here's to a great encoded corpus in the making!
