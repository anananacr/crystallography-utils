#!/bin/sh
source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0.11.0
ROOT=/asap3/petra3/gpfs/p09/2023/data/11019088/processed/rodria
INPUT=$1
OUTPUT=$2

rm ${ROOT}/streams/${OUTPUT}

#command="indexamajig -i ${ROOT}/lists/${INPUT} -o  ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/eiger500k.geom --peaks=peakfinder8 --indexing=none"
command="indexamajig -i ${ROOT}/lists/${INPUT} -o  ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/eiger500k-refined-fakp.geom --peaks=peakfinder8 --indexing=none"
#command="$command -j 64 --threshold=30 --min-snr=3.5 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=10 --int-radius=3,4,5"
command="$command -j 64 --threshold=30 --min-snr=3.5 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=10 --int-radius=3,4,5"
command="$command --copy-header=/entry/shots/detector_shift_x_in_mm --copy-header=/entry/shots/detector_shift_y_in_mm --copy-header=/entry/shots/refined_center_flag --copy-header=/entry/data/raw_file_id "

$command


