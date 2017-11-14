#!/usr/bin/python

import numpy as np

def get_lists(file_name):
    """Get the time, accel, gy, mag, |accel|, |gy|, |mag| lists
    from the input file
    Input: [Nx10] csv file in order time, accel (x,y,z), gy (x,y,z), and mag(x,y,z)
    Output: Lists from the input file"""
    vals = np.genfromtxt(file_name, delimiter=",")
    t = vals[:,0].flatten()
    t /= 10**6
    ac = np.transpose(vals[:,1:4])
    gy = np.transpose(vals[:,4:7])
    mag = np.transpose(vals[:,7:10])
    
    ac_mag = np.array([sum([ac[0,i]**2, ac[1,i]**2, ac[2,i]**2])**.5 for i in range(len(t))])
    ac_mag-= 9.8

    gy_mag = np.array([sum([gy[0,i]**2, gy[1,i]**2, gy[2,i]**2])**.5 for i in range(len(t))])
    
    mag_mag = np.array([sum([gy[0,i]**2, gy[1,i]**2, gy[2,i]**2])**.5 for i in range(len(t))])
    
    out = []
    #drop any nan values in the lists
    out.append(np.array([val for val in t if not np.isnan(val)]))
    for l in [ac,gy,mag]:
        tmp = []
        for i,r in enumerate(l):
            tmp1 = [val for val in r if not np.isnan(val)]
            tmp.append(tmp1)
        #switch the values back to column format
        out.append(np.transpose(np.array(tmp)))
    out.append(np.array([val for val in ac_mag if not np.isnan(val)]))
    out.append(np.array([val for val in gy_mag if not np.isnan(val)]))
    out.append(np.array([val for val in mag_mag if not np.isnan(val)]))
    
    return out
