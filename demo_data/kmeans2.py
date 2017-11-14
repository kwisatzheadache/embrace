import embrace_setup as es
import embrace_analysis as ea
import embrace_metrics as em
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

if __name__  == "__main__":
    x = []
    y = []
    z = []

    vals = es.get_lists(sys.argv[1])
    print(ea.kmeans2(vals))
    #for i in range(4,8):
    #    for j in range(8,15):
    #        x.append(i)
    #        y.append(j)
    #        z.append(np.abs(int(sys.argv[2])-ea.kmeans(vals,i,j)))
    
    #fig = plt.figure()
    #ax = fig.gca(projection='3d')

    #ax.plot_trisurf(x,y,z)
    #plt.show()
