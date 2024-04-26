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
        "-i",
        "--input",
        type=str,
        action="store",
        help="input frames separated per memory cell",
    )

    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args()

    filename=args.input
    dark = np.zeros((16, 3, 512, 1024), dtype=np.float32)
    panel_id: int

    gain_mode=1

    data_file: Any = h5py.File(filename, "r")
    
    for i in range(16):
        if i<6 or i>10:
            dark[i,gain_mode,:,:] =  np.nanmedian(np.array(data_file[f"{i}"]),axis=0)
        else:
            dark[i,gain_mode,:,:] =  dark[5,gain_mode,:,:]
        
    data_file.close()

    dark=np.nan_to_num(dark)
    
    with h5py.File(args.output, "w") as f:
        f.create_dataset("/gain0", data=dark[:,0,:,:])
        f.create_dataset("/gain1", data=dark[:,1,:,:])
        f.create_dataset("/gain2", data=dark[:,2,:,:])

if __name__ == "__main__":
    main()
