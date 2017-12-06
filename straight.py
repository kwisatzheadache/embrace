import matplotlib.pyplot as plt
import os
import scipy.stats as stats

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

def return_straight_walk(walk_input, angle):
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
    mag_z = walks[:,9]
    lagged = lag(mag_z, 100)
    straight = []
    for i in lagged:
        avg = np.mean(i)
        low = avg - rotation
        high = avg + rotation
        if all(low <= j <= high for j in i):
            straight.append(i)
    return np.array(straight)
