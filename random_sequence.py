execfile('start.py')
execfile('stand_sit.py')
execfile('walk_binary.py')

ran = DataFrame(np.genfromtxt('random_seq.csv', delimiter=",")).dropna
random = ran.drop([ran.columns[0]], axis=1)

"""
stand_sit is used to train stand_sit_model
stand_sit_model.predict(random)
output: 0=sit, 1=stand

walk_bin is used to train walk_model
walk_model.predict(random)
output: 2=walk, 3=not_walk
"""

walk_predict=walk_model.predict(random)
