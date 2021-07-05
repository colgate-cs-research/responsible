#! /usr/bin/env python3

import json

def main(inpath="output/search_no-around.json", outpath="output/stats-search_no-around.json"):
    with open(inpath, 'r') as infile:
        data = json.load(infile)
    
    stats = {}
    for company_name, company_urls in data.items():
        company_urls = len(company_urls)
        stats[company_name] = {
            "urls" : company_urls
        }

    with open(outpath, 'w') as outfile: 
        json.dump(stats, outfile, indent=4)   

if __name__ == "__main__":
    main()