---
layout: post
title: Where Can I Find Data?
---

"Where can I find data?" may well be the question I am most often asked by students.
It's a good question, and although the answer changes over time,
there are some relatively stable sites to point to.
This page summarises some of those options as a starting point for further exploration.
Access conditions vary: some sources require registration, approval, or a subscription.
Other initiatives like [UNICC](https://www.unicc.org/artificial-intelligence/) are
a matter of "watch this space" and not yet included.
Consider these as you begin to explore what others have created,
so that you can make sure your work complements and/or extends what has gone before,
and that we continue to build a great cathedral of cumulative science together!

In short, this is a sign-posting service to accessible data.
```
    ┌──────────────────┐
    │ ← DATA THIS WAY  │
    └────────┬┬────────┘
             ││
    ┌────────┴┴────────────┐
    │  AND MORE THIS WAY → │
    └────────┬┬────────────┘
             ││
             ││
─────────────┘└──────────────
```

### In brief:
- Title: "Where Can I Find Data?"
- By: Mark Gotham, 2025-present
- Licence: CC-By-SA
- URLs last reviewed: November 2026
- Suggestions/contributions: ... are welcome! PR or email ([contact details here](https://markgotham.github.io/))


### Top Tips

Practical:
- Check _many_ sources, not just one! If in doubt, start with Kaggle/Hugging Face for most beginner projects ... but do branch out to check others once you settle on a topic.
- You may have access to more resources than you think. E.g., some databases require a subscription or similar, but school/university/city library membership might unlock access.
- Accessing data with APIs takes a bit more technical overhead, but that's often worthwhile, especially if you want structured data from/about social media.

Ethical:
- Check each dataset's licence and terms of use before using or redistributing it.
Public availability does not imply permission for all and every use case.
Most of the datasets on the repositories listed here will have permissive licences that enable research (at least!), but always check.
- "Scraping" websites is possible but should be considered a last resort for want of a better option,
and having checked for any indication of permission/restrictions (e.g., `robots.txt` file). 
- ... and many more! E.g., among _your_ ethical considerations should be how _they_ made their datasets.

Sensible:
- In working with data it's likely you'll end up expanding and/or improving it.
Having gone to that trouble, find a way to contribute your work back into the ecosystem!
I.e., this page can double as a "where can I _put_ my data"? 

---

## **Publicly Accessible Data Sources for Analysis**

### For the Data Itself

*✅ Hundreds of thousands of datasets, freely downloadable, across many formats and topics.*

*❌ Quality varies. Most are user-uploads and not subject to quality control (see 'Paired Academic Publications' below).*

- **[Zenodo](https://zenodo.org/)**
  > "Built and operated by CERN and OpenAIRE to ensure that everyone can join in Open Science".
- **[Open Science Framework (OSF)](https://osf.io/)**
  > Public research projects, data, and materials.
  > [IMPORTANT UPDATE](https://www.cos.io/osf-changes): no new projects will be accepted from 16 November 2026;
  projects become read-only after 19 February 2027.
  Existing public projects will remain accessible. 
  Choose another repository for new deposits.
  > See also [OSF's API](https://developer.osf.io/).
- **[Harvard Dataverse](https://dataverse.harvard.edu/)**
  > Research data across disciplines, with dataset citations and versioning. Some files have restricted access.
- **[Kaggle Datasets](https://www.kaggle.com/datasets)**  
  > Datasets as well as benchmarks, models and more.
- **[Hugging Face Datasets](https://huggingface.co/datasets)**  
  > ML-focus. Includes search by modality (text, audio, vision).
- **[UC Irvine (UCI) Machine Learning Repository](https://archive.ics.uci.edu/)**
  > Documented datasets for machine learning, including many small tabular datasets suited to teaching.
- **[GitHub Datasets](https://github.com/datasets)**  
  > This is a small list of curated public datasets via GitHub repos among the  
   many more [datasets on GitHub outside this](https://github.com/).

### **Paired Academic Publications**

*✅ Many datasets (e.g., those at the platforms above) are paired with an academic publication.
Having an associated academic publication (that has been properly reviewed) provides some quality control.*

*❌ The academic journals themselves tend not to host the data (so you need the paired dataset above).
There are many great datasets without a paired academic publication.*

- **Journals that focus on publishing datasets and their descriptions:**  
  > - General (all subject) examples include [Data (MDPI)](https://www.mdpi.com/journal/data),
  [Scientific Data (Nature Portfolio)](https://www.nature.com/sdata/),
  [Earth System Science Data](https://www.earth-system-science-data.net/),
  [GigaScience](https://academic.oup.com/gigascience)
  > - Examples specific to the humanities include [Journal of Open Humanities Data (JOHD)](https://openhumanitiesdata.metajnl.com/)
- **Humanities journals that include a "track" (or similar) specifically for introducing datasets**
  > - [Digital Humanities Quarterly](https://dhq.digitalhumanities.org/),
  > - [Digital Scholarship in the Humanities](https://academic.oup.com/dsh),
  > - [Cultural Analytics](https://culturalanalytics.org/),
  > - [Transactions of the International Society for Music Information Retrieval (TISMIR)](https://transactions.ismir.net/)

---

## **Knowledge Graphs and Metadata**

*✅ Knowledge graphs and metadata support sharing of and search over structured representations of knowledge.
Individual datasets like those above may not adhere to such best practices.*

*❌ Use for structure and relationships, not (usually) as a primary source of data.*
Metadata may describe items whose underlying texts, images, or other files are not openly available.

- **[Wikidata](https://www.wikidata.org)**  
  Free, collaborative knowledge base (not Wikipedia). *Use for: Entity relationships, multilingual facts, ontology.*

- **[Europeana](https://www.europeana.eu)**  
  Cultural heritage data (art, books, music). *Millions of items from European museums/libraries.*

- **[OpenAlex](https://openalex.org/)**  
  Scholarly metadata linking works, authors, institutions, and citations. *Access via API and bulk downloads.*

---

## **Aggregated and Processed Data**  

*✅ Pre-processed and visualised data, often with source links and regular updates.*

*❌ Where the raw data is not provided, this leaves you less scope to explore your own analysis.*

- **[Gapminder](https://www.gapminder.org)**  
  > Global development data (health, economy). Includes interactive tools and datasets.

- **[Our World in Data (OWID)](https://ourworldindata.org)**  
  > Rigorous, source-verified datasets on global issues (climate, inequality, ...). 
  Most cases include an option to download the data used directly,
  or (failing that) at least provide a redirect to the third-party website hosting that data. 

- **[Global Data Tracker](https://globaldatatracker.com/)**  
  > Interactive country comparisons and visualisations of World Bank indicators.
  Follow the source links for underlying data; moving counters are estimates, not live measurements.

- **[Google Trends](https://trends.google.com)**  
  > See what the world is searching for by topic (and also region, time, ...).
  Free, but limited to _trends_ (not raw counts).
  See also [Google Books Ngram Viewer](https://books.google.com/ngrams/)

---

## **Paid Resources (but often free via Libraries)**  

*❌ Not easily available to all.*

*✅ May be more available than you think, e.g., via your local library.*

- **[Factiva](https://www.dowjones.com/factiva)**  
  > News, business, and financial data. *Available via university libraries.*
  
- **[LexisNexis Nexis Uni](https://www.lexisnexis.com/en-us/products/nexis-uni.page)**  
  > Legal, news, and business databases. *Available through subscribing academic libraries.*

---

## Further Specific Sources by Type

*✅ Specific sources such as government data tend to be free, high-quality and as authoritative (for their subject) as can be expected.*

*❌ Given the specific focus, the overall scope is more limited than Kaggle, for instance.* 

---

### **Government and Similar**  

- **[data.gov (USA)](https://data.gov)**  
  > Public datasets from US government agencies (health, environment, economy).
- **[data.gov.uk (UK)](https://data.gov.uk)**  
  > UK public sector data (crime, education, transport).
  Related UK sites include
  [UK Data Service](https://ukdataservice.ac.uk/),
  [Police data](https://data.police.uk/),
  the [Office for National Statistics (ONS)](https://www.ons.gov.uk/),
  and the [Open Data Institute (ODI)](https://theodi.org/) (for guidance on data practice).
  Some cities and regions also offer public data, e.g.,
  the [London Data Store](https://data.london.gov.uk/)
  traverses jobs, transport, and more.

- **[European Data Portal](https://data.europa.eu)**  
  > Public datasets from EU institutions and European national and local portals (trade, environment, research).  
- **[UN System Data Commons](https://data.un.org)**  
  > Search across public data and statistics from UN agencies (demographics, health, development, ...).  

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
  > Global company registry. API and bulk access have separate terms and may require a paid plan.
- **[OpenSpending](https://www.openspending.org/)**
  > "Spending" (financial) data about countries all around the world.
- **[World Bank Open Data](https://data.worldbank.org)**  
  > Many indicators for most countries across topics including poverty, education, and energy.  
- **[OECD Data Explorer](https://data-explorer.oecd.org/)**  
  > Comparable economic, social, and environmental statistics, with CSV downloads and an API.

---

### **Health and Life Sciences**  
 
- **[WHO (World Health Organisation)](https://www.who.int/data/gho)**  
  > Global health statistics: diseases, mortality, healthcare access.
- **[CDC (Centers for Disease Control and Prevention) WONDER](https://wonder.cdc.gov)**  
  > US public health data: mortality, births, infectious diseases.  
- **[GBIF (Global Biodiversity Information Facility)](https://www.gbif.org/)**  
  > Species occurrence and biodiversity data worldwide. A free account is required to request occurrence downloads.
  
---

## **APIs for Social Media and More**  


*✅ Social media stores a great repository of cultural trends and more.
Many social media and related companies offer APIs which provide a structured set of data and controls for all/only the data the company is content to share.*

*❌ Not all APIs are equal, "free" can be a misnomer, and APIs are more technically demanding than direct downloads.*

- **[Academic Torrents](https://academictorrents.com/docs/downloading.html)**
  > Download datasets using a BitTorrent client, command-line tools, or Python; an API is not required.
- **[GDELT Project](https://www.gdeltproject.org)**
  > Global event data across the media (broadcast, print, and web).
- **[Reddit data access](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data)**  
  > Academic research requires approval through [Reddit for Researchers](https://support.reddithelp.com/hc/en-us/articles/49381918834964-Reddit-for-Researchers-Program).
  The general Data API and wrappers such as
  [`PRAW` (The Python Reddit API Wrapper)](https://praw.readthedocs.io/en/stable/) have separate permitted uses.
- **["X" / "Twitter" API](https://docs.x.com/overview)**
    > Paid, usage-based access; check current pricing and rate limits before planning a project.
- **[Meta Content Library (Facebook and Instagram)](https://www.icpsr.umich.edu/sites/somar/meta-content-library)**
    > Research access to public content for approved, eligible researchers; 
    application and access restrictions apply.
- **Many other companies like [Spotify](https://developer.spotify.com/documentation/web-api)**
    > Restrictions apply and the data coverage can change without warning (it has done so in this case).
    See also secondary representations such as [Spotify Playlist Archive](https://spotifyplaylistarchive.com/).

---

That's all folks! Thanks for reading!
Have you enjoyed this?
Is it missing something?
Suggestions are welcome
(PR or email [contact details here](https://markgotham.github.io/))
