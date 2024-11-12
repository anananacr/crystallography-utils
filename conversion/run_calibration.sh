#!/bin/bash

RUN=$1

for i in {0..11}; do
  echo "Submitting chunk file: $i"
  sbatch convert_jf_4m.sh $RUN $i
  sleep 30
done
