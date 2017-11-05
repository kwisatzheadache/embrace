execfile('functions.py')

walk = get_nx10('data/walk.csv')

walk = np.array(walk)
walk = walk.transpose()

# Set window and freqency values and labels
window = 100
freq = 10
walk_label = 1
sit_label = 2
stand_label = 3
bin_size = 100


binned = make_bins(walk, bin_size)

""" determine optimal reduction of signal"""
run_klds(binned[1][1])

""" 33 dominant freqencies maintains kld entropy less than .05
Check other signals to determine if this holds"""

