import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
from math import sqrt
from pandas import DataFrame
from pandas import concat

stand_sit = np.genfromtxt('stand_sit.csv', delimiter=",")
walk1 = np.genfromtxt('walking.csv', delimiter=",")
walk2 = np.genfromtxt('walking_2.csv', delimiter=",")
random = np.genfromtxt('random_seq.csv', delimiter=",")

"""
First step is to label the stand_sit, so that they can be classified... Clustering ought to
yield four groups? Sitting, up, standing, and down.

Then, once labels have been applied, do I use the same NN? Or do I take the labeled data a train
a binary classifier?

Perhaps the easiest place to start is just to label walk1 and walk2 as 1, and stand_sit as 0 to
train a binary classifier to recognize walking. I think I'll do that.
"""

# Create the label variable and append it to the data
walk_both = np.vstack([walk1, walk2])
walk_y = []
for i in walk_both:
    walk_y.append([1])
walk_y = np.array(walk_y)
walk_combined = np.hstack((walk_both, walk_y))

# Again for the stand_sit data
stand_sit_y = []
for i in stand_sit:
    stand_sit_y.append([0])
stand_sit_y = np.array(stand_sit_y)
stand_sit_combined = np.hstack((stand_sit, stand_sit_y))

combined = np.vstack((walk_combined, stand_sit_combined))

""" Begin modeling for walking """

# Determine what is the best window for the classification models
# I should have the binary class models picked out already. Now,
# iteratively run through different window sizes, testing the model fit.


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

df_walk = DataFrame(walk_combined)
df_stand_sit = DataFrame(stand_sit_combined)

cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z', 'y']
df_walk.columns = cols
df_stand_sit.columns = cols

def lag_set(df, window):
    for column in df:
        lagged = lag(df[column], window)
        cols = lagged.columns
        print df[cols]
        # df[cols] = lagged

to_lag = cols[1:-1]
window = 10
