from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from statistics import mean

def get_pred(df_input):

    df = pd.read_csv('page_by_page3.csv')

    X_vars = list(df.loc[:, 'innovation':'against network neutrality'])
    X = df[X_vars]
    y = df['NN']

    clf = MLPClassifier()
    clf.fit(X, y)

    X_test = df_input[X_vars]

    preds = clf.predict(X_test)
    #print('PREDICTIONS------------------------------------------------')
    #print(preds)

    count = 0
    for i in range(0, len(preds)):
        if preds[i] == True:
            count += 1
    NN_guess = count/len(preds)

    return NN_guess