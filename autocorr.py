from scipy.signal import find_peaks_cwt
execfile('functions.py')
execfile('peakdet.py')

dire = './demo_data/walk'
straight, index = straight_walk(dire, 15)
longest = longest_walk(straight, index)

steps, len_steps = find_steps(longest)
