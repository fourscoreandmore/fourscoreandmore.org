---
layout: post
title: Where is the Data?
---

"Where is the data?" may well be the question I am most often asked by students.
It's a good question, and although the answer changes over time,
there are some relatively stable sites to point to.
This page summarises some of those options as a staring point for further exploration.
All sites have been manually checked against minimal criteria: URL works and data accessible.
Other initiatives like [UNICC](https://www.unicc.org/artificial-intelligence/) are
a matter of "watch this space" and not yet included.
Consider these as you begin to explore what others have created,
so that you can make sure your work complements and/or extends what has gone before,
and that we continue to build a great cathedral of cumulative science together!

### In brief:
- Title: "Where is the Data?"
- By: Mark Gotham, 2025
- Licence: CC-By-SA
- URLs last accessed and verified: October 2025
- Suggestions/contributions: ... are welcome! PR or email ([contact details here](https://markgotham.github.io/))


### Top Tips

Practical:
- Check _many_ sources, not just one! If in doubt, start with Kaggle/Hugging Face for most beginner projects ... but do branch out to check others once you settle on a topic.
- You may have access to more resources than you think. E.g., some databases require a subscription or similar, but school/university/city library membership might unlock access.
- Accessing data with APIs takes a bit more technical overhead, but that's often worthwhile, especially if you want structured data from/about social media.

Ethical:
- Check licenses (e.g., MIT, etc.) before using data. Most of the datasets on the repositories listed here will have permissive licences that enable research (at least!), but always check.
- "Scraping" websites is possible but should be considered a last resort for want of a better option, and having checked for any indication of permission/restrictions (e.g., `robots.txt` file). 
- ... and many more! E.g., among _your_ ethical considerations should be how _they_ made their datasets.

---

## **Publicly Accessible Data Sources for Analysis**

*✅ Hundreds of thousands of datasets, freely downloadable, across many formats and topics, which tend to be well-organised.*

*❌ Most are user-uploads and not subject to quality control.*

- **[Kaggle Datasets](https://www.kaggle.com/datasets)**  
  > Datasets as well as benchmarks, models and more.
  
- **[Hugging Face Datasets](https://huggingface.co/datasets)**  
  > ML-focus. Includes search by modality (text, audio, vision).
  
- **[GitHub Datasets](https://github.com/datasets)**  
  > This is small list of curated public datasets via GitHub repos among the  
   many more [datasets on GitHub outside this](https://github.com/). 

---

## **Knowledge Graphs and Metadata**

*✅ Knowledge graphs and metadata support sharing of and search over structured representations of knowledge.
Individual datasets like those above may not adhere to such best practices.*

*❌ Use for structure and relationships, not (usually) as a primary source of data.*

- **[Wikidata](https://www.wikidata.org)**  
  Free, collaborative knowledge base (not Wikipedia). *Use for: Entity relationships, multilingual facts, ontology.*

- **[Europeana](https://www.europeana.eu)**  
  Cultural heritage data (art, books, music). *10M+ items from European museums/libraries.*

---

## **Curated and Processed Data**  

*✅ Pre-processed, visualised, and updated by experts.*

*❌ Where the raw data is not provided, this leaves you less scope to explore your own analysis.*

- **[Gapminder](https://www.gapminder.org)**  
  > Global development data (health, economy). Includes interactive tools and datasets.

- **[Our World in Data (OWID)](https://ourworldindata.org)**  
  > Rigorous, source-verified datasets on global issues (climate, inequality, ...). 
  Most of the studied include an option to download the data used directly,
  or (failing that) at least provide a redirect to the third-party website hosting that data. 

- **[Google Trends](https://trends.google.com)**  
  > See what the world is searching for by topic (and also region, time, ...).
  Free, but limited to _trends_ (not raw counts).

---

## **Paid Resources (but often free via Libraries)**  

*❌ Not easily available to all.*

*✅ May be more available than you think, e.g., via your local library.*

- **[Factiva](https://www.dowjones.com/factiva)**  
  > News, business, and financial data. *Available via university libraries.*
  
- **[NexisLexis](https://www.lexisnexis.com)**  
  > Legal, news, and business databases. *Typically included in academic library subscriptions.*

---

## Further Specific Sources by Type

*✅ Specific sources such as government data tend to be free, high-quality and as authoritative (for their subject) as can be expected.*

*❌ Given the specific focus, the overall scope is more limited than Kaggle, for instance.* 

---

### **Government and Similar**  

- **[data.gov (US)](https://data.gov)**  
  > 250k+ datasets from US federal agencies (health, environment, economy).
- **[data.gov.uk (UK)](https://data.gov.uk)**  
  > UK public sector data (crime, education, transport).  
- **[EU Open Data Portal](https://data.europa.eu)**  
  > 500k+ datasets from EU institutions (trade, environment, research).  
- **[UN Data](https://data.un.org)**  
  > UN-aggregated global statistics (demographics, trade, SDGs).  

---

### **Geospatial (Location-Based) Data**  

- **[OpenStreetMap (OSM) Data](https://www.openstreetmap.org)**  
  > Free global map data for roads, buildings, and places of interest.
  Explore manually or engage computationally using [`osmnx` (Python)](https://osmnx.readthedocs.io/en/stable/) or [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API).  
- **[NASA Earthdata](https://earthdata.nasa.gov)**  
  > Satellite imagery, climate, and environmental data.  
- **[NOAA Climate Data](https://www.ncei.noaa.gov)**  
  > Historical weather, ocean, and climate records.  

---

### **Economic and Financial Data**

- **[FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org)**  
  > US economic time series data (GDP, unemployment, interest rates, ...).
  Most data is directly downloadable as CSV.
- **[OpenCorporates](https://opencorporates.com)**  
  > Global company registry (100M+ entities).
- **[World Bank Open Data](https://data.worldbank.org)**  
  > Many indicators for most countries across topics including poverty, education, and energy.  

---

### **Health and Life Sciences**  
 
- **[WHO (World Health Organisation)](https://www.who.int/data/gho)**  
  > Global health statistics: diseases, mortality, healthcare access.
- **[CDC (Centre for Disease Control) WONDER](https://wonder.cdc.gov)**  
  > US public health data: mortality, births, infectious diseases).  
  
---

## **APIs for Social Media and More**  


*✅ Social media stores a great repository of cultural trends and more.
Many social media and related companies offer APIs which provide a structured set of data and controls for all/only the data the company is content to share.*

*❌ Not all APIs are equal, "free" can be a misnomer, and APIs are more technically demanding than direct downloads.*

- **[GDELT Project](https://www.gdeltproject.org)**
  > Global event data across the media (broadcast, print, and web).
- **[Reddit API](https://www.reddit.com/wiki/api)**  
  > Access Reddit API for posts/comments e.g., via
  [`PRAW` (The Python Reddit API Wrapper)](https://praw.readthedocs.io/en/stable/)
- **["X" / "Twitter" API](https://developer.x.com/en/docs/x-api)**
    > 'Free', but be wary of rate limits.
- **Facebook**
    >  Not publicly accessible. There are ways, but generally to be avoided.
- **Many other companies like [Spotify](https://developer.spotify.com/documentation/web-api)**
    > Restrictions apply and the data coverage can change without warning (it has done so in this case).
    See also secondary representations such as https://spotifyplaylistarchive.com/.

---

That's all folks! Thanks for reading!
Have you enjoyed this?
Is it missing something?
Suggestions are welcome
(PR or email [contact details here](https://markgotham.github.io/))
