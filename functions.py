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
    mag_gy = []
    for i in range(len(dataset)):
        xa = (dataset['acc_x'][i])
        ya = (dataset['acc_y'][i])
        za = (dataset['acc_z'][i])
        xm = (dataset['mag_x'][i])
        ym = (dataset['mag_y'][i])
        zm = (dataset['mag_z'][i])
        xg = (dataset['gy_x'][i])
        yg = (dataset['gy_y'][i])
        zg = (dataset['gy_z'][i])
        acc = (xa**2+ya**2+za**2)**1/2
        grav = acc - 9.8
        mag = (xm**2+ym**2+zm**2)**1/2
        gy = (xg**2+yg**2+zg**2)**1/2
        mag_acc.append(grav)
        mag_mag.append(mag)
        mag_gy.append(gy)
    return[mag_acc, mag_mag, mag_gy]
    
import numpy as np
import scipy.stats as stats
import sys 


def get_fft(signal):
    """Get the coefficient and frequency vectors for the given signal
        Input:
            [N] array of values
        Output: 
            [Fk, freq] where Fk is a list of coefficient values and freq is a list
            of frequency values"""
    fs = 100.
    Fk = np.fft.rfft(signal)/len(signal)
    
    f = np.fft.rfftfreq(len(signal), 1/fs)
    #remove the noise
    Fk[0] = 0
    
    return Fk, f

def get_dom_freq(Fk, freq, n_freq):
    """Get the n_freq most dominant frequencies from the transformed signal
        Input:
            [Fk] = list of coefficient values
            n_freq = number of frequencies to preserve
        Output:
            dom_Fk = list of the dominant frequency coefficients in the signal sorted by the frequency
            
            dom_f = list of the dominant frequencies in the signal"""

    #get the magnitude of the coefficients
    Fk_abs = np.abs(Fk)
    #sort the coefficients in descending order
    Fk_sort = sorted(Fk_abs, reverse=True)
    
    dom_Fk = []
    dom_f = []
    i = 0
    while i < n_freq:
        inds = np.where(Fk_abs == Fk_sort[i])
        for ind in inds:
            dom_f.append(freq[ind])
            dom_Fk.append(Fk[ind])
        i += 1
    
    #sort based on frequency from lo to hi
    #convert from numpy float to python float for mapping
    dom_f = [float(abs(f)) for f in dom_f]
    f_Fk = dict(zip(dom_f,dom_Fk))
    f_sorted = sorted(dom_f)
    # return(dom_f, f_Fk, f_sorted, dom_Fk)


    dom_Fk = []
    for f in f_sorted:
        dom_Fk.append(f_Fk[f][0])
        
    return np.array(dom_Fk), np.array(f_sorted)

def bin_dom_freqs(Fk, f, num_bins=0):
    """Bin the transform data to reduce data complexity. Note that the arrays Fk and f must be one to one, that is, the value Fk[i] is the coefficient of the frequenct at f[i]
    Input:
        Fk - transform coefficients
        f - frequencies
        num_bins - number of bins to create. If num_bins is not specified, defaults to a quarter of the input size
    Output:
        Fk_bin - binned transform coefficients. The individual terms are summed
        f_bin - the binned frequency data. The final frequency is determined as a weighted average"""
    
    #default behavior
    if num_bins == 0:
        num_bins = len(Fk)/4
    
    #get the number of elements per bin
    bin_len = len(Fk)/num_bins
    #and the number of remainder bins
    rem = len(Fk) % num_bins
    
    #output lists
    Fk_bin = []
    f_bin = []
    i = 0
    while i < len(Fk)-rem:
        #sum the coefficients in the bin
        tot = sum(Fk[i:i+bin_len])
        #determine the weighted average for the new frequency
        f_final = 0
        for j,a in enumerate(Fk[i:i+bin_len]):
            f_final += (a/tot * f[i+j])
        f_final /= bin_len
        Fk_bin.append(tot)
        f_bin.append(f_final)
        i += bin_len
    #bin any remaining values that are not a multiple of bin_len
    tot = sum(Fk[i:i+rem])
    f_final = 0
    for j,a in enumerate(Fk[i:i+rem]):
        f_final += (a/tot * f[i+j])
    f_final /= rem
    Fk_bin.append(tot)
    f_bin.append(f_final)
    
    return [Fk_bin, f_bin]

def get_reduced_signal(Fk, f, sig_len=0):
    """Given two vectors Fk and f that have been reduced in their size, recomputes the time series based on the filtered information
    Input:
        Fk - coefficients of the fft
        f - freqencies of the fft
        sig_len - number of points in the output. If no length is given, the method defaults to len(Fk)
    Output:
        signal - reduced time series"""
    
    if sig_len == 0 or sig_len < max(f):
        sig_len = int(max(f))*200
        """max(f) is limited by window size - wavelength of 1/2 the windowsize is the largest observable frequency. Each point of the wavelength corresponds to 1/100 of a second, so max freqency times 100 corresponds to at max, half of the window size."""
    
    signal = np.fft.irfft(Fk, sig_len)
    return signal   

    """
    reduced signal will be transformed via fft, then passed to kld
    """
        
def kld(Fk, freq, Fk_red, f_red):
    """Caclulate the Kullback-Leibler divergence between two signals """
    
    #pad the reduced input with zeros
    f_red = [float(val) for val in f_red]
    freq = [float(val) for val in freq]
    f_Fk_red = dict(zip(f_red,Fk_red))
    Fk_red_pad = []
    #for each frequency in the nonreduced signal
    for i,f in enumerate(freq):
        #if the frequency is shared with the reduced signal
        if f in f_red:
            #add the coefficient from the reduced signal
            Fk_red_pad.append(f_Fk_red[f])
        #otherwise, pad it with a zero
        else:
            Fk_red_pad.append(0.)
    Fk_red_pad = np.array(Fk_red_pad)
    
    Fk = np.abs(Fk)
    Fk /= sum(Fk)
    Fk_red_pad = np.abs(Fk_red_pad)
    Fk_red_pad /= sum(Fk_red_pad)
    
    return stats.entropy(Fk_red_pad, Fk)

def fft_to_signal(dataset, reduced_signal_length, coordinate_axes):
    """Input:  binned fft tranforms comprising dominant frequency lists.
    Output: reconstructed signal with specified length
    """
    reduced = DataFrame()
    for i in coordinate_axes:
        coord = []
        for j in range(len(dataset)):
            Fk, f = dataset[i][j]
            signal = get_reduced_signal(Fk, f, reduced_signal_length)
            coord.append(signal)
        reduced[i] = coord
        reduced['id'] = dataset['id']
    return reduced
