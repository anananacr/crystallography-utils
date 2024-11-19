#!/bin/sh

#SBATCH --partition=upex,allcpu
#SBATCH --time=2-00:00:00
#SBATCH --requeue
#SBATCH --nodes=1
#SBATCH --mincpus=64
#SBATCH --mem=10G
#SBATCH --nice=100
#SBATCH --job-name  none
#SBATCH --output   /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/none-%N-%j.out
#SBATCH --error   /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/none-%N-%j.err

source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0.11.0
ROOT=/gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria
INPUT=$1
OUTPUT=$2

rm ${ROOT}/streams/${OUTPUT}

command="indexamajig -i ${ROOT}/lists/${INPUT} -o  ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/jf_4m_vds_8396_v1_shift.geom --indexing=none"
#command="indexamajig -i ${ROOT}/lists/${INPUT} -o  ${ROOT}/streams/${OUTPUT} -g ${ROOT}/geoms/eiger500k-refined-fakp.geom --peaks=peakfinder8 --indexing=none"
command="$command -j 64 --peaks=peakfinder8 --threshold=200 --min-snr=5 --min-pix-count=3 --max-pix-count=200 --min-res=100 --max-res=1665 --min-peaks=10 --int-radius=3,4,5 --local-bg-radius=4"
#command="$command -j 64 --peaks=zaef --threshold=100 --min-snr=5 --min-squared-gradient=100000 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=2 --int-radius=8,10,12"
command="$command --copy-header=/entry_1/instrument_1/refined_center_flag --copy-header=/entry_1/instrument_1/hit --copy-header=/entry_1/instrument_1/pre_centering_flag"

$command


