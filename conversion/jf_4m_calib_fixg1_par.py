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
from multiprocessing import Pool
import matplotlib.colors as color
import pathlib


def apply_calibration(data: np.ndarray, dark=None, gain=None) -> np.ndarray:
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
    dark_gain_1 = np.array(dark[:,:,1], dtype=np.int32)
    gain_1 = np.array(gain[:,:,1], dtype=np.float32).reshape(512,1024)
    corrected_data -= dark_gain_1
    corrected_data /= gain_1
    return corrected_data.astype(np.int32)


def process_raw_file(process_args: list):
    gain, darks, bad_pixels_map, raw_file, detector = process_args
    
    with h5py.File(f"{raw_file}", "r") as f:
        data_shape=f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"].shape
        if data_shape[0] != 0:
            n_frames = f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"].shape[0]
        else:
            return 0
        
        #converted_data = np.zeros((512,1024, 10,16), dtype=np.int32)
        converted_data = np.zeros((512,1024, n_frames,16), dtype=np.int32)
        
        for i in range(data_shape[0]):
        #for i in range(10):
            for j in range(16):
                storage_cell=int(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/memoryCell"][i,j])
                bad_pixels_gain_1_mask = bad_pixels_map[:,:,storage_cell,1].copy()
                bad_pixels_gain_1_mask[np.where(bad_pixels_gain_1_mask!=0)]=0
                bad_pixels_gain_1_mask[np.where(bad_pixels_gain_1_mask==0)]=1
                raw_data=np.array(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"][i,j])
                converted_data[:,:,i,j] = apply_calibration(raw_data*bad_pixels_gain_1_mask, darks[:,:,storage_cell,:], gain[:,:,storage_cell,:])
                converted_data[np.isnan(converted_data)]=0
    
    file_label=raw_file.split("RAW")[-1]
    
    output_folder = args.output
    path = pathlib.Path(output_folder)
    path.mkdir(parents=True, exist_ok=True)

    command = f"cp {raw_file} {output_folder}/CORR{file_label}"
    sub.call(command, shell=True)
    with h5py.File(f"{output_folder}/CORR{file_label}", "a") as f:
        del f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"]
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc", data=converted_data, compression="gzip", compression_opts=6)

def calibrate_detector_frames(calib_args: list):

    gain_filename, dark_filename, bad_pixels_filename, detector, detector_id = calib_args
  
    # open gain map for the detector
    gain = np.ndarray((1024, 512, 16, 3), dtype=np.float64)
    gain_mode = 1
    with h5py.File(gain_filename[:-1], "r") as gain_file:
        gain = np.array(gain_file[f"/{detector_id}/RelativeGain10Hz/0/data"])
    
    # open the dark for the detector

    darks = np.ndarray((512, 1024,16, 3), dtype=np.int32)
    with h5py.File(dark_filename[:-1], "r") as dark_file:
        darks = np.array(dark_file[f"/{detector_id}/Offset10Hz/0/data"])
            
    # open the bad pixels map for the detector
    bad_pixels_map = np.ndarray((512, 1024,16, 3), dtype=np.int32)
    with h5py.File(bad_pixels_filename[:-1], "r") as bad_pixels_file:
        bad_pixels_map = np.array(bad_pixels_file[f"/{detector_id}/BadPixelsDark10Hz/0/data"])
    
    ## collect raw path for the detector in raw folder
    print(os.path.join(args.input, f"RAW-*-{detector}-S{args.file_number:05}.h5"))
    raw_file = glob.glob(os.path.join(args.input, f"RAW-*-{detector}-S{args.file_number:05}.h5"))[0]
    process_args = [gain, darks, bad_pixels_map, raw_file, detector]

    process_raw_file(process_args)


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
        "-n",
        "--file_number",
        type=int,
        action="store",
        help="chunk file index",
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="hdf5 output path"
    )

    global args
    args = parser.parse_args()
    
    raw_folder = args.input
       
    gain_filenames=open(args.gain, "r").readlines()
    dark_filenames=open(args.pedestal, "r").readlines()
    bad_pixels_filenames=open(args.bad_pixels, "r").readlines()
    detectors =  ["JNGFR01", "JNGFR02", "JNGFR03", "JNGFR04", "JNGFR05", "JNGFR06", "JNGFR07", "JNGFR08"]
    detectors_id = ["Jungfrau_M275", "Jungfrau_M510", "Jungfrau_M273", "Jungfrau_M384", "Jungfrau_M322", "Jungfrau_M311", "Jungfrau_M267", "Jungfrau_M318"]
    calib_args = list(zip(gain_filenames, dark_filenames, bad_pixels_filenames, detectors, detectors_id))
    
    with Pool(8) as p:
        p.map(calibrate_detector_frames, calib_args)

if __name__ == "__main__":
    main()
