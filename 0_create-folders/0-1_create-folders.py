#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# CREATE FOLDER STRUCTURE
# 0-1_create-folders.py

# Created by: Steven Chao
# Summer 2020
# The George Washington University

# This script creates a folder structure as specified by the user. This code
# is optional and is only used to create a sample file structure in which
# the inputs and outputs of the subsequent code can be saved.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import os


# Set working directory in which folders will be created *
working_directory = r"""folder path"""

# Get character length (for printing purposes only)
working_length = len(working_directory)

# Set working directory
os.chdir(working_directory)


def create_subfolders(working_length, folder_path, subfolders):
    '''This function looks into a subfolder and determines whether there are
    more subfolders (dictionaries). If there are, this function is recursive
    and calls this function again. If there are not, it creates the folder.'''
    
    # Set breadcrumb used to track subfolder path (used to create new
    # subfolders when function becomes recursive)
    # breadcrumb = folder_path
    
    # Iterate through each subfolder
    for subfolder in subfolders:
        
        # Check the type of the subfolder
        if isinstance(subfolder, str):
            
            # If the subfolder is a string, update breadcrumb
            breadcrumb = os.path.join(folder_path, subfolder)
            
            # Create subfolder
            print("Making subfolder: {}".format(breadcrumb[working_length:]))
            os.mkdir(breadcrumb)
            
        elif isinstance(subfolder, dict):
            
            # If the subfolder is a dictionary, iterate through each
            # subfolder (keys of dictionary)
            for subfolder2 in subfolder:
                
                # Update breadcrumb with subfolder name
                breadcrumb = os.path.join(folder_path, subfolder2)
                
                # Create subfolder
                print("Making subfolder: {}".format(breadcrumb[working_length:]))
                os.mkdir(breadcrumb)
                
                # Call function recursively to create new subsubfolders from
                # this subfolder
                create_subfolders(working_length, breadcrumb, subfolder[subfolder2])
            
        else:
            # If there are no subfolders or if not a string or dictionary,
            # exit out of this function
            return
       
        
def update_name(breadcrumb):
    '''This function checks if a folder path already exists. If it does, it
    adds a incremental number to the end of the folder name until one does
    not already exist. It then returns that updated folder name.'''
    
    # Initialize count
    count = 0
    
    # Continue running while the folder path exists
    while os.path.isdir(breadcrumb):
        
        # Add number to end of folder name
        breadcrumb = "{}_{}".format(breadcrumb, count)
        
        # Increase count by 1
        count += 1
    
    # If folder does not already exist, return the updated folder name
    return breadcrumb
        

# Create list of contextual feature outputs used to create subfolders
spfeas = ["fourier", "gabor", "hog", "lac", "lbpm", "lsr", "mean", "ndvi", "orb", "pantex", "sfs"]

# Create folder structure *
# The keys are the main folder names
# The values are the subfolders
# To create subfolders within subfolders, create a dictionary as a value;
# there can be multiple dictionaries for each key or one dictionary with
# multiple key/value pairs for each key.
# Do not repeat names
folders = {"data": ["zone_shapefile", "population", "imagery",
                    {"osm": ["buildings", "roads", "tables", "raw"]}],
           "outputs": ["vrt", "zonal_stats","features",
                       {"band": spfeas}],
           "regressions": [{"urban_attributes": ["enr", "rfr"],
                            "population_density": ["enr", "rfr"]}],
           "scripts": []}


# Set name for parent folder
parent_folder = "features-analysis"

try:
    
    # Try to create parent folder
    os.mkdir(parent_folder)
    
except:
    
    # If folder already exists, call function to update folder name
    parent_folder = update_name(parent_folder)
    
    # Create folder
    os.mkdir(parent_folder)

# Set working directory to parent folder
parent_folder_path = os.path.join(working_directory, parent_folder)
os.chdir(parent_folder_path)
print("Folders will be created in {}".format(parent_folder_path))

# Iterate through each main folder
for folder in folders:
    
    # Get complete folder path
    folder_path = os.path.join(parent_folder_path, folder)
    
    # Create main folder
    print("\n\nMaking folder: {}".format(folder_path[working_length:]))
    os.mkdir(folder)
    
    # Get list of subfolders
    subfolders = folders[folder]
    
    # Check if there are subfolders
    if len(subfolders) != 0:
        
        # If subfolders exist, call function to create subfolders
        create_subfolders(working_length, folder_path, subfolders)
    
    # Otherwise, pass
    else:
        pass


print("\n\nDone.")