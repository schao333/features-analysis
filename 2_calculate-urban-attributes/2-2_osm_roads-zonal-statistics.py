#!/usr/bin/env python
# coding: utf-8


###############################################################################
# CALCULATE OSM ROADS
# 2-2_osm_roads-zonal-statistics.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script is part 2 of 3. The script takes in a tract shapefile and OSM
# roads shapefile. OSM data can be downloaded from GeoFabrik. Zonal
# statistics, specifically road area and road length, are calculated.
# Road widths are determined by estimating road widths for each road "fclass"
# using the Ruler/Measurement tool in ArcGIS.

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

# Name of raw roads file (in raw OSM folder) *
raw_roads_file = """roads.shp"""


# OUTPUT NAMES
# Folder path of where new road files will be stored *
roads_folder = r"""roads/"""

# Output name for merged roads across tracts (within roads folder) *
roads_merged_output = """OSM_roads_merged.shp"""

# Output name of merged roads across tracts joined with tract data
# (within roads folder) *
roads_joined_output = """OSM_roads.shp"""

# Folder path of where new road statistics will be stored *
final_tables_folder = r"""tables/"""

# Output table name of previous output (within tables folder) *
roads_joined_table = """OSM_roads_table"""

# Output Excel name of previous output (within tables folder) *
roads_joined_table_xls = """OSM_roads_table.xls"""


# SET COLUMN NAMES
road_area_column_name = "RD_AREA"
road_length_column_name = "RD_LENGTH"


# Set workspace, checkout extension, and overwrite output
arcpy.env.workspace = raw_osm_folder
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True


print("Clipping roads...")
# Use cursor to clip and extract all roads within each tract polygon
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

        print(os.path.join(roads_folder, "osm_roads_" + feature_id + ".shp"))

        # Clip
        arcpy.Clip_analysis(in_features = raw_roads_file,
                            clip_features = row[0],
                            out_feature_class = os.path.join(roads_folder, "osm_roads_" + feature_id + ".shp"))

                            
print("\n\nMerging roads...")
# Set workspace
arcpy.env.workspace = roads_folder

# List and sort feature classes in the workspace (clipped OSM buildings
# in each tract)
feature_list = arcpy.ListFeatureClasses()
feature_list.sort()
print(feature_list)

# Create full file path for output
merged_output = os.path.join(roads_folder, roads_merged_output)

# Merge all clipped building shapefiles into one
arcpy.Merge_management(inputs = feature_list,
                       output = merged_output)


# Deletes the roads classified as "steps" because not relevant
'''
with arcpy.da.UpdateCursor(merged_output, ["fclass"]) as cursor:
    for row in cursor:
        if row[1] == "steps":
            print("Delete")
            cursor.deleteRow()
        else:
            pass
'''

print("\n\nCalculating road area and road length...")
# Add field to roads shapefile
arcpy.AddField_management(in_table = roads_merged_output,
                          field_name = road_length_column_name,
                          field_type = "DOUBLE")


# Add field to roads shapefile
arcpy.AddField_management(in_table = roads_merged_output,
                          field_name = road_area_column_name,
                          field_type = "DOUBLE")


# Use cursor to calculate road length and road area and assign the values
# to the corresponding fields

# Replace script between the hashes (i.e., ########### AREA ###########)
# with the relevant widths for the area

# Links used to set OSM widths
## https://wiki.openstreetmap.org/wiki/Key%3ahighway
## https://wiki.openstreetmap.org/wiki/Sri_Lanka_Tagging_Guidelines
## http://www.geofabrik.de/data/geofabrik-osm-gis-standard-0.7.pdf
## http://www.geofabrik.de/data/shapefiles.html

# OSM Attributes
## 'cycleway' 'footway' 'living_street' 'motorway' 'motorway_link' 'path'
## 'pedestrian' 'primary' 'primary_link' 'residential' 'secondary'
## 'secondary_link' 'service' 'steps' 'tertiary' 'tertiary_link' 'track'
## 'track_grade3' 'track_grade5' 'trunk' 'trunk_link' 'unclassified' 'unknown'

