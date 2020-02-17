import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
from model_build import get_ngrams
import csv

net_neutral_links = ['https://corporate.comcast.com/openinternet/open-net-neutrality', 'https://about.att.com/sites/broadband/network', 'https://www.sonic.com/transparency', 'https://starry.com/net-neutrality', 'https://www.verizon.com/about/news/net-neutrality-path-forward', 'https://ting.com/blog/net-neutrality-repeal-statement/', 'https://www.cnbc.com/2017/07/12/facebook-ceo-mark-zuckerberg-supports-net-neutrality.html', 'https://www.google.com/takeaction/action/net-neutrality/', 'https://blog.mozilla.org/blog/2018/11/16/mozilla-fights-on-for-net-neutrality/', 'https://www.t-mobile.com/brand/binge-on-letter', 'https://frontier.com/corporate/responsibility/policy-blog/net-neutrality', 'https://www.bloomberg.com/news/articles/2017-07-17/microsoft-google-back-strong-net-neutrality-on-broadband-firms', 'https://www.investors.com/politics/commentary/amazon-big-tech-neutrality/', 'https://www.cnet.com/news/groups-backed-by-facebook-alphabet-and-amazon-push-for-return-of-net-neutrality-rules/', 'https://www.usatoday.com/story/tech/2017/07/11/net-neutrality-day-action-heres-what-happen/460459001/', 'https://ir.vonage.com/press-releases/2015/26-02-2015-193417416', 'https://www.iac.com/media-room/news/vimeo-ongoing-battle-net-neutrality-refiles-lawsuit-against-fcc', 'https://finance.yahoo.com/news/barry-diller-almost-un-american-want-internet-201720478.html', 'https://www.cjr.org/analysis/reddit-net-neutrality-fcc.php', 'https://www.etsy.com/advocacy/net-neutrality', 'https://action.etsy.com/redalert', 'https://www.greenpeace.org/usa/greenpeace-supports-net-neutrality/', 'https://www.ericsson.com/en/news/2015/9/ericssons-perspective-on-the-net-neutrality-debate']

non_nn_links = ['https://www.bloomberg.com/news/articles/2018-11-08/sprint-is-throttling-microsoft-s-skype-service-study-finds', 'https://arstechnica.com/tech-policy/2018/08/verizon-throttled-fire-departments-unlimited-data-during-calif-wildfire/', 'https://boingboing.net/2018/09/17/gougin-in-the-rain.html', 'https://www.fudzilla.com/news/34955-cisco-comes-out-against-net-neutrality', 'https://www.cultofmac.com/305821/ibm-intel-cisco-come-net-neutrality/', 'https://www.extremetech.com/computing/195790-ibm-intel-qualcomm-join-dozens-of-tech-companies-to-argue-against-net-neutrality', 'http://netneutrality.koumbit.org/en/node/5', 'https://fortune.com/2009/04/03/group-asks-fcc-to-probe-iphone-skype-restrictions/', 'https://www.wired.com/2011/01/metropcs-net-neutrality-challenge/', 'https://www.eff.org/deeplinks/2011/08/update-paxfire-and-search-redirection', 'https://www.washingtonpost.com/blogs/post-tech/post/fcc-fines-verizon-125m-for-blocking-tethering-apps/2012/07/31/gJQAXjRLNX_blog.html', 'https://arstechnica.com/tech-policy/2018/09/net-neutrality-gives-free-internet-to-netflix-and-google-isp-claims/', 'https://www.fiercewireless.com/wireless/nokia-ceo-argues-favor-paid-prioritization-net-neutrality-introduces-programmable-world', 'https://www.computerworld.com/article/2890146/net-neutrality-could-hamper-new-mobile-services-nokia-ceo-says.html', 'https://v1.escapistmagazine.com/news/view/139028-Intel-Qualcomm-Broadcom-IBM-Against-Title-II-Net-Neutrality', 'https://www.engadget.com/2014/12/11/turkeys-vote-against-christmas/', 'https://www.medianama.com/2017/05/223-akamai-net-neutrality/', 'https://www.washingtonpost.com/news/the-switch/wp/2014/11/25/wikipedias-complicated-relationship-with-net-neutrality/', 'https://www.accessnow.org/wikipedia-zero-and-net-neutrality-wikimedia-turns-its-back-on-the-open/', 'https://en.wikipedia.org/wiki/Facebook_Zero', 'https://ghostnet.fandom.com/wiki/Google_Free_Zone', 'https://www.channelpartnersonline.com/2014/12/10/alcatel-lucent-cisco-urge-fcc-to-reject-title-ii-regulation-of-internet/', 'https://www.businesswire.com/news/home/20190306005619/en/Council-Citizens-Government-Waste-Statement-Proposed-Government', 'https://www.phonenews.com/cingular-against-net-neutrality-for-consumers-1371/', 'https://www.technewsworld.com/story/56272.html']

links = net_neutral_links + non_nn_links
# to_remove = []
# clean_links = []
# for i, l in enumerate(links):
#     clean = re.search('\/url\?q\=(.*)\&sa',l)

#     # Anything that doesn't fit the above pattern will be removed
#     if clean is None:
#         to_remove.append(i)
#         continue
#     clean_links.append(clean.group(1))

# print(clean_links)

labels = len(net_neutral_links)

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
with open('page_by_page3.csv', mode='w') as csv_file:
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
            if nn_idx < labels:
                phrase_dict["NN"] = True
            else:
                phrase_dict["NN"] = False
            writer.writerow(phrase_dict)
        nn_idx += 1


