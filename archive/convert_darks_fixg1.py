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
        description="Convert Jungfrau1M dark frames collected in fixg1 for burst mode calibration."
    )
    parser.add_argument(
        "-p",
        "--pedestal",
        type=str,
        action="store",
        help="path to the pedestal file for module 1",
    )

    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args()

    dark_pattern = args.pedestal+"*"

    dark_filenames=sorted(glob.glob(f"{dark_pattern}"))
    n: int = 1024 * 512
    sd = np.zeros((16, 3, n), dtype=np.float64)
    nd = np.zeros((16, 3, n))

    panel_id: int

    for gain_mode in range(1,2):

        dark_filename=dark_filenames[0]
        dark_file: Any = h5py.File(dark_filename, "r")
        darks = dark_file["data_f000000000000"]
        debug = dark_file["debug"]
        darks_shape = darks.shape
        storage_cell_number: int

        for frame in range(darks.shape[0]):
            storage_cell_number = int(debug[frame]//256)%16
            dark[storage_cell_number, gain_mode, : , :] += darks[frame]
            d[storage_cell_number]+=1            
        
        dark_file.close()
        for storage_cell_number, counter in d.items():
            if counter!=0:
                dark[storage_cell_number,gain_mode,:,:]/=counter

    ### bad_pixels set to zero

    with h5py.File(args.output, "w") as f:
        f.create_dataset("/gain0", data=dark[:,0,:,:])
        f.create_dataset("/gain1", data=dark[:,1,:,:])
        f.create_dataset("/gain2", data=dark[:,2,:,:])

if __name__ == "__main__":
    main()
