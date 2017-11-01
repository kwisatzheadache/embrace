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
        sig_len = max(f)
    
    signal = np.fft.irfft(Fk, sig_len)
        
        
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
            
            
