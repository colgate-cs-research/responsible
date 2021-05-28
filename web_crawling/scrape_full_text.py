from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import urllib
import urllib3
import os
import re

urllib3.disable_warnings()

def scrape(link):
    ua = UserAgent()
    try:
        response = requests.get(link, {"User-Agent": ua.random}, verify = False)
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

keywords = ["net neutrality", "open Internet", "zero-rating", "paid prioritization"]

companies = ["Cogent Communications", "FirstLight Fiber", "Hurricane Electric", "Internet2", "Zayo", "NYSERNET", "Orange", "Telia Carrier", "Sprint", "AT&T", "Deutsche Telekom", "Telefonica", "British Telecom", "KDDI"]

num_results_per_keyword = 50

dict_of_links = {}

# Issue Google query to obtain URLS
for company in companies:
    dict_of_links[company] = {}
    for keyword in keywords:
        query = '"%s" "%s"' % (company, keyword)
        query = urllib.parse.quote_plus(query) # Format into URL encoding
        number_result = 50
        print(query)
        ua = UserAgent()

        google_url = "https://www.google.com/search?q=%s&num=%d" % (query, num_results_per_keyword)
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, "html.parser")

        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

        links = []
        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href = True)

                # Check to make sure everything is present before appending
                if link != '':
                    links.append(link['href'])

            # Next loop if one element is not present
            except:
                continue

        for link in links:
            # Anything that doesn't fit a specific pattern is ignored
            clean = re.search('\/url\?q\=(.*)\&sa', link)
            if clean is None:
                continue
            url = clean.group(1)
            if url in dict_of_links[company]:
                dict_of_links[company][url].append(keyword)
            else:
                dict_of_links[company][url] = [keyword]

# Fetch pages and store in files

base_outdir = "output/pages/"
i = 0
for company in dict_of_links:
    print(company)
    company_outdir = os.path.join(base_outdir, company)
    os.makedirs(company_outdir, exist_ok=True)
    company_links = dict_of_links[company]
    i = 0
    for link, keywords in company_links.items():
        print(link)
        title, full_text = scrape(link)
        title = title.strip()
        print(title)
        if full_text:
            i += 1
            with open(os.path.join(company_outdir, '%03d.txt' % (i)), 'w') as f:
                f.write("##LINK: %s\n" % link)
                f.write("##KEYWORDS: %s\n" % ",".join(keywords))
                f.write("##TITLE: %s\n\n" % title)
                f.write(full_text)