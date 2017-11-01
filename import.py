execfile('functions.py')

stand_sit = get_nx10('data/stand_sit.csv')
walk = get_nx10('data/walk.csv')
sit = get_nx10('data/sits.csv')
stand = get_nx10('data/stands.csv')
random = get_nx10('data/random_seq.csv')

# Set window and freqency values and labels
window = 100
freq = 10
walk_label = 1
sit_label = 2
stand_label = 3


"""----------------- TRANSFORM DATA ------------------"""
walk = data_transform(walk, window, freq)
sit = data_transform(sit, window, freq)
stand = data_transform(stand, window, freq)

stand_sit = data_transform(stand_sit, window, freq)
random = data_transform(random, window, freq)

"""----------------- LABEL Y-VALUES --------------------""" 
# Has y-values
walk = label_y(walk, walk_label)
sit = label_y(sit, sit_label)
stand = label_y(stand, stand_label)

