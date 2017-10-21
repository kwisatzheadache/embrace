# embrace

Initial analyses of sit, stand, walk data. 

`random_sequence.py' outputs predictions based on the random_seq.csv data. 0=sit, 1=stand, 2=walk, -1=noise.

I encountered some difficulty with transforming the data, as most transformations broke my DBScan model for the stand_sit data. I'm 
wondering how the data were transformed before this point because while it broke the stand_sit model, it worked to make the random
sequence data more useable. 

`stand_sit.py` shows the analysis and training of an unsupervised model to fit the stand_sit data. I chose DBScan because it seemed
optimally suited for data with most points falling into two groups and the remainder representing transition between groups.

`walk_binary.py' in conjunction with `window.py' show the process of determining the best window for an LR model to fit to the walk data, which I combined with 
the stand_sit data to create a positive and a negative group.
Very quickly, the lag window provided an accuracy score approaching 1. I mention that 16 was the sweet spot, though in reality,
I found an error later that showed convergence much sooner. Nevertheless, I left that bit in their and I'm not sure how relevant
it was because in the random_sequence, I didn't use a lag window at all, so as to keep the dimensionality of the same across groups.

I expect there is much room for improvement; this has been my first experience with signal data, as well as unsupervised learning,
so I look forward to learning more. 
