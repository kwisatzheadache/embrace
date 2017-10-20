"""
Binary classification of walk against stand_sit.
"""
execfile('start.py')
execfile('window.py')

"""
Running `test_window(200, 10)` tests accuracy of a LogisticRegression classification, with
lag window varying from 1 to 201 in 10 unit increments. Accuracy seems to peak between a window
size of 11 and 41.
"""

window_scores = test_window(40, 1)
"""
Accuracy seems to peak at window = 16
"""
