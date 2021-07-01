from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import urllib
import urllib3
import re
import random
import time
import json

urllib3.disable_warnings()

def main(outpath="output/search.json"):
    keywords = ["net neutrality", "open Internet", "zero-rating", "paid prioritization"]

    companies = []
    companies += ["Cogent Communications", "FirstLight Fiber", "Hurricane Electric", "Internet2", "Zayo", "NYSERNet", "Orange"]
    companies += ["Telia Carrier", "Sprint", "AT&T", "Deutsche Telekom", "Telefonica", "British Telecom", "KDDI"]
    #companies += ["Tata Communications", "PCCW GLobal", "Lumen Technologies", "Liberty Global", "GTT Communications", "Verizon", "Comcast"]
    #companies += ["FirstLight Fiber"]

    num_results_per_keyword = 50

    dict_of_links = {}

    # Issue Google query to obtain URLS
    for company in companies:
        dict_of_links[company] = {}
        for keyword in keywords:
            query = '"%s" AROUND(50) "%s"' % (company, keyword)
            print(query)
            query = urllib.parse.quote_plus(query) # Format into URL encoding
            ua = UserAgent()

            google_url = "https://www.google.com/search?q=%s&num=%d" % (query, num_results_per_keyword)
            response = requests.get(google_url, {"User-Agent": ua.random})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            #result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})
            #result_div = soup.find_all('div', attrs = {'class': 'g'})
            result_div = soup.find_all('div', attrs = {'class': 'kCrYT'})
            #print(result_div)

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
            #print(links)

            new = 0
            update = 0
            for link in links:
                # Anything that doesn't fit a specific pattern is ignored
                clean = re.search('\/url\?q\=(.*)\&sa', link)
                if clean is None:
                    continue
                url = clean.group(1)
                if url in dict_of_links[company]:
                    dict_of_links[company][url].append(keyword)
                    update += 1
                else:
                    dict_of_links[company][url] = [keyword]
                    new += 1

            print("Added %d URLs; Updated %d URLs" % (new, update))
            delay = random.randint(10,60)
            print("Delaying for %d seconds..." % (delay))
            time.sleep(delay)

    with open(outpath, 'w') as out:
        json.dump(dict_of_links, out, indent=4)

if __name__ == "__main__":
    main()