import matplotlib.pyplot as plt
import sys
import numpy as np


if __name__ == "__main__":
	"""A simple script to plot the accelerometer, gyroscope, and magnetometer signals
	from an [Nx10] data file.
	Pass in the data file as the first argument, that is
	>python plot_it.py [datafile]""" 

	vals = np.genfromtxt(sys.argv[1], delimiter=",")

	t = np.array([i * .01 for i in range(vals.shape[0])])
	ac = np.transpose(vals[:,1:4])
	gy = np.transpose(vals[:,4:7])
	mag = np.transpose(vals[:,7:10])

	subplot = 311

	labs_ax = ["x", "y", "z"]
	labs_d = ["acceleration m/s^2", "gyroscope deg/s", "magnetometer gauss"]
	for i,data in enumerate([ac,gy,mag]):
		lines = []
		plt.subplot(subplot)
		plt.title(labs_d[i])
		for j,d in enumerate(data):
			tmp, = plt.plot(t,d, label=labs_ax[j])
			lines += [tmp]
		subplot += 1
		plt.legend(handles=lines)
	plt.show()
