import spacy
import pandas as pd
import numpy as np
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import KFold

nlp = spacy.load('en')

whole_dataset = pd.read_csv('more_data.csv', header= None)
whole_dataset = whole_dataset.rename(index=str, columns={ 0: "text", 1: "aspect_category", 2: "sentiment"})
kf = KFold(n_splits = 10) # break into tenths

for train_index, test_index in kf.split(whole_dataset):
    # split train and test reviews
    dataset = whole_dataset.iloc[train_index]
    dataset_test = whole_dataset.iloc[test_index]

    #### ASPECT PORTION

    aspect_terms = []
    for sentence in nlp.pipe(dataset.text):
        chunks = [(chunk.root.text) for chunk in sentence.noun_chunks if (chunk.root.pos_ == 'NOUN')]
        aspect_terms.append(' '.join(chunks))
    dataset['aspect_terms'] = aspect_terms


    ## build aspect categories model
    aspect_categories_model = Sequential()
    aspect_categories_model.add(Dense(512, input_shape=(1000,), activation='relu'))
    # net_neutral, blocking, shaping, fcc_repeal-> 4
    aspect_categories_model.add(Dense(4, activation='softmax'))
    aspect_categories_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    vocab_size = 1000 # We set a maximum size for the vocabulary
    tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(dataset.text)
    aspect_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(dataset.aspect_terms))

    label_encoder = LabelEncoder()
    integer_category = label_encoder.fit_transform(dataset.aspect_category)
    dummy_category = to_categorical(integer_category)

    aspect_categories_model.fit(aspect_tokenized, dummy_category, epochs=10, verbose=1)

    ### SENTIMENT PORTION

    sentiment_terms = []
    for review in nlp.pipe(dataset['text']):
            if review.is_parsed:
                sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
            else:
                sentiment_terms.append('')  
    dataset['sentiment_terms'] = sentiment_terms

    sentiment_model = Sequential()
    sentiment_model.add(Dense(512, input_shape=(1000,), activation='relu'))
    # positive, negative, neutral-> 3
    sentiment_model.add(Dense(3, activation='softmax')) 
    sentiment_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    sentiment_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(dataset.sentiment_terms))

    label_encoder_2 = LabelEncoder()
    integer_sentiment = label_encoder_2.fit_transform(dataset.sentiment)
    dummy_sentiment = to_categorical(integer_sentiment)

    sentiment_model.fit(sentiment_tokenized, dummy_sentiment, epochs=10, verbose=1)


    # Aspect preprocessing
    test_reviews = dataset_test['text']
    test_aspect_terms = []
    for review in nlp.pipe(test_reviews):
        chunks = [(chunk.root.text) for chunk in review.noun_chunks if (chunk.root.pos_ == 'NOUN')]
        test_aspect_terms.append(' '.join(chunks))
    test_aspect_terms = pd.DataFrame(tokenizer.texts_to_matrix(test_aspect_terms))

                                
    # Sentiment preprocessing
    test_sentiment_terms = []
    for review in nlp.pipe(test_reviews):
            if review.is_parsed:
                test_sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
            else:
                test_sentiment_terms.append('') 
    test_sentiment_terms = pd.DataFrame(tokenizer.texts_to_matrix(test_sentiment_terms))

    # Models output
    test_aspect_categories = label_encoder.inverse_transform(aspect_categories_model.predict_classes(test_aspect_terms))
    test_sentiment = label_encoder_2.inverse_transform(sentiment_model.predict_classes(test_sentiment_terms))
    j = 0
    correct_sentiment = 0
    correct_aspect = 0
    while j < len(test_index):
        print()
        print(test_reviews[j])
        print("Model answer: Review " + str(j+1) + " is expressing a  " + test_sentiment[j] + " opinion about " + test_aspect_categories[j])
        #print(dataset_test.iloc[j, 0])
        print("True answer: Review " + str(j+1) + " is expressing a  " + dataset_test.iloc[j, 2] + " opinion about " + dataset_test.iloc[j, 1])
        print()
        if test_sentiment[j] is dataset_test.iloc[j, 2]:
            correct_sentiment += 1
        if test_aspect_categories[j] is dataset_test.iloc[j, 1]:
            correct_aspect += 1
        j += 1

    print('------------------------------')
    print("Sentiment accuracy this round is : " + str(correct_sentiment/j))
    print()
    print("Aspect accuracy this round is : " + str(correct_aspect/j))
    print('------------------------------')
    

