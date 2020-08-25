#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# CREATE BANDS FROM SPFEAS
# 1-2a_spfeas_create-bands.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script takes the VRT files (the output of spfeas) and extracts the VRT
# band-by-band, assigning each band according to its output name. The order of
# outputs is determined from the spfeas package.

# **This script produces a .txt file, so it must be copied over into a .sh file
# **The output_tif directory needs to be created beforehand

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import os
import glob

# Set directory that contains all the feature VRTs (the parent output folder) *
# Make sure there is end slash
output_directory = r"""outputs/"""

# Set text file name
text_file = "to_bands.txt"

# Group contextual features by scale *
group_a = ["gabor", "hog", "lac", "lbpm", "mean", "ndvi", "pantex"] # Scales of 30 m, 50 m, 70 m
group_b = ["fourier", "lsr", "orb", "sfs"] # Scales of 31 m, 51 m, 71 m

# Create list of contextual features
spfeas = sorted(group_a + group_b)

# Create dictionary of outputs for each feature
# The number of bands differs based on contextual feature; more information
# can be found at https://github.com/jgrss/spfeas.
outputs = {"fourier": ["mean", "variance"],
           "gabor": ["mean", "variance", "filter_1", "filter_2", "filter_3",
                     "filter_4", "filter_5", "filter_6", "filter_7", "filter_8",
                     "filter_9", "filter_10", "filter_11", "filter_12",
                     "filter_13", "filter_14"],
           "hog": ["max", "mean", "variance", "skew", "kurtosis"],
           "lac": ["lac"],
           "lbpm": ["max", "mean", "variance", "skew", "kurtosis"],
           "lsr": ["line_length", "line_mean", "line_contrast"],
           "mean": ["mean", "variance"],
           "ndvi": ["mean", "variance"],
           "orb": ["max", "mean", "variance", "skew", "kurtosis"],
           "pantex": ["min"],
           "sfs": ["max_line_length", "min_line_length", "mean", "w_mean", "std", "max_ratio_of_orthogonal_angles"]}


# Function writes the outputs to a text file in the format necessary to run .sh
# Need to extract the VRT band-by-band and assign each band to its output name
def write_outputs(scales):
    
    # Set band count to 0
    # The band count will help associate a band in the VRT to its output (i.e., variance)
    # based on the spfeas package
    band_count = 0
    
    # Iterate through each scale, which contains multiple outputs
    for scale in scales:
        
        # Iterate through each output of the feature
        for output in outputs[feature]:
            
            # Open file and add comment indicating the scale and the output
            with open(os.path.join(output_directory, text_file), "a+") as file:
                file.write("# scale: {}, output: {}\n".format(scale, output))
            
            # Increase band count by 1
            band_count = band_count + 1
            
            # Create the relative path for the output tif that will be
            # extracted from the VRT band-by-band *
            output_tif = os.path.join(r"../outputs/band", feature, feature + "_sc" + str(scale) + "_" + output + ".tif")
            
            # Open file and write the code *
            with open(os.path.join(output_directory, text_file), "a+") as file:
                file.write("gdal_translate -b {} -of GTiff -co \"COMPRESS=LZW\" -co \"BIGTIFF=YES\" {} {}\n\n".format(band_count, vrt, output_tif))

# Create a new file
with open(os.path.join(output_directory, text_file), "w+") as file:
    file.write("SH FILE TO CONVERT VRT INTO BANDS")
    

# Iterate through each feature
for feature in spfeas:
    print("\n\nWorking on {}".format(feature))
    
    # Add feature name as comment to file
    with open(os.path.join(output_directory, text_file), "a+") as file:
        file.write("\n\n\n############################\n\n\n# {}\n".format(feature.upper()))
    
    # Get folder where feature is located *
    folder = os.path.join(output_directory, "features", """area""" + feature)
    
    # Get VRT file
    vrt = glob.glob(os.path.join(folder, "*.vrt*"))[0] # Last asterisk not necessary
    
    # Replace absolute path with relative path *
    # vrt is global variable used above
    vrt = vrt.replace(output_directory, r"../outputs/")
    
    # Check which group feature is in and assign the appropriate scales to the
    # write_output function
    if feature in group_a:
        write_outputs(scales = [3, 5, 7])
    elif feature in group_b:
        write_outputs(scales = [31, 51, 71])
        
    # If feature is not assigned, let user know
    else:
        print("Feature not in a group!")

print("\n\nOutput file located at: {}".format(os.path.join(output_directory, text_file)))
print("\n\nDone.")