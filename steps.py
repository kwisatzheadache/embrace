import os
import sys
import pprint
from sklearn.decomposition import PCA

execfile('functions.py')

# dire = sys.argv[1]
# output_file = sys.argv[2]

straight, index = straight_walk(dire, 15)
longest = longest_walk(straight, index)

steps = find_steps(longest)
lens = lens(steps)

a_side = []
b_side = []
for i in range(len(lens)):
    if i % 2 = 0:
        a_side.append(lens[i])
    else:
        b_side.append(lens[i])
