#! /usr/bin/env python3

import json

def main(inpath="output/extract.json", outpath="output/company.csv"):
    with open(inpath, 'r') as infile:
        data = json.load(infile)
    
    with open(outpath, 'w') as outfile:
        for company_name, company in data.items():
            for article_name, article in company.items():
                for paragraph in article["paragraphs"]:
                    for sentence in paragraph:
                        if "company" in sentence["phrases"]:
                            for phrase in sentence["phrases"]["company"]:
                                outfile.write("%s\5%s\t%s\t%s\n" % (company_name, article_name, phrase.strip(), "TODO"))

if __name__ == "__main__":
    main()