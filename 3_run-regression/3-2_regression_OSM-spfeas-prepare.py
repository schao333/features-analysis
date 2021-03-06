#!/usr/bin/env python
# coding: utf-8


###############################################################################
# OSM VARIABLES vs CONTEXTUAL FEATURES
# Data Preparation
# 3-2_regression_OSM-spfeas-prepare.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University
# Script based on work by Robert Harrison

# This script is part 1 of 2. The code prepares the data for regression
# analysis.
# It creates CSV files for each dependent variable (appended with all
# independent variables). The script conducts bivariate correlations between
# each independent variable and the dependent variable and obtains Pearson's
# correlations. The associated p-value for each correlation is obtained, and
# only the independent variables that have p-values less than a significance
# level of 0.05 are kept. Of these, only the top 200 variables with the
# strongest correlation coefficients (positive or negative) are kept.

# Input files should have the same primary key. Input files required include:
# contextual features CSV and the OSM CSV.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import pandas as pd
import scipy.stats as stats
from sklearn import preprocessing


def import_csv(y_variable_index, contextual_features, osm, index_number, index_name):
    '''This function imports, modifies, and combines CSV files.'''
    
    print("\n\n=============================================\n\n")
    print("IMPORT CSVs")
    
    # Read and load contextual features data into dataframe
    print("Importing contextual features data...")
    spfeas = pd.read_csv(contextual_features)
    spfeas[index_name] = spfeas[index_name].astype(int)
    spfeas = spfeas.set_index(index_name)
    # print(spfeas.head())
    
    
    # Read and load OSM data into dataframe
    print("Importing OSM data...")
    osm = pd.read_csv(osm) #, sheet_name = 0)
    osm[index_name] = osm[index_name].astype(int)
    osm = osm.set_index(index_name)
    # print(osm.head())
    
    
    # Merge contextual features and OSM dataframes based on index_name column
    print("Merging contextual features and OSM Data...")
    spfeas_osm = spfeas.merge(osm,
                              left_on = index_name,
                              right_on = index_name,
                              how = 'inner')
    spfeas_osm = spfeas_osm.round(3)
    # print(spfeas_osm.head())
    
    
    # Print shape of merged dataframe
    print("The dimension of the merged table is {}.".format(spfeas_osm.shape))
    
    # ### Analysis
    print("\n\nSET INDEPENDENT AND DEPENDENT VARIABLES")
    
    # Get the list of dependent variables from the dataframe to store in
    # list y_vars
    print("Obtaining dependent variable...")
    y_var = list(spfeas_osm.axes[1])[y_variable_index] # axes1 = column
    # print(y_var)
    
    
    # Get a list of all independent variables from the dataframe in list all_x
    print("Obtaining independent variables...")
    all_x = list(spfeas_osm.axes[1])[0:index_number]
    # print(all_x)
    
    # Return variables for next function
    return all_x, y_var, spfeas_osm


