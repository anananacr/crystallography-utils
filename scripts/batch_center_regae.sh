#!/bin/sh

#SBATCH --partition=allcpu,upex
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=64
#SBATCH --mem=10G
#SBATCH --nice=100
#SBATCH --job-name  bb
#SBATCH --output   /asap3/fs-bmx/gpfs/regae/2023/data/11018148/processed/rodria/error/bb-%N-%j.out
#SBATCH --error    /asap3/fs-bmx/gpfs/regae/2023/data/11018148/processed/rodria/error/bb-%N-%j.err
ROOT=/asap3/fs-bmx/gpfs/regae/2023/data/11018148/processed/rodria/
source /etc/profile.d/modules.sh
source /home/rodria/software/beambusters-dev-env/bin/activate
module purge
module load maxwell crystfel/0-devel
python /home/rodria/scripts/beambusters/beambusters/center_data.py $ROOT/lists/231221_c4_tas_b05_001_merged.lst config_regae.yaml