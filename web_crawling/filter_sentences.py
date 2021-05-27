import os
import nltk
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_entities")
#nlp.add_pipe("merge_noun_chunks")
#nlp.add_pipe('spacytextblob')

def main():
    outdir = "output"
    for company in sorted(os.listdir(outdir)):
        companydir = os.path.join(outdir, company)
        if os.path.isfile(companydir):
            continue
        if "cogent" not in company:
            continue
        print(company)
        for filename in sorted(os.listdir(companydir)):
            #if "01" not in filename:
            #    continue
            filepath = os.path.join(companydir, filename)
            print(filename)
            with open(filepath, 'r') as f:
                paragraphs = f.readlines()
            process_article(paragraphs, limit=3)
            

def process_article(paragraphs, limit=-1):
    count = 0
    for paragraph in paragraphs:
        if paragraph.startswith("##"):
            continue
        paragraph = paragraph.strip()
        if len(paragraph.split()) < 20:
            continue
        count += 1
        process_paragraph(paragraph)
 
        if limit > 0 and count >= limit:
            break

def process_paragraph(paragraph, merge_compound=False):
    #print(paragraph)
    doc = nlp(paragraph)

    # Merge Net Neutrality compund
    if (merge_compound):
        with doc.retokenize() as retokenizer:
            i = 0
            for token in doc:
                if token.text == "Net" and token.dep_ == "compound":
                    retokenizer.merge(doc[i:i+2])
                i += 1
    sentences = doc.sents
    process_sentences(sentences)

def process_sentences(sentences):
    extract_raw(sentences)
    #extract_adjectives(sentences)
    #extract_aspects(sentences)

def extract_raw(sentences):
    for sentence in sentences:
        print(sentence.text)
        for token in sentence:
            print('\t"'+token.text+'"', token.dep_, token.head.text, token.head.pos_,token.pos_,[child for child in token.children])

def extract_adjectives(sentences):
    for sentence in sentences:
        print(sentence.text)
        descriptive_terms = []
        for token in sentence:
            if token.pos_ == 'ADJ':
                descriptive_terms.append(token)
        print(descriptive_terms)

def extract_aspects(sentences):
    aspects = []
    for sentence in sentences:
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

if __name__ == "__main__":
    main()