#!/bin/sh

# Split a large indexing job into many small tasks and submit using SLURM

# ./turbo-index my-files.lst label my.geom /location/for/streams

# Copyright © 2016-2020 Deutsches Elektronen-Synchrotron DESY,
#                       a research centre of the Helmholtz Association.
#
# Authors:
#   2016      Steve Aplin <steve.aplin@desy.de>
#   2016-2017 Thomas White <taw@physics.org>

SPLIT=1000  # Size of job chunks
#MAIL=you@example.org  # Email address for SLURM notifications

INPUT=$1
RUN=$2
GEOM=$3
STREAMDIR=$4

# Set up environment here if necessary
source /etc/profile.d/modules.sh
module purge
module load maxwell crystfel/0.10.2
module load xray

# Generate event list from file above
#list_events -i $INPUT -g $GEOM -o events-${RUN}.lst
#if [ $? != 0 ]; then
#       echo "list_events failed"
#       exit 1
#fi
# If you are using single-event files instead of multi-event ("CXI") ones,
# comment out the above lines and uncomment the following one:
cp $INPUT events-${RUN}.lst

# Count total number of events
wc -l events-${RUN}.lst

# Split the events up, will create files with $SPLIT lines
split -a 3 -d -l $SPLIT events-${RUN}.lst split-events-${RUN}.lst

# Clean up
rm -f events-${RUN}.lst

# Loop over the event list files, and submit a batch job for each of them
for FILE in split-events-${RUN}.lst*; do
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
    echo "#SBATCH --time=2-00:00:00" >> $SLURMFILE
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
    echo "module load maxwell crystfel/0.11.0" >> $SLURMFILE  # Set up environment here (again) if necessary
    echo "module load xray" >> $SLURMFILE
    echo >> $SLURMFILE

    command="indexamajig -i $FILE -o $STREAMDIR/$STREAM --serial-start=$POS"
    command="$command -j 64 -g $GEOM"
    command="$command --peaks=peakfinder8 --threshold=0 --min-snr=5 --local-bg-radius=3 --min-pix-count=2 --max-pix-count=200 --min-res=0 --max-res=1200 --min-peaks=10 --int-radius=4,6,7 --copy-header=/entry/data/raw_file_id "
    command="$command --no-retry --indexing=pinkIndexer --pinkIndexer-considered-peaks-count=4 --no-check-peaks --no-refine --no-check-cell --pinkIndexer-angle-resolution=4 --pinkIndexer-refinement-type=3 --pinkIndexer-tolerance=0.04 --fix-profile-radius=0.002e9 --pinkIndexer-max-refinement-disbalance=0.4 --no-non-hits-in-stream --camera-length-estimate=0.0513"
    command="$command -p /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/cell/lyso.cell"
    echo $command >> $SLURMFILE

    sbatch $SLURMFILE
done

