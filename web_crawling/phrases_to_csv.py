#! /usr/bin/env python3

import json

def main(inpath="output/phrases_net-neutrality_debug.log", outpath="output/company_net-neutrality.csv"):

    with open(outpath, 'w') as outfile:
        with open(inpath, 'r') as infile:
            for line in infile:
                line = line.strip()
                if not line.startswith("{"):
                    continue
                phrases = eval(line)
                if "company" not in phrases:
                    continue
                for phrase in phrases["company"]:
                    outfile.write("%s\t%s\n" % (phrase.strip(), "TODO"))

if __name__ == "__main__":
    main()