#!/bin/sh

# Split a large indexing job into many small tasks and submit using SLURM

# ./turbo-index my-files.lst label my.geom /location/for/streams

# Copyright © 2016-2020 Deutsches Elektronen-Synchrotron DESY,
#                       a research centre of the Helmholtz Association.
#
# Authors:
#   2016      Steve Aplin <steve.aplin@desy.de>
#   2016-2017 Thomas White <taw@physics.org>

SPLIT=10000  # Size of job chunks
#MAIL=you@example.org  # Email address for SLURM notifications

INPUT=$1
RUN=$2
GEOM=$3
STREAMDIR=$4

# Set up environment here if necessary
source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0-devel

# Generate event list from file above
list_events -i $INPUT -g $GEOM -o events-${RUN}.lst
if [ $? != 0 ]; then
       echo "list_events failed"
       exit 1
fi
# If you are using single-event files instead of multi-event ("CXI") ones,
# comment out the above lines and uncomment the following one:
#cp $INPUT events-${RUN}.lst

# Count total number of events
wc -l events-${RUN}.lst

# Split the events up, will create files with $SPLIT lines
split -a 3 -d -l $SPLIT events-${RUN}.lst split-events-${RUN}.lst

# Clean up
rm -f events-${RUN}.lst

# Loop over the event list files, and submit a batch job for each of them
N=0
for FILE in split-events-${RUN}.lst*; do

    mkdir /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/streams/lyso_pink_mille/mille_${N}
    # Stream file is the output of crystfel
    STREAM=`echo $FILE | sed -e "s/split-events-${RUN}.lst/${RUN}.stream/"`

    # Job name
    NAME=`echo $FILE | sed -e "s/split-events-${RUN}.lst/${RUN}-/"`

    # Job number
    NUMBER=${NAME##$RUN-}
    POS=`expr $NUMBER \* $SPLIT + 1`

    echo "$NAME (serial start $POS): $FILE  --->  $STREAM"

    SLURMFILE="${NAME}.sh"

    echo "#!/bin/sh" > $SLURMFILE
    echo >> $SLURMFILE

    echo "#SBATCH --partition=allcpu" >> $SLURMFILE  # Set your partition here
    echo "#SBATCH --time=1-00:00:00" >> $SLURMFILE
    echo "#SBATCH --nodes=1" >> $SLURMFILE
    # It may be polite to set the priority very low to allow other jobs through:
    echo "#SBATCH --nice=100" >> $SLURMFILE
    echo >> $SLURMFILE

    echo "#SBATCH --job-name  $NAME" >> $SLURMFILE
    echo "#SBATCH --output    $NAME-%N-%j.out" >> $SLURMFILE
    echo "#SBATCH --error     $NAME-%N-%j.err" >> $SLURMFILE
    #echo "#SBATCH --mail-type END" >> $SLURMFILE
    #echo "#SBATCH --mail-user $MAIL" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "module purge" >> $SLURMFILE
    echo "module load maxwell crystfel/0-devel" >> $SLURMFILE  # Set up environment here (again) if necessary
    echo >> $SLURMFILE

    command="indexamajig -i $FILE -o $STREAMDIR/$STREAM --serial-start=$POS"
    command="$command -j 64 -g $GEOM"
    command="$command --peaks=peakfinder8 --threshold=0 --min-snr=5 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=10 --int-radius=4,5,6 --copy-header=/entry/shots/detector_shift_x_in_mm -p /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/cell/lyso.cell --copy-header=/entry/shots/detector_shift_y_in_mm --copy-header=/entry/data/raw_file_id --indexing=pinkIndexer --pinkIndexer-considered-peaks-count=4 --pinkIndexer-angle-resolution=4 --pinkIndexer-refinement-type=3 --pinkIndexer-tolerance=0.065 --fix-profile-radius=0.002e9 --int-radius=5,7,9 --pinkIndexer-max-refinement-disbalance=0.5 --no-non-hits-in-stream --mille --mille-dir=/gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/streams/lyso_pink_mille/mille_${N}"
    echo $command >> $SLURMFILE

    sbatch $SLURMFILE
    N=$((N + 1))

done

