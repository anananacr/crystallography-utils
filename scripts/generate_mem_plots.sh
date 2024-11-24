#!/bin/sh

for i in {0..15}; do
  ./detector_center_shift_memory.py ../../streams/fosakp_sweep/fosakp.stream ${i}
done