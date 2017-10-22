import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat


# Function receives the df, xyz columns, and a window size; returns a new df with xyz lagged
# according to window size, with id and y untouched.
def lag_set(df, lag_variables, window):
    df1 = DataFrame(df[['id', 'y']])
    for column in lag_variables:
        lagged = lag(df[column], window)
        cols = lagged.columns
        df1[cols] = lagged
    return df1[:][window:]


stand_sit = np.genfromtxt('stand_sit.csv', delimiter=",")
walk1 = np.genfromtxt('walking.csv', delimiter=",")
walk2 = np.genfromtxt('walking_2.csv', delimiter=",")

indices = {'id':0, 'acc_x':1, 'acc_y':2, 'acc_z':3,
           'gy_x':4, 'gy_y':5, 'gy_z':6,
           'mag_x':7, 'mag_y':8, 'mag_z':9}

"""
Input: dataset, window
Output: list of [Fk, n_freq]
"""
def lag(variable, window):
    df = DataFrame(variable)
    for i in range(window):
        j = window - i
        df = concat([df, DataFrame(variable).shift(j)], axis=1)
    return np.array(df.dropna())

def dataset_to_windows(dataset, windowsize):
    windows = list()
    row, col = dataset.shape
    for i in range(col):
        if i > 0:
           windows.append(lag(dataset[:,i], windowsize))
    return np.array(windows)

# INPUT dataset_to_windows output
# OUTPUT 3 dimensional array
def fft_transform(windows):
    arr_windows = list()
    for i in range(len(windows)):
        arr_transforms = list()
        for j in range(len(windows[i])):
            arr_transforms.append(get_fft(windows[i,j,:]))
        arr_windows.append(arr_transforms)
    return np.array(arr_windows)

windows = dataset_to_windows(walk1, 15)

fft_transformed = fft_transform(windows)
