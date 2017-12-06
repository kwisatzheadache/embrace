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

def return_straight_walk(walk_file, angle):
    """
    Return windows where all values fall within the range of +/- rotation angle around the average.
    """
    rotation = (.72*angle)/360
    csv = get_nx10(walk_file)
    mag_z = csv[:,9]
    lagged = lag(mag_z, 100)
    straight = []
    for i in lagged:
        avg = np.mean(i)
        low = avg - rotation
        high = avg + rotation
        if all(low <= j <= high for j in i):
            straight.append(i)
    return np.array(straight)

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

# Set the threshold determining straight. The range of the magnetometer is .73, so a 30 degree window corresponds to .03 above and below the average.
rotation = .03

# If all the values in window fall within the range from low to high, add window to straight set.
straight = []
for i in lagged:
    avg = np.mean(i)
    low = avg - rotation
    high = avg + rotation
    if all(low <= j <= high for j in i):
        straight.append(i)

print(np.array(straight).shape)
