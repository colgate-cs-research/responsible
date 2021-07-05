from bs4 import BeautifulSoup
import requests
import urllib3
import os
import json
#from newspaper import Article

urllib3.disable_warnings()

def parse_html(response):
    
    page = BeautifulSoup(response, "html.parser")

    articles = page.find_all('article', recursive=True)
    if len(articles) > 0:
        method = "article %d" % len(articles)
        site_text = ""
        for article in articles:
            inner_articles = article.find_all('article', recursive=True)
            if len(inner_articles) > 0:
                article_text = ""
                for inner_article in inner_articles:
                    inner_article_text = inner_article.get_text(separator=" ") 
                    if len(inner_article_text.split()) >= 50:
                        article_text += "\n" + inner_article_text
            else:
                article_text = article.get_text(separator=" ")
            if len(article_text.split()) >= 5)0:
                site_text += "\n" + article_text

    else:
        method = "paragraphs"
        site_text = None
        paragraphs = page.find_all('p')
        for paragraph in paragraphs:
            text = paragraph.get_text()
            if text:
                if site_text is None:
                    site_text = text
                else:
                    site_text += "\n" + text
    if page.title is not None:
        title = page.title.get_text()
    else:
        title = ""
    return title, site_text, method

def parse_pdf(response):
    pass

def scrape(link):
    parts = link.split("/")
    if "tag" in parts or "category" in parts:
        return None, None, "tag/category"
    """try:
        article = Article(link, fetch_images=False)
        article.download()
        article.parse()
        return article.title, article.text, "newspaper"
    except Exception as ex:
        return None, None, str(ex)"""

    try:
        response = requests.get(link, {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}, verify=False, timeout=5)
        if response.status_code == 200:
            content_type = response.headers["content-type"]
            if content_type.startswith("text/html"):
                return parse_html(response.text)
            #elif content_type.startswith("application/pdf"):
            #   return parse_pdf(response)
            else:
                return None, None, "Unhandled content type: %s" % (content_type)
        else:
            return None, None, "Response: %d %s" % (response.status_code, response.reason)
    except Exception as ex:
        print(ex)
    return None, None, str(ex)

def main(inpath="output/search_around.json", base_outdir="output/pages_around", logpath="output/scrape_around.json",
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
            filename = None
            if full_text:
                i += 1
                filename = '%03d.txt' % (i)
                with open(os.path.join(company_outdir, filename), 'w') as f:
                    f.write("##LINK: %s\n" % link)
                    f.write("##KEYWORDS: %s\n" % ",".join(keywords))
                    f.write("##TITLE: %s\n" % title)
                    f.write("##METHOD: %s\n\n" % method)
                    f.write(full_text)
                print("\t%s" % (filename))
            company_links[link] = {
                "keywords" : keywords,
                "title" : title,
                "method" : method,
                "filename" : filename
            }
    
    with open(logpath, 'w') as outlog:
        json.dump(dict_of_links, outlog, indent=4)

if __name__ == "__main__":
    main()