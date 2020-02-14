from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv('training_data_new.csv')
#print(df)

X_vars = list(df.loc[:, 'network neutral':'against network neutrality'])
X = df[X_vars]
y = df['NN']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = RandomForestClassifier(n_jobs=2, random_state=0)
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
print("Prediction")
print(preds)

print("Actual")
print(y_test)



