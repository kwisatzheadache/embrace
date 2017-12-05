execfile('functions.py')
import matplotlib.pyplot as plt

def stack_walks(direc):
    files = os.listdir(direc)
    csvs = []
    for x in files:
        if '.csv' in x:
            csvs.append(x)
    complete = np.vstack([get_nx10(direc+'/'+x) for x in csvs])
    return complete

complete = stack_walks('./demo_data/walk/ryan')
walk.shape
walk.columns
plt.plot(walk['mag_x'])
plt.show
walk['mag_x']
walk.values
walk['mag_x'].values
vals = _
vals
vals.shape
plt.plot(vals)
plt.show()
plt.plot(vals)
plt.show()
x = walk['mag_x'].values
y = walk['mag_y'].values
z = walk['mag_z'].values
coords = [x,y,z]
plt.plot(y)
plt.show()
plt.plot(z)
plt.show()
import readline
readline.write_history_file('./repl_history_12_02.py')
