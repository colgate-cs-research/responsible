import spacy
import pandas as pd
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

dataset = pd.read_csv('absa_data.csv', header= None)
dataset = dataset.rename(index=str, columns={ 0: "text", 1: "aspect_category", 2: "sentiment"})

dataset.head(5)
nlp = spacy.load('en')

dataset.text = dataset.text.str.lower()

#### ASPECT PORTION

aspect_terms = []
for sentence in nlp.pipe(dataset.text):
    chunks = [(chunk.root.text) for chunk in sentence.noun_chunks if (chunk.root.pos_ == 'NOUN' or chunk.root.pos_ == 'PROPN')]
    aspect_terms.append(' '.join(chunks))
dataset['aspect_terms'] = aspect_terms
#print(dataset.head(10))

# for word in nlp("NetNeutrality OpenInternet FCC TitleII blocking throttling paid prioritization PaidPrioritization"):
#     print(word.pos_)

## build aspect categories model
aspect_categories_model = Sequential()
aspect_categories_model.add(Dense(512, input_shape=(6000,), activation='relu'))
# net_neutral,i nterference, fcc_repeal
aspect_categories_model.add(Dense(3, activation='softmax'))
aspect_categories_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

vocab_size = 6000 # We set a maximum size for the vocabulary
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(dataset.text)
aspect_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(dataset.aspect_terms))

label_encoder = LabelEncoder()
integer_category = label_encoder.fit_transform(dataset.aspect_category)
dummy_category = to_categorical(integer_category)

aspect_categories_model.fit(aspect_tokenized, dummy_category, epochs=5, verbose=1)

# new_text = "Net neutrality is the principle that all Internet service providers (ISPs) should treat all traffic coming over their networks without discrimination"
# new_text = "Although it has been a key tenet of the net neutrality discussion for years, paid prioritization has recently become a more prominent focal point."
# new_text = "Commonly spoken of in terms of “fast lanes,” paid prioritization is when online companies pay ISPs to give their data traffic preferential treatment"
# new_text = "The value of the FCC’s 2015 Open Internet Order was not just in the banning of those specific practices, but also in giving the FCC ability to investigate actions that violate net neutrality but don't fall neatly into one of those three buckets."
new_text = "The District of Columbia Court of Appeals says the FCC had authority to reclassify internet service providers as “information services” under Title I of the Telecommunications Act, rather than “common carriers” that can be more heavily regulated"
chunks = [(chunk.root.text) for chunk in nlp(new_text).noun_chunks if chunk.root.pos_ == 'NOUN']
new_review_aspect_terms = ' '.join(chunks)
new_review_aspect_tokenized = tokenizer.texts_to_matrix([new_review_aspect_terms])

new_review_category = label_encoder.inverse_transform(aspect_categories_model.predict_classes(new_review_aspect_tokenized))
#print(new_review_category)

### SENTIMENT PORTION

sentiment_terms = []
for review in nlp.pipe(dataset['text']):
        if review.is_parsed:
            sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
        else:
            sentiment_terms.append('')  
dataset['sentiment_terms'] = sentiment_terms
#print(dataset.head(10))

sentiment_model = Sequential()
sentiment_model.add(Dense(512, input_shape=(6000,), activation='relu'))
# positive, negative, neutral
sentiment_model.add(Dense(3, activation='softmax')) 
sentiment_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

sentiment_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(dataset.sentiment_terms))

label_encoder_2 = LabelEncoder()
integer_sentiment = label_encoder_2.fit_transform(dataset.sentiment)
dummy_sentiment = to_categorical(integer_sentiment)

sentiment_model.fit(sentiment_tokenized, dummy_sentiment, epochs=5, verbose=1)

new_review = "As a community, we believe that the basic principle of net neutrality should be safeguarded, and we encourage policymakers to adopt clear rules that allow any business, including micro-entrepreneurs, to compete on an even playing field online"

chunks = [(chunk.root.text) for chunk in nlp(new_review).noun_chunks if chunk.root.pos_ == 'NOUN']
new_review_aspect_terms = ' '.join(chunks)
new_review_aspect_tokenized = tokenizer.texts_to_matrix([new_review_aspect_terms])

new_review_category = label_encoder_2.inverse_transform(sentiment_model.predict_classes(new_review_aspect_tokenized))
#print(new_review_category)

test_reviews = [
    "NetNeutrality has been a bedrock principle of the Internets development to date, and is a big part of what has made the internet such an important force for democracy, as it creates a level playing field for everyone",
    "like many other websites pushing for rules which prevent internet service providers from blocking, throttling, or prioritizing certain customers and users, such practices are the foundation of Amazon's business model ",
    "Because the value (and therefore the price) of PaidPrioritization increases as networks become more congested, it also rewards ISPs for letting their networks become clogged rather than upgrading their capacity.",
    "They have claimed that content delivery networks (CDNs) do the same thing as PaidPrioritization",
    "The court said the FCC exhibited “disregard of its duty” to evaluate how its rule change would affect public safety.",
    "NetNeutrality is a highly controversial topic.",
    "We do not support PaidPrioritization, blocking, or throttling."
]

# Aspect preprocessing
test_reviews = [review.lower() for review in test_reviews]
test_aspect_terms = []
for review in nlp.pipe(test_reviews):
    chunks = [(chunk.root.text) for chunk in review.noun_chunks if (chunk.root.pos_ == 'NOUN' or chunk.root.pos_ == 'PROPN')]
    test_aspect_terms.append(' '.join(chunks))
print(test_aspect_terms)
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
for i in range(7):
    print("Review " + str(i+1) + " is expressing a  " + test_sentiment[i] + " opinion about " + test_aspect_categories[i])


## Notes:
# leave input data cased
# append NetNeutrality, PaidPrioritization, OpenInternet, Federal Communications Commission -> FCC, TitleII)
# 