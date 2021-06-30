import os
import spacy
#import neuralcoref
import json

keywords = ["net neutrality", "open internet", "zero-rating", "paid prioritization"]

companies = {
    "Cogent Communications": ["Cogent"], 
    "FirstLight Fiber": ["FirstLight"], 
    "Hurricane Electric": ["Hurricane"],
    "Internet2": [],
    "Zayo": [],
    "NYSERNet": [],
    "Orange": [], 
    "Telia Carrier": ["Telia"], 
    "Sprint": [], 
    "AT&T": [], 
    "Deutsche Telekom": ["Telekom", "DT"],
    "Telefonica": ["Telefónica"], 
    "British Telecom": ["BT"], 
    "KDDI": []
    }

nlp = spacy.load("en_core_web_md")
nlp.add_pipe("merge_entities")
nlp.add_pipe("merge_noun_chunks")
#nlp.add_pipe('spacytextblob')
#neuralcoref.add_pipe(nlp)

def main():
    #process_file("cogent communications", "01.txt")
    #process_file("cogent communications", "03.txt")
    #process_file("AT&T", "02.txt")
    result = process_outdir("output/taurin_submit/pages")
    #result = {"FirstLight Fiber" : process_company("FirstLight Fiber", "output/taurin_submit/pages")}
    #result = {"Deutsche Telekom" : process_company("Deutsche Telekom", "output/taurin_submit/pages")}
    with open("output/extract.json", 'w') as out:
        json.dump(result, out, indent=4)

def process_outdir(outdir="output/pages"):
    result = {}
    for company in sorted(os.listdir(outdir)):
        result[company] = process_company(company, outdir)
    return result
    
def process_company(company, outdir):
    result = {}
    companydir = os.path.join(outdir, company)
    for filename in sorted(os.listdir(companydir)):
        try:
            result[filename] = process_file(company, filename, outdir)
        except Exception as ex:
            print(ex)
    return result
            
def process_file(company, filename, outdir="output"):
    print("Processing %s %s..." % (company, filename))#, file=sys.stderr)
    filepath = os.path.join(outdir, company, filename)
    with open(filepath, 'r') as f:
        paragraphs = f.readlines()
    result = process_article(company, paragraphs, limit=-1)
    #print("*****%s,%s,%d" %( company, filename, phrases))#, file=sys.stderr)
    return result

def process_article(company, paragraphs, limit=-1):
    count = 0
    result = {"paragraphs" : []}
    for paragraph in paragraphs:
        if paragraph.startswith("##"):
            index = paragraph.find(': ')
            key = paragraph[2:index].lower()
            value = paragraph[index+2:].strip()
            if key == "keywords":
                value = value.split(',')
            result[key] = value
            continue
        paragraph = paragraph.strip()
        if len(paragraph.split()) < 25:
            continue
        count += 1
        paragraph_result = process_paragraph(company, paragraph, count, merge_compound=True)
        if len(paragraph_result) > 0:
            result["paragraphs"].append(paragraph_result)
 
        if limit > 0 and count >= limit:
            break
    return result

def process_paragraph(company, paragraph, num, merge_compound=False):
    #print(paragraph)
    doc = nlp(paragraph)

    # Merge Net Neutrality compund
    if (merge_compound):
        with doc.retokenize() as retokenizer:
            i = 0
            for token in doc:
                if token.text.lower() == "net" and token.nbor().text.lower() == "neutrality": #token.dep_ == "compound":
                    retokenizer.merge(doc[i:i+2])
                i += 1

    #svg = spacy.displacy.render(doc, style='dep')
    #svg_path = os.path.join("output", "svgs", "%02d.svg" % num)
    #with open(svg_path, "w", encoding="utf-8") as f:
    #    f.write(svg)

    sentences = doc.sents
    #if doc._.has_coref:
    #    print(doc._.coref_clusters)
    result = process_sentences(company, sentences)
    return result

def process_sentences(company, sentences):
    result = []
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence.text.lower():
                #extract_adjectives(sentence)
                #extract_aspects(sentence)
                phrases = extract_phrases(company, sentence)
                if phrases is not None:
                    tokens = extract_token_details(sentence)
                    result.append(
                        {"sentence" : sentence.text,
                        "tokens" : tokens,
                        "phrases" : phrases})
                break
    return result

