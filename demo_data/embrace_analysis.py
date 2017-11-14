import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import embrace_setup as es
import embrace_fft as ef
import embrace_metrics as em

#default window size for kmeans clustering
WIN_SIZE = 11
#default number of clusters for walk cycles
NUM_CLUSTERS = 4

COLOR = {0:"r",1:"b",2:"w",3:"g",4:"k",5:"y",6:"c",7:"m"}

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
    """Plot the states of the sequence as predicted by the clustering"""
    plt.plot(range(len(state_seq)), state_seq)
    plt.show()

def graph_kmeans_2(state_seq,vals, num_clusters=NUM_CLUSTERS):
    """Graph the signal labeled by kmeans"""
    #get the time windows for each state
    state_breaks = [ [] for i in range(num_clusters)]
    pos = 0
    while pos < len(state_seq)-1:
        start = pos
        while pos <len(state_seq)-1 and state_seq[pos] == state_seq[pos+1]:
            pos += 1
        state_breaks[state_seq[pos]].append([start,pos])
        pos += 1

    #plot the ac, gy, and mag
    subplot = 311
    for sig in vals[1:4]:
        plt.subplot(subplot)
        #iterate over each axis
        for r in sig:
            #iterate over each state
            for s,state in enumerate(state_breaks):
                #iterate over each break
                for brk in state:
                    plt.plot(range(brk[0],brk[1]),r[brk[0]:brk[1]],color=COLOR[s])
        subplot += 1
    plt.show()


def find_steps(state_seq):
    step_count_ccw = 0
    step_count_cw = 0
    for i in range(len(state_seq)-1):
        if state_seq[i+1] < state_seq[i]:
            step_count_cw += 1
        if state_seq[i+1] > state_seq[i]:
            step_count_ccw += 1
    return min(step_count_cw, step_count_ccw)

def gen_seq_1(transition):
    seq = [0]
    while len(seq) < len(transition):
        probs = transition[seq[-1]]
        sorted_probs = sorted(probs, reverse=True)
        old_len = len(seq)
        pos = 0
        #until a new element has been added
        while len(seq) < len(transition) and len(seq) == old_len:
            #get the nth largest transition
            nex = np.where(probs == sorted_probs[pos])[0][0]
            #if the element is not already in seq, add it
            if nex not in seq:
                seq.append(nex)
            pos += 1
    return seq

def gen_seq_2(transition):
    max_pos = 0
    max_prob = 0
    for i,prob in enumerate(transition):
        if max(prob) > max_prob:
            max_prob = max(prob)
            max_pos = i
    
    seq = [i]
    for i in range(len(transition)):
        probs = transition[seq[-1]]
        max_prob = max(probs)
        nex = np.where(probs == max_prob)[0][0]
        if nex not in seq:
            seq.append(nex)
    return seq


def map_k_to_seq(state_seq, num_clusters=NUM_CLUSTERS):
    #eliminated repeated states
    i = 0
    while i < len(state_seq)-1:
        while i < len(state_seq)-1 and state_seq[i] == state_seq[i+1]:
            state_seq.pop(i)
        i += 1

    #transition probability matrix
    transition = np.zeros((num_clusters,num_clusters))
    #total number of transitions from state
    tot_obs = np.zeros((num_clusters,))
    for i in range(len(state_seq)-1):
        cur = state_seq[i]
        nex = state_seq[i+1]
        #update the transition matrix
        if cur != nex:
            transition[cur][nex] += 1
            tot_obs[cur] += 1
    #normalize the transition probs
    for i in range(len(transition)):
        transition[i] /= tot_obs[i]
   

    seq = gen_seq_2(transition)
    #map the states to a sequence
    final_seq = []
    for state in state_seq:
        if state in seq:
            final_seq.append(seq.index(state))

    plt.plot(range(len(final_seq)), final_seq)
    plt.show()
    return final_seq

    

def kmeans(vals, num_clusters=NUM_CLUSTERS, win_size=WIN_SIZE):
    #list to hold the windows over all signals
    wins = []

    #transpose ac,gy,and mag
    pos = 1
    for v in vals[1:4]:
        if len(v) != 3:
            vals[pos] = np.transpose(v)
            pos += 1

    #iterate through the 3 subdimensions for ac,gy
    for v in vals[1:2]:
        for r in v:
            wins.append(kmeans_window(r, win_size))

    #the magnitude vectors are 1 dimensional
    for i,v in enumerate(vals[4:5]):
        wins.append(kmeans_window(v, win_size))

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
    kmeans = KMeans(n_clusters=num_clusters, n_init=50, init='random')
    kmeans.fit(X)


    #get the predicted states for each window
    state_seq = np.ndarray.tolist(kmeans.predict(X))
   
    #plot the results
    #graph_kmeans(state_seq)
    #graph_kmeans_2(state_seq, vals)
    
    #convert the variable states to a single sequence
    state_seq = map_k_to_seq(state_seq,num_clusters)

    steps = find_steps(state_seq)

    #a rough measurement of steps
    #print("Window size: " + str(win_size))
    #print("Num clusters: " + str(num_clusters))
    #print("Number of steps from step count: " + str(steps))
    return steps


def kmeans2(vals, num_clusters=NUM_CLUSTERS, win_size=WIN_SIZE):

    v_train = None
    for filename in os.listdir("walk/"):
        print(filename)
        if v_train == None:
            v_train = es.get_lists("walk/"+filename)
            pos = 1
            for v in v_train[1:4]:
                v_train[pos] = np.transpose(v)
                pos += 1
        else:
            v_cur = es.get_lists("walk/"+filename)
            
            pos = 1
            for v in v_cur[1:4]:
                v = np.transpose(v)
                tmp = []
                for i,r in enumerate(v):
                    tmp.append(np.concatenate((v_train[pos][i],r)))
                v_train[pos] = tmp
                pos += 1

            for v in v_train[4:7]:
                v_train[pos] = np.concatenate((v_train[pos],v))
                pos += 1

    wins = []

    #transpose ac,gy,and mag
    pos = 1
    for v in v_train[1:4]:
        if len(v) != 3:
            vals[pos] = np.transpose(v)
            pos += 1

    #iterate through the 3 subdimensions for ac,gy
    for v in v_train[1:2]:
        for r in v:
            wins.append(kmeans_window(r, win_size))

    #the magnitude vectors are 1 dimensional
    for i,v in enumerate(v_train[4:5]):
        wins.append(kmeans_window(v, win_size))

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
    kmeans = KMeans(n_clusters=num_clusters, n_init=50, init='random')
    kmeans.fit(X)


    #get the predicted states for each window
    state_seq = np.ndarray.tolist(kmeans.predict(X))
   
    #plot the results
    #graph_kmeans(state_seq)
    #graph_kmeans_2(state_seq, vals)
    
    #convert the variable states to a single sequence
    state_seq = map_k_to_seq(state_seq,num_clusters)

    steps = find_steps(state_seq)

    #a rough measurement of steps
    #print("Window size: " + str(win_size))
    #print("Num clusters: " + str(num_clusters))
    #print("Number of steps from step count: " + str(steps))
    return steps

