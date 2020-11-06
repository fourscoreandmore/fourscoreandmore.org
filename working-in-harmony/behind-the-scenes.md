---
layout: post
title: 'Working in Harmony'
---

_Part of [Working in Harmony](/working-in-harmony)._

## You are here

On this page:
- A 'Behind the scenes' look at how the bot works

On other pages:
- [Click here to use the app](/apps/working-in-harmony/)
- [Index](./index.md): home page for using the app
- [Notes for Analysts](./analysis.md): detailed notes on writing harmonic analyses in Roman numerals
- [Motivation](./motivation.md): why do this(?!), and more about score formats
- [Work in ... progress](./work-in-progress.md): feedback, planned improvements, data protection (we don't keep any personal data)

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
