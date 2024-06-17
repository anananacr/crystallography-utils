#!/bin/sh

#SBATCH --partition=allcpu,upex
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=64
#SBATCH --mem=10G
#SBATCH --nice=100
#SBATCH --job-name  bb
#SBATCH --output   /path/to/error/bb-%N-%j.out
#SBATCH --error   /path/to/error/bb-%N-%j.err

INPUT=$1
ROOT=/path/to

source /etc/profile.d/modules.sh
module purge
source /path/to/beambusters-env/bin/activate

command="beambusters run_centering ${ROOT}/lists/${INPUT} ${ROOT}/config/config_231222_mica_001.yaml"

echo $command
$command
 
