import spacy
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

nlp = spacy.load('en')

df = pd.read_csv('aligned_labeled_data.csv', header= None)
df = df.rename(index=str, columns={ 0: "text", 1: "aspect_category", 2: "sentiment", 3: "predicted_AS"})

# assume all are labeled as NET_NEUTRAL
df = df.drop(["predicted_AS"], axis=1)
df = df.drop(["aspect_category"], axis=1)

indeces_none = df[df['sentiment'] == 'NONE'].index
df.drop(indeces_none, inplace=True)

print(Counter(df["sentiment"]).keys())


#### attempt just using ASPECT PORTION
X_train, X_test = train_test_split(df, test_size=0.10)

aspect_terms = []
for sentence in nlp.pipe(X_train.text):
    chunks = [(chunk.root.text) for chunk in sentence.noun_chunks if (chunk.root.pos_ == 'NOUN' or chunk.root.pos_ == 'PROPN')]
    aspect_terms.append(' '.join(chunks))
X_train['aspect_terms'] = aspect_terms



## build aspect categories model
aspect_categories_model = Sequential()
aspect_categories_model.add(Dense(512, input_shape=(6000,), activation='relu'))
# positive, negative, neutral -> 3
aspect_categories_model.add(Dense(3, activation='softmax'))
aspect_categories_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

vocab_size = 6000 # We set a maximum size for the vocabulary
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(X_train.text)
aspect_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(X_train.sentiment)) # map to sentiment not aspect_category

label_encoder = LabelEncoder()
integer_category = label_encoder.fit_transform(X_train.sentiment) # map to sentiment not aspect_category
dummy_category = to_categorical(integer_category)

aspect_categories_model.fit(aspect_tokenized, dummy_category, epochs=5, verbose=1)

### attempt using SENTIMENT PORTION

sentiment_terms = []
for review in nlp.pipe(X_train.text):
        if review.is_parsed:
            sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB" or token.pos_ == "PART"))]))
        else:
            sentiment_terms.append('')  
X_train['sentiment_terms'] = sentiment_terms
# print(sentiment_terms)


sentiment_model = Sequential()
sentiment_model.add(Dense(512, input_shape=(6000,), activation='relu'))
# positive, negative, neutral-> 3
sentiment_model.add(Dense(3, activation='softmax')) 
sentiment_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

sentiment_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(X_train.sentiment_terms))

label_encoder_2 = LabelEncoder()
integer_sentiment = label_encoder_2.fit_transform(X_train.sentiment)
dummy_sentiment = to_categorical(integer_sentiment)

sentiment_model.fit(sentiment_tokenized, dummy_sentiment, epochs=5, verbose=1)


# Aspect preprocessing
test_reviews = X_test.text
test_aspect_terms = []
for review in nlp.pipe(test_reviews):
    chunks = [(chunk.root.text) for chunk in review.noun_chunks if (chunk.root.pos_ == 'NOUN' or chunk.root.pos_ == 'PROPN')]
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

aspect_model_accuracy = 0
sentiment_model_accuracy = 0

while j < len(X_test.sentiment):
    print()
    print(test_reviews[j])
    print("Aspect model answer: Review " + str(j+1) + " is expressing a  " + test_aspect_categories[j] + " opinion about net neutrality")
    #print(dataset_test.iloc[j, 0])
    print("Sentiment model answer: Review " + str(j+1) + " is expressing a  " + test_sentiment[j] + " opinion about net neutrality")
    print("True answer: Review " + str(j+1) + " is expressing a  " + X_test.iloc[j, 1] + " opinion about net neutrality")
    print()
    if test_aspect_categories[j] == X_test.iloc[j, 1]:
        aspect_model_accuracy += 1
    if test_sentiment[j] == X_test.iloc[j, 1]:
        sentiment_model_accuracy += 1
    j += 1

print("sentiment model accuracy: {}".format(sentiment_model_accuracy/j))
print("aspect model accuracy: {}".format(aspect_model_accuracy/j))  

