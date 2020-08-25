#!/bin/bash

#SBATCH -p defq
#SBATCH -J to_bds
#SBATCH --export=NONE
#SBATCH -t 8-00:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=NetID@gwu.edu


export PATH="/usr/bin:$PATH"
source activate myenv


###############################################################################
# CREATE BANDS FROM SPFEAS
# 1-2b_spfeas_to-bands.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script takes the VRT files (the output of spfeas) and extracts the VRT
# band-by-band, assigning each band according to its output name. The order of
# outputs is determined from the spfeas package.

# The commands from this script should be copied from the text file produced
# by 1-2a_spfeas_create-bands.py.
###############################################################################


# FOURIER
# scale: 31, output: mean
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_fourier/Accra__BD1_BK1_SC31-51-71_TRfourier.vrt ../outputs/band/fourier/fourier_sc31_mean.tif

# scale: 31, output: variance
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_fourier/Accra__BD1_BK1_SC31-51-71_TRfourier.vrt ../outputs/band/fourier/fourier_sc31_variance.tif

# scale: 51, output: mean
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_fourier/Accra__BD1_BK1_SC31-51-71_TRfourier.vrt ../outputs/band/fourier/fourier_sc51_mean.tif

# scale: 51, output: variance
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_fourier/Accra__BD1_BK1_SC31-51-71_TRfourier.vrt ../outputs/band/fourier/fourier_sc51_variance.tif

# scale: 71, output: mean
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_fourier/Accra__BD1_BK1_SC31-51-71_TRfourier.vrt ../outputs/band/fourier/fourier_sc71_mean.tif

# scale: 71, output: variance
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_fourier/Accra__BD1_BK1_SC31-51-71_TRfourier.vrt ../outputs/band/fourier/fourier_sc71_variance.tif




############################


# GABOR
# scale: 3, output: mean
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_mean.tif

# scale: 3, output: variance
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_variance.tif

# scale: 3, output: filter_1
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_1.tif

# scale: 3, output: filter_2
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_2.tif

# scale: 3, output: filter_3
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_3.tif

# scale: 3, output: filter_4
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_4.tif

# scale: 3, output: filter_5
gdal_translate -b 7 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_5.tif

# scale: 3, output: filter_6
gdal_translate -b 8 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_6.tif

# scale: 3, output: filter_7
gdal_translate -b 9 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_7.tif

# scale: 3, output: filter_8
gdal_translate -b 10 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_8.tif

# scale: 3, output: filter_9
gdal_translate -b 11 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_9.tif

# scale: 3, output: filter_10
gdal_translate -b 12 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_10.tif

# scale: 3, output: filter_11
gdal_translate -b 13 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_11.tif

# scale: 3, output: filter_12
gdal_translate -b 14 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_12.tif

# scale: 3, output: filter_13
gdal_translate -b 15 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_13.tif

# scale: 3, output: filter_14
gdal_translate -b 16 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc3_filter_14.tif

# scale: 5, output: mean
gdal_translate -b 17 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_mean.tif

# scale: 5, output: variance
gdal_translate -b 18 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_variance.tif

# scale: 5, output: filter_1
gdal_translate -b 19 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_1.tif

# scale: 5, output: filter_2
gdal_translate -b 20 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_2.tif

# scale: 5, output: filter_3
gdal_translate -b 21 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_3.tif

# scale: 5, output: filter_4
gdal_translate -b 22 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_4.tif

# scale: 5, output: filter_5
gdal_translate -b 23 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_5.tif

# scale: 5, output: filter_6
gdal_translate -b 24 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_6.tif

# scale: 5, output: filter_7
gdal_translate -b 25 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_7.tif

# scale: 5, output: filter_8
gdal_translate -b 26 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_8.tif

# scale: 5, output: filter_9
gdal_translate -b 27 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_9.tif

# scale: 5, output: filter_10
gdal_translate -b 28 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_10.tif

