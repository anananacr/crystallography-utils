#!/bin/sh

#SBATCH --partition=partition
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=64
#SBATCH --mem=10G
#SBATCH --nice=100
#SBATCH --job-name  bb
#SBATCH --output   /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/bb-%N-%j.out
#SBATCH --error   /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/bb-%N-%j.err

INPUT=$1
PATH=$2
OUTPUT=$3
ROOT=/gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria

source /etc/profile.d/modules.sh
module purge
source /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/crystallography-utils-env/bin/activate

command="python ${ROOT}/crystallography-utils/scripts/sum_frames.py -i ${ROOT}/centered/${INPUT} -p ${PATH}-o ${ROOT}/powder/${OUTPUT}"

echo $command
$command