import h5py
import argparse
import math
import numpy as np
import os

def skip_lost_panel(data:np.array, lost_flag:int):
    if len(np.where(data<=lost_flag)[0])>5.2e5:
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Sum up Jungfrau frames."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        action="store",
        help="input file (.h5, .cxi)",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        action="store",
        default ="/entry/data/data",
        help="data hdf5 path",
    )
    parser.add_argument(
        "-l",
        "--lost_flag",
        type=int,
        action="store",
        default = -1.15e8,
        help="lost packet value",
    )
    parser.add_argument(
        "-n",
        "--number_of_frames",
        type=int,
        action="store",
        default = -1,
        help="number of frames to sum, -1 sum all of the frames ",
    )
    parser.add_argument(
        "-s",
        "--starting_frame",
        type=int,
        action="store",
        default=0,
        help="starting frame, default is 0.",
    )
    parser.add_argument(
        "-lt",
        "--mask_less_than",
        type=int,
        action="store",
        default=None,
        help="mask values less than a value in the output array, default is None which means not mask anything. Masked values are replaced by 0 (zero).",
    )

    parser.add_argument(
        "-gt",
        "--mask_greater_than",
        type=int,
        action="store",
        default=None,
        help="mask values greater than a value in the output array, default is None which means not mask anything. Masked values are replaced by 0 (zero).",
    )
    parser.add_argument(
        "-e",
        "--apply_exponential",
        type=bool,
        action="store",
        default=False,
        help="apply exponential to each number of the array, default is False which will not apply the exponential to each number of the array.",
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path in .h5"
    )

    args = parser.parse_args()

    h5_data_path = args.path
    print(h5_data_path)
    h5_data_path = "/entry_1/data_1/data"
    starting_frame = args.starting_frame
    print(h5_data_path)

    with h5py.File(args.input, "r") as f:
        if args.number_of_frames==-1:
            n_frames = f[h5_data_path].shape[0]
        else:
            n_frames = args.number_of_frames
        
        
        data_shape=f[h5_data_path].shape[1:]
        print((1,*data_shape))
        acc_data=np.zeros((1,*data_shape), dtype=np.float32)
        if len(data_shape)>1:
            count=[0,0,0,0,0,0,0,0]
            print("I understand this is a VDS file.")          
            for frame in f[h5_data_path][starting_frame:starting_frame+n_frames]:
                for panel_id in range(data_shape[0]):
                    panel_data = np.array(frame[panel_id,:], dtype=np.int32)
                    # Skip lost packets
                    if not skip_lost_panel(panel_data, args.lost_flag):
                        acc_data[0,panel_id,:]+=panel_data
                        count[panel_id]+=1

            for panel_id in range(data_shape[0]):
                acc_data[0,panel_id,:]/=count[panel_id]               
        else:
            count=0
            for frame in f[h5_data_path][starting_frame:starting_frame+n_frames]:
                acc_data+=frame
                count+=1
            acc_data/=count

    if args.apply_exponential:
        acc_data=np.exp(acc_data)

    if args.mask_less_than is not None:
        acc_data[np.where(acc_data<args.mask_less_than)]=0
    
    if args.mask_greater_than is not None:
        acc_data[np.where(acc_data>args.mask_greater_than)]=0
        print("hi")

    with h5py.File(args.output, "w") as f:
        f.create_dataset(f"{h5_data_path}", data=(acc_data).astype(np.int32))


if __name__ == "__main__":
    main()
