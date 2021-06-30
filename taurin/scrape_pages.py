from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import urllib3
import os
import json

urllib3.disable_warnings()

def scrape(link):
    ua = UserAgent()
    try:
        response = requests.get(link, {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}, verify=False, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            result_div = soup.find_all('p')
            site_text = ""
            for r in result_div:
                text = r.get_text()
                if text:
                    site_text = site_text + "\n" + text
            title = soup.title.get_text()
            return title, site_text
    except:
        pass
    return None, None

def main(inpath="output/search.json", base_outdir="output/pages"):
    with open(inpath, 'r') as infile:
        dict_of_links = json.load(infile)

    # Fetch pages and store in files
    i = 0
    for company in dict_of_links:
        print('\n'+company)
        company_outdir = os.path.join(base_outdir, company)
        os.makedirs(company_outdir, exist_ok=True)
        company_links = dict_of_links[company]
        i = 0
        for link, keywords in company_links.items():
            print(link)
            title, full_text = scrape(link)
            if title is not None:
                title = title.strip()
            print(title)
            if full_text:
                i += 1
                with open(os.path.join(company_outdir, '%03d.txt' % (i)), 'w') as f:
                    f.write("##LINK: %s\n" % link)
                    f.write("##KEYWORDS: %s\n" % ",".join(keywords))
                    f.write("##TITLE: %s\n\n" % title)
                    f.write(full_text)
