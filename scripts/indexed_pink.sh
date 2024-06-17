#!/bin/sh

INPUT=$1
OUTPUT=$2
START=$3
END=$4
ROOT=/path/to/

for i in $(seq $START 1 $END); do
    if [ "$i" -le 9 ]; then
        LIST_NAME=${INPUT}.lst0${i}
    fi
    #elif [ "$i" -ge 10 ] && [ "$i" -le 99 ]; then
    #    LIST_NAME=${INPUT}.lst0${i}
    #else
    #    LIST_NAME=${INPUT}.lst${i}
    
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
    command="indexamajig -i ${ROOT}/lists/${INPUT}.lst0${i} -o ${ROOT}/streams/${OUTPUT}.stream${i} -j 64 -g ${ROOT}/geoms/JF_regae.geom --peaks=peakfinder8 --threshold=10 --min-snr=5 --local-bg-radius=6 --min-pix-count=3 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=10 --int-radius=9,12,14 --copy-header=/entry/data/raw_file_id --copy-header=/entry/shots/refined_center_flag -p ${ROOT}/cell/mica.cell --indexing=pinkindexer --no-retry --pinkIndexer-reflection-radius=0.02 --pinkIndexer-tolerance=0.06 --pinkIndexer-max-refinement-disbalance=2 --pinkIndexer-refinement-type=3 --camera-length-estimate=4.878"
    echo $command >> $SLURMFILE
    echo "chmod a+rw $PWD" >> $SLURMFILE
    sbatch $SLURMFILE 
    mv $SLURMFILE ${ROOT}/shell
done
