"""
Function apply_calibration is based on OnDA - Deutsches Elektronen-Synchrotron DESY,
a research centre of the Helmholtz Association.
"""

import h5py
import argparse
import math
from scipy import constants
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, BinaryIO, List
import glob
import subprocess as sub
import os
import matplotlib.colors as color
import pathlib


def main():
    parser = argparse.ArgumentParser(
        description="Separate Jungfrau1M frames collected in fixg1 in memoray cell to take the median of each memory cell to fake pedestals for burst mode calibration."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        action="store",
        help="input frames",
    )

    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args()

    filename = args.input
    panel_id: int



    number_of_frames = {i:0 for i in range(16)}
    frames_file: Any = h5py.File(filename, "r")
    data = frames_file["data_f000000000000"]
    debug = frames_file["debug"]
    data_shape = data.shape
    storage_cell_number: int

    for frame in range(data_shape[0]):
        storage_cell_number = int(debug[frame]//256)%16
        number_of_frames[storage_cell_number]+=1            
        
        
    d = {i:np.zeros((number_of_frames[i], *data_shape[1:])) for i in range(16)}
    accumulated_frames_counter = {i:0 for i in range(16)}

    for frame in range(data_shape[0]):
        storage_cell_number = int(debug[frame]//256)%16
        index=accumulated_frames_counter[storage_cell_number]
        masked_data=(data[frame].copy()).astype(float)

        #print(storage_cell_number,len(np.where(masked_data>1.03*np.median(masked_data))[0]))

        #if len(np.where(masked_data>1.03*np.median(masked_data))[0])>1000:
        #if len(np.where(masked_data>1.03*np.median(masked_data))[0])>66000:
        #    masked_data[:,:]=np.nan
        #else:
        #    masked_data=(data[frame].copy()).astype(float)
        #    masked_data[np.where(masked_data>1.03*np.median(masked_data))]=np.nan
        masked_data[np.where(masked_data>1.03*np.median(masked_data))]=np.nan

        #d[storage_cell_number][index,:,:]=data[frame]
        d[storage_cell_number][index,:,:]=masked_data
        accumulated_frames_counter[storage_cell_number]+=1
        
    frames_file.close()

    with h5py.File(args.output, "w") as f:
        for key, value in d.items():
            print(key,type(value))
            f.create_dataset(str(key), data=value)
if __name__ == "__main__":
    main()
