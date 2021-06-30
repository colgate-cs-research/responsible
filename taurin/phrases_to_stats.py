#! /usr/bin/env python3

import json

def main(inpath="output/extract.json", outpath="output/stats.json"):
    with open(inpath, 'r') as infile:
        data = json.load(infile)
    
    stats = {}
    for company_name, company in data.items():
        company_articles = len(company.values())
        company_phrases = 0
        for article in company.values():
            article_phrases = 0
            for paragraph in article["paragraphs"]:
                for sentence in paragraph:
                    if "company" in sentence["phrases"]:
                        article_phrases += len(sentence["phrases"]["company"])
            company_phrases += article_phrases
        stats[company_name] = {
            "articles" : company_articles,
            "phrases" : company_phrases
        }

    with open(outpath, 'w') as outfile: 
        json.dump(stats, outfile, indent=4)   

if __name__ == "__main__":
    main()