# scale: 5, output: filter_11
gdal_translate -b 29 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_11.tif

# scale: 5, output: filter_12
gdal_translate -b 30 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_12.tif

# scale: 5, output: filter_13
gdal_translate -b 31 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_13.tif

# scale: 5, output: filter_14
gdal_translate -b 32 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc5_filter_14.tif

# scale: 7, output: mean
gdal_translate -b 33 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_mean.tif

# scale: 7, output: variance
gdal_translate -b 34 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_variance.tif

# scale: 7, output: filter_1
gdal_translate -b 35 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_1.tif

# scale: 7, output: filter_2
gdal_translate -b 36 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_2.tif

# scale: 7, output: filter_3
gdal_translate -b 37 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_3.tif

# scale: 7, output: filter_4
gdal_translate -b 38 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_4.tif

# scale: 7, output: filter_5
gdal_translate -b 39 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_5.tif

# scale: 7, output: filter_6
gdal_translate -b 40 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_6.tif

# scale: 7, output: filter_7
gdal_translate -b 41 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_7.tif

# scale: 7, output: filter_8
gdal_translate -b 42 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_8.tif

# scale: 7, output: filter_9
gdal_translate -b 43 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_9.tif

# scale: 7, output: filter_10
gdal_translate -b 44 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_10.tif

# scale: 7, output: filter_11
gdal_translate -b 45 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_11.tif

# scale: 7, output: filter_12
gdal_translate -b 46 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_12.tif

# scale: 7, output: filter_13
gdal_translate -b 47 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_13.tif

# scale: 7, output: filter_14
gdal_translate -b 48 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_gabor/Accra__BD1_BK1_SC3-5-7_TRgabor.vrt ../outputs/band/gabor/gabor_sc7_filter_14.tif




############################


# HOG
# scale: 3, output: max
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc3_max.tif

# scale: 3, output: mean
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc3_mean.tif

# scale: 3, output: variance
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc3_variance.tif

# scale: 3, output: skew
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc3_skew.tif

# scale: 3, output: kurtosis
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc3_kurtosis.tif

# scale: 5, output: max
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc5_max.tif

# scale: 5, output: mean
gdal_translate -b 7 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc5_mean.tif

# scale: 5, output: variance
gdal_translate -b 8 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc5_variance.tif

# scale: 5, output: skew
gdal_translate -b 9 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc5_skew.tif

# scale: 5, output: kurtosis
gdal_translate -b 10 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc5_kurtosis.tif

# scale: 7, output: max
gdal_translate -b 11 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc7_max.tif

# scale: 7, output: mean
gdal_translate -b 12 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc7_mean.tif

# scale: 7, output: variance
gdal_translate -b 13 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc7_variance.tif

# scale: 7, output: skew
gdal_translate -b 14 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc7_skew.tif

# scale: 7, output: kurtosis
gdal_translate -b 15 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_hog/Accra__BD1_BK1_SC3-5-7_TRhog.vrt ../outputs/band/hog/hog_sc7_kurtosis.tif




############################


# LAC
# scale: 3, output: lac
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lac/Accra__BD1_BK1_SC3-5-7_TRlac.vrt ../outputs/band/lac/lac_sc3_lac.tif

# scale: 5, output: lac
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lac/Accra__BD1_BK1_SC3-5-7_TRlac.vrt ../outputs/band/lac/lac_sc5_lac.tif

# scale: 7, output: lac
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lac/Accra__BD1_BK1_SC3-5-7_TRlac.vrt ../outputs/band/lac/lac_sc7_lac.tif




############################


# LBPM
# scale: 3, output: max
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc3_max.tif

# scale: 3, output: mean
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc3_mean.tif

# scale: 3, output: variance
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc3_variance.tif

# scale: 3, output: skew
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc3_skew.tif

# scale: 3, output: kurtosis
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc3_kurtosis.tif

# scale: 5, output: max
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc5_max.tif

