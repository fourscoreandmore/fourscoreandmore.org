---
layout: post
title: 'MusoRepo: a Directory of Resources for Computational Musicology'
---

This is a list of links to resources for computational musicology, with a focus on working with symbolic scores.
All of the resources are free and open source/access, except where specified.

There are other, excellent lists out there compiled and hosted by institutions like:

* [CCARH: Digital Resources for Musicology](https://wiki.ccarh.org/wiki/Digital_Resources_for_Musicology)
* [ISMIR: Resources list](https://www.ismir.net/resources.html) – research centers, datasets and more, mostly for audio analysis.
* [SMT: Music Informatics Group (login required)](https://sites.google.com/site/smtmig/)

... and individuals like [noteflakes](https://github.com/noteflakes/awesome-music) as part of the
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
series.

There are also many lists for more specific tasks and subjects.
Many of these are included in the relevant section below.

I have / will contribute this content to those lists where appropriate, but I think that this list is sufficiently distinct to warrant a separate existence, particularly in light of the focus on working with scores.
Please do reach out if you would like to contribute an item to this list, or if you have a suggestion for how to organize it better, or perhaps even a grand idea for us list makers should coordinate our efforts.

## Contents

On this page:

* [Datasets (including scores)](#datasets)
* [Formats](#formats)
* [Metadata (including linked open data)](#metadata)
* [Software](#software)
* [Teaching](#teaching)
* [Venues](#venues)

*Not* on this page:

* Research Groups. I've now integrated this section into the ISMIR website for which the [source code is here](https://github.com/ismir/ismir-home/blob/master/docs/pages/research-centers.md) and the public-facing [website is here](https://www.ismir.net/resources/research-centers/).


## Datasets

Lists of MIR-focussed datasets include several that are explictily audio-focussed, such as Alexander Lerch's list for ['audiocontentanalysis.org/']
(https://www.audiocontentanalysis.org/datasets).

These are often cross-listed, but don't seem to be maintained/updated:

* [Colin Raffel](https://colinraffel.com/wiki/mir_datasets),
* [dharasim's MCR](https://github.com/dharasim/MCR/wiki)
* [Georg Holzmann](https://grh.mur.at/sites/default/files/mir_datasets_0.html)

### Analysis

Analysis datasets (e.g., of harmony, form, ...) are growing in number and sophistication.
Here are some:

* [Annotated Beethoven Corpus](https://github.com/DCMLab/ABC) – Harmonic analysis of the Beethoven String Quartets.
* [Beethoven Piano Sonata with Functional Harmony dataset (BPS-FH)](https://github.com/Tsung-Ping/functional-harmony) – harmonic and formal analyses of the first movements of Beethoven Piano Sonatas.
* [GTTM](https://gttm.jp/gttm/) – Masatoshi Hamanaka's XML markups of musical examples from (and using the tree structure representation of) A Generative Theory of Tonal Music (Lerdahl and Jackendoff 1983).
* [Machine-readable Schenkerian analyses](https://www.cs.rhodes.edu/~kirlinp/diss.html).
* ['Taking-Form'](https://github.com/MarkGotham/Taking-Form) – formal analysis of c.150 Mozart and Beethoven movements along with conversion code.
* [TAVERN](https://u.osu.edu/tavern/) – Theme And Variation Encodings with Roman Numerals. 27 sets of variations by Mozart and Beethoven.
* ['When in Rome'](https://github.com/MarkGotham/When-in-Rome) – a collection of harmonic analysis datasets in the 'Roman Text' format combining new corpora with conversions of all existing ones (ABC, BPS-FH, and TAVERN as above).

### Datasets related to scores (e.g., of chord progressions)

* [Algomus group datasets](https://algomus.fr/data/) – fugues, sonatas and more
* [‘Annotated jazz chord progression corpus’](https://jazzparser.granroth-wilding.co.uk/ParserPaper.html) – Mark Granroth-Wilding and Mark Steedman
* [Billboard Project (DDMAL)](https://ddmal.music.mcgill.ca/research/billboard) – chords, structure, instrumentation, and timing annotations of Billboard chart hits.
* [EWLD (Enhanced Wikifonia Leadsheet Dataset)](https://zenodo.org/record/1476555#.XGXW4eJKjMI) – more than 5,000 leadsheets and rich metadata based on the crowd-source 'Wikifonia' corpus (see below).
* [iRb Jazz Corpus](https://csml.som.ohio-state.edu/home/index.php/iRb_Jazz_Corpus) – OSU
* [Isophonics](https://www.isophonics.net/datasets) – data (and software) from the [Centre for Digital Music (‘C4DM’)](https://c4dm.eecs.qmul.ac.uk/) across a range of repertoires and parameters (structure, key, chord, beats).
* [Jazzomat Research Project’s ‘Weimar Jazz Database’](https://jazzomat.hfm-weimar.de/dbformat/dbcontent.html)
* [Jazz Audio-Aligned Harmony (JAAH) Dataset](https://zenodo.org/record/1290737#.W6vIKxNKixM) – 113 tracks selected from Smithsonian jazz collections. See also [MTG's Open Source Technologies](https://mtg.github.io/JAAH/)
* [Peachnote](https://www.peachnote.com/datasets.html) – Ngrams of melodies and chord progressions from IMSLP c.2011.
* [Pop/rock chord progressions](https://rockcorpus.midside.com) from deClercq and Temperley 2011
* [RWC Music Database](https://staff.aist.go.jp/m.goto/RWC-MDB/) – various repertoires, permission required
* [Temperley / Kostka-Payne chords](https://davidtemperley.com/kp-stats/) – by Temperley, after the textbook by Kostka and Payne. Direct download [here](https://davidtemperley.com/wp-content/uploads/2016/09/kp-corpus-files.zip)
* ‘Wikifonia’ – corpus of lead sheets (vocal lines and harmonies). NB: no longer hosted online. (See also 'EWLD' above).
* [YCAC Dataset](https://ycac.yale.edu/) – .csv datasets of pitch 'slices' from the [Classical Archives](https://www.classicalarchives.com/) MIDI corpus

### Encoded scores

* [Choral Public Domain Library (CPDL)](https://www.cpdl.org/) – vocal music in a range of formats
* [ELVIS](https://database.elvisproject.ca/) – metacorpus, various formats.
* [JRP](https://josquin.stanford.edu/) – krn format. Works by Josquin and contemporaries.
* [Kern Scores](https://kern.ccarh.org/) – krn format.
* LvH corpora: krn format files with vocal lines of songs by composers from [France](https://github.com/leighvh1/19th-century-art-songs-by-French-composers) and [Germany](https://github.com/leighvh1/19th-century-art-songs-by-German-composers),
now mostly included in the [OpenScore Lieder](https://github.com/OpenScore/Lieder).
* [MuseData](https://www.musedata.org/) – MuseData format, mostly Baroque and Classical music.
* [music21 Corpus](https://web.mit.edu/music21/doc/about/referenceCorpus.html)
* [Mutopia](https://www.mutopiaproject.org)
* [Nottingham dataset, cleaned version](https://github.com/jukedeck/nottingham-dataset)
* [Neuma](https://neuma.huma-num.fr/) – metacorpus, various formats.
* [OpenScore](https://openscore.cc/) – the initial effort, vastly surpassed by two "satellite" projects: 
	* **OpenScore Lieder**. ~1,300 songs on [musescore.com](https://musescore.com/openscore-lieder-corpus) and with a [GitHub Mirror](https://github.com/OpenScore/Lieder).
	* **OpenScore String Quartets**. ~100 (multi-movement) quartets on [musescore.com](https://musescore.com/openscore-string-quartets) and again with a [GitHub Mirror](https://github.com/OpenScore/StringQuartets/)
* [Public Domain Song Anthology](https://aperio.press/site/books/10.32881/book2/) – a book of leadsheets in several formats.
* [Tasso in Music Project](https://www.tassomusic.org/) – Digital Edition of the [Musical] Settings of Torquato Tasso's Poetry.

### MIDI

* [Band-in-a-Box Jazz standards](https://bhs.minor9.com/)
* [BitMidi](https://bitmidi.com/)
* [Classical Archives](https://www.classicalarchives.com/) – crowd-sourced, restrictions on download-at-scale
* [Kunst der Fuge](https://www.kunstderfuge.com/) – crowd-sourced, restrictions on download-at-scale
* [Lakh MIDI Dataset](https://colinraffel.com/projects/lmd/)
* [MAESTRO (MIDI and Audio Edited for Synchronous TRacks and Organization)](https://magenta.tensorflow.org/datasets/maestro) – piano performances with fine alignment between note labels and audio waveforms.
* The 'Midi man' collection. 130,000 Midi Files across all genres. See [this article](https://www.reddit.com/r/datasets/comments/3akhxy/the_largest_midi_collection_on_the_internet/) and [this website](https://mega.nz/#!Elg1TA7T!MXEZPzq9s9YObiUcMCoNQJmCbawZqzAkHzY4Ym6Gs_Q)

### Scores as *images* (not encoded)

* [Digital Image Archive of Medieval Music (DIAMM)](https://www.diamm.ac.uk/)
* [Diva.js](https://ddmal.github.io/diva.js/)
* [Europeana](https://www.europeana.eu/portal/en) – includes music
* [Gesualdo Online](https://ricercar.gesualdo-online.cesr.univ-tours.fr/) – MEI sources also available
* [HathiTrust Research Center](https://www.hathitrust.org/) – includes music
* [International Music Score Library Project (IMSLP)](https://imslp.org) – some encodings, primarily PDF
* [Measuring Polyphony](https://measuringpolyphony.org/) – polyphonic, late-medieval music
* [Web Library of Seventeenth-Century Music (WLSCM)](https://www.sscm-wlscm.org) – Open access, peer-reviewed editions of seventeenth-century music.


## Formats

### Notation

Many apps exist for notation, engraving, and score rendering.
Start with [Wikipedia's 'Comparison of scorewriters'](https://en.wikipedia.org/wiki/Comparison_of_scorewriters) to compare many including:

- [Dorico](https://www.steinberg.net/en/products/dorico.html),
- [Finale](https://www.finalemusic.com/), [FORTE](https://www.fortenotation.com/en/products/writing-scores/forte-home/), 
- [Lilypond](http://lilypond.org/) and editors including
	- [Denemo](http://www.denemo.org/), 
	- [Frescobaldi](https://sourceforge.net/projects/frescobaldi.mirror/), and
	- [Hacklily](https://www.hacklily.org),
- [MuseScore](https://musescore.org/), 
- [Notion](https://www.presonus.com/products/Notion/),
- [Sibelius](https://www.avid.com/sibelius),
- and more!

... in addition to which, see also these open source options:

* [Abjad](http://abjad.mbrsi.org/#)
* GUIDO [Music Notation Format (GMN)](http://guidolib.sourceforge.net/GUIDO/) and [Engine Library](http://guidolib.sourceforge.net)
* SCORE: abandonware, but see Craig Sapp’s [Scorelib](http://scorelib.sapp.org/) library for parsing SCORE data files.
* [VexFlow](http://www.vexflow.com)
* [Verovio](http://www.verovio.org) - 'a fast, portable and lightweight open-source library for engraving Music Encoding Initiative (MEI) music scores into SVG.'

... and these online-only applications (all commercial):

* [Flat](https://flat.io/)
* [forScore](https://forscore.co/)
* [irealpro](https://irealpro.com/) - real time accompaniment also supporting chord charts
* [neoScores](https://www.gogustaf.com/)
* [Newzik](https://newzik.com/)
* [Nkoda](https://www.nkoda.com/)
* [Noteflight](https://www.noteflight.com/)

Finally, see also the [Scoring Notes](https://www.scoringnotes.com/) blog and podcast for recent news and reviews.

### Optical Music Recognition (OMR)

See [Wikipedia's comparison](https://en.wikipedia.org/wiki/Optical_music_recognition) for:

* commercial software like:
	* [musitek](http://www.musitek.com/),
	* [sharpeye](http://www.musicaleditor.com/scan-music.html), and 
	* [SmartScore](https://www.musitek.com/smartscore-pro.html), 
* ... as well as open-source/freeware like
	* [Audiveris](https://github.com/Audiveris/audiveris/wiki).

... in addition to which:

* [enote](https://enote.com/about.html) - [not free]
* [PlayScore/ReadScoreLib](http://www.playscore.co/readscorelib/) by [SeeScore](https://www.seescore.co.uk/) - [not free]

### Other Standard Formats

* [IEEE 1599](http://ieee1599.lim.di.unimi.it/) - multi-layer XML-based format for music.
* [MEI (Music Encoding Initiative)](http://music-encoding.org/) - an open-source effort to define a system for encoding musical documents in a machine-readable structure.
* [MIDI](https://www.midi.org)
* MNX File format (forthcoming) - [draft specifications](https://w3c.github.io/mnx/specification/).
* [MusicXML](http://www.musicxml.com/) - the standard open format for exchanging digital sheet music.
* [SMuFL (Standard Music Font Layout)](http://www.smufl.org/) - a specification for mapping music symbols to Unicode for use in music fonts.
* XXX - Further (not international standard) file formats supported by music21: ABC, Capella, Humdrum, MuseData, Noteworthy, NoteworthyBinary, Scala, TinyNotation (native to music21), Volpiano


## Metadata

Metadata and linked data feature through many of the [venues listed below](#venues), especially [DLfM](https://dlfm.web.ox.ac.uk).
Naturally, this intersects with other/wider fields in library studies and data managements.

Here are online sites (libraries and companies) offering and/or working with linked data relevant to music:

- [AllMusic](https://www.allmusic.com/)
- [Classical Archives](https://www.classicalarchives.com/)
- [Discography of American Historical Recordings (DAHR)](https://adp.library.ucsb.edu/)
- [Discogs](https://www.discogs.com/)
- [Genius](https://genius.com/)
- [International Music Score Library Project (IMSLP, aka Petrucci Music Library)](https://imslp.org/)
- [Internet Broadway Database (IBDb)](https://www.ibdb.com/)
- [Internet Movie Database (IMDb)](https://www.imdb.com/)
- [iTunes](https://itunes.apple.com/)
- [last.fm](https://www.last.fm/)
- [Library of Congress](https://id.loc.gov/)
- [MusicBrainz](https://musicbrainz.org/)
- [Muziekweb (music library of the Netherlands)](https://www.muziekweb.nl/)
- [Music Ontology data](http://musicontology.com/)
- [Open Library](https://openlibrary.org/)
- [Pandora](https://www.pandora.com/) - (not all countries/territories)
- [Rate Your Music](https://rateyourmusic.com/)
- [SecondHandSongs](https://secondhandsongs.com/)
- [Social Networks and Archival Context (SNAC)](http://snaccooperative.org/)
- [Songkick](https://www.songkick.com/)
- [SoundtrackCollector](https://soundtrackcollector.com/)
- [Deezer](https://www.deezer.com/)
- [SoundCloud](https://soundcloud.com/)
- [Spotify](https://open.spotify.com/)
- [Trove (National Library of Australia)](https://nla.gov.au/)
- [Amazon](https://www.amazon.com/)
- [Virtual International Authority File (VIAF)](https://viaf.org/)
- [Visual Arts and Games, Music of (VGMdb)](https://vgmdb.net/)
- [WhoSampled](https://www.whosampled.com/)
- [Wikidata](https://www.wikidata.org/)
- [WorldCat](https://www.worldcat.org/)

There are also many (not music-specific) national libraries including:

- [Bibliothèque nationale de France (BnF)](https://catalogue.bnf.fr/)
- [Deutsche Nationalbibliothek (DNB)](https://d-nb.info/)
- [National Diet Library, Japan](https://www.ndl.go.jp/)
- [National Digital Library of India](https://ndl.iitkgp.ac.in/)

## Software

This section lists some main other relevant apps, software, and code Libraries for scores.

### Analysis / Parsing / Manipulation of Scores

* [Humdrum](https://www.humdrum.org/)
* [jfugue](https://www.jfugue.org/) – writing programs that create music. Java and JVM languages
* [Midifile](https://midifile.sapp.org/) – library for parsing Standard MIDI Files from [Craig Sapp](https://ccrma.stanford.edu/~craig/)
* [music21 (p)](https://web.mit.edu/music21/) – python
* [music21 (j)](https://web.mit.edu/music21/music21j/doc/index.html) – javascript
* ['Spectral Orchestrator' (SPORCH)](https://sourceforge.net/projects/sporch/) – harmonies/orchestrations from digitally recorded sound files.
* [Timidity](https://timidity.sourceforge.net/) – command line synthesizer that plays MIDI files from [Tuukka Toivonen](https://tuukkatoivonen.org).

### Digital music-making

* [OpenMusic](https://repmus.ircam.fr/openmusic/home) – Computer-assisted composition.
* [Chuck](https://chuck.stanford.edu) – strongly-timed, concurrent, and on-the-fly music programming language.
* [Common Music / GRACE](https://sourceforge.net/projects/commonmusic/) – Live-coding
* [Max/MSP](https://cycling74.com/products/max/) – Real-time audio manipulation [not free]
* [Open Software System for Interactive Applications (OSSIA)](https://ossia.io) – Open-source intermedia sequencer  (previously ‘i-score’)
* [Overtone](https://overtone.github.io/) – Live-coding. See also the [Leipzig](https://github.com/ctford/leipzig) composition library for Clojure and Clojurescript.
* [Sonic Pi](https://sonic-pi.net/) – Live-coding
* [SuperCollider](https://supercollider.github.io/) – Live-coding

### Edition

* [Beethovens Werkstatt](https://beethovens-werkstatt.de)
* [Digitale Musikedition](www.edirom.de) – based on Frans Wiering’s idea of a “multidimensional model” of a musical edition
* [Freischütz Digital](www.freischuetz-digital.de)
* [Digitale Mozart-Edition](https://dme.mozarteum.at)
* [OCVE](www.chopinonline.ac.uk/ocve/) – Collection and comparison of primary source Chopin scores
* [OPERA](www.opera.adwmainz.de/informationen.html)
* [Tido](https://www.tido-music.com/) – [not free]

### Visualisation / Annotation

* "Timeliner" annotation tools:
	* [Audio Timeliner](https://www.singanewsong.org/audiotimeliner/)
	* [Briformer](https://www.brianedwardjarvis.com/MusicTheoryWebApps/BriFormer/briformer.html)
	* [TiLiA](https://tilia-ad98d.web.app/)
* [Dezrann](https://www.dezrann.net/)
* [Marcomusy’s 'pianoplayer'](https://github.com/marcomusy/pianoplayer) — automatic fingering for any xml score
* [mdecks](https://mdecks.com/mapharmony.phtml) [not free]
* [Peachnote](https://www.peachnote.de/) – apps including
	* [Tuttitempi](https://tuttitempi.com/): Score-aligned visualisation of the tempi used in multiple recordings.
* [Music Connection Machine](https://www.musicconnectionmachine.org/)
* [XronoMorph](https://www.dynamictonality.com/xronomorph.htm) – app for creating rhythmic and melodic loops

## Teaching

### Audio Textbooks

There are many textbooks on audio and particularly on the wider subject of signal processing.
Two notable releases from protagonists of the ISMIR community:

* Alexander Lerch: *An Introduction to Audio Content Analysis*. 
	* [own website](https://www.audiocontentanalysis.org/datasets),
	* [on IEEE](https://ieeexplore.ieee.org/servlet/opac?bknumber=9965970)
* Meinard Müller’s *Fundamentals of Music Processing* (Springer, 2015/2021):
	* [Overview and links](https://www.audiolabs-erlangen.de/fau/professor/mueller/bookFMP)
	* ["FMP Notebooks": Python Notebooks for Fundamentals of Music Processing](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C0/C0.html)

### Apps for Music Theory, Fundamentals, Aural Skills

Free and open:

* [Four Score and More](https://fourscoreandmore.org/) – music theory resources including automatic score exercises generation
* [musictheory.net](https://www.musictheory.net) – Lessons and exercises (freemium)
* [Music Theory Practice](https://music-theory-practice.com) and their [external recommendations](https://music-theory-practice.com/best-online-music-theory-courses.html)
* [Music Theory Tutor](https://musictheorytutor.weebly.com/index.html) – free lessons over video conferencing
* [The "Open Music Theory" online textbook.](https://viva.pressbooks.pub/openmusictheory/).
This c.200k word survey of Western music theory has attracted c.1.5 million visitors to date.
It is an expansion of the (concept of) a v.1 hosted [here)](http://openmusictheory.com/)

Not free (commercial apps):

* [Ars-Nova](https://www.ars-nova.com/home6.html) – including 'Practica Musica', 'Counterpointer', 'Songworks', 'Musica Touch', 'Rythmist'
* [Artusi](https://www.artusi.xyz) – interactive music theory exercises.
* [Auralia and Musition (from 'Rising Software')](https://www.risingsoftware.com/) – aural and fundamentals training
* [Chordify](https://chordify.net) – songwriting / leadsheets [fremium]
* [Harmonia](https://harmonia.illiacsoftware.com)
* [Hook Theory](https://www.hooktheory.com) – songwriting / leadsheets
* [Indiana MFO](https://www.music.indiana.edu/departments/academic/music-theory/mfonline/about.shtml)
* [Meludia](https://www.meludia.com/en/): Aural skills and ear training without staff notation
* [nSpireMe](www.nspireme.co.uk)
* [SmartMusic](https://www.smartmusic.com) – [not free]
* [Teoria](https://www.teoria.com)
* [tx2Mus](https://wmich.edu/mus-theo/tx2mus/) – online music dictation tool by David Loberg Code

### ... And more

- The MEI has a [pedagogy resources page](https://music-encoding.org/resources/pedagogy.html)
- There are also various guides to specific code libraries that serve partially /incidentally to teach symbolic music content, e.g., the music21 [User guide](https://web.mit.edu/music21/doc/usersGuide/index.html)

## Venues

Below is a list of relevant venues (journals and conferences).
In addition, there are also various music industry trade fairs.
Note that the *MusicMesse* no longer runs in Frankfurt Germany,
it is now hosted in [Shanghai, China](https://music-china.hk.messefrankfurt.com/).

### Journals and Conferences

Notes on the table:

- The “full title” is the official name,
- The “short title” removes specific words that are common to many (e.g., “conference on”),
regions (like “Australasian”, “European”),
and publishers (“ACM” and “IEEE”).
This assists with easy searching by topic (and the info is still there in the full title).
- “J/C” stands for conference or journal. Please note that distinction between the two is more slight in computer science than many other contexts (e.g., most conferences have extensive peer review and full publication of written proceeding).
- “Music?” stands for “Is there a musical term in the title?”: i.e., is this primarily about music?
Here “musical terms” include “composition” and similar, as far as “audio” and “acoustics”, but not “sound” or “signal” alone.
- This table is sorted by “Music?”, then short title.


Short Title / Theme|Full Title|URL|J/C?|Music?|Last checked
| --- | --- | --- | --- | --- | --- |
AI Music Creativity|Conference on AI Music Creativity (AIMC)|[Click here](https://2022.aimusiccreativity.org)|Conference|Yes|Jan-24
Audio Engineering Society|Journal of the Audio Engineering Society|[Click here](http://www.aes.org/journal/)|Journal|Yes|Jan-24
Audio Technologies for Music and Media|Audio Technologies for Music and Media (ATMM)|[Click here](http://atmm-conference.org/)|Conference|Yes|Jan-24
Audio, Speech, and Music Processing|EURASIP Journal on Audio, Speech, and Music Processing|[Click here](http://asmp.eurasipjournals.com/)|Journal|Yes|Jan-24
Auditory Displays|International Conference on Auditory Displays (ICAD)|[Click here](https://icad.org/)|Conference|Yes|Jan-24
Cognitive Sciences of Music|European Society for the Cognitive Sciences of Music (ESCOM)|[Click here](https://www.escomsociety.org/)|Conference|Yes|Jan-24
Computational Intelligence in Music, Sound, Art, and Design|EvoMUSART: International Conference on Computational Intelligence in Music, Sound, Art, and Design (Part of EvoStar)|[Click here](https://link.springer.com/conference/evomusart)|Conference|Yes|Jan-24
Computer Music|Computer Music Journal (CMJ)|[Click here](https://www.mitpressjournals.org/loi/comj)|Journal|Yes|Jan-24
Computer Music Conference|Australasian Computer Music Conference (ACMC)|[Click here](http://acma.asn.au/conferences/)|Conference|Yes|Jan-24
Computer Music Conference|International Computer Music Conference (ICMC)|[Click here](http://www.computermusic.org/)|Conference|Yes|Jan-24
Computer Music Journal|Computer Music Journal|[Click here](http://www.mitpressjournals.org/cmj)|Journal|Yes|Jan-24
Computer Music Multidisciplinary Research|International Symposium on Computer Music Multidisciplinary Research (CMMR)|[Click here](http://www.cmmr2020.gttm.jp/)|Conference|Yes|Jan-24
Contemporary Composition|International Journal of Contemporary Composition|[Click here](http://www.ijournalcc.com/)|Journal|Yes|Jan-24
Creative Music Systems|Journal of Creative Music Systems (JCMS)|[Click here](https://www.jcms.org.uk/)|Journal|Yes|Jan-24
Digital Audio Effects|International Conference on Digital Audio Effects (DAFX)|[Click here](http://www.dafx.de/)|Conference|Yes|Jan-24
Digital Libraries for Musicology|Digital Libraries for Musicology (DLfM)|[Click here](https://dlfm.web.ox.ac.uk)|Conference|Yes|Jan-24
Digital Music Research Network|Digital Music Research Network|[Click here](https://www.qmul.ac.uk/dmrn/)|Conference|Yes|Jan-24
Electroacoustic Music Studies|Electroacoustic Music Studies (EMS) Network Conference|[Click here](http://www.ems-network.org/)|Conference|Yes|Jan-24
Empirical Musicology Review|Empirical Musicology Review (EMR)|[Click here](http://emusicology.org/)|Journal|Yes|Jan-24
Interdisciplinary Music Studies|Journal of Interdisciplinary Music Studies (JIMS)|[Click here](http://musicstudies.org)|Journal|Yes|Jan-24
Interdisciplinary Musicology|Conference on Interdisciplinary Musicology (CIM)|[Click here](http://www.idmusicology.com/cim/index2.htm)|Conference|Yes|Jan-24
Leonardo Music Journal|Leonardo Music Journal|[Click here](https://leonardo.info/leonardo-music-journal)|Journal|Yes|Jan-24
Libraries, Archives and Documentation|International Association of Music Libraries, Archives and Documentation Centres (IAML)|[Click here](http://www.iaml.info/)|Conference|Yes|Jan-24
Linux Audio Conference|Linux Audio Conference (LAC)|[Click here](https://linuxaudio.org/)|Conference|Yes|Jan-24
Live Coding|International Conference on Live Coding (ICLC)|[Click here](https://iclc.livecodenetwork.org/)|Conference|Yes|Jan-24
Mathematics and Computation in Music|International Conference on Mathematics and Computation in Music (MCM)|[Click here](http://www.smcm-net.info/)|Conference|Yes|Jan-24
Mathematics and Music|Journal of Mathematics and Music (JMAM)|[Click here](https://www.tandfonline.com/toc/tmam20/current)|Journal|Yes|Jan-24
Multimedia Computing, Communications, and Applications|ACM Transactions on Multimedia Computing, Communications, and Applications|[Click here](https://dl.acm.org/journal/tomm)|Journal|Yes|Jan-24
Multimedia Retrieval|ACM International Conference on Multimedia Retrieval (ICMR)|[Click here](http://www.sigmm.org/view_conference)|Conference|Yes|Jan-24
Music & Science|Music & Science|[Click here](https://journals.sagepub.com/home/mns)|Journal|Yes|Jan-24
Music Encoding|Music Encoding Conference (MEC)|[Click here](http://music-encoding.org/conference/)|Conference|Yes|Jan-24
Music Information Retrieval|International Society for Music Information Retrieval Conference (ISMIR)|[Click here](http://www.ismir.net/)|Conference|Yes|Jan-24
Music Information Retrieval|Music Information Retrieval EXchange (MIREX)|[Click here](https://www.music-ir.org/mirex/wiki/MIREX_HOME)|Conference|Yes|Jan-24
Music Information Retrieval|Transactions of the International Society for Music Information Retrieval (TISMIR)|[Click here](http://tismir.ismir.net/)|Journal|Yes|Jan-24
Music Perception|Music Perception|[Click here](https://online.ucpress.edu/mp)|Journal|Yes|Jan-24
Music Perception and Cognition|International Conference of Music Perception and Cognition (ICMPC)|[Click here](https://www.icmpc.org/)|Conference|Yes|Jan-24
Musicae Scientiae|Musicae Scientiae|[Click here](http://msx.sagepub.com/)|Journal|Yes|Jan-24
Musical Metacreation|International Workshop on Musical Metacreation|[Click here](http://musicalmetacreation.org/)|Conference|Yes|Jan-24
New Interfaces for Musical Expression|International Conference on New Interfaces for Musical Expression (NIME)|[Click here](http://www.nime.org/)|Conference|Yes|Jan-24
New Music Research|Journal of New Music Research (JNMR)|[Click here](http://www.tandfonline.com/toc/nnmr20/current)|Journal|Yes|Jan-24
Organised Sound|Organised Sound|[Click here](https://www.cambridge.org/core/journals/organised-sound)|Journal|Yes|Jan-24
Psychomusicology|Psychomusicology: Music, Mind, and Brain|[Click here](https://www.apa.org/pubs/journals/pmu)|Journal|Yes|Jan-24
Sound and Music Computing|Sound and Music Computing (SMC) conference of the SMC Network|[Click here](https://smcnetwork.org/)|Conference|Yes|Jan-24
Technologies for Music Notation and Representation|International Conference on Technologies for Music Notation and Representation (TENOR)|[Click here](http://www.tenor-conference.org/index.html)|Conference|Yes|Jan-24
Acoustical Society of America|Meetings of the Acoustical Society of America|[Click here](http://acousticalsociety.org/meetings)|Conference|X|Jan-24
Acoustical Society of America|Journal of the Acoustical Society of America|[Click here](http://asadl.org/jasa/)|Journal|X|Jan-24
Acoustics, Speech, and Signal Processing|IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP)|[Click here](http://www.signalprocessingsociety.org/technical-committees/list/audio-tc/conferences-and-workshops/)|Conference|X|Jan-24
Acta Acustica|Acta Acustica|[Click here](https://acta-acustica.edpsciences.org/)|Journal|X|Jan-24
AES Conferences|AES International Conferences|[Click here](http://www.aes.org/events/conferences/)|Conference|X|Jan-24
AES Conventions|AES Conventions|[Click here](http://www.aes.org/events/conventions/)|Conference|X|Jan-24
Applications of Signal Processing to Audio and Acoustics|IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA)|[Click here](http://www.signalprocessingsociety.org/technical-committees/list/audio-tc/conferences-and-workshops/)|Conference|X|Jan-24
Audio, Speech and Language Processing|IEEE Transactions on Audio, Speech and Language Processing|[Click here](https://signalprocessingsociety.org/publications-resources/ieeeacm-transactions-audio-speech-and-language-processing)|Journal|X|Jan-24
Auditory Display|International Conference on Auditory Display (ICAD)|[Click here](http://www.icad.org/conferences)|Conference|X|Jan-24
Information Retrieval|ACM Special Interest Group on Information Retrieval (SIGIR) Conference|[Click here](http://www.sigir.org/)|Conference|X|Jan-24
Multimedia Magazine|IEEE Multimedia Magazine|[Click here](http://www.computer.org/portal/site/multimedia)|Journal|X|Jan-24
Multimedia Signal Processing|IEEE International Workshop on Multimedia Signal Processing (MMSP)|[Click here](http://www.signalprocessingsociety.org/technical-committees/list/mmsp-tc/conferences-workshops/)|Conference|X|Jan-24
Recommender Systems|ACM Conference on Recommender Systems|[Click here](https://recsys.acm.org/)|Conference|X|Jan-24
Signal Processing|European Signal Processing Conference (EUSIPCO)|[Click here](https://eurasip.org/eusipco-conferences/)|Conference|X|Jan-24
