import json
import os

def main(base_indir="output/taurin_submit/pages/", outpath="output/search.json"):
    result = process_indir(base_indir)
    with open(outpath, 'w') as outfile:
        json.dump(result, outfile, indent=4)

def process_indir(indir):
    result = {}
    for company in sorted(os.listdir(indir)):
        result[company] = process_company(company, indir)
    return result

def process_company(company, indir):
    result = {}
    companydir = os.path.join(indir, company)
    for filename in sorted(os.listdir(companydir)):
        try:
            url, keywords = process_file(company, filename, indir)
            result[url] = keywords
        except Exception as ex:
            print(ex)
    return result
            
def process_file(company, filename, indir="output"):
    print("Processing %s %s..." % (company, filename))#, file=sys.stderr)
    filepath = os.path.join(indir, company, filename)
    with open(filepath, 'r') as f:
        paragraphs = f.readlines()

    link_raw = paragraphs[0]
    _, url = link_raw.split(':', 1)
    url = url.strip()
    keywords_raw = paragraphs[1]
    _, keywords = keywords_raw.split(':', 1)
    keywords = keywords.strip().split(',')

    return url, keywords
    
if __name__ == "__main__":
    main()
