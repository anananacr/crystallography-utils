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

def filter_data(data):
    """
    Filter JUNGFRAU 1M faulty images based on number of pixels at gain 2.

    Parameters
    ----------
    data: np.ndarray
        JUNGFRAU 1M single raw image

    Returns
    ----------
    bool
        True if file should be skipped before apply calibration
    """
    gain_3 = np.where(data & 2**15 > 0)
    counts_3 = gain_3[0].shape[0]
    if counts_3 > 1e6:
        return True
    else:
        return False


def apply_calibration(data: np.ndarray, dark=dark, gain=gain) -> np.ndarray:
    """
    Applies the calibration to a JUNGFRAU 1M detector data frame.

    This function determines the gain stage of each pixel in the provided data
    frame, and applies the relevant gain and offset corrections.

    Parameters:

        data: The detector data frame to calibrate.

    Returns:

        The corrected data frame.
    """
    corrected_data: np.ndarray = data.astype(np.float32)

    where_gain: List[np.ndarray] = [
        np.where((data & 2**14 == 0) & (data & 2**15 == 0)),
        np.where((data & (2**14) > 0) & (data & 2**15 == 0)),
        np.where(data & 2**15 > 0),
    ]

    gain_mode: int

    for gain_mode in range(3):
        corrected_data[where_gain[gain_mode]] -= dark[gain_mode][where_gain[gain_mode]]
        corrected_data[where_gain[gain_mode]] /= (gain[gain_mode][where_gain[gain_mode]] * photon_energy_in_kev)

    return corrected_data.astype(np.int32)


def main(raw_args=None):
    parser = argparse.ArgumentParser(
        description="Convert JUNGFRAU 1M H5 images collected at REGAE for rotational data step/fly scan and return images in rotation sequence according tro the file index."
    )
    parser.add_argument(
        "-i", "--input", type=str, action="store", help="hdf5 input image"
    )
    parser.add_argument(
        "-p1",
        "--pedestal1",
        type=str,
        action="store",
        help="path to the pedestal file for module 1",
    )
    parser.add_argument(
        "-p2",
        "--pedestal2",
        type=str,
        action="store",
        help="path to the pedestal file for module 2",
    )
    parser.add_argument(
        "-g1",
        "--gain1",
        type=str,
        action="store",
        help="path to the gain info file for module 1",
    )
    parser.add_argument(
        "-g2",
        "--gain2",
        type=str,
        action="store",
        help="path to the gain info file for module 2",
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args(raw_args)

    global dark, gain

    raw_folder = os.path.dirname(args.input)
    output_folder = os.path.dirname(args.output)
    path = pathlib.Path(output_folder)
    path.mkdir(parents=True, exist_ok=True)

    num_panels: int = 2
    dark_filenames = [args.pedestal1, args.pedestal2]
    gain_filenames = [args.gain1, args.gain2]
    dark = np.ndarray((3, 512 * num_panels, 1024), dtype=np.float32)
    gain = np.ndarray((3, 512 * num_panels, 1024), dtype=np.float64)
    panel_id: int
    for panel_id in range(num_panels):
        gain_file: BinaryIO = open(gain_filenames[panel_id], "rb")
        dark_file: Any = h5py.File(dark_filenames[panel_id], "r")
        gain_mode: int
        for gain_mode in range(3):
            dark[gain_mode, 512 * panel_id : 512 * (panel_id + 1), :] = dark_file[
                "gain%d" % gain_mode
            ][:]
            gain[gain_mode, 512 * panel_id : 512 * (panel_id + 1), :] = np.fromfile(
                gain_file, dtype=np.float64, count=1024 * 512
            ).reshape(512, 1024)
        gain_file.close()
        dark_file.close()


    f = h5py.File(f"{args.input}", "r")
    data_shape = f["entry/data/data"].shape
    converted_data = np.zeros(data_shape, dtype=np.int32)

    for i in range(data_shape[0]):
        raw_data=np.array(f["entry/data/data"][i])
        if not filter_data(raw_data):
            converted_data[i] = apply_calibration(raw_data, dark, gain)
        
    with h5py.File(args.output, "w") as f:
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        grp_data = entry.create_group("data")
        grp_data.attrs["NX_class"] = "NXdata"
        grp_data.create_dataset("data", data=converted_data, compression="gzip", compression_opts=6)

if __name__ == "__main__":
    main()
