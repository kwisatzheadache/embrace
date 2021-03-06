import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
import sys
import os
import scipy.stats as stats
import pandas as pd
import pprint
from sklearn.decomposition import PCA

execfile('peakdet.py')

def get_nx10(location):
    """
    Receives raw data, returns labeled dataframe
    """
    cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
    array = np.genfromtxt(location, delimiter=",")
    df = DataFrame(array).dropna()
    df.columns = cols
    return(df)

def label_y(df, y_value):
    # Used to label input for classification training
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
    """
    Used to convert nx10 data to lagged dataset. Windowsize determines amount of lag. Typically use 100 for windosize.
    """
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
    """
    Transforms nx10 data to lagged, then reduces signal to dom_freq_size, using fft_transform
    """
    cols = dataset.columns
    windows = dataset_to_windows(dataset, windowsize)
    fft = fft_transform(windows)
    df = DataFrame()
    acc_mag, mag_mag, mag_gy = get_mags(dataset)
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
    df['mag_gy'] = mag_gy[diff:]
    return(df)

def make_bins(dataset, bin_size):
    # Used for comparison of binning vs windows.
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
    # Calculate magnitude of each sensor signal. Mag_acc is one of the best indicators of classification behavior.
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

def generate_features(filename, window=100):
    ''' Receives nx10 csv file.
    Transforms data into windows according to pre-declared window size, performs fourier transform, keeps only the dominant frequencies, and creates magnitude values for the acc and mag.

    Output is array shape (x, 409). 

    '''
    print('generating features for ' + filename)
    data = get_nx10(filename)
    doms = data_transform(data, window, num_freqs)
    coords = doms.columns[:9]
    for i in coords:
        Fks = []
        n_freqs = []
        for j in range(len(doms[i])):
            Fk, n_freq = doms[i][j]
            Fk = abs(Fk)
            Fks.append(Fk)
            n_freqs.append(n_freq)

        doms[i+'coeffs'] = Fks
        doms[i+'n_freqs'] = n_freqs
    doms = doms.drop(coords, axis=1)
    columns = data.columns
    X_data = np.array(data[:][window:])
    for i in doms.columns[9:]:
        arrays = np.array([np.array(x) for x in doms[i]])
        X_data = np.hstack([X_data, arrays])
    return X_data

def stack(direc):
    ''' Receives directory of csv files. Generates features on all of them, then stacks the output in shape (x, 409), in preparation for global PCA.
    '''
    files = os.listdir(direc)
    csvs = []
    for x in files:
        if '.csv' in x:
            csvs.append(x)
    complete = np.vstack([generate_features(direc+'/'+x) for x in csvs])
    return complete

def run_pca(data): 
    ''' Runs PCA analysis on dataset. Prints top ten weights for ten components.'''
    print(data.shape)
    pca = PCA(n_components = 10)
    pca.fit(data)
    variance_ratio = pca.explained_variance_ratio_
    components = pca.components_
    highest = components[0]
    for i in components:
        sorted = list(reversed(np.argsort(i)))
        weights = {}
        for j in range(10):
            weights[sorted[j]] = round(i[sorted[j]], 5)
        # print (i[sorted[:10]], sorted[:10])
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(weights)
        print(variance_ratio)

def stack_walks(direc):
    """
    Gather all csv's from a directory and stack them into one array
    """
    files = os.listdir(direc)
    csvs = []
    for x in files:
        if '.csv' in x:
            csvs.append(x)
    complete = np.vstack([get_nx10(direc+'/'+x) for x in csvs])
    return complete

def straight_walk(walk_input, angle):
    """
    Input: walk_directory, angle
    Alternately, instead of directory, use nx10 data in np.array
    Return windows where all values fall within the range of +/- rotation angle around the average.
    """
    rotation = (.72*angle)/360
    if isinstance(walk_input, str):
        walks = stack_walks(walk_input)
    else:
        walks = walk_input
    array = np.array(walks[100:])
    mag_z = walks[:,9]
    lagged = lag(mag_z, 100)
    straight = []
    index = []
    for i in range(len(lagged)):
        avg = np.mean(lagged[i])
        low = avg - rotation
        high = avg + rotation
        if all(low <= j <= high for j in lagged[i]):
            straight.append(array[i])
            index.append(avg)
    return np.array(straight), index

def longest_walk(straights, index):
    """
    Returns the single, longest walk from a series of walks. Could probably also use non-walks input.
    """
    counter = range(len(index))
    acc1 = []
    longest = []
    while len(index) > 2:
        i = index[0]
        j = index[1]
        count = counter[0]
        index.pop(0)
        counter.pop(0)
        if abs(i - j) < .01:
            acc1.append(count)
        else:
            if len(acc1) >= len(longest):
                longest = list(acc1)
                acc1 = []
            else:
                acc1 = []
    return straights[[longest]]

def make_auto(feature):
    """
    Performs autocorrelation on selected input (feature). Used in autocorrelation graphs to determine walk cycles.
    """
    series = pd.Series(feature)
    auto = []
    for i in range(len(feature)):
        auto.append(series.autocorr(i))
    return auto

def reduce_signal(signal):
    """
    Reduces signal, post fft transform. 
    """
    fft = get_fft(signal)
    doms = get_dom_freq(fft[0], fft[1], 50)
    reduced = get_reduced_signal(doms[0], doms[1], len(signal))
    return reduced

def find_steps(walk):
    """
    Receives walk dataframe, returns location of each step, using autocorrelation of gyroscope. 
    """
    cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
    df = DataFrame(walk)
    df.columns = cols
    acc_mag, mag_mag, mag_gy = get_mags(df)
    reduced_gy = reduce_signal(mag_gy)
    gy = [make_auto(mag_gy), make_auto(reduced_gy)]
    maxtab, mintab = peakdet(gy[1], .02)
    ind = maxtab[:, 0]
    ind = ind.astype(int)
    len_btw_steps = [j-i for i, j in zip(ind[:-1], ind[1:])]
    loc_and_len = zip(ind, len_btw_steps)
    steps = []
    for location, length in loc_and_len:
        start = location
        stop = location + length
        step = longest[start:stop]
        steps.append(step)
    return steps

def avg_len(steps):
    """
    Calculates average length of stride, based on output from find_steps(walk)
    """
    lens = []
    for i in steps:
        lens.append(len(i))
    avg = sum(lens) / float(len(lens))
    return avg

def lens(steps):
    """
    Returns list of stride lengths. Used to determine stride variability.
    """
    lens = []
    for i in steps:
        lens.append(len(i))
    return lens

def left_right(steps):
    """
    Returns list of right side and left side steps. Used in determining variance between sides and symmetry.
    """
    lengths = lens(steps)
    a_side = []
    b_side = []
    for i in range(len(lengths)):
        if i % 2 == 0:
            a_side.append(steps[i])
        else:
            b_side.append(steps[i])
    return a_side, b_side
