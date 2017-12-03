execfile('functions.py')
walk = get_nx10('./data/walk.csv')
walk.shape
walk.columns
import matplotlib.pyplot as plt
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
