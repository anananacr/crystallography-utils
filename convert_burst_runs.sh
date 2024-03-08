#!/bin/sh

DARKS_D0=pedal_d0_20240307_184151_darks_sc_6.8us_0.0us.h5
DARKS_D1=pedal_d1_20240307_184151_darks_sc_6.8us_0.0us.h5

sbatch convert_images_burst.sh lyso_04_sweep/run0001_sc_6.8us_0.0us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh lyso_04_sweep/run0002_sc_6.8us_0.0us_12_master_0.h5 $DARKS_D0 $DARKS_D1;