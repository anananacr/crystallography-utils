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

photon_energy_in_kev=1


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
    dark_gain_1 = np.array(dark[:,:,1], dtype=np.uint16)
    gain_1 = np.array(gain[:,:,1], dtype=np.float32).reshape(512,1024)
    corrected_data -= dark_gain_1
    corrected_data /= gain_1
    return corrected_data.astype(np.int32)


def main():
    parser = argparse.ArgumentParser(
        description="Convert JUNGFRAU 4M images collected at SPB/SFX of the EuXFEL."
    )
    parser.add_argument(
        "-i", "--input", type=str, action="store", help="raw input folder"
    )
    parser.add_argument(
        "-p",
        "--pedestal",
        type=str,
        action="store",
        help="list file containing the path to the pedestals",
    )
    parser.add_argument(
        "-g",
        "--gain",
        type=str,
        action="store",
        help="list file containing the path to the gain info file",
    )
    parser.add_argument(
        "-b",
        "--bad_pixels",
        type=str,
        action="store",
        help="list file containing the path to the bad pixels files",
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )
    args = parser.parse_args()

    global dark, gain

    raw_folder = args.input
    output_folder = args.output
    path = pathlib.Path(output_folder)
    path.mkdir(parents=True, exist_ok=True)

    args = parser.parse_args()
    
    gain_filenames=open(args.gain, "r").readlines()
    dark_filenames=open(args.pedestal, "r").readlines()
    bad_pixels_filenames=open(args.bad_pixels, "r").readlines()

    detectors =  ["JNGFR01", "JNGFR02", "JNGFR03", "JNGFR04", "JNGFR05", "JNGFR06", "JNGFR07", "JNGFR08"]
    detector_id =  ["Jungfrau_M275", "Jungfrau_M510", "Jungfrau_M273", "Jungfrau_M384", "Jungfrau_M322", "Jungfrau_M311", "Jungfrau_M267", "Jungfrau_M318"]

    for detector_index, detector in enumerate(detectors):
        num_panels = 1
        gain = np.ndarray((1024, 512, 16, 3), dtype=np.float64)
        gain_mode = 1
        darks = np.ndarray((512, 1024,16, 3), dtype=np.float32)
        bad_pixels_map = np.ndarray((512, 1024,16, 3), dtype=np.float32)

        # open gain map for the detector
        gain_file: Any = h5py.File(gain_filenames[detector_index][:-1], "r")
        for storage_cell_number in range(16):
            gain[:,:,storage_cell_number, gain_mode] = gain_file[
            f"/{detector_id[detector_index]}/RelativeGain10Hz/0/data"][:,:, storage_cell_number, gain_mode]
        gain_file.close()

        # open the dark for the detector
        dark_file: Any = h5py.File(dark_filenames[detector_index][:-1], "r")
        for storage_cell_number in range(16):
            darks[:,:, storage_cell_number, gain_mode] = dark_file[f"/{detector_id[detector_index]}/Offset10Hz/0/data"][:,:, storage_cell_number, gain_mode]
        dark_file.close()

        # open the bad pixels map for the detector
        bad_pixels_file: Any = h5py.File(bad_pixels_filenames[detector_index][:-1], "r")
        for storage_cell_number in range(16):
            bad_pixels_map[:,:, storage_cell_number, gain_mode] = bad_pixels_file[f"/{detector_id[detector_index]}/BadPixelsDark10Hz/0/data"][:,:, storage_cell_number, gain_mode]
        bad_pixels_file.close()

        #data_shape = f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}::daqOutput/data/adc"].shape
        #converted_data = np.zeros(data_shape, dtype=np.int32)
        ## for test data
        converted_data = np.zeros((512,1024, 10,16), dtype=np.int32)

        ## collect raw path for the detector in raw folder
        raw_files_path = sorted(glob.glob(os.path.join(args.input, f"RAW-*-{detector}-S*.h5")))

        for raw_file in raw_files_path:
            print(raw_file)
            with h5py.File(f"{raw_file}", "r") as f:
                print(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"].shape)
                data_shape=f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"].shape
                if data_shape[0] != 0:
                    n_frames = f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"].shape[0]
                else:
                    continue
                
                #for i in range(data_shape[0]):
                for i in range(10):
                    for j in range(16):
                        storage_cell=int(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/memoryCell"][i,j])
                        bad_pixels_gain_1_mask = bad_pixels_map[:,:,storage_cell,1].copy()
                        bad_pixels_gain_1_mask[np.where(bad_pixels_gain_1_mask!=0)]=0
                        bad_pixels_gain_1_mask[np.where(bad_pixels_gain_1_mask==0)]=1
                        raw_data=np.array(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"][i,j])
                        converted_data[:,:,i,j] = apply_calibration(raw_data*bad_pixels_gain_1_mask, darks[:,:,storage_cell,:], gain[:,:,storage_cell,:])
            file_label=raw_file.split("RAW")[-1]
            with h5py.File(f"{output_folder}/CORR{file_label}", "w") as f:
                entry = f.create_group("entry_1")
                entry.attrs["NX_class"] = "NXentry"
                grp_data = entry.create_group("data_1")
                grp_data.attrs["NX_class"] = "NXdata"
                grp_data.create_dataset("data", data=converted_data, compression="gzip", compression_opts=6)

if __name__ == "__main__":
    main()