def extract_token_details(sentence):
    tokens = []
    for token in sentence:
        tokens.append({"text": token.text, 
        "pos" : token.pos_,
        "dep" : token.dep_,
        "head_text" : token.head.text,
        "head_pos" : token.head.pos_,
        "children" : [child.text for child in token.children]})
    return tokens

def extract_adjectives(sentence):
    print(sentence.text)
    descriptive_terms = []
    for token in sentence:
        if token.pos_ == 'ADJ':
            descriptive_terms.append(token)
    #print(descriptive_terms)

def extract_aspects(sentence):
    aspects = []
    descriptive_term = ''
    target = ''
    for token in sentence:
        if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
            target = token.text
        if token.pos_ == 'ADJ':
            prepend = ''
            for child in token.children:
                if child.pos_ != 'ADV':
                    continue
                prepend += child.text + ' '
            descriptive_term = prepend + token.text
    aspects.append({'aspect': target,
    'description': descriptive_term})
    #print(aspects)

def extract_phrases(company, sentence):
    phrases  = {"company" : []}
    for keyword in keywords:
        phrases[keyword] = []

    for token in sentence:
        token_text = token.text.lower()
        for keyword in keywords:
            if keyword in token_text:
                if token.dep_ == 'dobj': # Direct object
                    parent = token.head
                    verb = parent.text
                    #stance = ""
                    #while True:
                    #    stance = parent.text + " " + stance
                    #    if parent.dep_ == "ROOT":
                    #        break
                    #    parent = parent.head
                    who = "XXX"
                    for child in parent.children:
                        if child.dep_ == 'nsubj':
                            who = child.text
                    phrases[keyword].append(" ".join([who, verb, token.text]))
                elif token.dep_ == 'pobj': # Object of preposition
                    parent = token.head
                    correlation = parent.text
                    grandparent = parent.head
                    what = grandparent.text
                    #phrases[keyword].append(" ".join([what, correlation, token.text]))
        for name in [company] + companies[company]:
            if name.lower() in token_text:
                if token.dep_ == 'nsubj': # Nominal subject
                    subject = token
                    verbs = [token.head]
                    if verbs[-1].pos_ == "AUX":
                        verbs += [verbs[-1].head]
                    for child in verbs[-1].rights:
                        if child.dep_ in ["ccomp", "xcomp", "dobj"]:
                            phrase = " ".join([subject.text, collate_verbs(verbs), collate_prep(child)])
                            if phrase not in phrases["company"]:
                                phrases["company"].append(phrase)
                        if child.dep_ in ["prep"]:
                            phrase = " ".join([subject.text, collate_verbs(verbs), collate_prep(child)])
                            if phrase not in phrases["company"]:
                                phrases["company"].append(phrase)

    # Only print keywords with phrases
    phrases = {key:value for (key,value) in phrases.items() if len(value) > 0}
    if len(phrases) > 0:
        return phrases
    return None

def collate_verbs(verbs):
    verbs = [] + verbs
    i = -1
    last_verb = verbs[-1]
    while len(list(last_verb.lefts)) > 0:
        pre_verb = list(last_verb.lefts)[-1]
        if pre_verb.dep_ in ["advmod", "neg", "aux"]:
            i = i - 1
            verbs.insert(i, pre_verb)
            last_verb = pre_verb
        else:
            break
    if len(list(last_verb.rights)) > 0:
        post_verb = list(last_verb.rights)[0]
        if post_verb.dep_ in ["attr"]:
            verbs.insert(-1, post_verb)
    return " ".join([v.text for v in verbs])

def collate_prep(start):
    current = start
    more = True
    result = [start.text]
    #print("\t\t", result)
    while more:
        more = False
        for child in current.children:
            if child.dep_ in ["prep", "pobj", "pcomp", "dobj", "acomp", "attr"]:
                result.append(child.text)
                more = True
                current = child
                break
            elif child.dep_ in ["nsubj", "advmod"]:
                result.insert(0, child.text)
            elif child.dep_ in ["neg"]:
                result.insert(-1, child.text)
    return " ".join(result)

if __name__ == "__main__":
    main()
