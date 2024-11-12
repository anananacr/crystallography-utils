#!/bin/sh
#SBATCH --partition=upex
#SBATCH --time=1-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=16
#SBATCH --mem=50G
#SBATCH --nice=50

#SBATCH --job-name calib
#SBATCH --output /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/convert-%N-%j.out
#SBATCH --error /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/convert-%N-%j.err


# Convert images using jf4m_calib_fixg1.py script. Remember to set correctly paths where data and pedestals from JUNGFRAU 4M are stored.

# Written by Ana Carolina Rodrigues.
#
# Mail: ana.rodrigues@desy.de

source /etc/profile.d/modules.sh
source /gpfs/cfel/user/rodria/software/crystallography-utils-env/bin/activate

INP=$1
INDEX=$2
DARKS=darks.lst
GAIN=gain_maps.lst
BAD_PIXELS=bad_pixels.lst
BAD_PIXELS_FF=bad_pixels_ff.lst
ROOT=/gpfs/exfel/exp/SPB/202425/p008396
echo $INP

python jf_4m_calib_fixg1_par.py -p ${ROOT}/scratch/rodria/calib/${DARKS} -g  ${ROOT}/scratch/rodria/calib/${GAIN} -b ${ROOT}/scratch/rodria/calib/${BAD_PIXELS} -bf ${ROOT}/scratch/rodria/calib/${BAD_PIXELS_FF} -i ${ROOT}/raw/${INP} -o ${ROOT}/scratch/rodria/converted/${INP} -n ${INDEX};