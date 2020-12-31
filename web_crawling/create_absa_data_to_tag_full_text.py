from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from sklearn.model_selection import KFold
import csv
import requests
import urllib
import urllib3
import csv
import re
import nltk
nltk.download('punkt')

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
                    site_text = site_text + text
            return site_text
    except:
        return []

predict_list = ["cogent communications", "firstlight fiber", "hurricane electric", "internet2", "zayo", "NYSERNET", "Orange", "Telia Carrier", "Sprint", "AT&T", "Deutsche Telekom", "Telefonica", "British Telecom", "KDDI"]
search_terms_list = {
    "cogent communications": ["cogent communications", "cogent"], 
    "firstlight fiber": ["firstlight fiber", "firstlight"],
    "hurricane electric" : ["hurricane electric", "hurricane"], 
    "internet2": ["internet2"], 
    "zayo": ["zayo"], 
    "NYSERNET": ["NYSERNET"],
    "Orange": ["Orange"], 
    "Telia Carrier": ["Telia Carrier", "Telia"], 
    "Sprint": ["Sprint"], 
    "AT&T": ["AT&T"], 
    "Deutsche Telekom": ["Deutsche Telekom", "Telekom"], 
    "Telefonica": ["Telefonica"], 
    "British Telecom": ["British Telecom", "BT", "Telecom"], 
    "KDDI": ["KDDI"]
}
list_of_links = []
search_tracker = [] #keep track of what links correspond to what search

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
    list_of_links += clean_links
    search_tracker += [company] * len(clean_links)

print(list_of_links)
duplicate_list = []

#write texts to file

data_file = open('data_to_tag_full_text.csv', mode='w')
data_writer = csv.writer(data_file)
data_writer.writerow(['text', 'category', 'sentiment', 'predicted AS'])

soln_file = open('data_to_tag_soln_full_text.csv', mode='w')
soln_writer = csv.writer(soln_file)
soln_writer.writerow(['text', 'category', 'sentiment', 'predicted AS', 'search term'])

sentences_file = open('sentences.csv', mode='w')
sentences_writer = csv.writer(sentences_file)
sentences_writer.writerow(['sentence', 'search term', 'sentiment'])

i = 0
for link in list_of_links:
    full_text = scrape(link)
    if full_text:
        data_writer.writerow(['"'+full_text.strip()+'"', "", "", ""])
        soln_writer.writerow(['"'+full_text.strip()+'"', "", "", "",search_tracker[i]])
        terms = search_terms_list[search_tracker[i]]
        sentences = full_text.split('.')
        for sentence in sentences:
            if any(word.lower() in sentence.lower() for word in terms):
                sentences_writer.writerow(['"'+sentence+'."', search_tracker[i], ""])
                print(sentence)
                print()
    i += 1

data_file.close()
soln_file.close()
sentences_file.close()

# make sure you handle NetNeutrality, FCC, PaidPrioritization, OpenInternet...
# fix pattern match


    