#! /usr/bin/env python3

import json

company_domains = [
    "cogentco.com",
    "about.att.com",
    "att.com",
    "attpublicpolicy.com",
    "cogentco.kr",
    "internet2.edu",
    "sprint.com",
    "telefonica.co",
    "telehouse.com",
    "telekom.com",
    "teliacompany.com",
    "t-mobile.com",


]

news_domains = [

    "theatlantic.com",
    "prnewswire.com",

    "law360.com",
    "24htech.asia",
    "abertoatedemadrugada.com",
    "adage.com",
    "advanced-television.com",
    "adweek.com",
    "aei.org",
    "afternines.com",
    "broadbandbreakfast.com",
    "broadbandtvnews.com",
    "businessinsider.com",
    "businesswire.com",
    "cnbc.com",
    "cnet.com",
    "computerworld.com",
    "consumerist.com",
    "consumerreports.org",
    "dailyherald.com",
    "datacenternews.asia",
    "denverpost.com",
    "detroitnews.com",
    "dispatch.com",
    "dmagazine.com",
    "economictimes.indiatimes.com",
    "fiercetelecom.com",
    "fiercevideo.com",
    "fiercewireless.com",
    "forbes.com",
    "fool.com",
    "freepress.net",
    "geekwire.com",
    "groundedreason.com",
    "hackaday.com",
    "ibtimes.com",
    "indiewire.com",
    "informationweek.com",
    "infoworld.com",
    "jsonline.com",
    "macrumors.com",
    "marketwatch.com",
    "m.economictimes.com",
    "money.cnn.com",
    "motherjones.com",
    "msfn.org",
    "nbcnews.com",
    "networkcomputing.com",
    "networkworld.com",
    "news.bloomberglaw.com",
    "newswire.telecomramblings.com",
    "nytimes.com",
    "pabroadbandnews.com",
    "phonearena.com",
    "reuters.com",
    "syracuse.com",
    "telecompaper.com",
    "telesintese.com.br",
    "time.com",
    "vice.com",
    "vox.com"
]

def main(inpath="output/scrape_around.json", outpath="output/stats-scrape_around.json"):
    with open(inpath, 'r') as infile:
        data = json.load(infile)
    
    stats = {}
    for company_name, company_pages in data.items():
        company_articles = len(company_pages.values())
        company_nonhtml = 0
        company_httperror = 0
        company_index = 0
        company_othererror = 0
        domains_company = 0
        domains_news = 0
        prefixes = {}
        for url, page in company_pages.items():
            # Check for errors/exclusions
            method = page["method"]
            if method is None:
                company_othererror += 1
            elif method.startswith("Unhandled content type"):
                company_nonhtml += 1
            elif method.startswith("Response"):
                company_httperror += 1
            elif method.startswith("tag"):
                company_index += 1
            elif page["filename"] is None:
                company_othererror += 1
            else:
                # Check for duplicates
                title = page["title"]
                if title is None:
                    continue
                title = title.lower().split()
                if len(title) >= 5:
                    prefix = " ".join(title[:5])
                    if prefix not in prefixes:
                        prefixes[prefix] = []
                    page["url"] = url
                    prefixes[prefix].append(page)

                # Categorize URL
                domain = url.split("/")[2]
                if domain.startswith('www.'):
                    domain = domain[4:]
                if domain in company_domains:
                    domains_company += 1
                elif domain in news_domains:
                    domains_news += 1
                #else:
                #    print(domain)

        # Count duplicates 
        company_duplicates = 0
        for prefix, pages in prefixes.items():
            if len(pages) > 1:
                print(company_name)
                for page in pages:
                    print("\t\t%s | %s | %s" % (page["filename"], page["title"], page["url"]))
                company_duplicates += len(pages) - 1

        stats[company_name] = {
            "articles" : company_articles,
            "http-error" : company_httperror,
            "other-error" : company_othererror,
            "non-html" : company_nonhtml,
            "index" : company_index,
            "duplicates" : company_duplicates,
            "final" : company_articles - (company_httperror + company_othererror + company_nonhtml + company_index + company_duplicates),
            "domains-company" : domains_company
        }

    with open(outpath, 'w') as outfile: 
        json.dump(stats, outfile, indent=4)   

if __name__ == "__main__":
    main()