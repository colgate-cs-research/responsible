from page_ranker import get_data
import requests
import urllib
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import csv
import pandas
from get_MLP_predictions import get_pred

predict_list = ["cogent communications", "firstlight fiber", "hurricane electric", "internet2", "zayo", "NYSERNET"]

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

    #print(clean_links)
    if ' ' in company:
        company = company.replace(' ', '')
        filename = company + ".csv"
    else:
        filename = company + ".csv"
    df = get_data(clean_links, filename)
    print(df)
    company_percentage = get_pred(df)
    print("----------")
    print(company + " query results include " + str(company_percentage * 100) + " percent net neutral sites.")
    print("----------")


