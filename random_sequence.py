import numpy as np
from pandas import DataFrame
from numpy.fft import fftn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import DBSCAN

execfile('fft.py')
execfile('start.py')
# execfile('stand_sit.py')
# execfile('walk_binary.py')

ran = np.genfromtxt('random_seq.csv', delimiter=",")

random_fft = data_transform(ran, 15)
walk_fft = data_transform(np.vstack((walk1, walk2)), 15)
stand_sit_fft = data_transform(stand_sit, 15)

y_walk = list()
for i in range(len(walk_fft)):
    y_walk.append(1)
for i in range(len(stand_sit_fft)):
    y_walk.append(0)

X = np.vstack((walk_fft, stand_sit_fft))
Y = y_walk
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.33, random_state=8)
walk_model = LogisticRegression()
walk_model.fit(X_train, Y_train)
# stand_sit_model = DBScan(eps=0.5, min_samples=10).fit(stand_sit_fft)

"""
stand_sit is used to train stand_sit_model
stand_sit_model.predict(random)
output: 0=sit, 1=stand, -1=noise

walk_bin is used to train walk_model
walk_model.predict(random)
output: 2=walk, 3=not_walk
"""

walk_predict=walk_model.predict(random)
# stand_sit_predict = stand_sit_model.fit_predict(random)

random_predict = []

# for i in walk_predict:
#     random_predict.append(i)

# for i in range(len(random_predict)):
#     if random_predict[i] == 3:
#         random_predict[i] = stand_sit_predict[i]
#     else:
#         continue

# print(random_predict)
