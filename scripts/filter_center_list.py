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

PixelResolution = 1 / (75 * 1e-3)

reading_geometry = False
reading_chunks = False
reading_peaks = False
max_fs = -100500
max_ss = -100500
is_a_hit = False
is_centered = False
is_refined = False
count_hits=0
count_centered=0
count_refined=0

output = open(sys.argv[2], "w")
file_name=""

def apply_shift_to_peak(fs: int, ss: int, detector_shift_x_in_px: int, detector_shift_y_in_px: int, panel_number: int):
    if panel_number<4:
        shifted_ss = ss - detector_shift_y_in_px
        shifted_fs = fs - detector_shift_x_in_px
    else:
        shifted_ss = ss + detector_shift_y_in_px
        shifted_fs = fs + detector_shift_x_in_px
        
    return shifted_fs, shifted_ss

if sys.argv[1] == '-':
    stream = sys.stdin
else:
    stream = open(sys.argv[1], 'r')

for count, line in enumerate(stream):
    if reading_chunks:
        if line.startswith('End of peak list'):
            reading_peaks = False
            if is_a_hit:
                count_hits+=1
            if is_centered:
                count_centered+=1    
            if is_refined:
                count_refined+=1

            if is_a_hit and is_centered:
            #if is_a_hit and is_centered and is_refined:
                output.write(file_name)
                filename=""          
        elif line.startswith('  fs/px   ss/px (1/d)/nm^-1   Intensity  Panel'):
            reading_peaks = True
        elif line.split(': ')[0]=="Image filename":
            file_name = line.split(': ')[1][:-1]+" "
        elif line.split(' ')[0]=="Event:":
            file_name += line.split(' ')[1]
        elif line.split(' = ')[0]=="header/float//entry_1/instrument_1/data_1/detector_shift_y_in_mm":
            detector_shift_y_in_mm = float(line.split(' = ')[-1])
            detector_shift_y_in_px = int(np.round(detector_shift_y_in_mm * PixelResolution))
        elif line.split(' = ')[0]=="header/float//entry_1/instrument_1/data_1/detector_shift_x_in_mm":
            detector_shift_x_in_mm = float(line.split(' = ')[-1])
            detector_shift_x_in_px = int(np.round(detector_shift_x_in_mm * PixelResolution))
        elif line.split(' = ')[0]=="hit":
            is_a_hit = int(line.split(' = ')[-1])
        elif line.split(' = ')[0]=="header/int//entry_1/instrument_1/data_1/pre_centering_flag":
            is_centered = int(line.split(' = ')[-1])
        elif line.split(' = ')[0]=="header/int//entry_1/instrument_1/data_1/refined_center_flag":
            is_refined = int(line.split(' = ')[-1])
        elif line.split(' = ')[0]=="header/int//entry_1/memoryCell":
            memory_cell_number = int(line.split(' = ')[-1])
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
    elif line.startswith('----- End chunk -----'):
        reading_chunks = False

print(f"--- Finished reading stream --- \n Number of hits: {count_hits} \n Number of centered frames: {count_centered} \n Number of frames with refined center: {count_refined} ")

output.close()
