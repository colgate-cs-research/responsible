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

predict_list = ["cogent communications", "firstlight fiber", "hurricane electric", "internet2", "zayo", "NYSERNET", "Orange", "Telia Carrier", "Sprint", "AT&T", "Deutsche Telekom", "Telefonica", "British Telecom", "KDDI"]
dict_of_links = {}

for company in predict_list:

    query = '"' + company + '"' + ' "net neutrality"'
    query = urllib.parse.quote_plus(query) # Format into URL encoding
    number_result = 20
    print(query)
    ua = UserAgent()

    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
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

    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search('\/url\?q\=(.*)\&sa',l)

        # Anything that doesn't fit the above pattern will be removed
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    dict_of_links[company] = clean_links

#write texts to file

base_outdir = "output"
i = 0
for company in dict_of_links:
    print(company)
    company_outdir = os.path.join(base_outdir, company)
    os.makedirs(company_outdir, exist_ok=True)
    company_links = dict_of_links[company]
    for i in range(len(company_links)):
        link = company_links[i]
        print(link)
        title, full_text = scrape(link)
        print(title)
        if full_text:
            with open(os.path.join(company_outdir, '%02d.txt' % (i+1)), 'w') as f:
                f.write("##LINK: %s\n\n" % link)
                f.write("##TITLE: %s\n\n" % title)
                f.write(full_text)