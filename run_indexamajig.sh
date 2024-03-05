#!/bin/sh
source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0.10.2
ROOT=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/scratch_cc/rodria
INPUT=$1
OUTPUT=$2

rm ${ROOT}/streams/${OUTPUT}

command="indexamajig -i ${ROOT}/lists/${INPUT} -o  ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/jungfrau-1m.geom --peaks=peakfinder8 --indexing=none"

command="$command -j 64 --threshold=0 --min-snr=4 --min-pix-count=2 --max-pix-count=200000 --min-res=0 --max-res=1200 --min-peaks=4 --int-radius=4,5,6"

$command

#--copy-header=/shift_vertical_mm --copy-header=/shift_horizonthal_mm
