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

def apply_calibration(data: np.ndarray, dark=None, gain=None, mask=None) -> np.ndarray:
    """
    Applies the calibration to a JUNGFRAU 1M detector data frame.

    This function determines the gain stage of each pixel in the provided data
    frame, and applies the relevant gain and offset corrections.

    Parameters:

        data: The detector data frame to calibrate.

    Returns:

        The corrected data frame.
    """
    d = data.astype(np.float32)
    d -= dark
    d /= gain
    d = np.nan_to_num(d, nan=0)

    ## revert the mask again
    bad_pixels_index=np.where(mask==0)
    good_pixels_index=np.where(mask==1)
    saved_mask = mask.copy()
    saved_mask[good_pixels_index]=0
    saved_mask[bad_pixels_index]=1

    return (d).astype(np.int32), saved_mask.astype(np.int32)

def process_raw_file(process_args: list):
    gain, darks, bad_pixels_map, bad_pixels_ff_map, raw_file, detector = process_args

    # prepare constants
    mask = np.moveaxis(bad_pixels_map, 2, 0)
    bad_pixels_index=np.where(mask>0)
    good_pixels_index=np.where(mask==0)
    mask[good_pixels_index]=1
    mask[bad_pixels_index]=0

    # format should be cell, x, y, gain
    mask_ff = np.moveaxis(bad_pixels_ff_map, [0, 1, 2, 3], [2, 1, 0, 3])
    bad_pixels_ff_index=np.where(mask_ff>0)
    good_pixels_ff_index=np.where(mask_ff==0)
    mask_ff[good_pixels_ff_index]=1
    mask_ff[bad_pixels_ff_index]=0
    
    mask[..., [255, 256], :, :] = 0
    mask[..., [255, 256, 511, 512, 767, 768], :] = 0

    #mask = np.nan_to_num(mask, nan=0)
    darks = np.moveaxis(darks, [0, 1], [1, 2])

    gain = np.moveaxis(gain, [0, 2], [2, 0])
    
    #print(darks.shape, gain.shape, mask.shape, mask_ff.shape)
    mask *= mask_ff

    with h5py.File(f"{raw_file}", "r") as f:
        data_shape=f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"].shape
        if data_shape[0] != 0:
            n_trains = data_shape[0]
        else:
            return 0
        
        #n_trains=8
        converted_data = np.zeros((n_trains, 512, 1024, 16), dtype=np.int32)
        mask_dataset = np.zeros((n_trains, 512, 1024, 16), dtype=np.int32)
        raw_data = np.zeros((512, 1024), dtype=np.int32)

        for i in range(n_trains):
            for j in range(16):
                storage_cell=int(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/memoryCell"][i,j])
                raw_data=np.array(f[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"][i,j], dtype=np.int32)
                # format should be cell, x, y, gain
                converted_data[i,:,:,j], mask_dataset[i,:,:,j] = apply_calibration(raw_data, darks[storage_cell,:,:,1], gain[storage_cell,:,:,1], mask[storage_cell,:,:,1])
                converted_data[i,:,:,j] *= mask[storage_cell,:,:,1]
                #print(raw_data.shape, converted_data.shape, mask_dataset.shape, darks.shape, gain.shape)
    
    converted_data = np.moveaxis(converted_data, 3,1)
    mask_dataset = np.moveaxis(mask_dataset, 3,1)

    file_label=raw_file.split("RAW")[-1]
    
    output_folder = args.output
    path = pathlib.Path(output_folder)
    path.mkdir(parents=True, exist_ok=True)

    command = f"cp {raw_file} {output_folder}/CORR{file_label}"
    sub.call(command, shell=True)

    with h5py.File(f"{raw_file}", "r") as g:
        frame_number_dataset = np.array(g[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/frameNumber"], dtype=np.int32)
        gain_dataset = np.array(g[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/gain"], dtype=np.int32)
        memory_cell_dataset = np.array(g[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/memoryCell"], dtype=np.int32)
        train_id_dataset = np.array(g[f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/trainId"], dtype=np.int64)
        count = np.array(g[f"/INDEX/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/count"], dtype=np.int32)
        first = np.array(g[f"/INDEX/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/first"], dtype=np.int32)


    with h5py.File(f"{output_folder}/CORR{file_label}", "a", libver=("v110", "v110")) as f:
        adc_hdf5_path = f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc"
        adc_shape = f[adc_hdf5_path].shape
        layouts = h5py.VirtualLayout(adc_shape, dtype=np.int32)
        vsrc = h5py.VirtualSource(raw_file, adc_hdf5_path, adc_shape)
        layouts[...] = vsrc
        f.create_virtual_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/adc", layouts)
        
        del f[adc_hdf5_path]
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/adc", data=converted_data, compression="gzip", compression_opts=6)
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/DET/{detector}:daqOutput/data/mask", data=mask_dataset)
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/frameNumber", data=frame_number_dataset)
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/gain", data=gain_dataset)
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/memoryCell", data=memory_cell_dataset)
        f.create_dataset(f"/INSTRUMENT/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/trainId", data=train_id_dataset)
        f.create_dataset(f"/INDEX/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/count", data=count)
        f.create_dataset(f"/INDEX/SPB_IRDA_JF4M/CORR/{detector}:daqOutput/data/first", data=first)

def calibrate_detector_frames(calib_args: list):

    gain_filename, dark_filename, bad_pixels_filename, bad_pixels_ff_filename, detector, detector_id = calib_args
  
    # open gain map for the detector
    
    gain_mode = 1
    gain = np.zeros((1024, 512, 16, 3), dtype=np.float32)
    with h5py.File(gain_filename[:-1], "r") as gain_file:
        gain = np.array(gain_file[f"/{detector_id}/RelativeGain10Hz/0/data"], dtype=np.float32)
    
    # open the dark for the detector
    darks = np.zeros((512, 1024,16, 3), dtype=np.int32)
    with h5py.File(dark_filename[:-1], "r") as dark_file:
        darks = np.array(dark_file[f"/{detector_id}/Offset10Hz/0/data"], dtype=np.int32)
            
    # open the bad pixels map for the detector
    bad_pixels_map = np.zeros((512, 1024,16, 3), dtype=np.int32)
    with h5py.File(bad_pixels_filename[:-1], "r") as bad_pixels_file:
        bad_pixels_map = np.array(bad_pixels_file[f"/{detector_id}/BadPixelsDark10Hz/0/data"], dtype=np.int32)

    # open the bad pixels ff map for the detector
    bad_pixels_ff_map = np.zeros((1024, 512,16, 3), dtype=np.int32)
    with h5py.File(bad_pixels_ff_filename[:-1], "r") as bad_pixels_ff_file:
        bad_pixels_ff_map = np.array(bad_pixels_ff_file[f"/{detector_id}/BadPixelsFF10Hz/0/data"], dtype=np.int32)
   
    ## collect raw path for the detector in raw folder
    print(os.path.join(args.input, f"RAW-*-{detector}-S{args.file_number:05}.h5"), glob.glob(os.path.join(args.input, f"RAW-*-{detector}-S{args.file_number:05}.h5"))[0])
    raw_file = glob.glob(os.path.join(args.input, f"RAW-*-{detector}-S{args.file_number:05}.h5"))[0]
    process_args = [gain, darks, bad_pixels_map, bad_pixels_ff_map, raw_file, detector]

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
        "-bf",
        "--bad_pixels_ff",
        type=str,
        action="store",
        help="list file containing the path to the bad pixels for JF FF files",
    )
    parser.add_argument(
        "-n",
        "--file_number",
        type=int,
        action="store",
        help="file index",
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
    bad_pixels_ff_filenames=open(args.bad_pixels_ff, "r").readlines()
    detectors =  ["JNGFR01", "JNGFR02", "JNGFR03", "JNGFR04", "JNGFR05", "JNGFR06", "JNGFR07", "JNGFR08"]
    detectors_id = ["Jungfrau_M275", "Jungfrau_M510", "Jungfrau_M273", "Jungfrau_M384", "Jungfrau_M322", "Jungfrau_M311", "Jungfrau_M267", "Jungfrau_M318"]
    calib_args = list(zip(gain_filenames, dark_filenames, bad_pixels_filenames, bad_pixels_ff_filenames, detectors, detectors_id))
    
    with Pool(8) as p:
        p.map(calibrate_detector_frames, calib_args)

if __name__ == "__main__":
    main()
