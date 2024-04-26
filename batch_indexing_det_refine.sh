#!/bin/sh

#SBATCH --partition=allcpu,upex
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=64
#SBATCH --mem=10G
#SBATCH --nice=100
#SBATCH --job-name  bb
#SBATCH --output   /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/error/bb-%N-%j.out
#SBATCH --error    /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/error/bb-%N-%j.err

INPUT=$1
OUTPUT=$2
ROOT=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria

source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0-devel

command="indexamajig -i ${ROOT}/lists/${INPUT} -o ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/jungfrau-1m-vertical-v1-100mm-shift.geom --peaks=peakfinder8"
command="$command -j 64 --threshold=0 --min-snr=5 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=650 --min-peaks=10 --int-radius=5,6,7 --copy-header=/entry/data/raw_file_id"
command="$command -p ${ROOT}/cell/lyso.cell "
#command="$command --indexing=mosflm"
echo $command
$command
 