def correlation(image_type, all_x, y_var, spfeas_osm, y_dict, scale_y):
    '''This function computes the correlations and only takes the top 200
    independent variables.'''
    
    print("\n\nCOMPUTE CORRELATIONS")
    
    # The Pearson correlation coefficient measures the linear relationship
    # between two datasets. Strictly speaking, Pearson's correlation requires
    # that each dataset be normally distributed, and not necessarily zero-mean.
    # 
    # Like other correlation coefficients, this one varies between -1 and +1
    # with 0 implying no correlation. Correlations of -1 or +1 imply an exact
    # linear relationship. Positive correlations imply that as x increases, so
    # does y. Negative correlations imply that as x increases, y decreases.
    # 
    # The p-value roughly indicates the probability of an uncorrelated system
    # producing datasets that have a Pearson correlation at least as extreme
    # as the one computed from these datasets. 
    # 
    # The p-values are not entirely reliable but are probably reasonable for
    # datasets larger than 500 or so.
    
    # Fill NA values with 0
    spfeas_osm[y_var] = spfeas_osm[y_var].fillna(0)
    spfeas_osm[y_var].isnull().values.any()

    # Create empty list
    x = []
    
    print("Calculating Pearson's r...")
    for x_var in all_x:
        
        # Calculate the Pearson statistics, returns the Pearson value and
        # p value
        p = stats.pearsonr(spfeas_osm[x_var],spfeas_osm[y_var])
        
        # If p < 0.05, append to list x
        if p[1] < 0.05:
            x.append([x_var,abs(p[0]),p[0]])
    
    # List x is made into a dataframe, which is sorted by the absolute values
    # of the Pearson values
    x_df = pd.DataFrame(x, columns = ["x_var","abs_r","r"]).sort_values("abs_r", ascending = False)
    x_df.to_csv("{}_{}_pearson.csv".format(image_type, y_var))
    
    # List x sorted by positive r
    x_df_pos = pd.DataFrame(x, columns = ["x_var","abs_r","r"]).sort_values("r", ascending = False)
    
    # List x sorted by negative r
    x_df_neg = pd.DataFrame(x, columns = ["x_var","abs_r","r"]).sort_values("r", ascending = True)
    
    # Print sorted x dataframes
    # print(x_df.head(5))
    # print(x_df_pos.head(5))
    # print(x_df_neg.head(5))
    
    
    # The dependent variable dictionary is given an entry,
    # where the key is the name of the dependent variable and the value is a
    # list of top 200 most significant values
    y_dict[y_var] = list(x_df["x_var"][0:200])
    
    # Print top 200 variables based on Pearson's r
    # print("The top 200 variables based on Pearson's r are:")
    # print(y_dict[y_var])
    
    # Print shape for last key (y_var)
    last_key = list(y_dict)[-1]
    print("For {}, there are {} variables.".format(last_key, len(y_dict[last_key])))
    
    # Correlation Significance
    print("\n\nCORRELATION SIGNIFICANCE")
    
    # Get independent variables from the variable dictionary and store in
    # list x_vars
    x_vars = y_dict[y_var]
    
    # Add dependent variable and 200 standardized independent variables
    # to new dataframe
    vars_df = spfeas_osm[[y_var] + x_vars]
    
    # Rename dependent variable column to indicate it will be scaled
    vars_df = vars_df.rename(columns = {y_var: "{}_scaled".format(y_var)})
        
    # Scale / normalize data
    print("Standardizing data...")
    standard_scaler = preprocessing.StandardScaler()
    names = vars_df.columns
    scaled_df = standard_scaler.fit_transform(vars_df)
    scaled_df = pd.DataFrame(scaled_df, index = vars_df.index, columns = names)
    # print(scaled_df.head())    
    print("The dimension of the scaled table is {}.".format(scaled_df.shape))
    
    # Concatenate unscaled dependent variable with scaled
    # independent variables
    full_df = pd.concat([spfeas_osm[y_var], scaled_df], axis=1)
    
    # Rename newly-added dependent variable column to indicate it is
    # not scaled
    full_df = full_df.rename(columns = {y_var: "{}_unscaled".format(y_var)})
        
    # Finalize full dataframe of independent and dependent variables
    if scale_y.strip().lower() == "yes":
        # If dependent variable is scaled, create a new dataframe consisting
        # of scaled and unscaled dependent variable
        y_values = full_df[["{}_unscaled".format(y_var), "{}_scaled".format(y_var)]]
        
        # Export to csv
        y_values.to_csv("{}_{}_y-values.csv".format(image_type, y_var))
        
        # Drop the unscaled column
        full_df = full_df.drop("{}_unscaled".format(y_var), axis = 1)
        
        # Change the scaled column name back
        full_df = full_df.rename(columns = {"{}_scaled".format(y_var): y_var})
    
    # Otherwise, if dependent variable is unscaled
    else:
        # Drop the scaled column
        full_df = full_df.drop("{}_scaled".format(y_var), axis = 1)
        
        # Change the unscaled column name back
        full_df = full_df.rename(columns = {"{}_unscaled".format(y_var): y_var})
        
    # Remove the index (FIPS code)
    # full_df.reset_index(drop = True, inplace = True)
    
    # Convert dataframe to csv
    full_df.to_csv("{}_{}_scaled.csv".format(image_type, y_var))
    # print(full_df.head())
    
    # Return variables for next function 
    return spfeas_osm, x_vars, y_var, full_df


def main(image_type, contextual_features, osm, index_number, index_name, scale_y):
    '''This is the main function that runs the script and calls the other
    functions.'''
    
    # Create empty dictionaries
    y_dict = {}
    
    # Run functions for each y variable
    # Range depends on the number of OSM dependent variables *
    for y_variable_index in range(-8, 0):
        
        # Import Excel spreadsheets
        all_x, y_var, spfeas_osm = import_csv(y_variable_index, contextual_features, osm, index_number, index_name)
        
        # Run correlation
        spfeas_osm, x_vars, y_var, scaled_df = correlation(image_type, all_x, y_var, spfeas_osm, y_dict, scale_y)

    print("\n\n=============================================\n\n")
    
    # Return variables
    # return y_dict, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, seed_df, y_summary_statistic_df


# Run script
# Index number is the number of contextual features, index name is the
# primary key column name (432 if using all spfeas in the study), and scale y
# allows for scaling of dependent variable *
main(image_type = """sl""", contextual_features = """sl_spfeas.csv""", osm = """sl_OSM.csv""", index_number = 432, index_name = """FIPS""", scale_y = """no""")
main(image_type = """blz""", contextual_features = """blz_spfeas.csv""", osm = """blz_OSM.csv""", index_number = 432, index_name = """FIPS""", scale_y = """no""")
main(image_type = """gh""", contextual_features = """gh_spfeas.csv""", osm = """gh_OSM.csv""", index_number = 432, index_name = """FIPS""", scale_y = """no""")
main(image_type = """sl-blz-gh""", contextual_features = """sl-blz-gh_spfeas.csv""", osm = """sl-blz-gh_OSM.csv""", index_number = 432, index_name = """FIPS""", scale_y = """no""")


print("Done.")