#!/bin/sh
source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0.11.0
ROOT=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria
INPUT=$1
OUTPUT=$2

rm ${ROOT}/streams/${OUTPUT}

command="indexamajig -i ${ROOT}/lists/${INPUT} -o  ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/jungfrau-1m-vertical-v2-100mm-shift.geom --peaks=peakfinder8 --indexing=none"
command="$command -j 64 --threshold=100 --min-snr=5 --min-pix-count=4 --max-pix-count=200 --local-bg-radius=5 --min-res=0 --max-res=1200 --min-peaks=20"
command="$command --copy-header=/entry/shots/detector_shift_x_in_mm --copy-header=/entry/shots/detector_shift_y_in_mm --copy-header=/entry/shots/refined_center_flag --copy-header=/entry/data/raw_file_id "

$command


