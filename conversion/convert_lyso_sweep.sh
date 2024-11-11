#!/bin/sh

DARKS_D0=pedal_d0_6.75us_6us_1.h5
DARKS_D1=pedal_d1_6.75us_6us_1.h5

sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_07_sweep/run0004_sc_6.8us_3.3us_12_master_0.h5 $DARKS_D0 $DARKS_D1;
