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
    for i in range(len(df['acc_x'])):
        y.append(y_value)
    df['y'] = y
    return(df)

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
    cols = dataset.columns
    windows = dataset_to_windows(dataset, windowsize)
    fft = fft_transform(windows)
    df = DataFrame()
    acc_mag, mag_mag = get_mags(dataset)
    for i in range(len(fft)):
        col = []
        for j in range(len(fft[1,:])):
            Fk, n_freq = fft[i,j]
            dom_Fk, f_sorted = get_dom_freq(Fk, n_freq, dom_freq_size)
            col.append(np.array([dom_Fk, f_sorted]))
        vectorize = np.array([np.array(x) for x in col])
        df[cols[i+1]] = col
    df['id'] = dataset['id']
    diff = len(acc_mag) - len(df)
    df['acc_mag'] = acc_mag[diff:]
    df['mag_mag'] = mag_mag[diff:]
    return(df)

def make_bins(dataset, bin_size):
    row, col = dataset.shape
    if row > col:
        dataset = dataset.transpose()
    bins = DataFrame()
    print dataset.shape
    for i in range(len(dataset)):
        binned = []
        for j in range(int(len(dataset[i])/bin_size)):
            print (i,j)
            binned.append(dataset[i][j*bin_size:(j+1)*bin_size])
        bins[i] = binned
    return bins


def run_klds(window):
    """Test reduction efficiency buy running kld divergence between original signal and signal comprising x number of dominant frequencies"""
    Fk, nfreq = get_fft(window)
    for size in range(50):
        print size
        dom_fk, dom_fq = get_dom_freq(Fk, nfreq, size)
        entropy = kld(Fk, nfreq, dom_fk, dom_fq)
        print(entropy)

def get_mags(dataset):
    mag_acc = []
    mag_mag = []
    for i in range(len(dataset)):
        xa = (dataset['acc_x'][i])
        ya = (dataset['acc_y'][i])
        za = (dataset['acc_z'][i])
        xm = (dataset['mag_x'][i])
        ym = (dataset['mag_y'][i])
        zm = (dataset['mag_z'][i])
        acc = (xa**2+ya**2+za**2)**1/2
        grav = acc - 9.8
        mag = (xm**2+ym**2+zm**2)**1/2
        mag_acc.append(grav)
        mag_mag.append(mag)
    return[mag_acc, mag_mag]
    
