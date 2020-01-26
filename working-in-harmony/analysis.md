---
layout: post
title: 'Notes for Analysts'
---

Here are instructions for entering musical analyses we can work with computationally.

On this page:
- Why do this?
- What scores?
- How to encode your analysis.

## Why do this?

The main reasons for encoding analyses in one of these formats are to:
- Keep your analysis in a format that can be re-purposed. Analyses on paper are fine, but they're not going any further than that. Analyses in an encoded format can be checked, edited, converted into scores, and much more besides.
- Get feedback: we offer an automated system for providing basic feedback on analysis (a kind of analytical spell-checker if you like). This is set to be launched as an independent web app on Four Score and More soon. In the meantime, you're welcome to email your analysis to `Mark dot Gotham at Cornell dot edu`. If you're in one of my classes at Cornell then I'll get right back to you; if not that's fine but it'll take a bit longer ...

## What Scores?

You can encode analyses for any music you like, though:
- Feedback is limited to those scores for which we have a corresponding encoding available;
- The current drive is for analyses of songs by women composers as part of the [Scores of Scores](/scores-of-scores) lieder project.

To get feedback, please submit your score in the 'compressed musicxml' format (extension '.mxl').
All music notation software packages (Finale, MuseScore, Sibelius ...) export to this format.
The 'Export' option is usually under the 'File' menu (or equivalent).

We cannot work with those notation software packages' own file formats or with PDFs.
There are an increasing number of scores available in encoded formats these days, including our 'Scores of Scores' collection of 19th century songs which you can download from [MuseScore.com](https://musescore.com/OpenScore-Lieder-Corpus) (free sign up required), or directly from [GitHub](https://github.com/MarkGotham/ScoresOfScores/tree/master/3-Corpus) and use for any purpose including this one.

If you have a particular piece in mind and don't have access to it in an encoded format, we recommend the 'PlayScore' app for converting PDFs.
There is a small charge for this software, and there are some modest restrictions on allowed uses, though nothing that should conflict with use for this educational purpose.

## How to encode your analysis

You can encode your analysis in one of two ways:

1. Directly in the encoded score itself as a 'lyric' on a newly added lowest part. To do this,
  - add a new part (e.g. press 'i' in MuseScore),
  - enter new notes (or perhaps copy over the rhythm from an existing part as a template), and
  - add Roman numeral lyrics to notes in that part. Here's an example analysis of a [Wolf song](../working-in-harmony-backend/app/Wolf_Hugo_-_Eichendorff-Lieder_Der verzweifelte Liebhaber.mxl). We need the new part because otherwise you'd have to change the music (adding notes in to attach lyrics to).
2. Typing in the 'Roman text' format. This is a very simple and intuitive format which adds no jargon beyond that already involved in Roman numeral analysis.
 - See the example below to get the gist of how it works at a glance. The complete form of this analysis can be downloaded [here](../working-in-harmony-backend/app/1.txt).
 - Scroll down for more advice on the formatting.
 - For those interested in knowing more, the full documentation can be found in our research report for [ISMIR 2019](http://archives.ismir.net/ismir2019/paper/000012.pdf) or on music21's [code base](github.com/cuthbertLab/music21/tree/master/music21/romanText), [documentation](web.mit.edu/music21/doc/moduleReference/moduleRoman.html), and [User’s Guide](http://web.mit.edu/music21/doc/usersGuide/usersGuide_23_romanNumerals.html).
 - In addition to the analysis examples above:
    + Here is a [generic blank template](RomanTextTemplate.txt) for entering Roman text (complete with 100 empty measures).
    + A growing corpus of examples is hosted [here](https://github.com/MarkGotham/When-in-Rome) (external link).

```
Composer: J.S. Bach
Title: Prelude No.1 (BWV846)
Analyst: Mark Gotham [feel free to leave this blank]

m1 b1 C: I
m2 b1 ii42
m3 b1 V65
m4 b1 I
m5 b1 vi6
m6 b1 G: V42
m7 b1 I6
m8 b1 IV42
m9 b1 ii7
m10 b1 V7
m11 b1 I
```

### Annotation basics

Basically the analyst's job is to:
- Decide where each chord change occurs;
- Enter a Roman numeral (in the format described below).

For 'On-score' analyses:
- Click on the note in the lowest part at that point;
- Click CTRL+L (Windows) CMD+L (Mac) to start entering a Roman numeral;

For (separate) Roman text files, make sure to:
- Note down the measure and beat carefully, and
- Start your analysis at the start of the piece (measure 1, or 0 in the case of anacruses).

### Format of Roman numeral entries

For either input type, use the following format:
- New chord: For each new chord, specify the Roman numeral in relation to the prevailing key, for instance 'I' for the tonic.
- New key: For the start of a new key area (including, necessarily, the start of the piece), specify that key followed by a colon (':') and the Roman numeral (e.g. 'G:I' for a move to G major and a tonic chord in that key). For a continuation of the prevailing key, there's no need to specify the key: just write in the Roman numeral alone ('I').
- Chord quality: don't forget to use upper case for Major (e.g. 'I'), lower case for minor ('i'), and add the symbols for a diminished triad ('o') or augmented triad ('+') as necessary.
- Finally, specify any added or altered notes in square brackets with 'add', '#', 'b', or 'no' as required.

In summary, enter a Roman numeral (that’s required), along with any or all of the other annotations (all optional) in the format: 'key:', 'root accidental', 'Roman numeral', 'chord form', 'figure', 'additions'.

For instance, the convoluted entry 'a:#viio6[add4]' indicates:
- a modulation to a minor;
- a chord on the raised seventh degree (G#) ...
- that is diminished (so G#, B, D) ...
- in first inversion (so with B in the bass, below the G# and D)..
- and with an added 4th above the root (sic, so the pitch C).

### Optional versus required entries

- [On-score format] It’s possible to input spaces in lyrics. In many notation programs, a normal SPACE key will move you on to lyric input for the next note, but ALT-SPACE will keep you on the current note and add a space to that lyric. Given how confusing that can be, we've made spaces optional: we don’t require them, but don’t worry if you do have them (the code throws them out anyway).
- [On-score format] All lyrics need to be appended to a note (not a rest) in the new part. You can put meaningful notes in that part (e.g. start by copying existing material and then adjusting the rhythms as necessary) but that's not required (the notes can just be nonsense as long as they're in the right place).
- [Either format] Changes of key remain in effect until the next marking, but changes of tonicization don’t so you need to reiterate them at every entry. That should help keep their use suitably fleeting! That said, you may want to put in reminders of the prevailing key occasionally (after a tonicization, or indeed elsewhere). That's fine and doesn't make any different to the analysis (again, these repetitions are ignored by the code as redundant information).