# scale: 5, output: mean
gdal_translate -b 7 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc5_mean.tif

# scale: 5, output: variance
gdal_translate -b 8 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc5_variance.tif

# scale: 5, output: skew
gdal_translate -b 9 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc5_skew.tif

# scale: 5, output: kurtosis
gdal_translate -b 10 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc5_kurtosis.tif

# scale: 7, output: max
gdal_translate -b 11 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc7_max.tif

# scale: 7, output: mean
gdal_translate -b 12 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc7_mean.tif

# scale: 7, output: variance
gdal_translate -b 13 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc7_variance.tif

# scale: 7, output: skew
gdal_translate -b 14 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc7_skew.tif

# scale: 7, output: kurtosis
gdal_translate -b 15 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lbpm/Accra__BD1_BK1_SC3-5-7_TRlbpm.vrt ../outputs/band/lbpm/lbpm_sc7_kurtosis.tif




############################


# LSR
# scale: 31, output: line_length
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc31_line_length.tif

# scale: 31, output: line_mean
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc31_line_mean.tif

# scale: 31, output: line_contrast
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc31_line_contrast.tif

# scale: 51, output: line_length
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc51_line_length.tif

# scale: 51, output: line_mean
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc51_line_mean.tif

# scale: 51, output: line_contrast
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc51_line_contrast.tif

# scale: 71, output: line_length
gdal_translate -b 7 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc71_line_length.tif

# scale: 71, output: line_mean
gdal_translate -b 8 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc71_line_mean.tif

# scale: 71, output: line_contrast
gdal_translate -b 9 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_lsr/Accra__BD1_BK1_SC31-51-71_TRlsr.vrt ../outputs/band/lsr/lsr_sc71_line_contrast.tif




############################


# MEAN
# scale: 3, output: mean
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_mean/Accra__BD1_BK1_SC3-5-7_TRmean.vrt ../outputs/band/mean/mean_sc3_mean.tif

# scale: 3, output: variance
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_mean/Accra__BD1_BK1_SC3-5-7_TRmean.vrt ../outputs/band/mean/mean_sc3_variance.tif

# scale: 5, output: mean
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_mean/Accra__BD1_BK1_SC3-5-7_TRmean.vrt ../outputs/band/mean/mean_sc5_mean.tif

# scale: 5, output: variance
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_mean/Accra__BD1_BK1_SC3-5-7_TRmean.vrt ../outputs/band/mean/mean_sc5_variance.tif

# scale: 7, output: mean
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_mean/Accra__BD1_BK1_SC3-5-7_TRmean.vrt ../outputs/band/mean/mean_sc7_mean.tif

# scale: 7, output: variance
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_mean/Accra__BD1_BK1_SC3-5-7_TRmean.vrt ../outputs/band/mean/mean_sc7_variance.tif




############################


# NDVI
# scale: 3, output: ndvi
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_ndvi/Accra__BD1_BK1_SC3-5-7_TRndvi.vrt ../outputs/band/ndvi/ndvi_sc3_mean.tif

# scale: 3, output: variance
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_ndvi/Accra__BD1_BK1_SC3-5-7_TRndvi.vrt ../outputs/band/ndvi/ndvi_sc3_variance.tif

# scale: 5, output: ndvi
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_ndvi/Accra__BD1_BK1_SC3-5-7_TRndvi.vrt ../outputs/band/ndvi/ndvi_sc5_mean.tif

# scale: 5, output: variance
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_ndvi/Accra__BD1_BK1_SC3-5-7_TRndvi.vrt ../outputs/band/ndvi/ndvi_sc5_variance.tif

# scale: 7, output: ndvi
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_ndvi/Accra__BD1_BK1_SC3-5-7_TRndvi.vrt ../outputs/band/ndvi/ndvi_sc7_mean.tif

# scale: 7, output: variance
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_ndvi/Accra__BD1_BK1_SC3-5-7_TRndvi.vrt ../outputs/band/ndvi/ndvi_sc7_variance.tif




