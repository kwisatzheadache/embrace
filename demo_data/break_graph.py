#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

def onClick(event):
    print(event.x)
    print(event.y)

if __name__ == "__main__":

    vals = np.genfromtxt(sys.argv[1], delimiter=",")

    breaks *= 100
    breaks = [int(b) for b in breaks]

    for i in range(1, len(breaks)):
            file_name = str(i)
            outfile = open(file_name, "w")
            tmp = vals[breaks[i-1]:breaks[i]]
            for t in tmp:
                    outfile.write(",".join(str(val) for val in t) + '\n')
            outfile.close()
