#!/bin/sh

DARKS_D0=pedal_d0_20240308_dark_fixg1_sc_1us_5.8us.h5
DARKS_D1=pedal_d1_20240308_dark_fixg1_sc_1us_5.8us.h5

sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_12_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images_burst.sh FAKP_apo_sweep_03/run0001_sc_1us_5.8us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
