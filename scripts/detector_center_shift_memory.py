#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generate "peak powder" from CrystFEL stream
#
# Copyright © 2017-2020 Deutsches Elektronen-Synchrotron DESY,
#                       a research centre of the Helmholtz Association.
#
# Author:
#    2024 Ana Carolina Rodrigues <ana.rodrigues@desy.de>

import sys
import numpy as np
import h5py
from os.path import basename, splitext
import statistics
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
is_refined = False
is_indexed = False
memory_cell_selected = int(sys.argv[2])

for count, line in enumerate(stream):
    if reading_chunks:
        if line.startswith('End of peak list'):
            reading_peaks = False
            if is_centered and is_indexed and memory_cell_number==memory_cell_selected:
            #if is_indexed:
                x_shift.append(shift_horizontal_mm)
                y_shift.append(shift_vertical_mm)                 
        elif line.startswith('  fs/px   ss/px (1/d)/nm^-1   Intensity  Panel'):
            reading_peaks = True
        elif line.split(': ')[0]=='Image filename':
            file_name=line.split(': ')[-1][:-1]
        elif line.split(': ')[0]=='Event':
            event=int(line.split(': //')[-1])
        elif line.split(' = ')[0] == 'indexed_by':
            if line.split(' = ')[-1] == "none":
                is_indexed = False
            else:
                is_indexed = True
        elif line.split(' = ')[0]=="header/float//entry_1/instrument_1/data_1/detector_shift_y_in_mm":
            shift_vertical_mm = float(line.split(' = ')[-1])
        elif line.split(' = ')[0]=="header/float//entry_1/instrument_1/data_1/detector_shift_x_in_mm":
            shift_horizontal_mm = float(line.split(' = ')[-1])
        elif line.startswith("header/int//entry_1/instrument_1/data_1/refined_center_flag = 0"):
            is_refined = False
        elif line.startswith("header/int//entry_1/instrument_1/data_1/refined_center_flag = 1"):
            is_refined = True
        elif line.startswith("header/int//entry_1/instrument_1/data_1/pre_centering_flag = 0"):
            is_centered = False
        elif line.startswith("header/int//entry_1/instrument_1/data_1/pre_centering_flag = 1"):
            is_centered = True
        elif line.startswith("header/int//entry_1/memoryCell"):
            memory_cell_number = int(line.split(' = ')[-1])
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

#mean_x=statistics.mean(x_shift)
#mean_y=statistics.mean(y_shift)

#x_shift=[i-mean_x for i in x_shift ]
#y_shift=[i-mean_y for i in y_shift ]

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, title="Detector center shift (mm)")
ax.set_xlabel("Detector center shift in x (mm)")
ax.set_ylabel("Detector center shift in y (mm)")

ax.set_xlim(-4,4)
ax.set_ylim(4,-12)

H, xedges, yedges = np.histogram2d(x_shift, y_shift, bins=(20,100))
H = H.T
Hmasked = np.ma.masked_where(H==0,H)

X, Y = np.meshgrid(xedges, yedges)
pos = ax.pcolormesh(X, Y, Hmasked, cmap="coolwarm")
fig.colorbar(pos)
fig.text(0.3,0.85,s=f"Memory cell number {memory_cell_selected}", fontsize=14, color="g")
plt.grid()
plt.savefig(f"fakp_sweep_centered_{memory_cell_selected}.png")
