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
df = df.drop(["predicted_AS"], axis=1)

indeces_none = df[df['aspect_category'] == 'NONE'].index
df.drop(indeces_none, inplace=True)

indeces_BS = df[df['aspect_category'] == 'BLOCKING SHAPING'].index
df['aspect_category'][indeces_BS] = 'SHAPING'

print(Counter(df["aspect_category"]).keys())


#### ASPECT PORTION
X_train, X_test = train_test_split(df, test_size=0.10)

aspect_terms = []
for sentence in nlp.pipe(X_train.text):
    chunks = [(chunk.root.text) for chunk in sentence.noun_chunks if (chunk.root.pos_ == 'NOUN' or chunk.root.pos_ == 'PROPN')]
    # chunks = [(chunk.root.text) for chunk in sentence.noun_chunks if (chunk.root.pos_ == 'NOUN')]
    aspect_terms.append(' '.join(chunks))
X_train['aspect_terms'] = aspect_terms



## build aspect categories model
aspect_categories_model = Sequential()
aspect_categories_model.add(Dense(512, input_shape=(6000,), activation='relu'))
# net_neutral, blocking, shaping, fcc_repeal-> 4
aspect_categories_model.add(Dense(4, activation='softmax'))
aspect_categories_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

vocab_size = 6000 # We set a maximum size for the vocabulary
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(X_train.text)
aspect_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(X_train.aspect_terms))

label_encoder = LabelEncoder()
integer_category = label_encoder.fit_transform(X_train.aspect_category)
dummy_category = to_categorical(integer_category)

aspect_categories_model.fit(aspect_tokenized, dummy_category, epochs=5, verbose=1)

### SENTIMENT PORTION

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
    # chunks = [(chunk.root.text) for chunk in review.noun_chunks if (chunk.root.pos_ == 'NOUN')]
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

while j < len(X_test.sentiment):
    print()
    print(test_reviews[j])
    print("Model answer: Review " + str(j+1) + " is expressing a  " + test_sentiment[j] + " opinion about " + test_aspect_categories[j])
    #print(dataset_test.iloc[j, 0])
    print("True answer: Review " + str(j+1) + " is expressing a  " + X_test.iloc[j, 2] + " opinion about " + X_test.iloc[j, 1])
    print()
    j += 1
    

