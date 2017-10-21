import numpy as np
import sys 


def get_fft(signal):
	"""Get the coefficient and frequency vectors for the given signal
		Input:
			[N] array of values
		Output: 
			[Fk, freq] where Fk is a list of coefficient values and freq is a list
			of frequency values"""
	fs = 100
	Fk = np.fft.rfft(signal)/len(signal)
	f = np.fft.rfftfreq(len(signal), 1/fs)
	return Fk, f

def get_dom_freq(Fk, n_freq):
	"""Get the n_freq most dominant frequencies from the transformed signal
		Input:
			[Fk] = list of coefficient values
			n_freq = number of frequencies to preserve
		Output:
			[Ind] = list of indexes that hold the dominant frequencies in the freq array"""
	Fk_mag = np.abs(Fk)**2
	Fk_mag_sort = np.abs(Fk)**2
    Fk_mag_sort.sort()
    idx = np.zeros(n_freq)
    for i in range(n_freq):
        idx[i] = np.where(Fk_mag == Fk_mag_sort[-(1+i)])[0]
return idx.astype(int)
