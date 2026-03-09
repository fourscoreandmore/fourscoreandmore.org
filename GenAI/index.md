---
layout: post
title: 'Generative AI Tools in Music'
---

Generative AI (aka GenAI) is a fast moving field, and
the provision of generative tools for music specifically is no exception to this.
To make sense of that, several teams have provided summaries.
Now there are a lot of summaries,
so here's a summary of the summaries,
and a few signposts that might be useful.

No knowledge is assumed, and we begin at the more fundamental level of defining
the different musical tasks to which you GenAI might be applied.

In brief:
- Title: 'Generative AI Tools in Music'
- By: Mark Gotham, 2026
- Licence: CC-By-SA
- Suggestions/contributions: Are welcome! PR or see [email contact details here](https://markgotham.github.io/)

> On this page:
> - [Tasks](#tasks)
> - [Use Cases](#use-cases)
> - [Summaries of tools available](#summaries)

---

# Tasks

There are many different tasks which GenAI can engage.
Often, breaking down a large creative task into smaller component parts allows the human to have a more active role.
Here are some example tasks, with notes and corresponding tools.

> In this section:
> - [Text to Music (text → audio)](#text-to-music-text--audio)
> - [Audio from scratch (nothing → audio)](#audio-from-scratch-nothing--audio)
> - [Symbolic from scratch (nothing → symbolic)](#symbolic-from-scratch-nothing--symbolic)
> - [Transcription (audio → symbolic)](#transcription-audio--symbolic)
> - [Source separation (mixed audio → audio in separate parts)](#source-separation-mixed-audio--audio-in-separate-parts)

### "Text to Music" (text → audio)

Going from a user's text prompt to an audio output
(also called "text to music" or "TTM")
is probably the most familiar GenAI use case.
As always, the results depend on many factors
chief among them, the model and the prompt.

Among the many apps providing this, is Stable Audio,
which we highlight for a few reasons including:
- It comes top of many metrics for openness (see below)
- The team have provided ["Prompt Guide" here](https://stability.ai/learning-hub/stable-audio-25-prompt-guide).
- The option to combine TTM with an audio prompt.*

*This model (among others) allows the user to 
combine (or even replace) the text prompt with audio.
In that case, we're not talking about
"text → audio"
so much as
"audio → audio"
or even
"text+audio → audio".
Use cases include the creation of new audio to fix with an existing template,
where "fit" could include matching the tempo
(to align in the timings) and/or the style. 


### Audio from scratch (nothing → audio)

What really is audio?
As a data type, audio is a form of time-series data.
To understand the nature of this data,
[here is a very basic demo for exploring raw audio sound data](https://github.com/music-computing/amads/blob/main/notebooks/explore_sound.ipynb).

A **Digital Audio Workstation** (DAW, pronounced to sound like "door") is a type of software application
for handling audio, in which you can record, edit, mix, and more.
These days, many DAW's have AI features internally.
[Here is Wiki's comparison of digital audio editors](https://en.wikipedia.org/wiki/Comparison_of_digital_audio_editors)
and here is a new open source DAW with the most pleasingly apposite name of "Open DAW":
- [About Open DAW](https://opendaw.org/)
- [Get started with the Open DAW Studio](https://opendaw.studio/)

Further hints:
- To create your own audio from nothing, use **sound synthesis**
(using any number of tools including many right there in the DAW).
- Additionally and/or alternatively, you might want to start working with existing
audio files e.g., as **samples** and building music with these blocks, Lego-style.
Again, all DAWs include some samples
and here are some external sources of samples with open licences:
  * [Free sound](https://freesound.org/)
  * [Soundcamp](https://soundcamp.org/)


### Symbolic from scratch (nothing → symbolic)

To engage with "the notes", you need to access those notes.
DAW's often feature some basic (limiter) controls of this kind.
Again, to understand this data a bit better,
[here is a very basic demo for exploring symbolic data](https://github.com/music-computing/amads/blob/main/notebooks/explore_symbolic.ipynb).

To create your own symbolic data from nothing, you might use:
- a **music notation app**. [Wikipedia has a summary of "score writers" here](https://en.wikipedia.org/wiki/Comparison_of_scorewriters).
- **programmatic interfaces** like music21 (more likely) or AMADS / partitura (less likely, they are more geared towards analysis)

Alternatively, start working with **existing symbolic data**.
There are many sites hosting musical scores, of varying and often unclear quantity and quality.
By contrast, "Datasets for Symbolic Music Processing" are typically clearer.
[I list some datasets at the end of my "Keeping Score" book](https://doi.org/10.5281/zenodo.14938027) 

Some systems include **Generative AI for symbolic music**.
[WeaveMuse](https://github.com/manoskary/weavemuse)
includes that functionality (among others spanning understanding and generation).


### Transcription (audio → symbolic)

Automatic Music Transcription (AMT) is the task of extracting symbolic data from raw audio.

Tools include:
- [Essentia](https://github.com/MTG/essentia)
- [Klang](https://klang.io/)


### Source separation (mixed audio → audio in separate parts)

As mentioned above, audio is time-series data.
All the signal and noise (literally) are mixed together.
For many use cases, it is necessary/helpful to separate the component parts of this sound (e.g. guitar based drums).
For example, source separation can help with,
- transcription (of music and/or lyrics),
- alignment,
- recognition/detection (of instruments, musicians, lyrics, ...).

Models include:
- [Audio Shake](https://www.audioshake.ai/)
- [Fadr](https://fadr.com/stems)
- Meta's ["Segment Anything Model" (SAM)](https://ai.meta.com/sam2/) which separates a target source based on text, visual, or temporal prompts.

See also
- Jordi Pons' [“SAM Audio Explained” blog post](https://artintech.substack.com/p/sam-audio-explained)
- ["Open Source Tools & Data for Music Source Separation"](https://source-separation.github.io/tutorial/landing.html)
by Ethan Manilow, Prem Seetharaman, and Justin Salamon (Adobe).

---

# Use Cases

> In this section:
> - [AI-Assisted Music Production](#ai-assisted-music-production)
> - [AI Song Contest](#ai-song-contestants)
> - [Artistic Trends](#artistic-trends)

Studies of previous use cases include experimental studies in the "lab" and surveys of uses in "the wild".
Both can give ideas for how you might use these tools.

Even where there is an experimental setup (as in Ronchini et al.),
these are not typically released publicly, so this is for information and ideation only.

### AI-Assisted Music Production
_Dated: Nov 2025_

Ronchini et al.'s ["AI-Assisted Music Production" paper](https://zenodo.org/records/17488808)
is an experimental study of how users engage with AI tools, especially "text to music" (TTM).
studies

### AI Song Contestants
_Accessed: September 2025_

The [AI Song Contest](https://www.aisongcontest.com) is probably the premiere venue for AI-based composition today.
Many winning and shortlisted entries from recent years are on the site, including an account of how the piece was made. 

### Artistic Trends
_Dated: July 2025_

The team at Stability AI (Jordi Pons et al.)
recently reviewed how GenAI has been used in recent music artistic work "in the wild".
This covers "A collection (337 artworks) of AI music released before July 31, 2025"
and includes model details.
- Data:
  - [Main page (GitHub) for the data](https://github.com/jordipons/ai-music-artistic-trends/)
  - [Actual List here](https://github.com/jordipons/ai-music-artistic-trends/blob/main/337.csv).
- Summary:
  - [Full paper (arXiv)](https://arxiv.org/abs/2508.11694)
  - [Blog](https://artintech.substack.com/p/report-artistic-trends-in-ai-music)
  - [Video](https://vimeo.com/1109592373)


---

# Summaries

> In this section:
> - [AI Song Contest](#ai-song-contest)
> - [Fairly Trained](#fairly-trained)
> - [Responsible AI](#responsible-ai)
> - [Survey on evaluation](#survey-on-the-evaluation-of-generative-models-in-music)


### AI Song Contest
_Accessed: September 2025_

The [AI Song Contest](https://www.aisongcontest.com) (mentioned above)
also includes a list of models, organised around use case (lyrics, composition, and more).
The [largest of those lists is here](https://docs.google.com/spreadsheets/d/1fic0FhZQu6qb-C-T02LTggZN3j6CrvNC6BRnrIH6zsY/edit?gid=990931099#gid=990931099).


### Fairly Trained
_Accessed: September 2025_

"Fairly trained" offers accreditation for models that are trained fairly (the clue's in the name).

[Their list of certified models is provided here](https://www.fairlytrained.org/certified-models).

As of September 2025, there are 19 total:
- 12 from Fairly trained's "Company certification",
- 2 from "Product certification",
- 5 from "Model certification",


### MusGO
_Accessed: Jan 2026 (but the authors plan continuous updates)_

The ["MusGO Framework"](https://roserbatlleroca.github.io/MusGO_framework/index.html)
from the Music Technology Group in Barcelona
serves to assess openness in gen AI model for music.

The author highlight the following attributes (quote):
- multidimensional with 13 categories 
- graded with different levels of openness 
- divided into essential and desirable categories 
- refined with feedback from +100 MIR members 
- continuously updated

The "Stable Audio Open" model (mentioned above) currently comes out on top.


### Responsible AI
_Dated: July 2025_

The Responsible AI (RAI) team at UAL (University of the Arts, London, UK)
has produced
"A Short Review of Responsible AI Music Generation".
(Elizabeth Wilson et al.,
Proceedings of the 6th Conference on AI Music Creativity, AIMC 2025).
The paper has a tabular summary (no need to replicate that here)
and the team have also provided a model explorer online.

- [Paper](https://doi.org/10.5281/zenodo.16946342) which includes input/output details.
- [Interactive "model explorer" here](https://modelexplorer.musicrai.org/)
which is in some ways more user-friendly but doens't have the I/O (feature requested)


### Survey on the Evaluation of Generative Models in Music
_Dated: October 2025_

And finally, the thorny issue of evaluation.
Do these systems “work”?
What does “work” mean in this context?

Here is an important
[“Survey on the Evaluation of Generative Models in Music”](https://dl.acm.org/doi/10.1145/3769106)
by Lerch et al.


---
