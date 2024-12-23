#!/bin/sh
#SBATCH --partition=allcpu,upex
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mem=8G
#SBATCH --nice=100

#SBATCH --job-name  convert_jf
#SBATCH --output /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/scratch_cc/rodria/error/convert-%N-%j.out
#SBATCH --error /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/scratch_cc/rodria/error/convert-%N-%j.err


# Convert images using convert_all.py script. Remember to set correctly paths where data and pedestals from JUNGFRAU 1M are stored.

# Written by Ana Carolina Rodrigues.
#
# Mail: ana.rodrigues@desy.de

source /etc/profile.d/modules.sh
source /gpfs/cfel/user/rodria/software/crystallography-utils-env/bin/activate

INP=$1
DARKS_D0=$2
DARKS_D1=$3
GAIN_D0=gainMaps_M524_sc
GAIN_D1=gainMaps_M525_sc
ROOT=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/converted
echo $INP

python convert_images_burst_fixg1_filter_blank.py -p1 ${ROOT}/../darks/${DARKS_D0} -p2 ${ROOT}/../darks/${DARKS_D1} -g1 ${ROOT}/../darks/${GAIN_D0} -g2 ${ROOT}/../darks/${GAIN_D1} -i ${ROOT}/../../RAW_DATA/${INP} -o ${ROOT}/${INP};