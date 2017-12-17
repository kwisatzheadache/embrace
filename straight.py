import matplotlib.pyplot as plt
import os
import scipy.stats as stats
import pandas as pd

execfile('functions.py')

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

def index_to_keep(index, acc=[]):
    if abs(index[0] - index[1]) < .01:
        acc.append(index[0])
    # lagged = lag(index, 2)
    # long1 = []
    # for i in range(len(lagged)):
    #     j, k = i
    #     if abs(j - k) < .01:
    #         long1.apend(i)
    #     else:


def loop_over_index(index, acc1, longest):
    if len(index) < 2:
        print('here')
        output = longest
        return(output)
    else:
        i = index[0]
        j = index[1]
        if abs(i - j) < .01:
            acc1.append(index[0])
            loop_over_index(index[1:], acc1, longest)
        else:
            if len(acc1) >= len(longest):
                loop_over_index(index[1:], [], acc1)
            else:
                loop_over_index(index[1:], [], longest)
