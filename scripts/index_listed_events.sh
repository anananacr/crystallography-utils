#!/bin/sh

INPUT=$1
OUTPUT=$2
START=$3
END=$4
ROOT=/asap3/petra3/gpfs/p09/2023/data/11019088/processed/rodria

for i in $(seq $START 1 $END); do
    #if [ "$i" -le 9 ]; then
    #    LIST_NAME=${INPUT}.lst00${i}
    #elif [ "$i" -ge 10 ] && [ "$i" -le 99 ]; then
    #    LIST_NAME=${INPUT}.lst0${i}
    #else
    #    LIST_NAME=${INPUT}.lst${i}
    #fi
    
    LABEL=index_${i}
    JNAME="index_${i}"
    NAME="index_${i}_${INPUT}"
    SLURMFILE="${NAME}_${INPUT}.sh"
    echo "#!/bin/sh" > $SLURMFILE
    echo >> $SLURMFILE
    echo "#SBATCH --partition=allcpu,upex" >> $SLURMFILE  # Set your partition here
    echo "#SBATCH --time=2-00:00:00" >> $SLURMFILE
    echo "#SBATCH --nodes=1" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "#SBATCH --chdir   $PWD" >> $SLURMFILE
    echo "#SBATCH --job-name  $JNAME" >> $SLURMFILE
    echo "#SBATCH --requeue" >> $SLURMFILE
    echo "#SBATCH --output    ${ROOT}/error/${NAME}-%N-%j.out" >> $SLURMFILE
    echo "#SBATCH --error     ${ROOT}/error/${NAME}-%N-%j.err" >> $SLURMFILE
    echo "#SBATCH --nice=100" >> $SLURMFILE
    echo "#SBATCH --mincpus=64" >> $SLURMFILE
    echo "#SBATCH --mem=20G" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "unset LD_PRELOAD" >> $SLURMFILE
    echo "source /etc/profile.d/modules.sh" >> $SLURMFILE
    echo "module purge" >> $SLURMFILE
    echo "module load maxwell crystfel" >> $SLURMFILE
    echo >> $SLURMFILE
    command="indexamajig -i ${ROOT}/lists/${INPUT}.lst${i} -o ${ROOT}/streams/${OUTPUT}.stream${i} -j 64 -g ${ROOT}/geoms/eiger500k-refined-fakp.geom --peaks=peakfinder8 --threshold=20 --min-snr=5 --local-bg-radius=3 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=10 --int-radius=3,4,5 --copy-header=/entry/data/raw_file_id --copy-header=/entry/shots/refined_center_flag --xgandalf-min-lattice-vector-length=45.26 --tolerance=5,5,2,1.5 -p ${ROOT}/cell/fakp_si_1.cell"
    echo $command >> $SLURMFILE
    echo "chmod a+rw $PWD" >> $SLURMFILE
    sbatch $SLURMFILE 
    mv $SLURMFILE ${ROOT}/shell
done
