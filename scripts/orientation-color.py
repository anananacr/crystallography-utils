"""
Based on Yaroslav Gevorkov script for orientation vectors.
"""

import numpy as np
import re
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import matplotlib.colors as colors
import math
import matplotlib as mpl
streamFileName = sys.argv[1]

if len(sys.argv) >= 3:
    markerSize = float(sys.argv[2])

f = open(streamFileName, 'r')
stream = f.read()
f.close()

output_path = os.path.dirname(os.path.abspath(streamFileName))  + '/plots_res'
if not os.path.exists(output_path):
    os.mkdir(output_path)

xStarNames = ["astar","bstar","cstar"]
colors = ["b","r","g"]

for i in np.arange(3):
    p = re.compile(xStarNames[i] + " = ([\+\-\d\.]* [\+\-\d\.]* [\+\-\d\.]*)")
    xStarStrings = p.findall(stream)

    xStars = np.zeros((3, 3*len(xStarStrings)), float)

    for j in np.arange(len(xStarStrings)):
        xStars[:,i*len(xStarStrings) +j] = np.array([float(s) for s in xStarStrings[j].split(' ')])

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot( 1, 1, 1, projection='3d')
    ax.scatter(xStars[0,:],xStars[1,:],xStars[2,:], marker=".", color=colors[i], s=1)
    plt.title(xStarNames[i] + "s")
    out = os.path.join(output_path, os.path.basename(streamFileName).split('.')[0]+ "_color_" + xStarNames[i])+'.png'
    #plt.savefig(out)
    plt.show()
    plt.close()
