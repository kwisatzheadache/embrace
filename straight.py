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
    chunk = []
    for i in range(len(lagged)):
        avg = np.mean(lagged[i])
        low = avg - rotation
        high = avg + rotation
        if all(low <= j <= high for j in lagged[i]):
            chunk.append(array[i])
        else:
            straight.append([chunk])
            chunk = []
    return np.array(straight)

def chunk_walks(walks):
    """
    """
    chunks = []
    mag_z = walks[:,9]
    for i in range(len(mag_z)):
        avg = np.mean(lagged[i])
        low = avg - rotation
        high = avg + rotation
        if all(low <= j <= high for j in lagged[i]):
            straight.append(array[i])
    return np.array(straight)
