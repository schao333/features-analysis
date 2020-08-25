#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# COMBINE ZONAL STATISTICS IN AN AREA
# 1-4_spfeas_combine-zonal-stats.py

# Created by: Steven Chao
# Summer 2020
# The George Washington University

# This script takes the zonal statistics calculated for each individual
# contextual feature and combines them into one CSV by putting all the
# columns together.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import pandas as pd
import os
import glob

# Set directory that contains output files *
## Adjust as needed
output_directory = r"""outputs/"""

# List of areas in which all CSVs will be combined
# CSVs across areas will NOT be combined *
areas = ["""list of areas"""]

# Create a combined csv file for ALL contextual features, one for EACH area
for area in areas:
    print("\n\nWorking on {}".format(area))
    
    # Creat empty list of contextual feature dataframes
    contextual_features_dfs = []

    # Set output path of combined zonal stats of each area *
    output_path = os.path.join(output_directory, "zonal_stats", "all_zonalstats_" + area + ".csv")
    
    # Get list of all zonal statistics CSVs in the directory *
    csv_list = sorted(glob.glob(os.path.join(output_directory, "zonal_stats", area, "zonalstats_*.csv")))

    # Create fourier dataframe (or whatever the first dataframe is)
    fourier_df = pd.read_csv(csv_list[0])

    # Append fourier dataframe to list
    contextual_features_dfs.append(fourier_df)

    # Append other dataframes to list
    for csv in csv_list[1:]:

        # Create dataframe from called file and drop non-unique columns *
        # Fourier dataframe is the only dataframe to contain these non-unique
        # columns to avoid error when joining
        # Adjust indexes as needed *
        dataframe = pd.read_csv(csv)
        
        dataframe2 = dataframe.drop(dataframe.columns["""index""":"""index"""], axis=1)
        dataframe3 = dataframe2.drop(dataframe2.columns["""index""":"""index"""], axis=1)
        print(csv, len(dataframe3.columns))

        # Append to list
        contextual_features_dfs.append(dataframe3)

    # Set index to GN for each dataframe
    # Adjust index name as needed *
    #contextual_features_dfs = [df.set_index('ADJ_EACODE') for df in contextual_features_dfs] #Neighborhood
    contextual_features_dfs = [df.set_index("""index""") for df in contextual_features_dfs] #FMV

    # Join all dataframes to fourier and save to new dataframe
    joined_dfs = contextual_features_dfs[0].join(contextual_features_dfs[1:])

    # Export dataframe to CSV (too large for Excel)
    joined_dfs.to_csv(output_path)
    
print("\n\nDone.")