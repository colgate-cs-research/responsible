import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd 
import collections
from model_build import get_ngrams

def get_cogent_dict():

    def scrape(link):
        response = requests.get(link, {"User-Agent": ua.random}, verify = False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            result_div = soup.find_all('p')
            site_text = []
            for r in result_div:
                text = r.get_text()
                if text:
                    site_text.append(text)
            return site_text

    query = "'cogent communications net neutrality'"
    query = urllib.parse.quote_plus(query) # Format into URL encoding
    number_result = 20

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

    phrase_dict = {"network neutral": 0, "net neutral": 0, "pay prioritization": 0, "throttle traffic": 0, "open internet": 0, "block traffic":0, "support net neutral": 0, "practice net neutral": 0, "support network neutral": 0, "practice network neutral": 0, "be net neutral": 0, "be network neutral": 0, "net neutral violation":0, "network neutral violation": 0, "violate net neutrality":0, "violate network neutrality":0, "against net neutrality":0, "against network neutrality":0}
    for link in clean_links:
        site_text = scrape(link)
        if site_text:
            nn_phrases= get_ngrams(site_text) ## this is a list of counts
            i = 0
            #print(phrase_dict.keys())
            for key in phrase_dict.keys():
                if i == 18:
                    break
                else:
                    phrase_dict[key] += nn_phrases[i]
                    i += 1
            phrase_dict["URL"] = link
            # phrase_dict["train/test"]
            # phrase_dict["Net Neutral? (Y/N/M)"]
    print("Cogent ------------------------")
    print(phrase_dict)
    return phrase_dict

get_cogent_dict()
        















