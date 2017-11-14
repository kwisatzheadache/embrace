#!/usr/bin/python

import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import embrace_setup as es

#get the constants out the way
THRESH_LOW = 1
#THRESH_LOW = .01
WIN_LEN = 50
BACK_TRACK = 15
STEP_SIZE = 13 #step size for step (walking) detection
#STEP_SIZE = 50

def merge_ics(ics):
    i = 0
    while i < len(ics)-1:
        if ics[i][1] == ics[i+1][0]:
            ics[i] = (ics[i][0],ics[i+1][1])
            ics.pop(i+1)
        else:
            i += 1
    return ics

def get_lics(signal, step_size=STEP_SIZE, thresh=THRESH_LOW):
    """Scans the signal in steps of STEP_SIZE. If the windows variance is less the THESH_LOW, the window is labeled as a lic. Otherwise, it is labeled as a hic. Consecutive lics and hics are combined to yield the final output
    
    Input: 
        signal - column vector containing data points
        step_size - the size of the windows. Defaults to 14
        thresh - the thresh hold for a low information winow. Defaults to 1
        
    Output:
        lics - list of tuples holding (start, stop) of lics
        hics - list of tuples holding (start, stop) of hics"""
    
    lics = []
    hics = []
    i = 0
    while i < len(signal) - step_size:
        if np.var(signal[i:i+step_size]) <= thresh:
            lics.append((i,i+step_size))
        else:
            hics.append((i,i+step_size))
        i += step_size
    #combine sequential hic and lic windows
    hics = merge_ics(hics)
    lics = merge_ics(lics)

    return [lics,hics]

def plot_var(signal):
    variances = []
    for i in range(len(signal)-WIN_LEN):
        variances.append(np.var(signal[i:i+WIN_LEN]))
    plt.title("Variance of Window - Size " + str(WIN_LEN))
    plt.plot(range(len(variances)), variances)
    plt.show()

def calc_step_var(vals):
    t,ac,gy,mag,ac_mag,gy_mag,mag_mag = vals
    
    max_ac_amp = max(ac_mag)
    max_ac_amps = []
    max_gy_amp = max(gy_mag)

    lics, hics = get_lics(ac_mag)

    #average time between steps
    f1 = []
    f2 = []
    flag = 0
    for i in range(2,len(hics)-1):
        if flag == 0:
            f1 += [hics[i][0] - hics[i-1][0]]
        else:
            f2 += [hics[i][0] - hics[i-1][0]]
        flag = 0 if flag == 1 else 1

    f1_av = np.average(f1)
    f2_av = np.average(f2)
    f1_sd = np.var(f1)**.5
    f2_sd = np.var(f2)**.5

    f1_l = f1_av-(1.5*f1_sd)
    f1_h = f1_av+(1.5*f1_sd)
    f2_l = f2_av-(1.5*f2_sd)
    f2_h = f2_av+(1.5*f2_sd)

    f1 = [ v for v in f1 if f1_l <= v and f1_h >= v]
    f2 = [ v for v in f2 if f2_l <= v and f2_h >= v]

    f_1 = sum(f1)/len(f1)
    f_2 = sum(f2)/len(f2)
    f3 = f_1 + f_2
    f_1 /= f3 * .01
    f_2 /= f3 * .01
    print("Number of steps counted: " + str(len(hics)))
    print("f1: " + str(f_1))
    print("f1 sd: " + str(np.var(f1)**.5))
    print("f2: " + str(f_2))
    print("f2 sd: " + str(np.var(f2)**.5))
    print("spread stance distribution: " + str(np.abs(f_1-f_2)))
    print("spread of std devs: " + str(np.abs(np.var(f1)**.5 - np.var(f2)**.5)))




