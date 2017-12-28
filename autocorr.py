from scipy.signal import find_peaks_cwt
execfile('functions.py')
execfile('peakdet.py')

dire = './demo_data/walk'
straight, index = straight_walk(dire, 15)
longest = longest_walk(straight, index)

step_ind, len_steps = find_steps(longest)

loc_and_len = zip(step_ind, len_steps)

steps = []
for location, length in loc_and_len:
    start = location
    stop = location + length
    step = longest[start:stop]
    steps.append(step)
