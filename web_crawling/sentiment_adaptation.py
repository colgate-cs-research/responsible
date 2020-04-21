import spacy
import pickle
import pandas as pd
import numpy as np
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

nlp = spacy.load('en')

df = pd.read_csv('aligned_labeled_data.csv', header= None)
df = df.rename(index=str, columns={ 0: "text", 1: "aspect_category", 2: "sentiment", 3: "predicted_AS"})

# assume all are labeled as NET_NEUTRAL
df = df.drop(["predicted_AS"], axis=1)
df = df.drop(["aspect_category"], axis=1)

indeces_none = df[df['sentiment'] == 'NONE'].index
df.drop(indeces_none, inplace=True)

## TRY DROPPING NEUTRAL LABEL
indeces_neutral = df[df['sentiment'] == 'NEUTRAL'].index
df.drop(indeces_neutral, inplace=True)


print(Counter(df["sentiment"]).keys())

#X_train, X_test = train_test_split(df, test_size=0.10)
kf = KFold(n_splits = 10) # break into tenths
accuracy_list = []

### attempt using SENTIMENT PORTION
for train_index, test_index in kf.split(df):
    X_train = df.iloc[train_index]
    X_test = df.iloc[test_index]

    sentiment_terms = []
    for review in nlp.pipe(X_train.text):
            if review.is_parsed:
                sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB" or token.pos_ == "PART"))]))
            else:
                sentiment_terms.append('')  
    X_train['sentiment_terms'] = sentiment_terms
    # print(sentiment_terms)

    vocab_size = 6000 # We set a maximum size for the vocabulary
    sentiment_model = Sequential()
    sentiment_model.add(Dense(512, input_shape=(6000,), activation='relu'))
    # positive, negative, neutral-> 3
    # WITHOUT NEUTRAL -> 2
    sentiment_model.add(Dense(2, activation='softmax')) 
    sentiment_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


    tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(X_train.text)
    tok_file= open('tokenizer.pkl', 'wb')
    pickle.dump(tokenizer, tok_file)
    tok_file.close()
    sentiment_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(X_train.sentiment_terms))

    label_encoder_2 = LabelEncoder()
    integer_sentiment = label_encoder_2.fit_transform(X_train.sentiment)
    le_file= open('label_encoder.pkl', 'wb')
    pickle.dump(label_encoder_2, le_file)
    le_file.close()
    dummy_sentiment = to_categorical(integer_sentiment)

    sentiment_model.fit(sentiment_tokenized, dummy_sentiment, epochs=5, verbose=1)

    test_reviews = X_test.text
                                
    # Sentiment preprocessing
    test_sentiment_terms = []
    for review in nlp.pipe(test_reviews):
            if review.is_parsed:
                test_sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
            else:
                test_sentiment_terms.append('') 
    test_sentiment_terms = pd.DataFrame(tokenizer.texts_to_matrix(test_sentiment_terms))

    # Models output
    test_sentiment = label_encoder_2.inverse_transform(sentiment_model.predict_classes(test_sentiment_terms))
    j = 0

    sentiment_model_accuracy = 0

    # pos_but_neg = 0
    # neutral_but_neg = 0

    # pos_but_neutral = 0
    # neg_but_neutral = 0

    # neg_but_pos = 0
    # neutral_but_pos = 0

    # num_errors = 0

    while j < len(X_test.sentiment):
        # print()
        # print(test_reviews[j])
        # print("Sentiment model answer: Review " + str(j+1) + " is expressing a  " + test_sentiment[j] + " opinion about net neutrality")
        # print("True answer: Review " + str(j+1) + " is expressing a  " + X_test.iloc[j, 1] + " opinion about net neutrality")
        # print()
        if test_sentiment[j] == X_test.iloc[j, 1]:
            sentiment_model_accuracy += 1
        # else:
        #     num_errors += 1
        #     if test_sentiment[j] == 'NEUTRAL':
        #         if X_test.iloc[j, 1] == 'POSITIVE':
        #             pos_but_neutral += 1
        #         else: # guessed negative
        #             neg_but_neutral += 1
        #     elif test_sentiment[j] == 'NEGATIVE':
        #         if X_test.iloc[j, 1] == 'POSITIVE':
        #             pos_but_neg += 1
        #         else: # guessed neutral
        #             neutral_but_neg += 1
        #     else: # correst sentiment is positive
        #         if X_test.iloc[j, 1] == 'NEGATIVE':
        #             neg_but_pos += 1
        #         else: # guessed neutral
        #             neutral_but_pos += 1
        j += 1


    print("sentiment model accuracy: {}".format(sentiment_model_accuracy/j))
    accuracy_list.append(sentiment_model_accuracy/j)

print("avg accuracy: {}".format(sum(accuracy_list)/10))
# print("Breakdown of errors:")
# print("######################")
# print("Guessed negative when positive: {}".format(neg_but_pos/j))
# print("######################")
# print("Guessed negative when neutral: {}".format(neg_but_neutral/j))
# print("Guessed neutral when positive: {}".format(neutral_but_pos/j))
# print("Guessed neutral when negative: {}".format(neutral_but_neg/j))
# print("######################")
# print("Guessed positive when negative: {}".format(pos_but_neg/j))
# print("######################")
# print("Guessed positive when neutral: {}".format(pos_but_neutral/j))

model_json = sentiment_model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
sentiment_model.save_weights("model.h5")
print("Saved model to disk")



