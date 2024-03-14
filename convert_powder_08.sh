#!/bin/sh

DARKS_D0=pedal_d0_20240304_022539_darks_160us.h5
DARKS_D1=pedal_d1_20240304_022539_darks_160us.h5

sbatch convert_images.sh Powder_08_215mm/run0001_160us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_08_215mm/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_08_155mm/run0001_160us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_08_155mm/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_08_100mm/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_07_100mm/run0003_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_07_100mm/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh Powder_06_100mm/run0003_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;