import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
import sys

def get_nx10(location):
    cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
    array = np.genfromtxt(location, delimiter=",")
    df = DataFrame(array).dropna()
    df.columns = cols
    return(df)

def label_y(df, y_value):
    y = []
    for i in len(df['acc_x']):
        y.append(value)
    df['y'] = y

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
    windows = []
    row, col = dataset.shape
    for i in range(col):
        if i > 0:
           windows.append(lag(np.array(dataset)[:,i], windowsize))
    return np.array(windows)

def fft_transform(windows):
    # INPUT dataset_to_windows output
    # OUTPUT 3 dimensional array
    arr_windows = []
    for i in range(len(windows)):
        arr_transforms = []
        for j in range(len(windows[i])):
                arr_transforms.append(get_fft(windows[i][j]))
        arr_windows.append(arr_transforms)
    return np.array(arr_windows)

def data_transform(dataset, windowsize, dom_freq_size):
    cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
    windows = dataset_to_windows(dataset, windowsize)
    fft = fft_transform(windows)
    df = DataFrame()
    for i in range(len(fft)):
        col = []
        for j in range(len(fft[1,:])):
            if type(i) != int:
                print(i)
            Fk, n_freq = fft[i,j]
            dom = get_dom_freq(Fk, dom_freq_size)
            freqs = Fk[[dom]]
            col.append(freqs)
        df[cols[i]] = col
    return(df)

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
    # n_freq_shape = n_freq.shape
    idx = np.zeros((n_freq))
    for i in range(n_freq):
        idx[i] = np.where(Fk_mag == Fk_mag_sort[-(1+i)])[0]
    return idx.astype(int)
