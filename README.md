# responsible
Socially responsible routing

## TAURIN
* Run `taurin/scrape_search.py` to query for companies and store URLs from each search in `taurin/output/search.json`
* Run `taurin/scrape_pages.py` to fetch URLs in `taurin/output/search.json` and store text from each page in `taurin/output/$COMPANY/$NUM.txt`
* Run `taurin/extract_phrases.py` to extract relevant phrases from text stored in `taurin/output/$COMPANY/$NUM` and create the file `taurin/output/extract.json`
* Run `taurin/phrases_to_csv.py` to convert phrases from the output of `taurin/extract_phrases.py` (stored in `taurin/output/extract.json`) into a tab-delimited file of phrases to be labeled (stored in `taurin/output/company.csv`)
* Run `taurin/phrases_learn.py` to learn and test a stance detection model