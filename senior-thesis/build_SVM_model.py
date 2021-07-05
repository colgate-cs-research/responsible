from sklearn.svm import SVC
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from statistics import mean

df = pd.read_csv('page_by_page3.csv')
#print(df)

X_vars = list(df.loc[:, 'innovation':'against network neutrality'])
X = df[X_vars]
y = df['NN']

avg_accuracy_list = [0] * 100
for j in range(0, 100):


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    clf = SVC()
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)

    y_test = y_test.to_frame()
    ans_list = y_test['NN'].values.tolist()

    count = 0
    for i in range(0, len(preds)):
        if preds[i] == ans_list[i]:
            count += 1
    avg_accuracy_list[j] = count/len(preds)

print(mean(avg_accuracy_list))