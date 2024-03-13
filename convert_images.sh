#!/bin/sh
#SBATCH --partition=allcpu,upex
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mem=8G

#SBATCH --job-name  convert_jf
#SBATCH --output /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/scratch_cc/rodria/error/convert-%N-%j.out
#SBATCH --error /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/scratch_cc/rodria/error/convert-%N-%j.err


# Convert images using convert_all.py script. Remember to set correctly paths where data and pedestals from JUNGFRAU 1M are stored.
# Enable H5 data to be converted in step-wise manner, using start and end frame number arguments,  dividing it in smaller jobs.

# ./convert_step.sh 231020_mos_c3_ms_001/ed_rot_step_003/231020_mos_c3_ms_001_003 step 0 12999

# Written by Ana Carolina Rodrigues.
#
# Mail: ana.rodrigues@desy.de

source /etc/profile.d/modules.sh
source /home/rodria/scripts/regae/env-regae/bin/activate

INP=$1
DARKS_D0=$2
DARKS_D1=$3
ROOT=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/converted
echo $INP

python3 convert_images.py -p1 ${ROOT}/../darks/${DARKS_D0} -p2 ${ROOT}/../darks/${DARKS_D1} -g1 ${ROOT}/../darks/gainMaps_M524_sc00_2022-05-20.bin -g2 ${ROOT}/../darks/gainMaps_M525_sc00_2022-05-20.bin -i ${ROOT}/../../RAW_DATA/${INP} -o ${ROOT}/${INP};