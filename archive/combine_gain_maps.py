
import argparse
import glob
import numpy as np
import h5py

def main():
    parser = argparse.ArgumentParser(
        description="Convert JUNGFRAU 1M H5 images collected at REGAE for rotational data step/fly scan and return images in rotation sequence according tro the file index."
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

    args = parser.parse_args()
    gain_d0_filenames=[]
    gain_d1_filenames=[]

    for n in range(16):
        gain_d0_pattern = args.gain1+"{:02d}".format(n)+"*"
        gain_d0_filenames.append(glob.glob(f"{gain_d0_pattern}")[0])
        gain_d1_pattern = args.gain2+"{:02d}".format(n)+"*"
        gain_d1_filenames.append(glob.glob(f"{gain_d1_pattern}")[0])

    num_panels = 2
    gain = np.ndarray((16, 3, 512 * num_panels, 1024), dtype=np.float64)
    panel_id: int
    for n in range(len(gain_d0_filenames)):
        gain_filenames=[gain_d0_filenames[n], gain_d1_filenames[n]]
        print(gain_filenames)
        for panel_id in range(num_panels):
            gain_file: BinaryIO = open(gain_filenames[panel_id], "rb")
            gain_mode: int
            for gain_mode in range(3):
                gain[n, gain_mode, 512 * panel_id : 512 * (panel_id + 1), :] = np.fromfile(
                    gain_file, dtype=np.float64, count=1024 * 512
                ).reshape(512, 1024)
            gain_file.close()

    dark_filenames = [args.pedestal1, args.pedestal2]
    dark = np.ndarray((3, 512 * num_panels, 1024), dtype=np.float32)

    for panel_id in range(num_panels):
        dark_file: Any = h5py.File(dark_filenames[panel_id], "r")
        gain_mode: int
        for gain_mode in range(3):
            dark[gain_mode, 512 * panel_id : 512 * (panel_id + 1), :] = dark_file[
                "gain%d" % gain_mode
            ][:]
        dark_file.close()
    
    f = h5py.File('/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/scratch_cc/rodria/gains_sc_M524_M525.h5', 'w')
    f.create_dataset('/gain_maps', data=gain.astype(np.float64))
    f.create_dataset('/darks', data=dark.astype(np.float32))
    f.close()


if __name__ == "__main__":
    main()
