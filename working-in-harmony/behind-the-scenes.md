---
layout: post
title: 'Working in Harmony'
---

_Part of [Working in Harmony](/working-in-harmony)._

## You are here

On this page:
- A 'Behind the scenes' look at how the bot works;
- Your feedback and future improvements;
- Data protection.

Other pages:
- [Index page](./index.md): home page for using the app
- [Notes for Analysts](./analysis.md): detailed instructions for how to encode your harmonic analysis in Roman numerals.

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
In short, this is supposed to give people who don't have access to music theory classes some help with their work, and to help those who are involved in formal education to use the limited contact time available better.

## Your feedback and future improvements

Apart from simply launching this site, we aim to continue improving the service by providing more specific, useful, and detailed feedback, with fewer false positives.

We welcome any feedback you might have, whether you've found errors in how the bot works, or opinions about which features are / aren't / would be useful.
We're happy to integrate further functionality, but bear in mind that anything we include will need to work automatically for all tonal music.
If you're sure your idea meets those criteria then please do get in touch, with the logical steps written out clearly and unequivocally, and preferably with some examples of edge cases that the system should / should not catch.

## Data protection

In order to improve and extend the services we offer, we will keep anonymous copies of the analyses submitted to this site.
Absolutely no personal data will be retained at any time; this is strictly about advancing Four Score and More's goals of democratizing access to music theory, (we promise there's nothing nefarious going on!).
Basically, not only are you getting free, Roman numeral analysis feedback, but you're also contributing to the development of the fields of music theory and music theory pedagogy.
Whether you get the analysis 'right' or 'wrong', your analysis is an important part of the process.
We're keen on areas like this which connect the interests and activities of music theorists, students, musicians, and music-enthusiasts.

Conversely, if you actively want to share your analysis and be identified as its author, then simply identify yourself in the 'Analyst:' line of the Roman text file, or somewhere on the on-score analysis and we'll keep that data point.
