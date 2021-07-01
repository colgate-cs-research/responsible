from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import urllib3
import os
import json

urllib3.disable_warnings()

def parse_html(response):
    page = BeautifulSoup(response.text, "html.parser")
    site_text = ""

    articles = page.find_all('article')
    if len(articles) > 0:
        method = "article"
        if len(articles) <= 2:
            article = articles[0]
            """paragraphs = article.find_all('p')
            if len(paragraphs) > 1:
                method += " paragraphs"
                for paragraph in paragraphs:
                    text = paragraph.get_text()
                    if text:
                        site_text = site_text + "\n" + text
            else:"""
            method += " text"
            site_text += "\n" + article.get_text(separator=" ")
        else:
            method += " list"
    else:
        method = "paragraphs"
        paragraphs = page.find_all('p')
        for paragraph in paragraphs:
            text = paragraph.get_text()
            if text:
                site_text += "\n" + text
    title = page.title.get_text()
    return title, site_text, method

def scrape(link):
    ua = UserAgent()
    try:
        response = requests.get(link, {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}, verify=False, timeout=5)
        if response.status_code == 200:
            content_type = response.headers["content-type"]
            if content_type.startswith("text/html"):
                return parse_html(response)
            #elif content_type.startswith("application/pdf"):
            #   return parse_pdf(response)
            else:
                return None, None, "Unhandled content type: %s" % (content_type)
        else:
            return None, None, "Response: %d %s" % (response.status_code, response.reason)
    except:
        pass
    return None, None, None

def main(inpath="output/search.json", base_outdir="output/pages", logpath="output/scrape.json",
        companies=None):
    with open(inpath, 'r') as infile:
        dict_of_links = json.load(infile)

    if companies is None:
        companies = dict_of_links.keys()

    # Fetch pages and store in files
    i = 0
    for company in companies:
        print('\n'+company)
        company_outdir = os.path.join(base_outdir, company)
        os.makedirs(company_outdir, exist_ok=True)
        company_links = dict_of_links[company]
        i = 0
        for link, keywords in company_links.items():
            print(link)
            title, full_text, method = scrape(link)
            print("\t%s" % (method))
            if title is not None:
                title = title.strip()
            print("\t%s" % (title))
            if full_text:
                i += 1
                with open(os.path.join(company_outdir, '%03d.txt' % (i)), 'w') as f:
                    f.write("##LINK: %s\n" % link)
                    f.write("##KEYWORDS: %s\n" % ",".join(keywords))
                    f.write("##TITLE: %s\n" % title)
                    f.write("##METHOD: %s\n\n" % method)
                    f.write(full_text)
            company_links[link] = {
                "keywords" : keywords,
                "title" : title,
                "method" : method
            }
    
    with open(logpath, 'w') as outlog:
        json.dump(dict_of_links, logpath, indent=4)

if __name__ == "__main__":
    main()