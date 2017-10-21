
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split
from scipy.fftpack import fft, ifft
from sklearn import metrics
from sklearn.cluster import DBSCAN
from numpy.fft import fftn

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
execfile('start.py')
execfile('stand_sit.py')
execfile('walk_binary.py')

ran = DataFrame(np.genfromtxt('random_seq.csv', delimiter=",")).dropna()
rand = ran.drop([ran.columns[0]], axis=1)
random = fftn(rand)

"""
stand_sit is used to train stand_sit_model
stand_sit_model.predict(random)
output: 0=sit, 1=stand, -1=noise

walk_bin is used to train walk_model
walk_model.predict(random)
output: 2=walk, 3=not_walk
"""

walk_predict=walk_model.predict(random)
stand_sit_predict = stand_sit_model.fit_predict(random)

random_predict = []

for i in walk_predict:
    random_predict.append(i)

for i in range(len(random_predict)):
    if random_predict[i] == 3:
        random_predict[i] = walk_predict[i]
    else:
        continue

# print(random_predict)
