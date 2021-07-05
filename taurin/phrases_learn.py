#! /usr/bin/env python3

import numpy
import spacy
from sklearn.svm import SVC
from sklearn.metrics import precision_score, recall_score, average_precision_score
import pprint

nlp = spacy.load("en_core_web_md")
label_map = {"OPPOSE": -1, "AGAINST" : -1, "FAVOR": 1, "NONE": 0, "UNKNOWN": 0, "MIXED" : 0, "LANGUAGE" : 0 }

#def main(csvfile="output/company_no-unknown.csv"):
def main(csvfile="output/phrases_around_sentences_no-unknown.csv"):
    isps, vectors, labels = get_data(csvfile)
    learn(vectors, labels)
    stats(isps, labels)

"""Get vectors and labels for a file of labeled phrases"""
def get_data(csvfile):
    with open(csvfile, 'r') as csvfile:
        isps = []
        vectors = []
        labels = []
        for line in csvfile:
            values = line.strip().split('\t')
            if len(values) == 2:
                isp = None
                phrase = values[0]
                label = values[1]
            else:
                isp = values[0][:-8]
                phrase = values[1]
                label = values[2]
            if isp is not None:
                isps.append(isp)
            vectors.append(get_vector(phrase))
            try:
                labels.append(get_label(label))
            except:
                print(line)
    return isps, vectors, labels

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
    confusion_matrix = { -1 : {-1 : 0, 1 : 0}, 1 : {-1 : 0, 1 : 0}}
    for i in range(0, len(vectors)-(len(vectors) % fold), fold):
        train_vectors = vectors[:i] + vectors[i+fold:]
        train_labels = labels[:i] + labels[i+fold:]
        test_vectors = vectors[i:i+fold]
        test_labels = labels[i:i+fold]
        classifier = SVC(kernel="rbf").fit(train_vectors, train_labels)
        accuracy = classifier.score(test_vectors, test_labels)
        print("Accuracy for fold ", int(i/fold+1), ": ", round(accuracy*100,2), "%", sep="")
        total += accuracy
        test_predict = classifier.predict(test_vectors)
        for i in range(len(test_predict)):
            predicted = test_predict[i]
            expected = test_labels[i]
            confusion_matrix[predicted][expected] += 1
        #print(precision_score(test_predict, test_labels))
    print("Total accuracy: ", round(total/10*100,2), "%", sep="")
    print("Confusion matrix")
    for predicted, predicted_counts in confusion_matrix.items():
        for expected, count in predicted_counts.items():
            print("\tPredicted: %d\tExpected: %d\t%d" % (predicted, expected, count))

def stats(isps, labels):
    counts = { "TOTAL" : {-1 : 0, 0 : 0, 1: 0 }}
    for i in range(len(labels)):
        label = labels[i]
        counts["TOTAL"][label] += 1
        if len(isps) > 0:
            isp = isps[i]
            if isp not in counts:
                counts[isp] = {-1 : 0, 0 : 0, 1: 0 }
            counts[isp][label] += 1
    pprint.PrettyPrinter(indent=4).pprint(counts)

if __name__ == "__main__":
    main()