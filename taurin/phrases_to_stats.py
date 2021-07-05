#! /usr/bin/env python3

import json

def main(inpath="output/extract_around.json", outpath="output/stats-phrases_around.json"):
    with open(inpath, 'r') as infile:
        data = json.load(infile)
    
    stats = {}
    for company_name, company in data.items():
        company_articles = len(company.values())
        company_phrases = 0
        no_phrases = 0
        one_phrase = 0
        more_phrases = 0
        for article in company.values():
            article_phrases = 0
            for paragraph in article["paragraphs"]:
                for sentence in paragraph:
                    if "company" in sentence["phrases"]:
                        #article_phrases += len(sentence["phrases"]["company"])
                        article_phrases += 1
            company_phrases += article_phrases
            if article_phrases == 0:
                no_phrases += 1
            elif article_phrases == 1:
                one_phrase += 1
            elif article_phrases > 1:
                more_phrases += 1
        stats[company_name] = {
            "articles" : company_articles,
            "phrases" : company_phrases,
            "articles_with_0_phrases" : no_phrases,
            "articles_with_1_phrase" : one_phrase,
            "articles_with_2+_phrases" : more_phrases
        }

    with open(outpath, 'w') as outfile: 
        json.dump(stats, outfile, indent=4)   

if __name__ == "__main__":
    main()