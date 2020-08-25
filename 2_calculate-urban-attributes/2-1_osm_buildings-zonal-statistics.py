#!/usr/bin/env python
# coding: utf-8


###############################################################################
# CALCULATE OSM BUILDINGS
# 2-1_osm_buildings-zonal-statistics.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script is part 1 of 3. The script takes in a tract shapefile and OSM
# buildings shapefile. OSM data can be downloaded from GeoFabrik. Zonal
# statistics, specifically building area and building count, are calculated.

# The shapefiles must all be in a projected coordinate system with a linear
# unit of measurement, such as meters.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import arcpy
import os

# INPUT NAMES
# Path of tract polygon *
tract_poly = r"""tract shapefile.shp"""
tract_poly_key = """key""" # Change based on census tract field name *

# Folder path of raw OSM data *
raw_osm_folder = r"""osm/"""

# Name of raw buildings file  (in raw OSM folder) *
raw_buildings_file = """buildings.shp"""


# OUTPUT NAMES
# Folder path of where new building files will be stored *
buildings_folder = r"""buildings/"""

# Output name for merged buildings across tract (within buildings folder) *
buildings_merged_output = """OSM_buildings_merged.shp"""

# Output name of merged buildings across tracts joined with tract data
# (within buildings folder) *
buildings_joined_output = """OSM_buildings.shp"""

# Folder path of where new building statistics will be stored *
final_tables_folder = r"""tables/"""

# Output table name of previous output (within tables folder) *
buildings_joined_table = """OSM_buildings_table"""

# Output Excel name of previous output (within tables folder) *
buildings_joined_table_xls = """OSM_buildings_table.xls"""


# SET COLUMN NAMES
building_area_column_name = "BUILD_AREA"


# Set workspace, checkout extension, and overwrite output
arcpy.env.workspace = raw_osm_folder
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

# Set output coordinates
spatial_ref = arcpy.Describe(tract_poly).spatialReference
arcpy.env.outputCoordinateSystem = spatial_ref


print("Clipping buildings...")
# Use cursor to clip and extract all buildings within each tract polygon
with arcpy.da.SearchCursor(tract_poly,['SHAPE@', 'FID']) as cursor:
    for row in cursor:
        print(row[1])
        
        # Set file name, with added zeros for sorting purposes
        if row[1] < 10:
            feature_id = "00" + str(row[1])
        elif row[1] < 100:
            feature_id = "0" + str(row[1])
        else:
            feature_id = str(row[1])

        print(os.path.join(buildings_folder, "osm_buildings_" + feature_id + ".shp"))

        # Clip
        arcpy.Clip_analysis(in_features = raw_buildings_file,
                            clip_features = row[0],
                            out_feature_class = os.path.join(buildings_folder, "osm_buildings_" + feature_id + ".shp"))
                         
print("\n\nMerging buildings...")
# Set workspace
arcpy.env.workspace = buildings_folder

# List and sort feature classes in the workspace (clipped OSM buildings
# in each tract)
feature_list = arcpy.ListFeatureClasses()
feature_list.sort()
# print(feature_list)

# Create full file path for output
merged_output = os.path.join(buildings_folder, buildings_merged_output)

# Merge all clipped building shapefiles into one
arcpy.Merge_management(inputs = feature_list,
                       output = merged_output)

print("\n\nCalculating building area...")
# Add field to shapefile
arcpy.AddField_management(in_table = buildings_merged_output,
                          field_name = building_area_column_name,
                          field_type = "DOUBLE")
                          
# Populate new filed with area of each building (represented by each row)
with arcpy.da.UpdateCursor(buildings_merged_output, [building_area_column_name, "SHAPE@AREA"]) as cursor:
    for row in cursor:
        row[0] = row[1]
        cursor.updateRow(row)

print("\n\nJoining buildings with tract shapefile...")
# Join merged building shapefile with tract polygon shapefile based on
# spatial location (merged building falls within tract polygon)
arcpy.SpatialJoin_analysis(target_features = buildings_merged_output,
                           join_features = tract_poly,
                           out_feature_class = buildings_joined_output,
                           join_operation = "JOIN_ONE_TO_ONE",
                           join_type = "KEEP_ALL",
                           match_option = "WITHIN")

print("Calculating summary statistics for building data...")
# Obtain summary statistics for each tract (building area and building count)
arcpy.Statistics_analysis(in_table = buildings_joined_output,
                          out_table = os.path.join(final_tables_folder, buildings_joined_table),
                          statistics_fields = [[building_area_column_name, "SUM"], [building_area_column_name, "COUNT"]],
                          case_field = tract_poly_key)

print("Converting to Excel file...")
# Convert summary statistics table to Excel
arcpy.TableToExcel_conversion(Input_Table = os.path.join(final_tables_folder, buildings_joined_table),
                              Output_Excel_File = os.path.join(final_tables_folder, buildings_joined_table_xls))

# Check in extension
arcpy.CheckInExtension("Spatial")

print("\n\nDone.")