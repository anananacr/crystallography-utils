#!/bin/sh

#SBATCH --partition=allcpu
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=20
#SBATCH --mem=4G
#SBATCH --nice=100
#SBATCH --job-name  batch_sum
#SBATCH --output   /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/sum-%N-%j.out
#SBATCH --error   /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/sum-%N-%j.err

INPUT=$1
OUTPUT=$2
N=$3
H5_PATH=$4
ROOT=/gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria

source /etc/profile.d/modules.sh
module purge
source /gpfs/cfel/user/rodria/software/crystallography-utils-env/bin/activate

#command="python ${ROOT}/crystallography-utils/scripts/sum_frames.py -i ${ROOT}/centered/${INPUT} -o ${ROOT}/powder/${OUTPUT} -n ${N} -p ${H5_PATH} -lt 0 -gt 1000 -e True"
command="python ${ROOT}/crystallography-utils/scripts/sum_frames.py -i ${ROOT}/centered/${INPUT} -o ${ROOT}/powder/${OUTPUT} -n ${N} -p ${H5_PATH}"

echo $command
$command