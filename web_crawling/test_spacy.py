import spacy
nlp = spacy.load("en")
doc = nlp("I am not angry that my dog ate my homework")

for word in doc:
    print(word)
    print(word.pos_)
    print(word.lemma_)