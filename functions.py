import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
import sys 

def lag(variable, window):
    """
    Input: dataset, window
    Output: list of [Fk, n_freq]
    """
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

def fft_transform(windows):
    # INPUT dataset_to_windows output
    # OUTPUT 3 dimensional array
    arr_windows = list()
    for i in range(len(windows)):
        arr_transforms = list()
        for j in range(len(windows[i])):
                arr_transforms.append(get_fft(windows[i][j]))
        arr_windows.append(arr_transforms)
    return np.array(arr_windows)

def data_transform(dataset, windowsize):
    windows = dataset_to_windows(dataset, windowsize)
    return fft_transform(windows)

def get_fft(signal):
    # INPUT: [N] array of values
    # OUTPUT: [Fk, frequ], list of coeff, list of freq values
    fs = 100
    Fk = np.fft.rfft(signal)/float(len(signal))
    f = np.fft.rfftfreq(len(signal), 1./fs)
    return Fk, f

def get_dom_freq(Fk, n_freq):
    # INPUT: [Fk] (list of coeff)
    #        n_freq (number of freq)
    # OUTPUT: [Ind] (list of indices of dominant frequencies)
    Fk_mag = np.abs(Fk)**2
    Fk_mag_sort = np.abs(Fk)**2
    Fk_mag_sort.sort()
    n_freq_shape = n_freq.shape
    idx = np.zeros((n_freq_shape))
    for i in range(len(n_freq)):
        idx[i] = np.where(Fk_mag == Fk_mag_sort[-(1+i)])[0]
    return idx.astype(int)
