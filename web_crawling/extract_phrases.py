import os
import spacy
#import neuralcoref

nlp = spacy.load("en_core_web_md")
nlp.add_pipe("merge_entities")
nlp.add_pipe("merge_noun_chunks")
#nlp.add_pipe('spacytextblob')
#neuralcoref.add_pipe(nlp)

def main():
    #process_file("cogent communications", "01.txt")
    #process_file("cogent communications", "03.txt")
    #process_file("AT&T", "02.txt")
    process_outdir()

def process_outdir(outdir="output"):
    for company in sorted(os.listdir(outdir)):
        companydir = os.path.join(outdir, company)
        if os.path.isfile(companydir) or companydir == "svgs":
            continue
        for filename in sorted(os.listdir(companydir)):
            process_file(company, filename, outdir)
            
def process_file(company, filename, outdir="output"):
    print(company, filename)
    filepath = os.path.join(outdir, company, filename)
    with open(filepath, 'r') as f:
        paragraphs = f.readlines()
    process_article(company, paragraphs, limit=-1)

def process_article(company, paragraphs, limit=-1):
    count = 0
    for paragraph in paragraphs:
        if paragraph.startswith("##"):
            continue
        paragraph = paragraph.strip()
        if len(paragraph.split()) < 25:
            continue
        count += 1
        process_paragraph(company, paragraph, count, merge_compound=True)
 
        if limit > 0 and count >= limit:
            break

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
    process_sentences(company, sentences)

def process_sentences(company, sentences, keywords=["net neutrality", "open internet", "zero-rating"]):
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence.text.lower():
                #extract_raw(sentence)
                #extract_adjectives(sentence)
                #extract_aspects(sentence)
                extract_phrases(company, sentence, keywords)
                break

def extract_raw(sentence):
    print(sentence.text)
    for token in sentence:
        print('\t"'+token.text+'"', token.pos_, token.dep_, '"'+token.head.text+'"', token.head.pos_, [child for child in token.children])

def extract_adjectives(sentence):
    print(sentence.text)
    descriptive_terms = []
    for token in sentence:
        if token.pos_ == 'ADJ':
            descriptive_terms.append(token)
    print(descriptive_terms)

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
    print(aspects)

def extract_phrases(company, sentence, keywords):
    company = company.lower()

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
                    phrases[keyword].append(" ".join([who, verb, token_text]))
                elif token.dep_ == 'pobj': # Object of preposition
                    parent = token.head
                    correlation = parent.text
                    grandparent = parent.head
                    what = grandparent.text
                    phrases[keyword].append(" ".join([what, correlation, token_text]))
        if company in token_text:
            if token.dep_ == 'nsubj': # Nominal subject
                parent = token.head
                verb = parent.text
                if parent.pos_ == "AUX":
                    token = parent
                    parent = parent.head
                    verb = parent.text
                seen_token = False
                for child in parent.children:
                    if child == token:
                        seen_token = True
                    if child.dep_ in ["ccomp", "xcomp", "dobj"]:
                        phrases["company"].append(" ".join([token_text, verb, collate_prep(child)]))
                    if seen_token and child.dep_ in ["prep"]:
                        phrases["company"].append(" ".join([token_text, verb, collate_prep(child)]))
    print(phrases)

def collate_prep(start):
    current = start
    more = True
    result = [start.text]
    while more:
        more = False
        for child in current.children:
            if child.dep_ in ["prep", "pobj", "pcomp", "dobj", "acomp", "attr"]:
                result.append(child.text)
                more = True
                current = child
                break
            elif child.dep_ in ["nsubj"]:
                result.insert(0, child.text)
            elif child.dep_ in ["neg"]:
                result.insert(-1, child.text)
    return " ".join(result)

if __name__ == "__main__":
    main()