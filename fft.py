import numpy as np
import sys 

# INPUT: [N] array of values
# OUTPUT: [Fk, frequ], list of coeff, list of freq values
def get_fft(signal):
    fs = 100
    Fk = np.fft.rfft(signal)/len(signal)
    f = np.fft.rfftfreq(len(signal), 1/fs)
    return Fk, f

# INPUT: [Fk] (list of coeff)
#        n_freq (number of freq)
# OUTPUT: [Ind] (list of indices of dominant frequencies)
def get_dom_freq(Fk, n_freq):
    Fk_mag = np.abs(Fk)**2
    Fk_mag_sort = np.abs(Fk)**2
    Fk_mag_sort.sort()
    idx = np.zeros(n_freq)
    for i in range(n_freq):
        idx[i] = np.where(Fk_mag == Fk_mag_sort[-(1+i)])[0]
    return idx.astype(int)
