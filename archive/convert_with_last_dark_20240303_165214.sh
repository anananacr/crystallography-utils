#!/bin/sh

DARKS_D0=pedal_d0_20240303_165214_darks_160us.h5
DARKS_D1=pedal_d1_20240303_165214_darks_160us.h5

sbatch convert_images.sh FAKP_A12_01/run0001_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0001_160us_12_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh empty_chip_test/run0002_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh powder_240303/run0002_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh powder_240303/run0003_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_A12_01/run0002_160us_12_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G08_01/run0001_160us_12_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_02_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_03_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_04_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_06_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_07_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_08_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_09_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_10_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_11_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh FAKP_G12_01/run0001_160us_12_master_0.h5 $DARKS_D0 $DARKS_D1;