#!/bin/sh
## ./generate_vds.sh start_index end_index

START=$1
END=$2
ROOT=/gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria

for i in $(seq $START 1 $END); do
    if [ "$i" -le 9 ]; then
        RUN_NAME=r000${i}
    elif [ "$i" -ge 10 ] && [ "$i" -le 99 ]; then
        RUN_NAME=r00${i}
    else
        RUN_NAME=r0${i}
    fi
    
    LABEL=new_${i}
    JNAME="new_${i}"
    NAME="new_${i}_${INPUT}"
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
    echo "#SBATCH --output    /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/${NAME}-%N-%j.out" >> $SLURMFILE
    echo "#SBATCH --error     /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/${NAME}-%N-%j.err" >> $SLURMFILE
    echo "#SBATCH --nice=100" >> $SLURMFILE
    echo "#SBATCH --mincpus=4" >> $SLURMFILE
    echo "#SBATCH --mem=4G" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "unset LD_PRELOAD" >> $SLURMFILE
    echo "source /etc/profile.d/modules.sh" >> $SLURMFILE
    echo "module purge" >> $SLURMFILE
    echo "module load exfel exfel-python" >> $SLURMFILE
    echo >> $SLURMFILE
    command="extra-data-make-virtual-cxi /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/converted/${RUN_NAME} -o /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/centered_fosakp_0/${RUN_NAME}.cxi"
    echo $command >> $SLURMFILE
    echo "chmod a+rw $PWD" >> $SLURMFILE
    sbatch $SLURMFILE 
    mv $SLURMFILE ${ROOT}/shell
done
