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

complete = stack_walks('./demo_data/walk/ryan')

# Grab the individual magnetometer readings
mag_x = complete[:,7]
mag_y = complete[:,8]
mag_z = complete[:,9]

# Print descriptive statistics
for x in [mag_x, mag_y, mag_z]:
    print(stats.describe(x))

# Need to separate walks into chunks, where all mag_z values are within .1 of the average.
# Perhaps use std deviation of chunks... Where std < .05?
# Make windows... std of windows?

lagged = lag(mag_z, 100)
