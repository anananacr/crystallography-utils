#!/bin/sh

DARKS_D0=pedal_d0_20240307_184151_darks_sc_6.8us_0.0us.h5
DARKS_D1=pedal_d1_20240307_184151_darks_sc_6.8us_0.0us.h5

sbatch convert_images_burst.sh lyso_04_sweep/run0001_sc_6.8us_0.0us_01_master_0.h5 $DARKS_D0 $DARKS_D1;