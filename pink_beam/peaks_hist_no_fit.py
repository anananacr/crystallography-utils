#!/usr/bin/env python3


import sys
import time
from multiprocessing import Pool, Manager
import numpy as np
import os
#from cfelpyutils.crystfel_utils import load_crystfel_geometry
from om.lib.geometry import _read_crystfel_geometry_from_text
import matplotlib.pyplot as plt
import argparse


def process_chunk(chunk, q, detector):
    reading_reflections = False
    reading_peaks = False
    indexed = False
    peaks = []
    reflections = []
    k_peak = []
    r_peak = []

    to_ev = 1239.84193e-9

    for line in chunk.split("\n"):

        if line.startswith("  fs/px   ss/px"):
            reading_peaks = True

        elif line.startswith("End of peak list"):
            reading_peaks = False
        elif line.split(" = ")[0]=="header/float//entry_1/instrument_1/detector_shift_x_in_mm":
             shift_x = float(line.split(" = ")[-1])*1e-3
        elif line.split(" = ")[0]=="header/float//entry_1/instrument_1/detector_shift_y_in_mm":
             shift_y = float(line.split(" = ")[-1])*1e-3
        elif reading_peaks:
            s = line.split()
            fs, ss, res, intensity = (float(i) for i in s[:4])
            peaks.append([fs, ss, s[-1]])

        elif line.startswith("   h    k    l "):
            reading_reflections = True

        elif line.startswith("End of reflections"):
            reading_reflections = False

        elif reading_reflections:
            s = line.split()
            reflections.append(
                [
                    float(s[-3]),
                    float(s[-2]),
                    int(s[0]),
                    int(s[1]),
                    int(s[2]),
                    va,
                    vb,
                    vc,
                    s[-1],
                ]
            )

        elif line.startswith("astar"):
            indexed = True
            s = line.split()
            va = np.array((float(s[2]), float(s[3]), float(s[4]))) * 1e9

        elif line.startswith("bstar"):
            s = line.split()
            vb = np.array((float(s[2]), float(s[3]), float(s[4]))) * 1e9

        elif line.startswith("cstar"):
            s = line.split()
            vc = np.array((float(s[2]), float(s[3]), float(s[4]))) * 1e9

    if not indexed:
        return

    for p in peaks:
        d = 100500.0
        nr = None
        for r in reflections:
            if (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2 < d:
                nr = r
                d = (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2

        if nr and np.sqrt(d) < 3:

            h = np.linalg.norm(nr[2] * nr[5] + nr[3] * nr[6] + nr[4] * nr[7])

            panel = detector["panels"][p[-1]]
            xp = shift_x + (
                (p[0] - panel["orig_min_fs"]) * panel["fsx"]
                + (p[1] - panel["orig_min_ss"]) * panel["ssx"]
                + panel["cnx"]
            ) / panel["res"]
            yp = shift_y + (
                (p[0] - panel["orig_min_fs"]) * panel["fsy"]
                + (p[1] - panel["orig_min_ss"]) * panel["ssy"]
                + panel["cny"]
            ) / panel["res"]
            dp = panel["clen"]

            k_peak.append(
                h / np.sqrt(2 * (1 - dp / np.sqrt(dp ** 2 + xp ** 2 + yp ** 2))) * to_ev
            )
            r_peak.append(h)

    q.put((k_peak, r_peak))


from scipy.optimize import curve_fit, leastsq

def parse_args():
    parser = argparse.ArgumentParser(
        description="", usage="./peaks_hist.py stream geometry spectrum [options]"
    )
    parser.add_argument("stream", type=str, help="stream file")
    parser.add_argument("geometry", type=str, help="geometry file")
    parser.add_argument(
        "-n",
        "--nproc",
        metavar="N",
        type=int,
        default=1,
        help="run N processes in parallel, default = 1",
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_args()

    stream = args.stream
    geometry_file = args.geometry
    
    nproc = args.nproc
    label=os.path.basename(stream)
    manager = Manager()
    q = manager.Queue()

    pool = Pool(processes=nproc)
    reading_chunk = False

    geometry_txt=open(geometry_file, "r").readlines()
    detector, _, _ = _read_crystfel_geometry_from_text(text_lines=geometry_txt)

    k_peak = []
    r_peak = []
    i = 0
    with open(stream) as f:
        for line in f:
            if line.startswith("----- Begin chunk -----"):
                reading_chunk = True
                chunk = line

            elif line.startswith("----- End chunk -----"):
                reading_chunk = False
                chunk += line
                pool.apply(process_chunk, (chunk, q, detector))
                i += 1
                print("\rChunk %d" % i, end="", flush=True)
                while pool._taskqueue.qsize() > nproc:
                    while not q.empty():
                        k, r = q.get()
                        k_peak.extend(k)
                        r_peak.extend(r)
                    time.sleep(1)

            elif reading_chunk:
                chunk += line

    pool.close()
    pool.join()

    while not q.empty():
        k, r = q.get()
        k_peak.extend(k)
        r_peak.extend(r)

    np.savetxt(f"k_{label[:-7]}.dat", list(zip(k_peak, r_peak)))

    d_peak = 1e10 / np.array(r_peak)
    k_peak = np.array(k_peak)

    ax2 = plt.gca()
    ax1 = ax2.twinx()

    ax1.set_xlabel("k, eV")
    ax1.set_ylabel("Normalized intensity", color="C0")
    for tl in ax1.get_yticklabels():
        tl.set_color("C0")

    #ax1.set_ylim(0, 1.05)
    k_peak = k_peak[np.where(d_peak < 30)]
    k_peak = k_peak[np.where(k_peak < 9.2e3)]
    k_peak = k_peak[np.where(k_peak > 9.0e3)]

    y, bins, patches = ax2.hist(
        k_peak, 100, alpha=0.6, color="C2", label="Found peaks"
    )

    ax2.set_ylabel("N peaks", color="C2")
    for tl in ax2.get_yticklabels():
        tl.set_color("C2")

    x = [(bins[i] + bins[i + 1]) / 2.0 for i in range(y.shape[0])]
    ax2.set_xlim(9000,9200)
    ax2.set_xlabel("k, eV")
    plt.tight_layout()
    plt.savefig(f"{label[:-7]}.png")
    #plt.show()
