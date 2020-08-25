#!/usr/bin/env python
# coding: utf-8


###############################################################################
# POPULATION DENSITY vs CONTEXTUAL FEATURES
# Data Preparation
# 3-3_regression_population-spfeas-prepare.py

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
# contextual features CSV, shape CSV that gives the geometry of each shapefile
# record in meters, and population counts CSV. All CSVs should have a record
# for each census tract.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import pandas as pd
import scipy.stats as stats
from sklearn import preprocessing
import os


def merge(csv_list, country, key, contextual_features, shape, population):
    '''This function imports, modifies, and combines CSV files.'''
    
    # Set population density column name
    pop_density = "pop_density_m"
    
    print("\n\n=============================================\n\n")
    print("IMPORT CSVs")
    print("Working on {}".format(country))
    
    # Read and load contextual features data into dataframe
    print("Importing contextual features data...")
    spfeas_df = pd.read_csv(contextual_features)
    spfeas_df[key] = spfeas_df[key].astype(int)
    spfeas_df = spfeas_df.set_index(key)
    # print(spfeas_df.head())
    
    # Read and load shape data into dataframe
    print("Importing shape data...")
    shape_df = pd.read_csv(shape)
    shape_df[key] = shape_df[key].astype(int)
    shape_df = shape_df.set_index(key)
    # print(shape_df.head())
    
    # Read and load population data into dataframe
    print("Importing population data...")
    population_df = pd.read_csv(population)
    population_df[key] = population_df[key].astype(int)
    population_df = population_df.set_index(key)
    # print(population_df.head())
    
    # Merge population and shape dataframes
    print("Merging population and shape data...")
    shp_pop_df = shape_df.merge(population_df, left_on = key, right_on = key, how = 'inner')
    # print(shp_pop_df.head())
    
    # Create population density column
    # Change column names as necessary *
    print("Creating population density column...")
    shp_pop_df[pop_density] = shp_pop_df["Population"] / shp_pop_df["area_m"]
    
    # Merge dataframe with contextual features dataframe
    print("Merging population density and contextual features...")
    cf_shp_pop_df = spfeas_df.merge(shp_pop_df, left_on = key, right_on = key, how = 'inner')
    # print(cf_shp_pop_df.head())
    
    # Remove columns
    # Change column names as necessary *
    cf_shp_pop_df = cf_shp_pop_df.drop(columns = ["area_m", "Population"])
    
    # Export to csv
    csv_file_name = country + "_pop_sf_RAW.csv"
    cf_shp_pop_df.to_csv(csv_file_name)
    
    # Append csv name to list
    csv_list.append(csv_file_name)
    
    # Print shape of merged dataframe
    print("The dimension of the merged table is {}.".format(cf_shp_pop_df.shape))
    
    # Return variable for next function
    return cf_shp_pop_df


def concat(csv_list, y_variable_index, index_name, ctry):
    '''This function concatenates the CSVs of multiple countries together.'''
    
    print("\n\n=============================================\n\n")
    print("CONCATENATE MULTIPLE COUNTRIES")
    
    # Create new list for merging country dataframes
    country_list = []
    
    # For loop reads each country dataframe and appends to a list
    for csv in csv_list:
        
        # Call combined zonal stats for each area
        # print(csv)
    
        # Read csv file into dataframe
        csv_df = pd.read_csv(csv)
    
        # Set index to GN
        csv_df.set_index(index_name, inplace = True)
        # print(csv_df.head(5))
    
        # Append dataframe to list
        country_list.append(csv_df)
        
    # Concatenate zonal stats csv files (must have same column names for
    # it to work)
    concat_country_dfs = pd.concat(country_list, sort = True)
    
    # As workaround, since concat will sort the variables, the dependent
    # variable will get moved to the middle this part copies the column into
    # a new column at the end and deletes the old column
    # Enter list of dependent variables backwards in line with y_variable_index
    ls_of_var = ["pop_density_m"] # taken from merge()
    new_name = ["pop_density"]
    
    # Select appropriate names
    select_ls_of_var = ls_of_var[y_variable_index]
    select_new_name = new_name[y_variable_index]
    
    # Copy column
    concat_country_dfs[select_new_name] = concat_country_dfs[select_ls_of_var]
    
    # Delete old column
    concat_country_dfs = concat_country_dfs.drop(columns = select_ls_of_var)
    
    # Print dataframe
    # print(concat_country_dfs.head(5))
    
    # Save to csv (too large for Excel)
    concat_country_dfs.to_csv(ctry + "_spfeas.csv")
    
    # Return variable for next function
    return concat_country_dfs


def get_variables(y_variable_index, index_number, joined_df):
    '''This function sets the independent and dependent variables.'''
    
    print("\n\nSET INDEPENDENT AND DEPENDENT VARIABLES")
    

    # Get the list of dependent variables from the dataframe to store in
    # list y_vars
    print("Obtaining dependent variable:")
    y_var = list(joined_df.axes[1])[y_variable_index] #axes1 = column
    # print(y_var)
    
    
    # Get a list of all independent variables from the dataframe in list all_x
    print("Obtaining independent variables:")
    all_x = list(joined_df.axes[1])[0:index_number]
    # print(all_x)
    
    # Return variables for next function
    return all_x, y_var, joined_df
        


