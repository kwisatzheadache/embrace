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

# mag_z has the highest variance. Presumably, this indicates it corresponds most with walk orientation.

# walk.shape
# walk.columns
# plt.plot(walk['mag_x'])
# plt.show
# walk['mag_x']
# walk.values
# walk['mag_x'].values
# vals = _
# vals
# vals.shape
# plt.plot(vals)
# plt.show()
# plt.plot(vals)
# plt.show()
# x = walk['mag_x'].values
# y = walk['mag_y'].values
# z = walk['mag_z'].values
# coords = [x,y,z]
# plt.plot(y)
# plt.show()
# plt.plot(z)
# plt.show()
# import readline
# readline.write_history_file('./repl_history_12_02.py')
