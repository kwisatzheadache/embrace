import numpy as np
from pandas import DataFrame
from numpy.fft import fftn

execfile('start.py')
execfile('stand_sit.py')
execfile('walk_binary.py')

ran = DataFrame(np.genfromtxt('random_seq.csv', delimiter=",")).dropna()
rand = ran.drop([ran.columns[0]], axis=1)
random = DataFrame(fftn(rand))

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
        random_predict[i] = stand_sit_predict[i]
    else:
        continue

print(random_predict)