# This function calculates correlations
def correlation(ctry, all_x, y_var, joined_df, y_dict):
    '''This function computes the correlations and only takes the top 200
    independent variables.'''
    
    print("\n\n=============================================\n\n")
    print("COMPUTE CORRELATIONS")
    
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
    joined_df[y_var] = joined_df[y_var].fillna(0)
    joined_df[y_var].isnull().values.any()

    # Create empty list
    x = []
    
    print("Calculating Pearson's r...")
    for x_var in all_x:
        
        # Calculate the Pearson statistics, 
        ## Returns the Pearson value and p value
        p = stats.pearsonr(joined_df[x_var],joined_df[y_var])
        
        # If p < 0.05, append to list x
        if p[1] < 0.05:
            x.append([x_var,abs(p[0]),p[0]])
    
    # List x is made into a dataframe, which is sorted by the absolute
    # values of the Pearson values
    x_df = pd.DataFrame(x, columns = ["x_var","abs_r","r"]).sort_values("abs_r", ascending = False)
    x_df.to_csv(ctry + "_" + y_var + "_PEARSON.csv")
    
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
    y_var_ydict_key = ctry + "_" + y_var
    y_dict[y_var_ydict_key] = list(x_df["x_var"][0:200])
    
    # Print top 200 variables based on Pearson's r
    print("The top 200 variables based on Pearson's r are:")
    print(y_dict[y_var_ydict_key])
    
    # Print shape for each key (y_var)
    for key in y_dict.keys():
        print("For {}, there are {} variables".format(key,len(y_dict[key])))
    
    
    print("\n\n=============================================\n\n")
    
    # Correlation Significance
    print("CORRELATION SIGNIFICANCE")
    
    # Get independent variables from the variable dictionary and store in
    # list x_vars
    x_vars = y_dict[y_var_ydict_key]
    
    # Build dataframe with the y variable as the first column and the top
    # 200 variables as the subsequent columns
    vars_df = pd.DataFrame()
    vars_df[y_var] = joined_df[y_var]
    
    # Add 200 variables to the dataframe
    for x_var in x_vars:
        vars_df[x_var] = joined_df[x_var]
    
    
    # Scale / normalize data
    print("Normalizing data...")
    standard_scaler = preprocessing.StandardScaler()
    names = vars_df.columns
    scaled_df = standard_scaler.fit_transform(vars_df)
    scaled_df = pd.DataFrame(scaled_df, columns = names)
    # print(scaled_df.head())
    print("The dimension of the scaled table is {}.".format(scaled_df.shape))
    
    # Convert dataframe to csv
    scaled_df.to_csv(ctry + "_" + y_var + "_scaled_csv.csv")
    
    # Return variables for next function 
    return joined_df, x_vars, y_var, y_dict, scaled_df


def main(countries, base_folder, index_name):
    '''This is the main function that runs the script and calls the other
    functions.'''
    
    # Create empty dictionaries
    y_dict = {}
    
    # Run functions for each y variable
    for y_variable_index in [-1]: #range(-8, 0):
        # Create list to store dataframes from merge()
        csv_list = []
        
        # Iterate through each country
        for ctry in countries:
            # Call merge function with parameters *
            cf_shp_pop_df = merge(csv_list,
                                  country = ctry,
                                  key = index_name,
                                  contextual_features = os.path.join(base_folder, ctry + "_spfeas.csv"),
                                  shape = os.path.join(base_folder, ctry + "_shape.csv"),
                                  population = os.path.join(base_folder, ctry + "_census.csv"))

            # Call function to set independent and dependent variables
            all_x, y_var, joined_df = get_variables(y_variable_index,
                                                    index_number = -1,
                                                    joined_df = cf_shp_pop_df)
            
            # Run correlation
            joined_df, x_vars, y_var, y_dict, scaled_df = correlation(ctry, all_x, y_var, joined_df, y_dict)
        
        
        # Only use this function if you are concatenating spfeas and
        # populations of 2+ countries together.
        # Otherwise, comment out the four lines below
        
        # Convert list into string separated by hypens
        ctry = "-".join(countries)

        country_list = concat(csv_list, y_variable_index, index_name, ctry)
        
        # Call function to set independent and dependent variables
        all_x, y_var, joined_df = get_variables(y_variable_index,
                                                index_number = -1,
                                                joined_df = country_list)

        # Run correlation
        joined_df, x_vars, y_var, y_dict, scaled_df = correlation(ctry, all_x, y_var, joined_df, y_dict)
        
        
    print("\n\n=============================================\n\n")
    
    # Return variables
    # return y_dict, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, seed_df, y_summary_statistic_df

# Run script
# Countries are the countries abbreviations for analysis, base folder is where
# the CSVs are saved, and inex name is the primary key column name *
main(countries = ["""sl""", """blz""", """gh"""], base_folder = r"""folder/""", index_name = """FIPS""")

print("Done.")