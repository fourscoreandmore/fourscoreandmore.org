---
layout: post
title: 'Working in Harmony'
---

[NB: Working in Harmony is a Work in Progress (so to speak!) ... expect changes to this draft.]

'Working in Harmony' offers automated 'marking' of a Roman numeral analysis.
You can submit an analysis for absolutely any music you have available in a suitable format.
Simply upload your score and analysis, wait a few seconds, and our bot will do it's best to give you some useful advice.

[TODO: Click here for the upload page and options]

Scroll down for full 'how to' instructions and further information:
- Score input;
- Analysis input;
- A 'Behind the scenes' look at how this bot works;
- Data protection and future improvements.

## Score input

Please submit your score in the 'compressed musicxml' format (extension '.mxl').
All music notation software packages (Finale, MuseScore, Sibelius ...) export to this format.
The 'Export' option is usually under the 'File' menu.

We cannot work with those notation software packages' own file formats or with PDFs.
There are an increasing number of scores available in encoded formats these days, usually downloadable for free.
For instance, we at Four Score and More recently encoded 300+ 19th century songs.
You can download them from [here](https://github.com/MarkGotham/ScoresOfScores/tree/master/3-Corpus) (external link) and use them for any purpose including this one.

If you have a particular piece in mind and don't have access to it in an encoded format, we recommend the 'PlayScore' app for converting PDFs.
There is a small charge for this software, and there are some modest restrictions on allowed uses, though nothing that should conflict with use for this educational purpose.

## Analysis input

You can submit your analysis in one of two ways:
1. directly onto the encoded score itself as 'lyric' on a newly added lowest part. To do this, add a new part (e.g. press 'I' in MuseScore), enter new notes (or perhaps copy over the rhythm from an existing part as a template), and add Roman numeral lyrics to notes in that part. Here's an example analysis of a [Wolf song](../working-in-harmony-backend/app/Wolf_Hugo_-_Eichendorff-Lieder_Der verzweifelte Liebhaber.mxl). We need the new part because otherwise you'd have to change the music (adding notes in to attach lyrics to).
2. type (or cut and paste) text into the box provided. 'Roman text' is very intuitive: have a look at the example below and/or [this analysis of a Bach prelude](../working-in-harmony-backend/app/1.txt) to get the gist of how it works at a glance. The full documentation can be found within music21 or in our research report for ISMIR 2019 (proceedings forthcoming). In addition to the analysis examples above:
- Here is a [blank template](RomanTextTemplate.txt) for entering Roman text (complete with 100 empty measures).
- A growing corpus of examples is hosted [here](https://github.com/MarkGotham/When-in-Rome) (external link).

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

The bot is equally happy with either analysis input method so the choice is free from that perspective.
On balance, I ask my student to use the score annotation method where possible as it let's you:
- keep both score and analysis in one place;
- listen to the piece;
- keep your place in the score;
- save time by not having to explicitly input measure and beat numbers.

### Annotation basics

Basically the analyst's job is to:
- Decide where each chord change occurs;
- Enter a Roman numeral (in the format described in the next section).

For 'On-score' analyses:
- Click on the note in the lowest part at that point;
- Click CTRL+L (Windows) CMD+L (Mac) to start entering a Roman numeral;

For separate Roman text files you need to make sure to note down the measure and beat carefully.

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

Finally, a word on optional versus required entries:
- [On-score format] It’s possible to input spaces in lyrics. In many notation programs, a normal SPACE key will move you on to lyric input for the next note, but ALT-SPACE will keep you on the current note and add a space to that lyric. Given how confusing that can be, we've made spaces optional: we don’t require them, but don’t worry if you do have them (the code throws them out anyway).
- [On-score format] All lyrics need to be appended to a note (not a rest) in the new part. You can use put meaningful notes in that part (e.g. start by copying existing material and then adjusting the rhythms as necessary) but that's not required (the notes can just be nonsense as long as they're in the right place).
- [Either format] Changes of key remain in effect until the next marking, but changes of tonicization don’t so you need to reiterate them at every entry. That should help keep their use suitably fleeting! That said, you may want to put in reminders of the prevailing key occasionally (after a tonicization, or indeed elsewhere). That's fine and doesn't make any different to the analysis (again, these repetitions are ignored by the code as redundant information).

## 'Behind the scenes'

To make the most of this resource, it's helpful to get a sense of how it works.

Very simply, the code:
- retrieves your Roman numerals;
- compares them with each 'vertical' slice of score that take place during the span in question;
- returns feedback for any moments that don't meet very simple criteria.

Currently, the comparisons involve very simple metrics for checking that:
- the proportion of notes in the score matching the corresponding Roman numeral (weighed by length) is high enough;
- the bass note you identify appears as the lowest of at least one vertical slice in the span;
- chord changes fall at relatively strong metrical positions (the measure level or next two levels down).
The feedback returns a list of those cases that don't meet the above criteria.
In some cases, there may be one or more suggestions for improvement.

As you can tell from this description, the metrics are very simple: they won't always 'get it right' (partly because it's very difficult to define what 'right' is in the abstract).
As such, you should take the feedback in the spirit it's intended: as suggestions only.
You'll likely find that it catches a few clear errors in cases where you've accidentally:
- used the wrong numeral;
- used the wrong bass;
- missed a passage;
... but it'll also flag up some areas as questionable which are actually fine.
The goal is to fix clear errors, but not necessarily to submit an analysis that returns no feedback.

Basically, we hope that this feedback will help analysts to check their work, and teachers to do a first parse through submitted work.
In short, this is supposed to give people who don't have access to music theory classes some help with their work, and to help those who are involved in formal education to use the time available efficiently.

Naturally, we welcome any feedback you might have, whether you've found errors in how the bot works, or opinions about which features are / aren't / would be useful.
We're happy to integrate further functionality, but bear in mind that anything we include will need to work automatically for all tonal music.
If you're sure your idea meets those criteria then please do get in touch, with the logical steps written out clearly and unequivocally, and preferably with some examples of edge cases that the system should / should not catch.

## Data protection and future improvements

Please note that in order to improve and extend the services we offer, we keep anonymous copies of the analyses submitted to this site.
Absolutely no personal data is retained at any time; this is strictly about advancing Four Score and More's goals of democratizing access to music theory, (we promise there's nothing nefarious going on!).
Basically, not only are you getting free, Roman numeral analysis feedback, but you're also contributing to the development of the fields of music theory and music theory pedagogy.
Whether you get the analysis 'right' or 'wrong', your analysis is an important part of the process.
We're keen on areas like this which connect the (sometimes too disparate) interests and activities of music theorists, students, musicians, and music-enthusiasts.

Conversely, if you actively want to share your analysis and be identified as its author, then simply identify yourself in the 'Analyst:' line of the Roman text file, or somewhere on the on-score analysis and we'll keep that data point.

By way of future work, we hope to improve this site by providing more specific, useful, and detailed feedback, with fewer false positives.
Please get in touch if you are interested in collaborating on that.