############################


# ORB
# scale: 3, output: max
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc31_max.tif

# scale: 3, output: mean
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc31_mean.tif

# scale: 3, output: variance
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc31_variance.tif

# scale: 3, output: skew
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc31_skew.tif

# scale: 3, output: kurtosis
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc31_kurtosis.tif

# scale: 5, output: max
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc51_max.tif

# scale: 5, output: mean
gdal_translate -b 7 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc51_mean.tif

# scale: 5, output: variance
gdal_translate -b 8 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc51_variance.tif

# scale: 5, output: skew
gdal_translate -b 9 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc51_skew.tif

# scale: 5, output: kurtosis
gdal_translate -b 10 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc51_kurtosis.tif

# scale: 7, output: max
gdal_translate -b 11 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc71_max.tif

# scale: 7, output: mean
gdal_translate -b 12 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc71_mean.tif

# scale: 7, output: variance
gdal_translate -b 13 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc71_variance.tif

# scale: 7, output: skew
gdal_translate -b 14 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc71_skew.tif

# scale: 7, output: kurtosis
gdal_translate -b 15 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_orb/Accra__BD1_BK1_SC31-51-71_TRorb.vrt ../outputs/band/orb/orb_sc71_kurtosis.tif




############################


# PANTEX
# scale: 3, output: min
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_pantex/Accra__BD1_BK1_SC3-5-7_TRpantex.vrt ../outputs/band/pantex/pantex_sc3_min.tif

# scale: 5, output: min
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_pantex/Accra__BD1_BK1_SC3-5-7_TRpantex.vrt ../outputs/band/pantex/pantex_sc5_min.tif

# scale: 7, output: min
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_pantex/Accra__BD1_BK1_SC3-5-7_TRpantex.vrt ../outputs/band/pantex/pantex_sc7_min.tif




############################


# SFS
# scale: 31, output: max_line_length
gdal_translate -b 1 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc31_max_line_length.tif

# scale: 31, output: min_line_length
gdal_translate -b 2 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc31_min_line_length.tif

# scale: 31, output: mean
gdal_translate -b 3 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc31_mean.tif

# scale: 31, output: w_mean
gdal_translate -b 4 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc31_w_mean.tif

# scale: 31, output: std
gdal_translate -b 5 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc31_std.tif

# scale: 31, output: max_ratio_of_orthogonal_angles
gdal_translate -b 6 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc31_max_ratio_of_orthgonal_angles.tif

# scale: 51, output: max_line_length
gdal_translate -b 7 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc51_max_line_length.tif

# scale: 51, output: min_line_length
gdal_translate -b 8 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc51_min_line_length.tif

# scale: 51, output: mean
gdal_translate -b 9 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc51_mean.tif

# scale: 51, output: w_mean
gdal_translate -b 10 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc51_w_mean.tif

# scale: 51, output: std
gdal_translate -b 11 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc51_std.tif

# scale: 51, output: max_ratio_of_orthogonal_angles
gdal_translate -b 12 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc51_max_ratio_of_orthgonal_angles.tif

# scale: 71, output: max_line_length
gdal_translate -b 13 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc71_max_line_length.tif

# scale: 71, output: min_line_length
gdal_translate -b 14 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc71_min_line_length.tif

# scale: 71, output: mean
gdal_translate -b 15 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc71_mean.tif

# scale: 71, output: w_mean
gdal_translate -b 16 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc71_w_mean.tif

# scale: 71, output: std
gdal_translate -b 17 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc71_std.tif

# scale: 71, output: max_ratio_of_orthogonal_angles
gdal_translate -b 18 -of GTiff -co "COMPRESS=LZW" -co "BIGTIFF=YES" ../outputs/features/Accra_sfs/Accra__BD1_BK1_SC31-51-71_TRsfs.vrt ../outputs/band/sfs/sfs_sc71_max_ratio_of_orthgonal_angles.tif

