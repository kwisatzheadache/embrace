import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.cluster import DBSCAN

stand_sit = DataFrame(np.genfromtxt('stand_sit.csv', delimiter=",")).dropna()

# Only lag the xyz data, not the id or the y data
cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z']
stand_sit.columns = cols
to_lag = cols[1:]
no_id = stand_sit.drop(['id'], axis=1)


"""
I think the best method for this is DBScan because it is designed for data with n groups, where most data is within the groups with small amounts between representing transition from one to the other.

In this clustering method, sit=0, standing=1
"""


stand_sit_model = DBSCAN(eps=0.5, min_samples=10).fit(no_id)
labels = stand_sit_model.labels_

"""
I have tried transforming the data via fttn, but it breaks the classification model.
"""
