"""
Binary classification of walk against stand_sit. First, I iterated over a large range of window sizes to determine the best lag. I found that a lag of 16 was best. Then, I ran LogisticRegression model to predict from X_test, Y_test. It's accuracy score is .978295, which is up a few points from the original logisticregression score - this could be in part due to doing a train_test_split, rather than kfold, as kfold can be problematic with time series.
The trained model is saved as 'walk_LR_bin.sav'
"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

execfile('start.py')
execfile('window.py')

"""
Running `test_window(200, 10)` tests accuracy of a LogisticRegression classification, with
lag window varying from 1 to 201 in 10 unit increments. Accuracy seems to peak between a window
size of 11 and 41.
"""

 window_scores = test_window(40, 1)
"""
Accuracy seems to peak at window = 16
"""

# test_window(17, 1)

"""
Since window = 16 yields the best results, that's what we'll use.
"""
window = 16

# Create lagged dataframes for walk and stand_sit
lagged_walk = lag_set(df_walk, to_lag, window)
lagged_stand_sit = lag_set(df_stand_sit, to_lag, window)
lagged_complete = concat([lagged_walk, lagged_stand_sit])

walk_bin = DataFrame(lagged_complete)



X = walk_bin.drop(walk_bin.columns[[0,1]], axis=1)
Y = walk_bin['y']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.33, random_state=7)
model = LogisticRegression()
model.fit(X_train, Y_train)
model.score(X_train, Y_train)

# print('Model coeffictient and intercept: %d, %d' % (model.coef_, model.intercept_))
predicted = model.predict(X_test)
filename = 'walk_LR_bin.sav'
pickle.dump(model, open(filename, 'wb'))

""" To load model from saved
`loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print result`
"""

