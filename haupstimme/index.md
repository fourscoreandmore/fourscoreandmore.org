---
layout: post
title: 'Haupstimme'
---

When listening to music, our attention is drawn back and forth between different elements.
Often this is guided by following the main, most prominent melodic line: the _hauptstimme_.
This task aims to capture something of that effect.

# The 'Haupstimme' Annotation Task

## The Main Task, in Brief:

- Identify where the 'main' melody is throughout an orchestral movement.
  - Note: Clearly this is partly a subjective judgement. Do not aim for 'perfection'
- Name those melodies.
  - By default, simply use 'a', 'b', 'c' for each successive theme.
  - If you prefer to use names like 'fate theme' that's fine – just be consistent.
- Annotate the scores with a 'lyric' text below the start of each new melody in the relevant part, i.e.:
  - Identify the start of a theme,
  - Click on a note:
    - the specific note where the theme starts …
    - … in the most prominent instrument (e.g., the first violin),
  - Press Ctrl+L (Windows) or CMD+L (Mac) to insert a 'lyrics text'
  - Enter the theme label (e.g., 'a' for the first theme you identify) as a lyric.
  - Click anywhere else to exit the text entry mode and continue.
  - Rinse and repeat! (Copy'n'paste can be helpful here.)

## 'Melody Score'

Once we have those annotations, we can process them in various ways.
For example, we can make a 'melody score' with all these melodies stitched together in one stave.
For instance, for the start of Beethoven's 5th, 
if the score annotation looks like this (only string parts shown):

<div class="image-collection">
  <a href="https://imslp.org/wiki/Symphony_No.5,_Op.67_(Beethoven,_Ludwig_van)">
    <img src="/images/5-i.png" alt="5-i">
  </a>
</div>

... then the corresponding 'melody score' looks like this ...

<div class="image-collection">
  <a href="https://imslp.org/wiki/Symphony_No.5,_Op.67_(Beethoven,_Ludwig_van)">
    <img src="/images/5-i_Melody_Score.png" alt="5-i_Melody_Score">
  </a>
</div>

## Review phase

- Use the 'melody score' to review. It's easier to spot errors there, e.g.:
  - Missing labels (e.g., 100 measures with no change).
  - Inconsistent labels (e.g., same theme labelled differently when it returns).
- Make any changes in the original (e.g., orchestral) score (not the 'melody score').

# Further notes, suggestions, and FAQs

What happens when there's more than one theme at once?

- Please still chose the one you hear as 'primary', as the _haupstimme_.
  - We're not aiming for a comprehensive analysis of all themes / motives used.
  - We only want _your view_ of the _main melody_ (which melody is most prominent, and in which instrument).
  - This is a judgement call and sometimes there's no single 'right' answer.
  - All corpora (indeed all analysis) involve some trade-off of this kind.

What happens when more than one instrument is playing the main theme?

- This will obviously happen a lot. Chose the one you think is most prominent (e.g., flute 1, or violin 1)
  - Don't bother labelling all the instruments with this theme:
    - the code ignores this information
    - we can easily retrieve this part automatically anyway,
    - it's often useful to be made to choose the _main_ instrument, even if that's sometimes arbitrary.
  - If you find that the musical choice is completely arbitrary, then opt for one
    - that will connect to those around it e.g.
    - in the same octave (often this is within the 2 octaves above middle c)
  - If you really can't choose between two equally viable options, flip a coin!

Must I always add lyrics to _notes_ and not rests?

- Yes. MuseScore will let you add a lyric to a rest,
  - … but this will get lost in conversion, so avoid doing that.

Can I specify that the melody is in the second voice (e.g., flute 2)?

- Sure, just make sure your lyric is in voice 2 (MuseScore colours it green).

Where do themes end?

- Don't worry about where themes end: For now, we assume that's defined by where the next one starts. There are cases where that's not ideal, but
  - it's not worth doubling the scale of this task by also specifying endings,
  - we don't support overlapping here (we enforce _a single moment_ of change).

Must I use MuseScore?

- For the musical preparation of getting to know the score, you may well want to prefer to do this away from MuseScore. This part is entirely up to you! E.g., you could use
  - a physical, printed copy of the score, with …
  - an actual recording of the work … and then …
  - transfer the annotations / observations over later.
- For the annotation / mark up, yes preferably.
  - If you really want to use another software like Finale or Sibelius, then ok we can make that work. Please ask.
  - If you want to just write down the measure and beat numbers 'off score' that's possible too. Please ask.

What melody label / tag / names can I use?

- In general, just use 'a', 'b', etc.
  - We all know that these themes will be altered at subsequent appearances, but if you really want to indicate a greater change from 'a' etc., then you might like to adopt one of the following conventions:
    - Brackets: (a)
    - Prime: a'
    - Combinations: a+b
    - 'Dev': a-dev
- That said, you're welcome to use anything you like. Feel free to go into detail:
  - E.g., "first subject group, main, 'fate' theme, motiv x"
  - (… but obviously it's a lot more work to keep track of all that.)
- While the _hauptstimme_ will usually be melodic, there are some moments with cadential fragments or the like where you want to register the movement between instruments, but where no melodic label fits. We have two main options in these cases:
  - use the prevailing melodic label (if it feels like a continuation of the context)
  - reserve a new special label like 'x' for these 'non-melodic melodies'.

'More is more' or 'less is more'?

- If in doubt, more is more! E.g., these annotations can also mark phrase boundaries:
  - For instance, repeat 'a', 'a', 'a' for each iteration of a motiv, even if it's within the same part. That's valuable information and doesn't detract from the main task.


