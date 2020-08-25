#!/usr/bin/env python
# coding: utf-8


###############################################################################
# CALCULATE OSM DENSITIES AND COMBINE ALL ZONAL STATISTICS
# 2-2_osm_roads-zonal-statistics.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script is part 3 of 3. The script takes in a tract shapefile and OSM
# zonal statistics tables calculated from parts 1 and 2. Zonal statistics,
# specifically built-up area, built-up density, building density, and road
# density, are calculated.

# Ensure that the files are mostly clean before running this script. This
# includes deleting columns that are not necessary (i.e., non-primary keys).
# This will save having to delete columns at the end.

# The shapefile must be in a projected coordinate system with a linear
# unit of measurement, such as meters. The area, in both meters and kilometers
# should already be calculated and exist as a field in the attribute table.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import pandas as pd
import arcpy
from arcpy import TableToExcel_conversion
# import os


# File path of road statistics *
roads_excel_path = r"""OSM_roads_table.xls"""

# File path of building statistics *
buildings_excel_path = r"""OSM_buildings_table.xls"""

# File path of tract output table *
tract_excel_path = r"""tract_poly_table.xls"""

# File path of combined statistic table *
output_path = r"""tables/OSM_FINAL.xls"""


# Set overwrite output to true
arcpy.env.overwriteOutput = True

print("Converting tract shapefile to Excel file...")
# Convert tract table from shapefile to Excel
# This shapefile should have area calculated in meters and kilometers *
TableToExcel_conversion(Input_Table = r"""tract shapefile.shp""",
                        Output_Excel_File = tract_excel_path)

print("\n\nImporting Excel files...")
# Create dataframes from Excel files
roads_df = pd.read_excel(roads_excel_path)
buildings_df = pd.read_excel(buildings_excel_path)
tract_df = pd.read_excel(tract_excel_path)

print("\n\nJoining Excel files...")
# Use outer joins in case some tracts actually do not have any values
# Join buildings and roads *
roads_buildings_df = pd.merge(roads_df, buildings_df, how = "outer", on = """key""")

# Join previous to tract *
join_df = pd.merge(roads_buildings_df, tract_df, how = "outer", left_on = """key""", right_on = """key""")

# Sort dataframe by tract *
join_df.sort_values(by = ["""key"""])


# Building area is the total area in square meters of building footprints.
# Building count is the number of buildings.
# Building density is building count divided by tract area.
# Road density is road length divided by tract area.
# Road length is the total (summed) length of all road segments.
# Road area is the total area of all road segments.
# Built-up area is the sum of road area and building area.
# Built-up density is built-up area divided by tract area.

# Set variables based on column names
building_area = "SUM_BUILD_AREA"
building_count = "COUNT_BUILD_AREA"
road_area = "SUM_RD_AREA"
road_length = "SUM_RD_LENGTH"
gn_area_km = "area_km" # Change based on area column in census shp
gn_area_m = "area_m" # Change based on area column in census shp
builtup_area = "BUILTUP_AREA"

print("\n\nCalculating density and built-up variables...")
# Calculate variables using algebra
join_df["BUILD_DEN"] = join_df[building_count] / join_df[gn_area_km]
join_df["RD_DEN"] = join_df[road_area] / join_df[gn_area_km]
join_df[builtup_area] = join_df[road_area] + join_df[building_area]
join_df["BUILTUP_DEN_PRCNT"] = (join_df[builtup_area]) / join_df[gn_area_m]

print(join_df.head(5))


# Save to Excel
join_df.to_excel(output_path)

print("\n\nDone.")