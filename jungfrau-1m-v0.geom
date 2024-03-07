; Manually optimized with hdfsee
; CrystFEL geometry file
; Detector Jungfrau 1M (PSI)
; Technical description https://www.psi.ch/en/lxn/jungfrau
; Geometry file written by Ana Carolina Rodrigues
; Version from 05.03.2024
; Based on O. Yevanof geometry file for Jungfrau 1M in /asap3/fs-bmx/gpfs/regae/2023/data/11018148/scratch_cc/yefanov/geom/JF_regae_v4.geom

adu_per_eV = 0.000066  ; 42 adu/keV for highest gain mode
clen = 0.0836
photon_energy = 15000
res = 13333.33
;max_adu = 7500

;mask_file = /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/masks/merged_mask.h5
;mask = /data/data
;mask_good = 0x01
;mask_bad = 0x00

mask0_file = /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/masks/mask_edges.h5
mask0_data = /data/data
mask0_goodbits = 0x01
mask0_badbits = 0x00

mask1_file = /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/masks/mask_asic.h5
mask1_data = /data/data
mask1_goodbits= 0x01
mask1_badbits = 0x00

mask2_file = /gpfs/cfel/group/cxi/scratch/2021/ESRF-2024-Meents-Mar-ID09/processed/rodria/masks/mask_beamstop.h5
mask2_data = /data/data
mask2_goodbits = 0x01
mask2_badbits = 0x00

data = /entry/data/data
dim0 = %
dim1 = ss
dim2 = fs

rigid_group_p1 = p1a1,p1a2,p1a3,p1a4,p1a5,p1a6,p1a7,p1a8
rigid_group_p2 = p2a1,p2a2,p2a3,p2a4,p2a5,p2a6,p2a7,p2a8
rigid_group_collection_det = p2,p1

p2a1/corner_x = 43.5
p2a1/corner_y = 519
p2a1/fs = +0.000000x -1.000000y
p2a1/ss = +1.000000x +0.000000y
p2a1/min_fs = 0
p2a1/max_fs = 255
p2a1/min_ss = 512
p2a1/max_ss = 767

p2a2/corner_x = 43.5
p2a2/corner_y = 261.5
p2a2/fs = +0.000000x -1.000000y
p2a2/ss = +1.000000x +0.000000y
p2a2/min_fs = 256
p2a2/max_fs = 511
p2a2/min_ss = 512
p2a2/max_ss = 767

p2a3/corner_x = 43.5
p2a3/corner_y = 3.5
p2a3/fs = +0.000628x -1.000000y
p2a3/ss = +1.000000x -0.000628y
p2a3/min_fs = 512
p2a3/max_fs = 767
p2a3/min_ss = 512
p2a3/max_ss = 767

p2a4/corner_x = 43.5
p2a4/corner_y = -253.5
p2a4/fs = +0.000000x -1.000000y
p2a4/ss = +1.000000x +0.000000y
p2a4/min_fs = 768
p2a4/max_fs = 1023
p2a4/min_ss = 512
p2a4/max_ss = 767

p2a5/corner_x = 301.5
p2a5/corner_y = 519
p2a5/fs = -0.000628x -1.000000y
p2a5/ss = +1.000000x +0.000628y
p2a5/min_fs = 0
p2a5/max_fs = 255
p2a5/min_ss = 768
p2a5/max_ss = 1023

p2a6/corner_x = 301.5
p2a6/corner_y = 261.5
p2a6/fs = +0.000000x -1.000000y
p2a6/ss = +1.000000x +0.000000y
p2a6/min_fs = 256
p2a6/max_fs = 511
p2a6/min_ss = 768
p2a6/max_ss = 1023

p2a7/corner_x = 301.5
p2a7/corner_y = 3.5
p2a7/fs = +0.000000x -1.000000y
p2a7/ss = +1.000000x +0.000000y
p2a7/min_fs = 512
p2a7/max_fs = 767
p2a7/min_ss = 768
p2a7/max_ss = 1023

p2a8/corner_x = 301.5
p2a8/corner_y = -253.5
p2a8/fs = +0.000000x -1.000000y
p2a8/ss = +1.000000x +0.000000y
p2a8/min_fs = 768
p2a8/max_fs = 1023
p2a8/min_ss = 768
p2a8/max_ss = 1023

p1a1/corner_x = -514.5
p1a1/corner_y = 518
p1a1/fs = +0.000000x -1.000000y
p1a1/ss = +1.000000x +0.000000y
p1a1/min_fs = 0
p1a1/max_fs = 255
p1a1/min_ss = 0
p1a1/max_ss = 255

p1a2/corner_x = -514.5
p1a2/corner_y = 260.5
p1a2/fs = +0.000000x -1.000000y
p1a2/ss = +1.000000x +0.000000y
p1a2/min_fs = 256
p1a2/max_fs = 511
p1a2/min_ss = 0
p1a2/max_ss = 255

p1a3/corner_x = -514.5
p1a3/corner_y = 2.5
p1a3/fs = +0.000000x -1.000000y
p1a3/ss = +1.000000x +0.000000y
p1a3/min_fs = 512
p1a3/max_fs = 767
p1a3/min_ss = 0
p1a3/max_ss = 255

p1a4/corner_x = -514.5
p1a4/corner_y = -254.5
p1a4/fs = +0.000000x -1.000000y
p1a4/ss = +1.000000x +0.000000y
p1a4/min_fs = 768
p1a4/max_fs = 1023
p1a4/min_ss = 0
p1a4/max_ss = 255

p1a5/corner_x = -257
p1a5/corner_y = 518
p1a5/fs = +0.000000x -1.000000y
p1a5/ss = +1.000000x +0.000000y
p1a5/min_fs = 0
p1a5/max_fs = 255
p1a5/min_ss = 256
p1a5/max_ss = 511

p1a6/corner_x = -257
p1a6/corner_y = 260.5
p1a6/fs = +0.000000x -1.000000y
p1a6/ss = +1.000000x +0.000000y
p1a6/min_fs = 256
p1a6/max_fs = 511
p1a6/min_ss = 256
p1a6/max_ss = 511

p1a7/corner_x = -257
p1a7/corner_y = 2.5
p1a7/fs = +0.000000x -1.000000y
p1a7/ss = +1.000000x +0.000000y
p1a7/min_fs = 512
p1a7/max_fs = 767
p1a7/min_ss = 256
p1a7/max_ss = 511

p1a8/corner_x = -257
p1a8/corner_y = -254.5
p1a8/fs = +0.000000x -1.000000y
p1a8/ss = +1.000000x +0.000000y
p1a8/min_fs = 768
p1a8/max_fs = 1023
p1a8/min_ss = 256
p1a8/max_ss = 511
