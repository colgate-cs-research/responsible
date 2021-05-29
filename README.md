# responsible
Socially responsible routing

## TAURIN
* Run `web_crawling/scrape_full_text.py` to query for companies and store text from each page in `web_crawling/output/$COMPANY/$NUM.txt`
* Run `web_crawling/extract_phrases.py` to extract relevant phrases from text stored in `output/$COMPANY/$NUM`
* Run `web_crawling/phrases_to_csv.py` to convert phrases from the output of `web_crawling/extract_phrases.py` into a tab-delimited file of phrases to be labeled
* Run `web_crawling/phrases_learn.py` to learn and test a stance detection model