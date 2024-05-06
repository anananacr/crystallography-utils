#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generate "peak powder" from CrystFEL stream
#
# Copyright © 2017-2020 Deutsches Elektronen-Synchrotron DESY,
#                       a research centre of the Helmholtz Association.
#
# Author:
#    2017 Alexandra Tolstikova <alexandra.tolstikova@desy.de>
#    2024 Ana Carolina Rodrigues <ana.rodrigues@desy.de>

import sys
import numpy as np
import h5py
from os.path import basename, splitext
import matplotlib.pyplot as plt

if sys.argv[1] == '-':
    stream = sys.stdin
else:
    stream = open(sys.argv[1], 'r')

reading_geometry = False
reading_chunks = False
reading_peaks = False
max_fs = -100500
max_ss = -100500
is_centered = False

for count, line in enumerate(stream):
    if reading_chunks:
        if line.startswith('End of peak list'):
            reading_peaks = False
            if is_centered:
                x_shift.append(shift_horizontal_mm)
                y_shift.append(shift_vertical_mm)                 
        elif line.startswith('  fs/px   ss/px (1/d)/nm^-1   Intensity  Panel'):
            reading_peaks = True
        elif line.split(': ')[0]=='Image filename':
            file_name=line.split(': ')[-1][:-1]
        elif line.split(': ')[0]=='Event':
            event=int(line.split(': //')[-1])
        elif line.split(' = ')[0]=="header/float//entry/shots/detector_shift_y_in_mm":
            shift_vertical_mm = float(line.split(' = ')[-1])
        elif line.split(' = ')[0]=="header/float//entry/shots/detector_shift_x_in_mm":
            shift_horizontal_mm = float(line.split(' = ')[-1])
        elif line.startswith("header/int//entry/shots/refined_center_flag = 0"):
            is_centered = False
        elif line.startswith("header/int//entry/shots/refined_center_flag = 1"):
            is_centered = True
    elif line.startswith('----- End geometry file -----'):
        reading_geometry = False
        x_shift = []
        y_shift = []
    elif reading_geometry:
        try:
            par, val = line.split('=')
            if par.split('/')[-1].strip() == 'max_fs' and int(val) > max_fs:
                max_fs = int(val)
            elif par.split('/')[-1].strip() == 'max_ss' and int(val) > max_ss:
                max_ss = int(val)
        except ValueError:
            pass
    elif line.startswith('----- Begin geometry file -----'):
        reading_geometry = True
    elif line.startswith('----- Begin chunk -----'):
        reading_chunks = True


bins = 0.035
xedges = np.arange(min(x_shift), max(x_shift), bins)
yedges = np.arange(min(y_shift), max(y_shift), bins)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, title="Detector center shift (mm)")
ax.set_xlabel("Detector center shift in x (mm)")
ax.set_ylabel("Detector center shift in y (mm)")
H, xedges, yedges = np.histogram2d(x_shift, y_shift, bins=(xedges, yedges))
H = H.T
X, Y = np.meshgrid(xedges, yedges)
pos = ax.pcolormesh(X, Y, H, cmap="coolwarm")
fig.colorbar(pos)
plt.savefig(f"test.png")
