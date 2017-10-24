
stand_sit_with = np.genfromtxt('stand_sit.csv', delimiter=",")
remove_nan = DataFrame(stand_sit_with).dropna()
stand_sit = np.array(remove_nan)
walk1 = np.genfromtxt('walking.csv', delimiter=",")
walk2 = np.genfromtxt('walking_2.csv', delimiter=",")

# indices = {'id':0, 'acc_x':1, 'acc_y':2, 'acc_z':3,
#            'gy_x':4, 'gy_y':5, 'gy_z':6,
#            'mag_x':7, 'mag_y':8, 'mag_z':9}


# windows = dataset_to_windows(walk1, 15)
# fft_transformed = fft_transform(windows)
