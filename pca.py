import os
import sys
import pprint
from sklearn.decomposition import PCA

execfile('functions.py')

csv_directory = sys.argv[1]
window = 100
num_freqs = 33

stacked = stack(csv_directory)
# drop acc_mag

run_pca(stacked)
