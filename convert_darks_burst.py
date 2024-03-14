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

dark = None
gain = None
fly_frames_to_merge = 1
mode = 0 #"fly"
photon_energy_in_kev=14.96


def main():
    parser = argparse.ArgumentParser(
        description="Convert JUNGFRAU 1M H5 images collected at REGAE for rotational data step/fly scan and return images in rotation sequence according tro the file index."
    )
    parser.add_argument(
        "-p1",
        "--pedestal1",
        type=str,
        action="store",
        help="path to the pedestal file for module 1",
    )

    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args()

    dark_pattern = args.pedestal1+"*"

    dark_filenames=sorted(glob.glob(f"{dark_pattern}"))
    dark = np.zeros((16, 3, 512, 1024), dtype=np.float32)
    panel_id: int

    #for gain_mode in range(len(dark_filenames)):
    for gain_mode in range(1):

        d = {i:0 for i in range(16)}
        dark_filename=dark_filenames[gain_mode]
        dark_file: Any = h5py.File(dark_filename, "r")
        darks = dark_file["data_f000000000000"]
        debug = dark_file["debug"]
        darks_shape = darks.shape

        storage_cell_number: int

        if gain_mode==0:
            #for frame in range(darks_shape[0]):
            for frame in range(10001):
                storage_cell_number = int(debug[frame]//256)%16
                dark[storage_cell_number, gain_mode, : , :] += darks[frame]
                d[storage_cell_number]+=1            
        else:
            skip_dict_counter = {i:0 for i in range(16)}

            for frame in range(darks_shape[0]):
                storage_cell_number = int(debug[frame]//256)%16
                if storage_cell_number!=0:
                    # take second 100
                    if d[storage_cell_number]<100 and skip_dict_counter[storage_cell_number]<100:
                        skip_dict_counter[storage_cell_number]+=1
                    else:
                        dark[storage_cell_number, gain_mode, : , :] += darks[frame]
                        d[storage_cell_number]+=1
                else:
                    # take first 100
                    if d[storage_cell_number]<100:
                        dark[storage_cell_number, gain_mode, : , :] += darks[frame]
                        d[storage_cell_number]+=1

        dark_file.close()
        for storage_cell_number, counter in d.items():
            dark[storage_cell_number,gain_mode,:,:]/=counter

    ## TODO pixels that don't have data in all gains, for all cells??

    with h5py.File(args.output, "w") as f:
        f.create_dataset("/gain0", data=dark[:,0,:,:])
        f.create_dataset("/gain1", data=dark[:,1,:,:])
        f.create_dataset("/gain2", data=dark[:,2,:,:])

if __name__ == "__main__":
    main()
