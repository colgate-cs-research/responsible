import json

def main(inpath="output/scrape_around.json"):
    with open(inpath, 'r') as infile:
        pages = json.load(infile)
    
    for company, company_urls in pages.items():
        print(company)
        prefixes = {}
        for url, page in company_urls.items():
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
        for prefix, pages in prefixes.items():
            if len(pages) > 1:
                print("\t%s" % prefix)
                for page in pages:
                    print("\t\t%s | %s | %s" % (page["filename"], page["title"], page["url"]))


if __name__ == "__main__":
    main()