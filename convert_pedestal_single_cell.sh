#!/bin/sh
#
# Convert pedestal images using om_jungfrau_dark.py script from Onda monitor.
# Remember to set correctly paths where pedestals from JUNGFRAU 1M are stored.
#
# ./convert_pedestal.sh input
#./convert_pedestal.sh 231020_mica_c4_m1_001/ed_rot_step_001/231020_mica_c4_m1_001_001 step

# Written by Ana Carolina Rodrigues.
#
# Mail: ana.rodrigues@desy.de

source /home/rodria/scripts/regae/env-regae/bin/activate

INP=$1
N=$(basename $INP)
OUTPUT=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/darks
DARKS_PATH_ON_RAW=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/RAW_DATA/darks
echo $N

## convert dark file
ls ${DARKS_PATH_ON_RAW}/${INP}_d0_f0_*.h5>${OUTPUT}/pedal_d0.lst
/home/rodria/software/om_dev_regae/om/bin_src/om_jungfrau_dark.py ${OUTPUT}/pedal_d0.lst ${OUTPUT}/pedal_d0_${N}.h5;

ls ${DARKS_PATH_ON_RAW}/${INP}_d1_f0_*.h5>${OUTPUT}/pedal_d1.lst
/home/rodria/software/om_dev_regae/om/bin_src/om_jungfrau_dark.py ${OUTPUT}/pedal_d1.lst ${OUTPUT}/pedal_d1_${N}.h5;

