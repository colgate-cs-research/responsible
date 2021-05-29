#! /usr/bin/env python3

import numpy
import spacy
from sklearn.svm import SVC

nlp = spacy.load("en_core_web_md")
label_map = {"AGAINST": 0, "FAVOR": 1, "NONE": 2, "UNKNOWN": 2}

def main(csvfile="output/company_net-neutrality.csv"):
    vectors, labels = get_data(csvfile)
    learn(vectors, labels)

"""Get vectors and labels for a file of labeled phrases"""
def get_data(csvfile):
    with open(csvfile, 'r') as csvfile:
        vectors = []
        labels = []
        for line in csvfile:
            values = line.strip().split('\t')
            vectors.append(get_vector(values[0]))
            labels.append(get_label(values[1]))
    return vectors, labels

"""Get vector for a phrase"""
def get_vector(phrase):
    phrase = nlp(phrase)
    phrase_vector = None
    for token in phrase:
        if token.has_vector:
            if phrase_vector is None:
                phrase_vector = numpy.array(token.vector)
            else:
                phrase_vector += numpy.array(token.vector)
    return phrase.vector

"""Convert a label to a numberic value"""
def get_label(label):
    return label_map[label]

def learn(vectors, labels):
    # 10-fold cross-validation
    total = 0
    fold = int(len(vectors)/10)
    for i in range(0, len(vectors)-(len(vectors) % fold), fold):
        train_vectors = vectors[:i] + vectors[i+fold:]
        train_labels = labels[:i] + labels[i+fold:]
        test_vectors = vectors[i:i+fold]
        test_labels = labels[i:i+fold]
        classifier = SVC(kernel="rbf").fit(train_vectors, train_labels)
        accuracy = classifier.score(test_vectors, test_labels)
        print("Accuracy for fold ", int(i/fold+1), ": ", round(accuracy*100,2), "%", sep="")
        total += accuracy
    print("Total accuracy: ", round(total/10*100,2), "%", sep="")


if __name__ == "__main__":
    main()