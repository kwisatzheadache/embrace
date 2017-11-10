execfile('functions.py')
execfile('embrace_fft.py')

coords = ['acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 

stand_sit = get_nx10('data/stand_sit.csv')
walk = get_nx10('data/walk.csv')
sit = get_nx10('data/sits.csv')
stand = get_nx10('data/stands.csv')
random = get_nx10('data/random_seq.csv')

# Set window and freqency values and labels
window = 100
freq = 33
walk_label = 1
sit_label = 2
stand_label = 3
reduced_sig_len = 50


"""----------------- TRANSFORM DATA ------------------"""
""" Windows are created, window_size=100. fft transform on all windows, retaining 33 most dominant signals."""
dom_walk = data_transform(walk, window, freq)
dom_sit = data_transform(sit, window, freq)
dom_stand = data_transform(stand, window, freq)

dom_stand_sit = data_transform(stand_sit, window, freq)
dom_random = data_transform(random, window, freq)

"""----------------- LABEL Y-VALUES --------------------""" 
# Has y-values
y_walk = label_y(dom_walk, walk_label)
y_sit = label_y(dom_sit, sit_label)
y_stand = label_y(dom_stand, stand_label)

"""------------------ REDUCE SIGNALS -------------------"""
red_walk = fft_to_signal(dom_walk, 50, coords)

X_walk = []

def w_avg(dataset):
    array = []
    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            Fk, n_freq = dataset[i,j]
            avg = []
            for l in range(len(Fk)):
                avg.append(abs(Fk[l]*n_freq[l]))
            w_avg = avg/len(avg)
    col = []

