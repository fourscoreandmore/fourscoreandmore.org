---
layout: post
title: 'Hauptstimme'
---

When listening to music, our attention is drawn back and forth between different elements.
Often this is guided by following the main, most prominent melodic line: the _hauptstimme_.
This task aims to capture something of that effect.

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

## Further notes, suggestions, and FAQs

**There's more than one theme at once**

- Please still chose the one you hear as 'primary', as the _hauptstimme_.
  - We're not aiming for a comprehensive analysis of all themes / motives used.
  - We only want _your view_ of the _main melody_ (which melody is most prominent, and in which instrument).
  - This is a judgement call and sometimes there's no single 'right' answer.
  - All corpora (indeed all analysis) involve some trade-off of this kind.
  - Some rules of thumb. In general, chose the ... :
     - ... *fastest-moving* part ... but not figuration / filler (melodies need a moment to breath between phrases!)
     - ... *highest part* ... but not "descant"-style lines above the main tune.
    - ... joins which *resolve voice-leading* correctly ... but not at the expense of the "true" line
    - *consistency* e.g.,:
       - In a fugue go for entrance of the subject/answer.
	  	- In a double canon pick one set of corresponding parts.

**More than one instrument is playing the main theme**

This will obviously happen a lot!
Here are some more rules of thumb:

- Chose the one you think is most prominent (e.g., flute 1, or violin 1)
	- Certain instruments tend to take priority. E.g., In choral-orchestral music, we tend to prioritise the voices. Exceptions include Bach's practice of bringing the trumpets in later-on in the moment (within corpus see the final movement of the b minor mass).
	- More generally, the loudest instruments are often the most prominent. Those trumptets again ...
- Don't bother labelling all the instruments with this theme:
  - the code ignores this information
  - we can easily retrieve this relationship between parts automatically anyway,
  - it's often useful to be made to choose the _main_ instrument, even if that's sometimes arbitrary.
- If you find that the musical choice is completely arbitrary, then opt for solutions that solve for the criteria listed in the "More than one theme" section above, e.g., staying in the same octave as the segments before and after.

**What about rests?**

- Annotations (lyrics or text expressions) must always be added to _notes_ and not rests?
  - MuseScore will let you add a lyric to a rest,
  - … but this will get lost in conversion, so avoid doing that.
- We can (often) have rests between phrases by leaving the filler unannotated (rest at the end of the preceding segment).

**Can basslines be melodic?**

- In theory, yes.
- In practice we almost never want a bassline hauptstimme annotation.
	- We can pick up the bassline as a separate part for 2-voice reduction automatically.
- Chose the bassline if there’s really nothing else going or it simply IS the melody.

**Where do themes end?**

- That's defined by where the next one starts.
- There are cases where that's not ideal, but ...
  - it's not worth doubling the scale of this task by also specifying endings,
  - we don't support overlapping here (we enforce _a single moment_ of change).

**Must I use MuseScore?**

- For the *musical preparation* of getting to know the score, you may well want to prefer to do this away from MuseScore. This part is entirely up to you! E.g., you could use
  - a physical, printed copy of the score, with …
  - an actual recording of the work … and then …
  - transfer the annotations / observations over later.
- For the *annotation / mark up* you can use any notation package that exports musicXML is fine (e.g., Dorico, Finale, Sibelius).

**What melody label / tag / names can I use?**

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
- We can also use different hauptstimme labels to annotate more different contrapuntal lines. A demonstration with the 6 voices of the Bach-Webern Ricercata will be on the repo soon.

**'More is more' or 'less is more'?**

- If in doubt, *more is more*! E.g., these annotations can also mark phrase boundaries:
  - For instance, repeatedly entering the same label (e.g., 'a') on the same instrumental part is still valuable if it indicated each iteration of a motiv. That's valuable information and doesn't detract from the main task or pose any problem for the code.
  - In such cases, it's useful to have an annotation on the start of each larger section even if the instrument and label stay the same, so again, be sure to add an extra one even if the melody stays in the same part.
- There is no *minimum length of gap*. Some moments call for extremely quick alternations e.g., occasional "hocket" such as in the first movement of the B minor mass where Bach goes back and forth every second eighth note.
	- (For certain tasks, we may use code to simplify these moments such that extremely short durations are combined, so aim to make the last such entry the start of a longer section.)
- We aim for a *maximum gap* between annotations of roughly 4 bars.