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
module load maxwell crystfel/0.11.0
module load xray

#Generate event list from file above
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

    #MILLE_DIR=$STREAMDIR/mille_$NUMBER
    #mkdir $MILLE_DIR

    echo "$NAME (serial start $POS): $FILE  --->  $STREAM"

    SLURMFILE="${NAME}.sh"

    echo "#!/bin/sh" > $SLURMFILE
    echo >> $SLURMFILE

    echo "#SBATCH --partition=upex" >> $SLURMFILE  # Set your partition here
    echo "#SBATCH --time=0-10:00:00" >> $SLURMFILE
    echo "#SBATCH --nodes=1" >> $SLURMFILE
    # It may be polite to set the niceness very high (low priority) to allow other jobs through:
    echo "#SBATCH --nice=0" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "#SBATCH --mincpus=64" >> $SLURMFILE
    echo "#SBATCH --job-name  $NAME" >> $SLURMFILE
    echo "#SBATCH --output    $NAME-%N-%j.out" >> $SLURMFILE
    echo "#SBATCH --error     $NAME-%N-%j.err" >> $SLURMFILE
    #echo "#SBATCH --mail-type END" >> $SLURMFILE
    #echo "#SBATCH --mail-user $MAIL" >> $SLURMFILE
    echo >> $SLURMFILE
    echo "module purge" >> $SLURMFILE
    echo "module load maxwell crystfel/0.11.0; module load maxwell xray" >> $SLURMFILE  # Set up environment here (again) if necessary
    echo >> $SLURMFILE

    command="indexamajig -i $FILE -o $STREAMDIR/$STREAM --serial-start=$POS"
    command="$command -j 64 -g $GEOM"
    command="$command --peaks=peakfinder8 --threshold=50 --min-snr=5 --local-bg-radius=3 --min-pix-count=2 --max-pix-count=30 --min-res=100 --max-res=1700 --min-peaks=10 --int-radius=4,5,6 --copy-header=/entry_1/instrument_1/data_1/pre_centering_flag --copy-header=/entry_1/instrument_1/data_1/hit --copy-header=/entry_1/instrument_1/data_1/refined_center_flag  --copy-header=/entry_1/memoryCell --copy-header=/entry_1/trainId --no-non-hits-in-stream"
    #command="$command --peaks=peakfinder8 --threshold=50 --min-snr=5 --local-bg-radius=3 --min-pix-count=2 --max-pix-count=30 --min-res=100 --max-res=1700 --min-peaks=10 --int-radius=3,4,5 --copy-header=/entry_1/instrument_1/pre_centering_flag --copy-header=/entry_1/instrument_1/hit --copy-header=/entry_1/instrument_1/refined_center_flag  --copy-header=/entry_1/memoryCell --copy-header=/entry_1/trainId --no-non-hits-in-stream"
    #command="$command --no-use-saturated"
    command="$command --xgandalf-grad-desc-iterations=5 "
    #command="$command --indexing=none"
    #command="$command --indexing=mosflm-latt-nocell"
    command="$command --indexing=xgandalf-nolatt-cell"
    command="$command --multi"
    #command="$command --xgandalf-min-lattice-vector-length=37.6 --xgandalf-min-lattice-vector-length=78.8 --tolerance=0.7,0.7,5,1.5"
    #command="$command  --xgandalf-grad-desc-iterations=5 --xgandalf-sampling-pitch=7 --xgandalf-max-lattice-vector-length=90.89 --xgandalf-min-lattice-vector-length=45.26 --xgandalf-tolerance=0.01 --multi"
    #command="$command  --xgandalf-grad-desc-iterations=4 --xgandalf-sampling-pitch=6 --xgandalf-min-lattice-vector-length=45.26 --xgandalf-max-lattice-vector-length=91.62 --xgandalf-tolerance=0.01 --multi"
    #command="$command --mille --mille-dir=$MILLE_DIR"
    command="$command -p /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/cell/fakp_mosflm.cell"
    #command="$command -p /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/cell/fakp_latt.cell"
    #command="$command -p /gpfs/exfel/exp/SPB/202425/p008396/scratch/rodria/cell/lyso.cell"
    #command="$command -p /asap3/petra3/gpfs/p09/2023/data/11019088/processed/rodria/cell/fakp_sweep_2.cell"
    #command="$command -p /asap3/petra3/gpfs/p09/2023/data/11019088/processed/rodria/cell/lyso.cell"
    #command="$command -p /asap3/petra3/gpfs/p09/2023/data/11019088/processed/rodria/cell/fakp_latt.cell"

    echo $command >> $SLURMFILE

    sbatch $SLURMFILE
done