########### ACCRA ###########
primary_road = ["primary"]
primary_link = ["primary_link", "unclassified"]
residential = ["residential"]
secondary_road = ["secondary"]
tertiary_road = ["tertiary"]
misc_road = ["cycleway", "track", "tertiary_link", "secondary_link", "service"]
paths = ["path", "track_grade3"]
footway = ["footway"]
pedestrian = ["pedestrian"]
trunk = ["trunk"]
trunk_link = ["trunk_link"]

with arcpy.da.UpdateCursor(roads_merged_output, [road_length_column_name, road_area_column_name, "SHAPE@LENGTH", "fclass", "oneway"]) as cursor:
    for row in cursor:
        
        # Set road length
        row[0] = row[2]
        
        print("Road is {}".format(row[3:5]))
        
        # Calculate road area based on class
        if (row[3] in primary_road) and (row[4] == "B"):
            print("Divided primary road = 10 m")
            row[1] = row[2] * 10
        elif (row[3] in primary_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way primary road = 8 m")
            row[1] = row[2] * 8

        elif (row[3] in primary_link) and (row[4] == "B"):
            print("Divided primary road link = 8 m")
            row[1] = row[2] * 8
        elif (row[3] in primary_link) and (row[4] == "F" or row[4] == "T"):
            print("One-way primary road link = 5 m")
            row[1] = row[2] * 5

        elif (row[3] in trunk) and (row[4] == "B"):
            print("Divided trunk = 20 m")
            row[1] = row[2] * 20
        elif (row[3] in trunk) and (row[4] == "F" or row[4] == "T"):
            print("One-way trunk = 10 m")
            row[1] = row[2] * 10

        elif (row[3] in trunk_link) and (row[4] == "B"):
            print("Divided trunk link = 10 m")
            row[1] = row[2] * 10
        elif (row[3] in trunk_link) and (row[4] == "F" or row[4] == "T"):
            print("One-way trunk link = 5 m")
            row[1] = row[2] * 5

        
        elif (row[3] in residential):
            print("Residential street = 7 m")
            row[1] = row[2] * 7
            
        elif (row[3] in secondary_road):
            print("Secondary road = 8 m")
            row[1] = row[2] * 8
            
        elif (row[3] in tertiary_road) and (row[4] == "B"):
            print("Two-way tertiary road = 10 m")
            row[1] = row[2] * 10
        elif (row[3] in tertiary_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way tertiary road = 5 m")
            row[1] = row[2] * 5

        elif (row[3] in paths):
            print("Path = 3 m")
            row[1] = row[2] * 3

        elif row[3] in pedestrian:
            print("Pedestrian walkway = 3.5 m")
            row[1] = row[2] * 3.5
            
        elif row[3] in footway:
            print("Footway = 4 m")
            row[1] = row[2] * 4
            
        elif row[3] in misc_road:
            print("Miscellaneous road = 5 m")
            row[1] = row[2] * 5

        else:
            print("Road not used!")

        print("\n")

        cursor.updateRow(row)

#############################


# Set workspace
arcpy.env.workspace = roads_folder

print("\n\nJoining roads with tract shapefile...")
# Join merged road shapefile with tract polygon shapefile based on
# spatial location (merged road falls within tract polygon)
arcpy.SpatialJoin_analysis(target_features = roads_merged_output,
                           join_features = tract_poly,
                           out_feature_class = roads_joined_output,
                           join_operation = "JOIN_ONE_TO_ONE",
                           join_type = "KEEP_ALL",
                           match_option = "WITHIN")

print("Calculating summary statistics for building data...")
# Obtain summary statistics for each tract (road area and road length)
arcpy.Statistics_analysis(in_table = roads_joined_output,
                          out_table = os.path.join(final_tables_folder, roads_joined_table),
                          statistics_fields = [[road_area_column_name, "SUM"], [road_length_column_name, "SUM"]],
                          case_field = tract_poly_key)

print("Converting to Excel file...")
# Convert summary statistics table to Excel
arcpy.TableToExcel_conversion(Input_Table = os.path.join(final_tables_folder, roads_joined_table),
                              Output_Excel_File = os.path.join(final_tables_folder, roads_joined_table_xls))


# Check in extension
arcpy.CheckInExtension("Spatial")

print("\n\nDone.")



########### OTHER AREA ROAD WIDTH DATA ###########
"""
########### BELIZE ###########
##############################
primary_road = ["primary", "primary_link"]
secondary_road = ["secondary", "secondary_link"]
tertiary_road = ["tertiary", "tertiary_link"]
minor_road = ["service", "residential", "track", "living_street", "unclassified", "track_grade1", "track_grade2", "track_grade3", "track_grade4", "track_grade5"]
misc_road = ["cycleway", "footway", "path", "pedestrian"]

with arcpy.da.UpdateCursor(roads_merged_output, [road_length_column_name, road_area_column_name, "SHAPE@LENGTH", "fclass", "oneway"]) as cursor:
    for row in cursor:
        
        # Set road length
        row[0] = row[2]
        
        print("Road is {}".format(row[3:5]))
        
        # Calculate road area based on class
        if (row[3] in primary_road) and (row[4] == "B"):
            print("Divided highway = 13 m")
            row[1] = row[2] * 13
        elif (row[3] in primary_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way highway = 6.5 m")
            row[1] = row[2] * 6.5
            
        elif (row[3] in secondary_road) and (row[4] == "B"):
            print("Two-way street = 10 m")
            row[1] = row[2] * 10
        elif (row[3] in secondary_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way street = 5 m")
            row[1] = row[2] * 5
            
        elif (row[3] in tertiary_road) and (row[4] == "B"):
            print("Two-way street = 7.5 m")
            row[1] = row[2] * 7.5
        elif (row[3] in tertiary_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way street = 3.75 m")
            row[1] = row[2] * 3.75
            
        elif row[3] in minor_road:
            print("Miscellaneous road = 5 m")
            row[1] = row[2] * 5
        elif row[3] in misc_road:
            print("Miscellaneous road = 4 m")
            row[1] = row[2] * 4

        else:
            print("Road not used!")

        print("\n")

        cursor.updateRow(row)

##############################


########### SRI LANKA ###########

# There are three main widths: 15 m, 10.5 m, and 8.5 m
## Two-way streets (oneway = B) are assigned one of these widths
## One-way streets (oneway = T or F) are assigned half of those widths (7.5 m, 5.25 m, 4.25 m)
## An exception is for really small roads that are technically both ways but are given a 4.25 m width

divided_highway = ["motorway", "motorway_link"]
main_road = ["trunk", "trunk_link", "primary", "primary_link"]
minor_road = ["secondary", "secondary_link"]
side_street = ["tertiary", "tertiary_link", "unclassified", "living_street", "residential", "service"]
misc_road = ["cycleway", "footway", "unknown", "path", "pedestrian", "track", "track_grade3", "track_grade5"]
not_used = ["steps"]

large_road = main_road + divided_highway
side_misc_road = side_street + misc_road

with arcpy.da.UpdateCursor(roads_merged_output, [road_length_column_name, road_area_column_name, "SHAPE@LENGTH", "fclass", "oneway"]) as cursor:
    for row in cursor:
        
        # Set road length
        row[0] = row[2]
        
        print("Road is {}".format(row[3:5]))
        
        # Calculate road area based on class
        if (row[3] in large_road) and (row[4] == "B"):
            print("Divided highway = 15 m")
            row[1] = row[2] * 15
        elif (row[3] in large_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way highway = 7.5 m")
            row[1] = row[2] * 7.5

        elif (row[3] in minor_road) and (row[4] == "B"):
            print("Two-way street = 10.5 m")
            row[1] = row[2] * 10.5
        elif (row[3] in minor_road) and (row[4] == "F" or row[4] == "T"):
            print("One-way street = 5.25 m")
            row[1] = row[2] * 5.25

        elif row[3] in side_misc_road:
            print("Miscellaneous road = 4.25 m")
            row[1] = row[2] * 4.25

        else:
            print("Road not used!")

        print("\n")

        cursor.updateRow(row)
        
#################################
"""
##################################################