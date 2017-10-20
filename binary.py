from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

X = walk_bin[to_lag]
Y = walk_bin['y']

kfold = KFold(n_splits=10, random_state=7)
model = LogisticRegression()
scoring = 'accuracy'
global results
results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
print("Accuracy: %.6f (%.6f)") % (results.mean(), results.std())

