import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

stand_sit = DataFrame(np.genfromtxt('stand_sit.csv', delimiter=",")).dropna()

"""
First step is to label the stand_sit, so that they can be classified... Clustering ought to
yield four groups? Sitting, up, standing, and down.

Then, once labels have been applied, do I use the same NN? Or do I take the labeled data a train
a binary classifier?

Perhaps the easiest place to start is just to label walk1 and walk2 as 1, and stand_sit as 0 to
train a binary classifier to recognize walking. I think I'll do that.
"""

# Creates a df with columns [T, t-1, t-2, ... t-window]
def lag(variable, window):
    df1 = DataFrame(variable)
    for i in range(window):
        j = window - i
        df1 = concat([df1, variable.shift(j)], axis=1)
    columns = [variable.name]
    for i in range(window):
        j = window - i
        columns.append(variable.name + ' t - %d' % j)
    df1.columns = columns
    return df1.iloc[window:]

# Only lag the xyz data, not the id or the y data
cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z']
stand_sit.columns = cols
to_lag = cols[1:]

# Use window of 16, as per window testing
window = 16

"""
Separate this into a different file? So it can be called in the window loop
"""
# Function receives the df, xyz columns, and a window size; returns a new df with xyz lagged
# according to window size, with id and y untouched.
def lag_set(df, lag_variables, window_x):
    df1 = DataFrame(df[['id']])
    for column in lag_variables:
        lagged = lag(df[column], window_x)
        cols = lagged.columns
        df1[cols] = lagged
    return df1[:][window_x:]

lagged_stand_sit = lag_set(stand_sit, to_lag, window)


X = DataFrame(lagged_stand_sit[1:])
X_train, X_test = train_test_split(X, test_size=.33, random_state=7)

model=KMeans()
k_means = KMeans(n_clusters=3, random_state=0)
model.fit(X_train)
predicted=model.predict(X_test)
