import json
import spacy
import pickle
import pandas as pd
import numpy as np
from urllib import request
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from keras.models import model_from_json
from create_csv_from_paths import get_AS_text

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

paths_file = open("sample_paths.txt", "r")
i = 0

# store unique ASNs/ASes
ASNs = []
AS_names_to_query = []

# these will be evaluated after we predict whether an AS is net neutral or not
paths_to_evaluate = []

for line in paths_file:
    path = line.split()
    # get ASes you want to evaluate- source and destination don't need to be evaluated
    intermediate_path = path[1:-1]
    if intermediate_path not in paths_to_evaluate:
        paths_to_evaluate.append(intermediate_path)
        for AS in intermediate_path:
            if AS not in ASNs:
                ASNs.append(AS)

paths_file.close()

# get AS names to query from ASNs
AS_to_ASN_dict = {}

for AS in ASNs:
    url = 'https://api.bgpview.io/asn/'  + str(AS)
    page = request.urlopen(url)
    content = page.read()
    soup = BeautifulSoup(content, 'html.parser')
    dictionary = json.loads(soup.text)
    description = dictionary['data']['description_short']
    AS_names_to_query.append(description)
    AS_to_ASN_dict[description] = AS #AS is ASN, description is name

output_file = 'AS_scraped_text.csv'

# get data (csv file) to run through model
# get_AS_text(AS_names_to_query, output_file)

# open data in output file
df = pd.read_csv(output_file)

# sentiment preprocessing

nlp = spacy.load('en')
test_sentiment_terms = []
for review in nlp.pipe(df.sentence):
    if review.is_parsed:
        test_sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
    else:
        test_sentiment_terms.append('') 

tok_file = open('tokenizer.pkl', 'rb')
tokenizer = pickle.load(tok_file) 
tok_file.close()
test_sentiment_terms = pd.DataFrame(tokenizer.texts_to_matrix(test_sentiment_terms))

# Model output
pkl_file = open('label_encoder.pkl', 'rb')
label_encoder_2 = pickle.load(pkl_file) 
pkl_file.close()
test_sentiment = label_encoder_2.inverse_transform(loaded_model.predict_classes(test_sentiment_terms))

# evaluate NN of ASes
NN_dict = {}

# Get net neutrality status of each individual AS, store in dictionary
for AS in AS_names_to_query:
    ASN = AS_to_ASN_dict[AS]
    indices = df[df['search term'] == AS].index
    sentiments = test_sentiment[indices]
    positives = np.count_nonzero(sentiments == 'POSITIVE')
    if positives > (1/2)*len(sentiments):
        NN_dict[ASN] = "POSITIVE"
    else:
        NN_dict[ASN] = "NEGATIVE"
print(NN_dict)

# label paths as socially responsble if all ASes are NN along it, else not socially responsible
for path in paths_to_evaluate:
    NN = True
    for AS in path:
        if NN_dict[AS] == "NEGATIVE":
            print(str(path) + " is NOT socially responsible")
            NN = False
    if NN:
        print(str(path) + " IS socially responsible")






