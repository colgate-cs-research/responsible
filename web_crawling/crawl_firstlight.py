import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd 
import collections

def scrape(link):
    response = requests.get(link, {"User-Agent": ua.random}, verify = False) ## how bad is this?
    if response.status_code == 200:
        #print(link)
        #print()
        #print()
        soup = BeautifulSoup(response.text, "html.parser")
        result_div = soup.find_all('p')
        site_text = []
        for r in result_div:
            #print("more than once")
            site_text.append(r.get_text())
        #print("DONE HERE>>>>>>")
        #print("SITE TEXT")
        #print(site_text)
        return site_text

query = "'firstlight fiber net neutrality'"
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

print(clean_links)
# test viable links
net_neutral_count = 0
network_neutral_count = 0
for link in clean_links:
    site_text = scrape(link)
    if site_text is not None:
        for paragraph in site_text:
            net_neutral_count += paragraph.lower().count("net neutral")
            network_neutral_count += paragraph.lower().count("network neutral")

print("Net Neutral or Network Neutral count for Firstlight Fiber:")
print(net_neutral_count + network_neutral_count)















