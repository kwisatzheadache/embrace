import matplotlib.pyplot as plt
import numpy as np

stand_sit = np.genfromtext('stand_sit.csv')
walk1 = np.genfromtext('walking.csv')
walk2 = np.genfromtext('walking_2.csv')
random = np.genfromtext('random_seq.csv')

"""
First step is to label the stand_sit, so that they can be classified... Clustering ought to
yield four groups? Sitting, up, standing, and down.

Then, once labels have been applied, do I use the same NN? Or do I take the labeled data a train
a binary classifier?

Perhaps the easiest place to start is just to label walk1 and walk2 as 1, and stand_sit as 0 to
train a binary classifier to recognize walking. I think I'll do that.
"""
