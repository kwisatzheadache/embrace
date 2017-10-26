from sklearn.cluster import DBSCAN

execfile('functions.py')

stand_sit_with = np.genfromtxt('data/stand_sit.csv', delimiter=",")
walk1 = np.genfromtxt('data/walking.csv', delimiter=",")
walk2 = np.genfromtxt('data/walking_2.csv', delimiter=",")
stand = np.genfromtxt('data/stands.csv', delimiter=",")
remove_nan = DataFrame(stand).dropna()
stands= np.array(remove_nan)
sit = np.genfromtxt('data/sits.csv', delimiter=",")
remove_nan = DataFrame(sit).dropna()
sits = np.array(remove_nan)
random = np.genfromtxt('data/random_seq.csv', delimiter=",")
remove_nan = DataFrame(random).dropna()
random = np.array(remove_nan)

random_transformed = data_transform(random, 100)

Fk, n_freq = random_transformed[1,1]

"""
data_transform/2 creates windows of size $2. The resultant dataset is 4d. transformed.shape = (a,b,c,d)
Consequently, dimensionality must be reduced to perform classification.
"""

