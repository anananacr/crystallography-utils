#!/bin/sh

DARKS_D0=pedal_d0_20240302_145550_darks_160us.h5
DARKS_D1=pedal_d1_20240302_145550_darks_160us.h5
sbatch convert_images.sh powder_03_70mm/run0001_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh powder_03_100mm/run0001_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh powder_03_130mm/run0001_160us_01_master_0.h5 $DARKS_D0 $DARKS_D1;

DARKS_D0=pedal_d0_20240303_074011_darks_160us.h5
DARKS_D1=pedal_d1_20240303_074011_darks_160us.h5

sbatch convert_images.sh powder_2403003/run0001_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;

DARKS_D0=pedal_d0_20240303_165214_darks_160us.h5
DARKS_D1=pedal_d1_20240303_165214_darks_160us.h5

sbatch convert_images.sh powder_240303/run0002_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;
sbatch convert_images.sh powder_240303/run0003_160us_05_master_0.h5 $DARKS_D0 $DARKS_D1;