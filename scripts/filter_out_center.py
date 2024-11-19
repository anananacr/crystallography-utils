#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generate "peak powder" from CrystFEL stream
#
# Copyright © 2017-2020 Deutsches Elektronen-Synchrotron DESY,
#                       a research centre of the Helmholtz Association.
#
# Author:
#    2024 Ana Carolina Rodrigues <ana.rodrigues@desy.de>s
#

import sys
import numpy as np
import h5py
from os.path import basename, splitext

PixelResolution = 1 / (75 * 1e-3)

if sys.argv[1] == '-':
    stream = sys.stdin
else:
    stream = open(sys.argv[1], 'r')

reading_geometry = False
reading_chunks = False
reading_peaks = False
is_centered = False
max_fs = -100500
max_ss = -100500

output = open(sys.argv[2], "w")
file_name=""

for line in stream:
    if reading_chunks:
        if line.startswith('End of peak list'):
            reading_peaks = False
        elif line.startswith('  fs/px   ss/px (1/d)/nm^-1   Intensity  Panel'):
            reading_peaks = True
        elif line.split(': ')[0]=="Image filename":
            file_name = line.split(': ')[1][:-1]+" "
        elif line.split(' ')[0]=="Event:":
            file_name += line.split(' ')[1]
        elif line.startswith('hit = 0'):
            is_a_hit = False
        elif line.split(' = ')[0]=="header/float//entry/shots/detector_shift_x_in_mm":
            shift_horizontal_mm = float(line.split(' = ')[-1])
            shift_horizontal_px = shift_horizontal_mm * PixelResolution
        elif line.split(' = ')[0]=="header/float//entry/shots/detector_shift_y_in_mm":
            shift_vertical_mm = float(line.split(' = ')[-1])
            shift_vertical_px = shift_vertical_mm * PixelResolution
        elif line.startswith("header/int//entry/shots/refined_center_flag = 1"):
        #elif line.startswith("header/int//entry/shots/refined_center_flag = 1") and shift_vertical_mm<3.15 and shift_vertical_mm>1.65 and shift_horizontal_mm<-0.5 and shift_horizontal_mm>-1.5:
                    output.write(file_name)
                    file_name="" 
    elif line.startswith('----- End geometry file -----'):
        reading_geometry = False
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

output.close()