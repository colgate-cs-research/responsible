from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from sklearn.model_selection import KFold
import csv
import requests
import urllib
import csv
import re
import nltk
nltk.download('punkt')

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
                    site_text = site_text + text
            print(site_text)
            return site_text
    except:
        return []

predict_list = ["cogent communications", "firstlight fiber", "hurricane electric", "internet2", "zayo", "NYSERNET"]
list_of_links = []
search_tracker = [] #keep track of what links correspond to what search

for company in predict_list:

    query = company + "net neutrality"
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
    list_of_links += clean_links
    search_tracker += [company] * len(clean_links)

print(list_of_links)
duplicate_list = []
  

with open('data_to_tag_full_text.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['text', 'category', 'sentiment', 'predicted AS'])

    keep_sentence_if_contains = ['neutral', 'neutrality' 'throttling', 'throttle', 'open internet', 'paid prioritization', 'prioritize', 'block']

    for link in list_of_links:
        full_text = scrape(link)
        if full_text:
            writer.writerow(['"'+full_text.strip()+'"', "", "", ""])

duplicate_list = []

with open('data_to_tag_soln_full_text.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['text', 'category', 'sentiment', 'predicted AS', 'search term'])
    keep_sentence_if_contains = ['neutral', 'neutrality' 'throttling', 'throttle', 'open internet', 'paid prioritization', 'prioritize', 'block']
    i = 0
    for link in list_of_links:
        full_text = scrape(link)
        if full_text:
            writer.writerow(['"'+full_text.strip()+'"', "", "", "",search_tracker[i]])
        i += 1



# make sure you handle NetNeutrality, FCC, PaidPrioritization, OpenInternet...
# fix pattern match


    