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
import re
import os
import matplotlib.colors as color
import pathlib


def main():
    parser = argparse.ArgumentParser(
        description="Convert Jungfrau1M dark frames collected in fixed gain for burst mode."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        action="store",
        help="pedestal list",
    )

    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args()
    const_dark: Tuple[int, int, int] = (0, 0, 0)

    s = 100
    filelist=open(args.input, "r")
    n: int = 1024 * 512
    sd = np.zeros((3, 16, n), dtype=np.float64)
    nd = np.zeros((3, 16, n))

    panel_id: int

    for fn in filelist:
        index = s
        fn=fn[:-1]
        i: int = int(re.findall("_f(\\d+)_", fn)[0])
        h5_data_path: str = "/data_" + f"f{i:012d}"
        f: Any
        with h5py.File(fn, "r") as f:
            n_frames: int = f[h5_data_path].shape[0]
            print("%s frames in %s" % (n_frames, fn))
            frame: NDArray[np.int_]
            for frame in f[h5_data_path][s:]:
                #storage_cell_number = 15 - ((int(f["debug"][index])//256)%16)
                storage_cell_number =(int(f["debug"][index])//256)%16

                d: NDArray[np.int_] = frame.flatten()
                where_gain: List[Tuple[NDArray[np.int_]]] = [
                    np.where((d & 2**14 == 0) & (d > 0)),
                    np.where((d & (2**14) > 0) & (d & 2**15 == 0)),
                    np.where(d & 2**15 > 0),
                ]
                for i in range(3):
                    sd[i, storage_cell_number][where_gain[i]] += d[where_gain[i]]
                    nd[i, storage_cell_number][where_gain[i]] += 1
                index+=1

    with np.errstate(divide="ignore", invalid="ignore"):
        dark: NDArray[np.float_] = (sd / nd).astype(np.float32)

    if np.any(nd == 0):
        print("Some pixels don't have data in all gains:")
        for i in range(3):
            for j in range(16):
                where: List[Tuple[NDArray[np.int_]]] = np.where(nd[i,j] == 0)
                dark[i,j][where] = const_dark[i]
                print(
                f"{len(where[0])} pixels in gain {i} are set to {const_dark[i]}",
            )

    with h5py.File(args.output, "w") as f:
        f.create_dataset("/gain0", data=dark[0].reshape(16, 512, 1024))
        f.create_dataset("/gain1", data=dark[1].reshape(16, 512, 1024))
        f.create_dataset("/gain2", data=dark[2].reshape(16, 512, 1024))

if __name__ == "__main__":
    main()
