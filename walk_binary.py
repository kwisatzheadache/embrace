"""
Binary classification of walk against stand_sit. First, I iterated over a large range of window sizes to determine the best lag. I found that a lag of 16 was best. Then, I ran LogisticRegression model to predict from X_test, Y_test. It's accuracy score is .978295, which is up a few points from the original logisticregression score - this could be in part due to doing a train_test_split, rather than kfold, as kfold can be problematic with time series.
The trained model is saved as 'walk_LR_bin.sav'
"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

execfile('start.py')
execfile('window.py')

"""
Running `test_window(200, 10)` tests accuracy of a LogisticRegression classification, with
lag window varying from 1 to 201 in 10 unit increments. Accuracy seems to peak between a window
size of 11 and 41.
"""

# window_scores = test_window(40, 1)
"""
Accuracy seems to peak at window = 16
"""

# test_window(17, 1)

"""
Since window = 16 yields the best results, that's what we'll use.
"""
# Create lagged dataframes for walk and stand_sit
window = 0
lagged_walk = lag_set(df_walk, to_lag, window)
lagged_stand_sit = lag_set(df_stand_sit, to_lag, window)
lagged_complete = concat([lagged_walk, lagged_stand_sit])
walk_bin = DataFrame(lagged_complete)

# Create test and train sets, removing 'id'
X = walk_bin.drop(walk_bin.columns[[0,1]], axis=1)
Y = walk_bin['y']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.33, random_state=7)
walk_model = LogisticRegression()
walk_model.fit(X_train, Y_train)
walk_model.score(X_train, Y_train)

# print('walk_model coeffictient and intercept: %d, %d' % (walk_model.coef_, walk_model.intercept_))
predicted = walk_model.predict(X_test)
