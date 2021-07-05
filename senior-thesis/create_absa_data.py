import csv
import requests
import urllib
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import pandas
import nltk
nltk.download('punkt')


links = ['https://corporate.comcast.com/openinternet/open-net-neutrality',
'https://www.sonic.com/transparency',
'https://starry.com/net-neutrality',
'https://ting.com/blog/net-neutrality-repeal-statement/',
'https://blog.mozilla.org/blog/2018/11/16/mozilla-fights-on-for-net-neutrality/',
'https://www.ericsson.com/en/news/2015/9/ericssons-perspective-on-the-net-neutrality-debate',
'https://www.phonenews.com/cingular-against-net-neutrality-for-consumers-1371/',
'https://www.washingtonpost.com/news/the-switch/wp/2014/11/25/wikipedias-complicated-relationship-with-net-neutrality/',
'https://www.engadget.com/2014/12/11/turkeys-vote-against-christmas/?guccounter=1',
'https://arstechnica.com/tech-policy/2018/08/verizon-throttled-fire-departments-unlimited-data-during-calif-wildfire/'
]

def scrape(link):
    ua = UserAgent()
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

with open('absa_data.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)

    keep_sentence_if_contains = ['neutral', 'neutrality' 'throttling', 'throttle', 'open internet', 'paid prioritization', 'prioritize', 'block']

    for link in links:
        full_text_list = scrape(link)
        for paragraph in full_text_list:
            sentences = nltk.tokenize.sent_tokenize(paragraph)
            #print(sentences)
            for sent in sentences:
                sent = sent.lower()
                if any(word in sent for word in keep_sentence_if_contains):
                    sent = sent.replace(',', '')
                    print('-------------------------------------------')
                    print(sent)
                    print('-------------------------------------------')
                    writer.writerow([sent, "CATEGORY", "SENTIMENT LABEL"])




    