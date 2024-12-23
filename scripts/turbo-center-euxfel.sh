#!/bin/sh
## ./turbo-center-euxfel.sh split_list_file start_index end_index

INPUT=$1
START=$2
END=$3
ROOT=/gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria

for i in $(seq $START 1 $END); do
    if [ "$i" -le 9 ]; then
        LIST_NAME=${INPUT}.lst00${i}
    elif [ "$i" -ge 10 ] && [ "$i" -le 99 ]; then
        LIST_NAME=${INPUT}.lst0${i}
    else
        LIST_NAME=${INPUT}.lst${i}
    fi
    
    LABEL=bb_l_v6_${i}
    JNAME="bb_l_v6_${i}"
    NAME="bb_l_v6_${i}_${INPUT}"
    SLURMFILE="${NAME}_${INPUT}.sh"
    echo "#!/bin/sh" > $SLURMFILE
    echo >> $SLURMFILE
    echo "#SBATCH --partition=cfel-cdi" >> $SLURMFILE  # Set your partition here
    echo "#SBATCH --time=4-00:00:00" >> $SLURMFILE
    echo "#SBATCH --nodes=1" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "#SBATCH --chdir   $PWD" >> $SLURMFILE
    echo "#SBATCH --job-name  $JNAME" >> $SLURMFILE
    echo "#SBATCH --requeue" >> $SLURMFILE
    echo "#SBATCH --output    /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/${NAME}-%N-%j.out" >> $SLURMFILE
    echo "#SBATCH --error     /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/error/${NAME}-%N-%j.err" >> $SLURMFILE
    echo "#SBATCH --nice=100" >> $SLURMFILE
    echo "#SBATCH --mincpus=128" >> $SLURMFILE
    echo "#SBATCH --mem=20G" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "unset LD_PRELOAD" >> $SLURMFILE
    echo "source /etc/profile.d/modules.sh" >> $SLURMFILE
    echo "module purge" >> $SLURMFILE
    echo "source /gpfs/cfel/user/rodria/software/beambusters-env/bin/activate" >> $SLURMFILE
    echo >> $SLURMFILE
    command="beambusters run_centering ${ROOT}/lists/${LIST_NAME} ${ROOT}/config/config_lyso_0.yaml"
    echo $command >> $SLURMFILE
    echo "chmod a+rw $PWD" >> $SLURMFILE
    sbatch $SLURMFILE 
    mv $SLURMFILE ${ROOT}/shell
done
