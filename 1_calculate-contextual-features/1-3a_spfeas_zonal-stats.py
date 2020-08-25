#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# CREATE ZONAL STATISTICS FROM SPFEAS BANDS
# 1-3a_spfeas_zonal-stats.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University
# Script adapted from Adane Bedada

# This script calculates the zonal statistics for the contextual feature
# outputs.

# **If there is a MemoryError, ensure that the coordinate systems of the
# shapefile and the tif files are the same
# (https://github.com/perrygeo/python-rasterstats/issues/107)

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Load modules
import os
import glob
from rasterstats import zonal_stats as zs
import geopandas as gpd
import pandas as pd
# import rasterio as rio

# Set contextual features *
spfeas = ["fourier", "gabor", "hog", "lac", "lbpm", "lsr", "mean", "ndvi", "orb", "pantex", "sfs"]

# Zonal statistic aggregations
metrics = ["sum", "mean", "std"]

# Read the shapefile *
shp = gpd.GeoDataFrame.from_file(r"""tract shapefile.shp""")
shp_cols = shp.drop(['geometry'],axis=1)

# Set parent directory that contains output folder *
# Must have slash at end
output_directory = r"""outputs/"""

# Iterate through each feature
for feature in spfeas:
    print("\n\nWorking on {}".format(feature))
    
    # Create empty dictionary to hold file name and relative path
    # i.e., 'pantex_sc7_min': '../../outputs/band/pantex/pantex_sc7_min.tif'
    rasters = dict()

    # Get absolute paths of the tif files *
    tifs_absolute_path = glob.glob(os.path.join(output_directory, "band", feature, r"*.tif"))
    
    # Iterate through each tif
    for tif in tifs_absolute_path:
        
        # Get the file name only (no path, no extension)
        file_name = os.path.splitext(os.path.basename(tif))[0]
        
        # Change absolute path to relative path *
        tif_relative_path = tif.replace(output_directory, r"""../outputs/""")
        
        # Add file name and relative path to dictionary
        rasters[file_name] = tif_relative_path
    
    # Set output location and file name for zonal statistics CSV file *
    zonal_stats_location = os.path.join(output_directory, "zonal_stats", "zonalstats_{}.csv".format(feature))
    
    # Copy metrics
    spfeas_stats = shp_cols.copy()
    
    # Calculate Rasters
    for rast, path in rasters.items():
    
    	# Calculate stats, this creates a dictionary with metrics as columns and values as rows
        stats = zs(shp, path, stats=metrics)
    
        # New column names using formatter
        new_colnames = ["{}_{}".format(rast, metric) for metric in metrics]
    
        # Create dataframe from stats dictionary
        df = pd.DataFrame(stats)
    
        # Rename the metrics column with the new column names
        # Zip puts the indices of two lists together (zip them together)
        # Dict creates a dictionary because rename needs a dictionary (old name: new name)
        df2 = df.rename(columns=dict(zip(metrics, new_colnames)))
        spfeas_stats =spfeas_stats.join(df2)
    
    # Save dataframe as csv
    spfeas_stats.to_csv(zonal_stats_location)
    
print("\n\nDone.")