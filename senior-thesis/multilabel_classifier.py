import re
import nltk
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# credit: https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/Multi%20label%20text%20classification.ipynb

df = pd.read_csv('Multilabel_noNNdouble.csv', header= None)
df = df.rename(index=str, columns={ 0: "text", 1: "aspect_categories", 2: "about_NN", 3: "about_blocking", 4: "about_shaping", 5: "about_FCC_repeal", 6: "sentiment", 7: "predicted_AS"})
# df_test = pd.read_csv('Multilabel_test.csv', header= None)
# df_test = df_test.rename(index=str, columns={ 0: "text", 1: "aspect_categories", 2: "about_NN", 3: "about_blocking", 4: "about_shaping", 5: "about_FCC_repeal", 6: "sentiment", 7: "predicted_AS"})

df = df.drop(["sentiment", "predicted_AS", "aspect_categories"], axis=1)
categories = ["about_NN", "about_blocking", "about_shaping", "about_FCC_repeal"]

#train, test = train_test_split(df, test_size=0.10, shuffle=True)
kf = KFold(n_splits = 10) # break into tenths

aspect_accuracy_dict = {"about_NN":[], "about_blocking":[], "about_shaping":[], "about_FCC_repeal":[]}

porter_stemmer=nltk.PorterStemmer()
stop_words = [porter_stemmer.stem(word) for word in stop_words]
stop_words.append('becau')
stop_words.append('r')
stop_words.append('v')

def Tokenizer(str_input):
    words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split()
    porter_stemmer=nltk.PorterStemmer()
    words = [porter_stemmer.stem(word) for word in words]
    return words

# # undersample
# # see original category breakdown- there may be overlap...
# num_nn = len(df[(df['about_NN'] == 1) & (df['about_blocking'] == 0) & (df['about_shaping'] == 0) & (df['about_FCC_repeal'] == 0)])
# print(num_nn)
# num_block = len(df[df['about_blocking'] == 1])
# print(num_block)
# num_shape = len(df[df['about_shaping'] == 1])
# print(num_shape)
# num_fcc = len(df[df['about_FCC_repeal'] == 1])
# print(num_fcc)

# nn_indices = df[(df.about_NN == 1) & (df.about_blocking == 0) & (df.about_shaping == 0) & (df.about_FCC_repeal == 0)].index
# random_nn_indices = np.random.choice(nn_indices,min(num_block, num_shape, num_fcc), replace=False)
# block_indices = df[df.about_blocking == 1].index
# shape_indices = df[df.about_shaping == 1].index
# fcc_indices = df[df.about_FCC_repeal == 1].index

# undersample_indices = np.concatenate([random_nn_indices, block_indices, shape_indices, fcc_indices])
# undersampled_df = df.loc[undersample_indices]


for train_index, test_index in kf.split(df):
    # split train and test reviews
    train = df.iloc[train_index]
    test = df.iloc[test_index]

    X_train = train.text
    X_test = test.text

    # Define a pipeline combining a text feature extractor with multi lable classifier
    NB_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(tokenizer = Tokenizer, stop_words=stop_words, ngram_range=(1,3))),
                    ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
                ])

    for category in categories:
        print('... Processing {}'.format(category))
        # train the model using X_dtm & y
        NB_pipeline.fit(X_train, train[category])
        # compute the testing accuracy
        prediction = NB_pipeline.predict(X_test)
        # print(prediction)
        # print(test[category])
        # print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))
        aspect_accuracy_dict[category].append(accuracy_score(test[category], prediction))
        # new_prediction = NB_pipeline.predict(df_test.text)
        # print(new_prediction)
        # print(df_test[category])
        # print('Second accuracy is {}'.format(accuracy_score(df_test[category], new_prediction)))

for category in categories:
    print('The average accuracy for {} is:'.format(category))
    print(sum(aspect_accuracy_dict[category])/10)



