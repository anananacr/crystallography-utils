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

def closest_index(arr, num):
    idx = np.abs(arr - num).argmin()
    return idx

if len(sys.argv) >= 3:
    markerSize = float(sys.argv[2])

f = open(streamFileName, 'r')
stream = f.read()
f.close()

output_path = os.path.dirname(os.path.abspath(streamFileName))  + '/plots_res'
if not os.path.exists(output_path):
    print(20)
    os.mkdir(output_path)

print(output_path)

xStarNames = ["astar","bstar","cstar"]


# Creating the theta and phi values.

intervals = 100
ntheta = intervals
nphi = 2*intervals
print(np.pi/ntheta)
theta = np.linspace(0, np.pi, ntheta+1)
phi   = np.linspace(0, 2*np.pi, nphi+1)

# Creating the coordinate grid for the unit sphere.
X = np.outer(np.sin(theta), np.cos(phi))
Y = np.outer(np.sin(theta), np.sin(phi))
Z = np.outer(np.cos(theta), np.ones(nphi+1))

# Creating a 2D array to be color-mapped on the unit sphere.
# {X, Y, Z}.shape → (ntheta+1, nphi+1) but c.shape → (ntheta, nphi)
c = np.zeros((ntheta, nphi))

for i in np.arange(3):
    p = re.compile(xStarNames[i] + " = ([\+\-\d\.]* [\+\-\d\.]* [\+\-\d\.]*)")
    xStarStrings = p.findall(stream)
    if i==0:
        xStars = np.zeros((3, 3*len(xStarStrings)), float)

    for j in np.arange(len(xStarStrings)):
        xStars[:,i*len(xStarStrings) +j] = np.array([float(s) for s in xStarStrings[j].split(' ')])
        norm_value = math.sqrt(xStars[0,i*len(xStarStrings)+j]**2 + xStars[1,i*len(xStarStrings)+j]**2 + xStars[2,i*len(xStarStrings)+j]**2)
        
        theta_meas = np.arccos(xStars[2,i*len(xStarStrings)+j]/norm_value)
        phi_meas = np.pi + np.arctan2(xStars[1,i*len(xStarStrings)+j],xStars[0,i*len(xStarStrings)+j])

        print(theta_meas,phi_meas)
        index_theta = closest_index(theta, theta_meas)
        index_phi = closest_index(phi, phi_meas)
        print(index_theta, index_phi)
        c[index_theta-1, index_phi-1]+=1
        

    c=np.log(c)
    c/=np.max(c)
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot( 1, 1, 1, projection='3d')
    cm = mpl.cm.viridis
    sm = mpl.cm.ScalarMappable(cmap=cm)
    sm.set_array([])
    ax = ax.plot_surface(X, Y, Z, facecolors=cm(c), rstride=1, cstride=1, alpha=0.8)
    plt.title(xStarNames[i] + "s")
    plt.xlabel("î")
    plt.ylabel("ĵ")
    plt.colorbar(ax)
    plt.show()
    c = np.zeros((ntheta, nphi))
    plt.close()
    out = os.path.join(output_path, os.path.basename(streamFileName).split('.')[0]+ "_" + xStarNames[i])+'.png'

