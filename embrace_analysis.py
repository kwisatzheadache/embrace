import numpy as np
import matplotlib as plt
import embrace_setup as es
import embrace_fft as ef
import embrace_metrics as em

#default window size for kmeans clustering
WIN_SIZE = 10
#default number of clusters for walk cycles
NUM_CLUSTERS = 8

def kmeans_window(signal, win_size=WIN_SIZE):
    """Get a list containing all the windows of size win_size from the signal
       Input:
         signal - 1-D array containing a time series signal
         win_size - length of the sliding window
       Output:
         wins - list of windows """
    wins = []
    for i in range(len(signal)-win_size):
        wins.append(signal[i:i+win_size])
    wins = np.array(wins)
    return wins

def graph_kmeans(state_seq):
    plt.plot(range(len(state_seq)), state_seq)
    plt.show()

def kmeans_walk(vals, num_clusters=NUM_CLUSTERS):
    #list to hold the windows over all signals
    wins = []

    #transpose ac,gy,and mag
    pos = 1
    for v in vals[1:4]:
        vals[pos] = np.transpose(v)
        pos += 1

    #iterate through the 3 subdimensions for ac,gy,mag
    for v in vals[1:4]:
        for r in v:
            wins.append(kmeans_windows(r))

    #the magnitude vectors are 1 dimensional
    for i,v in enumerate(vals[4:7]):
        wins.append(kmeans_windows(v))

    #convert to a numpy array and reshape as (num_wins,num_signals,win_size)
    wins = np.array(wins)
    wins = np.swapaxes(wins,0,1)

    #prepare the training matrix
    X = []
    for win in wins:
        tmp = np.empty(0)
        for sig in win:
            tmp = np.concatenate((tmp,sig))
        X.append(tmp)
    X = np.array(X)

    #create the kmeans clusterer and fit X to it
    kmeans = KMeans(n_clusters=8)
    kmeans.fit(X)

    #get the predicted states for each window
    state_seq = kmeans.predict(X)
    
    #plot the results
    graph_kmeans(state_seq)

    inds = np.ndarray.tolist(np.where(labs == 0)[0])
    i = 0
    while i < len(inds)-1:
        if inds[i] == inds[i+1]-1:
            del inds[i]
        else:
            i += 1
    #a rough measurement of steps
    print(len(inds))

