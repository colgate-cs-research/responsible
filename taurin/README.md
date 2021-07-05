# About
This directory contains the data and scripts for the paper "Divesting in Socially (Ir)responsible Internet Service Provider" by Emily Huff and Aaron Gember-Jacobson published in _ACM SIGCOMM 2021 Workshop on Technologies, Applications, and Uses of a Responsible Internet (TAURIN 2021)_.

# Data
## Documents
* `search_around.json` contains the URLs from the search results indexed by company; also includes the keyword(s) for which the URL appeared in the search results
* `stats-search_around.json` contains a summary of the above search results
* `search_no-around.json` contains URLs from the search results without a "AROUND(50)" modifier
* `stats-search_no-around.json` contains a summary of the above search results
* `scrape_around.json` contains information about the (attempted) scraped web pages from the search results, including any errors that occurred; indexed by company then URL; every URL in `search_around.json` also appears in `scrape_around.json`
* `pages_around` contains files with the URL, keyword(s), title, and text for each successfully scraped page; organized by company; files are numbered based on the order in which the pages were scraped; the filenames, URL(s), keywords, and titles are also stored in `scrape_around.json`
* `stats-scrape_around.json` contains a summary of the above scraping results

## Phrases
* `extract_around.json` contains the part-of-speech details, phrases, and sentences that were extracted from each scraped page; indexed by company then filename
* `stats-phrases_around.json` contains a summary of the above phrase extraction results
* `phrases_around_sentences.csv` is a tab-separated variable file containing company and filenames, sentences, and their assigned labels (FAVORS, OPPOSES, UNKNOWN)

# Scripts
## Gathering documents
* Run `scrape_search.py` to query for companies and store URLs from each search in `output/search_around.json`
* Run `search_to_stats.py` to summarize the search results in `output/search_around.json` and store the summary in `output/stats-search_around.json`
* Run `scrape_pages.py` to fetch URLs in `output/search_around.json` and store text from each page in `output/pages_around/COMPANY/NUM.txt` and details about the scraped pages in `output/scrape_around.json`
* Run `scrape_to_stats.py` to summarize the scraping results in `output/scrape_around.json` and store the summary in `output/stats-scrape_around.json`

## Extracting phrases
* Run `extract_phrases.py` to extract relevant phrases from text stored in `output/pages_around` and create the file `output/extract_around.json` containing the part-of-speech details, phrases, and sentences extracted from each scraped page
* Run `pharses_to_stats.py` to summarize the phrase extraction results in `output/extract_around.json` and store the summary in `output/stats-phrases_around.json`
* Run `phrases_to_csv.py` to store relevant sentences from `output/extract_around.json` into a tab-delimited file `output/phrases_around_sentences.csv` of sentences to be labeled

## Determining stance
* Run `egrep "FAVOR|OPPOSE" output/phrases_around_sentences.csv > output/phrases_around_sentences_no-unknown.csv` to extract sentences labeled "FAVOR" or "OPPOSE"
* Run `phrases_learn.py` to learn and test a stance detection model