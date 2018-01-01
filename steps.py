import os
import sys
import pprint
from sklearn.decomposition import PCA

execfile('functions.py')

# dire = sys.argv[1]
# output_file = sys.argv[2]

straights, index = straight_walk(dire, 15)
longest = longest_walk(straights, index)

steps = find_steps(longest)
# lens = lens(steps)

a, b = left_right(steps)

avg_step = avg_len(steps)
avg_a = avg_len(a)
avg_b = avg_len(b)

ratio_ab = avg_a/float(avg_b)

