from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
#embrace functions
import embrace_setup as es
import embrace_fft as ef
import embrace_analysis as ea
import embrace_metrics as em


if __name__ == "__main__":
    #run listen on the current thread. Terminates with ^C
    port = "7011"
    filename = sys.argv[1]
    #start the tcp server and save data to file
    os.system("listen "+port+" > "+filename)
    os.system("head -$(wc -l "+filename+" | cut -d' ' -f1) "+filename+" > "+filename+".tmp")
    os.system("mv "+filename+".tmp "+filename)
    vals = es.get_lists(filename)

    ea.kmeans(vals)

    em.calc_step_var(vals)


    
    

    



