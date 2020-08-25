#!/bin/bash

#SBATCH -p defq
#SBATCH -J to_vrt-spfeas
#SBATCH --export=NONE
#SBATCH -t 8-00:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=NetID@gwu.edu


export PATH="/usr/bin:$PATH"
source activate myenv


###############################################################################
# CREATE VRT AND CONTEXTUAL FEATURES
# 1-1_spfeas_create-vrt-spfeas.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script takes imagery (multiple) and combines them together to form
# one single image as a VRT file. The first argument is the output .vrt file,
# the remaining arguments are the input TIFs (number depends on how many input
# TIFs you have).

# This script subsequently runs contextual features on each image. Change the
# filepath after -i (should be the VRT) and after -o (should be a folder;
# it will create the folder when running so no need to create beforehand).

# **Once complete, do not move or delete anything within each output folder,
# or else it will mess up the subsequent code. This is how the VRT works.**
###############################################################################


# Create VRT
# Put in outputs/vrt
gdalbuildvrt Accra.vrt ../../data/Accra_Sentinel2.tif

# Create contextual features
# Output folders will be created automatically
spfeas -i Accra.vrt -o ../features/Accra_fourier --vis-order rgb --block 1 --scales 31 51 71 --tr fourier
spfeas -i Accra.vrt -o ../features/Accra_gabor --vis-order rgb --block 1 --scales 3 5 7 --tr gabor
spfeas -i Accra.vrt -o ../features/Accra_hog --vis-order rgb --block 1 --scales 3 5 7 --tr hog
spfeas -i Accra.vrt -o ../features/Accra_lac --vis-order rgb --block 1 --scales 3 5 7 --tr lac
spfeas -i Accra.vrt -o ../features/Accra_lbpm --vis-order rgb --block 1 --scales 3 5 7 --tr lbpm
spfeas -i Accra.vrt -o ../features/Accra_lsr --vis-order rgb --block 1 --scales 31 51 71 --tr lsr
spfeas -i Accra.vrt -o ../features/Accra_mean --block 1 --scales 3 5 7 --tr mean
spfeas -i Accra.vrt -o ../features/Accra_ndvi --vis-order rgb --block 1 --scales 3 5 7 --tr ndvi
spfeas -i Accra.vrt -o ../features/Accra_orb --vis-order rgb --block 1 --scales 31 51 71 --tr orb
spfeas -i Accra.vrt -o ../features/Accra_pantex --vis-order rgb --block 1 --scales 3 5 7 --tr pantex
spfeas -i Accra.vrt -o ../features/Accra_sfs --vis-order rgb --block 1 --scales 31 51 71 --tr sfs
