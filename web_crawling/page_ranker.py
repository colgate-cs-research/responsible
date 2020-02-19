import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
from model_build import get_ngrams
import csv
import pandas

def get_data(links, filename):

    labels = len(links)

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

    phrase_dict = {"innovation":0, "news":0, "network neutral": 0, "net neutral": 0, "pay prioritization": 0, "throttle traffic": 0, "open internet": 0, "block traffic":0, "tech company":0, "support net neutral": 0, "practice net neutral": 0, "support network neutral": 0, "practice network neutral": 0, "be net neutral": 0, "be network neutral": 0, "net neutral violation":0, "network neutral violation": 0, "violate net neutrality":0, "violate network neutrality":0, "against net neutrality":0, "against network neutrality":0}
    with open(filename, mode='w') as csv_file:
        fieldnames = ["innovation", "news", "network neutral", "net neutral", "pay prioritization", "throttle traffic", "open internet", "block traffic", "tech company", "support net neutral", "practice net neutral", "support network neutral", "practice network neutral", "be net neutral", "be network neutral", "net neutral violation", "network neutral violation", "violate net neutrality", "violate network neutrality", "against net neutrality", "against network neutrality", "URL", "NN"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        nn_idx = 0
        for link in links:
            ua = UserAgent()
            site_text = scrape(link)
            if site_text:
                nn_phrases= get_ngrams(site_text) ## this is a list of counts
                i = 0
                phrase_dict = {"innovation":0, "news":0, "network neutral": 0, "net neutral": 0, "pay prioritization": 0, "throttle traffic": 0, "open internet": 0, "block traffic":0, "tech company":0, "support net neutral": 0, "practice net neutral": 0, "support network neutral": 0, "practice network neutral": 0, "be net neutral": 0, "be network neutral": 0, "net neutral violation":0, "network neutral violation": 0, "violate net neutrality":0, "violate network neutrality":0, "against net neutrality":0, "against network neutrality":0}
                #print(phrase_dict.keys())
                for key in phrase_dict.keys():
                    if i == 21:
                        break
                    else:
                        phrase_dict[key] = nn_phrases[i]
                        i += 1
                phrase_dict["URL"] = link
                writer.writerow(phrase_dict)
            nn_idx += 1

    df = pandas.read_csv(filename)
    return df

