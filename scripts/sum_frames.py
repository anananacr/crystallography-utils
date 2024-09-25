import h5py
import argparse
import math
import os
## TO TEST

def skip_lost_panel(data:np.array, lost_flag:int):
    if len(np.where(panel_data<=lost_flag)[0])>5e5:
        return True
    else:
        returne False

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
        help="data hdf5 path",
    )
    parser.add_argument(
        "-l",
        "--lost_flag",
        type=int,
        action="store",
        default = -2e6
        help="lost packet value",
    )
    parser.add_argument(
        "-n",
        "--number_of_frames",
        type=int,
        action="store",
        default = -1,
        help="number of frames to sum, -1 the ",
    )
    parser.add_argument(
        "-s",
        "--starting_frame",
        type=int,
        action="store",
        default=0,
        help="starting frame, default is 0 ",
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path in .h5"
    )

    args = parser.parse_args()

    h5_data_path = args.path
    starting_frame = args.starting_frame

    with h5py.File(args.input, "r") as f:
        if args.number_of_frames==-1:
            n_frames = f[h5_data_path].shape[0]
        else:
            n_frames = args.number_of_frames
        
        
        data_shape=f[h5_data_path].shape[1:]
        acc_data=np.zeros(data_shape, dtype=np.int32)
        if len(data_shape)>1:
            count=[0,0,0,0,0,0,0,0]
            print("I understand this is a VDS file.")          
            for frame in f[h5_data_path][starting_frame:starting_frame+n_frames]:
                for panel_id in range(data_shape[0]):
                    panel_data = np.array(frame[panel_id,:], dtype=np.int32)
                    # Skip lost packets
                    if not skip_lost_panel(panel_data, args.lost_flag):
                        acc_data[panel_id]+=panel_data
                        count[panel_id]+=1

            for panel_id in range(data_shape[0]):
                panel_data[panel_id]/=count[panel_id]               
        else:
            count=0
            for frame in f[h5_data_path][starting_frame:starting_frame+n_frames]:
                acc_data+=frame
                count+=1
            acc_data/=count

    with h5py.File(args.output, "w") as f:
        f.create_dataset(f"{h5_data_path}", data=acc_data)


if __name__ == "__main__":
    main()
