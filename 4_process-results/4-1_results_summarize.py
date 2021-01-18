#!/usr/bin/env python
# coding: utf-8


###############################################################################
# PROCESS RESULTS
# 4-1_results_summarize.py

# Created by: Steven Chao
# Fall 2020
# The George Washington University

# This script processes the results to aid in the analysis of the results. It
# processes the results by first separating each full feature output into its
# subcomponent, or sub-outputs. Within each area, it then groups each full
# feature output based on various sub-outputs to obtain the mean or the
# count (frequency) of each group. The top 6 or top 25 values are obtained
# (top 5 is actually analyzed, but top 6 is used to account for any ties).
# The script finally exports the results into an Excel file.
# This is essentially equivalent to using the Microsoft Excel Pivot Table
# feature.

# Input files required include: Pearson CSV, summary importance CSV, and
# summary statistics CSV

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import module
import pandas as pd
import os
import glob


def create_data_frame(df_list, files_corpus, urban = "", area = ""):
    '''This function reads in files, converts them to dataframes, and adds
    them to a list with an overarching urban and/or area group.'''

    # Check if user specified input for urban variable
    if len(urban) != 0:
        
        # Set variable, which will be used as key to pull from dictionary
        # and as a way to group rows together
    	urban_key = urban[1]
        
        # Check length of urban key
    	urban_specified = len(urban_key) != 0
    
    # Otherwise, set variables to relfect that user did not specify inputs
    else:
        urban_key = None
        urban_specified = False
    
    # Check if user specified input for urban variable
    if len(area) != 0:
        
        # Set variable, which will be used as key to pull from dictionary
        # and as a way to group rows together
    	area_key = area[1]
        
        # Check length of urban key
    	area_specified = len(area_key) != 0
        
    # Otherwise, set variables to relfect that user did not specify inputs
    else:
        area_key = None
        area_specified = False


    # Get file name, first using the urban key as key, then using area key
    # as key
    if urban_specified:
    	filepath = files_corpus[urban_key]
    elif area_specified:
    	filepath = files_corpus[area_key]
    else:
    	raise Exception("Fill out urban or area key!")
    
    
    # Try to read if CSV file
    try:
        df = pd.read_csv(filepath)
        
    # Otherwise, read in as Excel file
    except:
        df = pd.read_excel(filepath)
    
    # Add urban name as column and fill with urban key if specified
    if urban_specified:
    	df.loc[:, urban[0]] = urban_key
    else:
    	pass
    
    # Add area name as column and fill with area key if specified and if
    # the area and urban keys do not match
    if area_specified and urban_key != area_key:
        df.loc[:, area[0]] = area_key
    else:
        pass
    
    # Append dataframe to list
    df_list.append(df)
    
    # Return dataframe
    return df
    
def subset_group_clean(df, importance_subdict, feature_column_name, mean_absval_column, urban_group_column = "", area_group_column = ""):
    '''This function takes the input dataframe, subsets only the relevant
    columns, cleans and processes the column values, and groups rows as
    necessary. Finally, the importance statistics are summarized using
    different groups and stored.'''
    
    # Check if urban group column name is specified
    if len(urban_group_column) == 0:
        
        # If not specified, run as population analysis and subset only
        # relevant columns
        df = df.loc[:, [feature_column_importance, area_group_column, "mean"]]
    
    # If specified, run as OSM analysis
    else:
        
        # Subset only relevant columns
        df = df.loc[:, [feature_column_name, urban_group_column, area_group_column, "mean"]]
    
    # Create new column with the absolute value of the mean value
    # (used for sorting purposes)
    df.loc[:, mean_absval_column] = df["mean"].abs()

    # Call function to split full feature output names
    df = split_feature_names(df = df, feature_column_name = feature_column_name)
    
    # Create new dataframe by grouping by feature and then by output,
    # getting the mean for each group
    df_fo = df.groupby(["feature", "output"]).mean()
    
    # Create new column with the absolute value of the mean value
    # (used for sorting purposes)
    df_fo.loc[:, mean_absval_column] = df_fo["mean"].abs()

    # Create new dataframe by grouping by feature, getting the mean
    # for each group
    df_f = df.groupby(["feature"]).mean()
    
    # Create new column with the absolute value of the mean value
    # (used for sorting purposes)
    df_f.loc[:, mean_absval_column] = df_f["mean"].abs()


    # Summarize results using different categories and add to Importance
    # dictionary under each relevant key associated with the result
    ## full_5: top 5 full feature outputs by absolute value of mean
    ##         importance value (or coefficient)
    ## feature-output_5: top 5 feature-output pairs by absolute value of
    ##                   mean value
    ## feature_5: top 5 features by absolute value of mean value
    ## feature-freq_5: top 5 most common features within the top 25 full
    ##                 feature outputs sorted by absolute value of mean
    importance_subdict = {"full_5": df.sort_values(by = [mean_absval_column], ascending = False)[[feature_column_importance, "mean", mean_absval_column]].head(6).set_index(feature_column_importance),
                          "feature-output_5": df_fo.sort_values(by = mean_absval_column, ascending = False)[["mean"]].head(6).reset_index().set_index("feature"),
                          "feature_5": df_f.sort_values(by = mean_absval_column, ascending = False)[["mean"]].head(6),
                          "feature-freq_5": df.sort_values(by = [mean_absval_column], ascending = False).head(25).groupby(["feature"]).count().sort_values(by = feature_column_importance, ascending = False)[[feature_column_importance]].rename(columns = {feature_column_importance: "count"}).head(6)}
    
    # Return dataframes
    return df, df_fo, df_f, importance_subdict


def split_feature_names(df, feature_column_name):
    '''This function takes the full feature output name, cleans up the name,
    and subsequently splits the full name into its various sub-outputs. This
    will enable analyses by various groupings of the sub-outputs.'''
    
    # Create list of text that will be replaced
    # Order matters, text will be replaced following the order of the list
    replace_text = [["filter_", "filter-"],
                    ["line_contrast","line-contrast"],
                    ["max_line_length","max-line-length"],
                    ["min_line_length","min-line-length"],
                    ["line_length","line-length"],
                    ["line_mean","line-mean"],
                    ["max_ratio_of_orthgonal_angles","max-ratio-of-orthgonal-angles"],
                    ["_w_mean_", "_w-mean_"]]
    
    # Iterate through each row
    for index, row in df.iterrows():
        
        # Get full feature output name
        feature_full = row[feature_column_name]

        # Iterate through the list
        for i in range(len(replace_text)):
            
            # Check if text is in feature name
            if replace_text[i][0] in feature_full:
                
                # If it is, replace the text with the new text
                df.loc[index, feature_column_name] = feature_full.replace(replace_text[i][0], replace_text[i][1])
                
                # Break out of for loop (because a feature name will only have
                # one of these text elements in it)
                break
            
            # If not, then move onto next row
            else:
                pass
        
        # Get updated full feature output name    
        feature_full = df.loc[index, feature_column_name]
        
        # Split the output name into its sub-outputs, using underscore to split
        feature_elements = feature_full.split("_")
        
        # Create column names for sub-outputs
        feature_elements_columns = ["feature", "scale", "output", "zonal-stat"]
        
        # Iterate through each sub-output and assign each sub-output to its
        # respective column
        for j in range(len(feature_elements)):
            df.loc[index, feature_elements_columns[j]] = feature_elements[j]
    
    # Return dataframe
    return df


def one_sheet_excel(result, input_df, sheet_b, start_row, start_column, sheet_a = ""):
    '''This function takes multiple related dataframes and exports them into
    on3 Excel sheet, with each dataframe side by side horizontally.'''
    
    # Create a dataframe containing a header with the area name, used to
    # identify each section of data (as multiple dataframes will be placed
    # side by side)
    if len(sheet_a) == 0:
        
        # If sheet_a not specified, run as population analysis
        df_header = pd.DataFrame({"area": [sheet_b]}).set_index("area")
        
    else:
        
        # If sheet_a is specified, run as OSM analysis
        df_header = pd.DataFrame({"area": ["{}_{}".format(sheet_a, sheet_b)]}).set_index("area")
    
    # Write the header dataframe to the sheet
    df_header.to_excel(writer, sheet_name = result, startrow = start_row, startcol = start_column)
    
    # Increment start row counter by the number of rows in the header
    # dataframe to prevent overwrite
    start_row += df_header.shape[0] + 3

    # Create empty list to hold max widths of dataframes, which will be used
    # to calculate how much to offset each subsequent dataframe (as they will
    # be placed side by side on one sheet)
    max_width = []
    
    # Iterate through the first key of the inputted dictionary (note: inputted
    # dataframe might be a subset of the original dictionary)
    for sheet_c, frame_c in input_df[sheet_b].items():
        
        # Create a dataframe containing a subheader with the summary type
        # used to identify each subsection of data
        df_subheader = pd.DataFrame({"table": [sheet_c]}).set_index("table")
        
        # Write the header dataframe to the sheet
        df_subheader.to_excel(writer, sheet_name = result, startrow = start_row, startcol = start_column)
        
        # Increment start row counter by the number of rows in the header
        # dataframe to prevent overwrite
        start_row += df_subheader.shape[0] + 2
        
        # Write the dataframe to the sheet
        frame_c.to_excel(writer, sheet_name = result, startrow = start_row, startcol = start_column)
        
        # Increment start row counter by the number of rows in the dataframe
        # to prevent overwrite
        start_row += frame_c.shape[0] + 3
        
        
        # Add width of dataframe to list of max widths
        max_width.append(frame_c.shape[1])
    
    # Increment start column counter by the number of columns in the dataframe
    # to prevent overwrite
    start_column += max(max_width) + 4
    
    # Increment start row counter to use for second start row
    start_row += 3
    
    # Return start row and column counters for use in writing the next
    # dataframe (which will be horizontally next to the current dataframe)
    return start_row, start_column


# Set analysis type *
analysis = "population"
# analysis = "osm"

# Set binary variable based on population or OSM analysis
if analysis == "population":
    pop_anal = True
elif analysis == "osm":
    pop_anal = False

# Raise exception if population or OSM not specified
else:
    raise Exception("Choose a type of analysis!")


print("Looking for files pertaining to CONTEXTUAL FEATURES vs. {}...".format(analysis.upper()))
# This portion of the script gets the appropriate results filepaths from the
# regression analysis. The code assumes that the file structure used is
# similar to the one provided in the example (0-1_create-folders.py).

# If a different file structure is used, this portion can be re-written to
# accommodate any differences.

# Whatever the code used, the end result from this section should produce four
# dictionaries with the following structure (the number of "methods" and
# "areas" will be based on area_list and methods_list variables as defined
# below):

# files_dict
# {'Pearson': {'area': []},
#  'method': {'Importance': {'area': []},
#             'Statistics': {'area': []}}}
#
# pearson_dict
# {'area': {'full_5': [],
#           'feature-freq_5': []}}
#
# importance_dict
# {'method': {'area': {'full_5': [],
#                      'feature-output_5': [],
#                      'feature-output_5': [],
#                      'feature-freq_5': []}}}
#
# statistics_dict
# {'method': []}

# Here is another way to retrieve files; this method is sorted by area
# (key is area)
# This method is intially simpler but requires separating out the files
# for the subsequent processing (Pearson, importance, and statistics):

# for a in area_list:
#     files_dict[a] = [glob.glob(os.path.join(base_folder_path, "{}_pop_density*pearson*".format(a)))[0],
#                      glob.glob(os.path.join(base_folder_path, "enr", "{}_{}_y_summary_stats*".format(a2, method)))[0],
#                      glob.glob(os.path.join(base_folder_path, "enr", "{}_{}_pop_density*summary_importance*".format(a2, method)))[0],
#                      glob.glob(os.path.join(base_folder_path, "rfr", "{}_{}_y_summary_stats*".format(a2, method)))[0],
#                      glob.glob(os.path.join(base_folder_path, "rfr", "{}_{}_pop_density*summary_importance*".format(a2, method)))[0]]

# Check if population analysis is specified
if pop_anal:
    
    # Set base folder path containing the files for the population analysis *
    base_folder_path = r"""/pop"""

# Otherwise, OSM analysis is specified
else:
    
    # Set base folder path containing the files for the OSM analysis *
    base_folder_path = r"""/osm"""
    
    # Create list of urban attributes used in analysis
    urban_attributes_list = ["SUM_BUILD_AREA", "COUNT_BUILD", "BUILD_DEN", "RD_AREA", "RD_LENGTH", "RD_DEN", "BUILTUP_AREA", "BUILTUP_DEN_PRCNT"]

# Set list of areas used in analysis *
area_list = ["""blz""", """sl""", """gh""", """sl-blz-gh"""]

# Set list of methods used in analysis
methods_list = ["enr", "rfr"]


# Create empty dictionary to hold file paths
files_dict = dict()

# Create empty subdictionary with a key of Pearson
files_dict["Pearson"] = dict()

# Iterate through each area
for a in area_list:

    if pop_anal:
        
        # Get Pearson file for the area and put in subdictionary with area as
        # key *
        # Note: Might have to add "_m_" to some file names
        files_dict["Pearson"][a] = glob.glob(os.path.join(base_folder_path, "{}_pop_density*pearson*".format(a)))[0]
        
    else:
        
        # Create empty subdictionary with area as key
        files_dict["Pearson"][a] = dict()
        
        # Iterate through each urban attribute
        for urban in urban_attributes_list:
            
            # Get Pearson file for the urban attribute and put in
            # subdictionary with area and urban attribute as keys *
            files_dict["Pearson"][a][urban] = glob.glob(os.path.join(base_folder_path, "{}_{}_pearson*".format(a, urban)))[0]

    # Iterate through each method
    for method in methods_list:
            
        # Create empty subdictionary with method as key
        files_dict[method] = dict()
        
        # Create empty subdictionaries under the method key to hold Importance
        # and Statistics filepaths
        files_dict[method]["Importance"] = dict()
        files_dict[method]["Statistics"] = dict()
        
        # Iterate through each area
        for a2 in area_list:
            
            # Check if population analysis is specified
            if pop_anal:
                
                # Get Importance file for the method and put in subdictionary
                # with method and Importance as keys
                # Note: Might have to add "_m_" to some file names
                files_dict[method]["Importance"][a2] = glob.glob(os.path.join(base_folder_path, method, "{}_{}_pop_density*summary_importance*".format(a2, method)))[0]
                
                # Get Statistics file for the method and put in subdictionary
                # with method and Statistics as keys
                files_dict[method]["Statistics"][a2] = glob.glob(os.path.join(base_folder_path, method, "{}_{}_y_summary_stats*".format(a2, method)))[0]
            
            # Otherwise, OSM analysis is specified
            else:
               
                # Iterate through each method
                for method in methods_list:
                    
                    # Create empty subdictionary with method as key
                    files_dict[method] = dict()
                    
                    # Create empty subdictionaries under the method key
                    files_dict[method]["Importance"] = dict()
                    files_dict[method]["Statistics"] = dict()
                    
                    # Iterate through each area
                    for a2 in area_list:
                        
                        # Create empty subdictionary under the area key to hold
                        # Importance filepath
                        files_dict[method]["Importance"][a2] = dict()
                        
                        # Get Statistics file for the method and put in
                        # subdictionary with method and Statistics as keys
                        files_dict[method]["Statistics"][a2] = glob.glob(os.path.join(base_folder_path, method, "{}_{}_y_summary_stats*".format(a2, method)))[0]

                        
                        # Iterate through each urban attribute
                        for urban in urban_attributes_list:

                            # Get Importance file for the method and put in
                            # subdictionary with method, Importance, and
                            # urban attribute as keys
                            files_dict[method]["Importance"][a2][urban] = glob.glob(os.path.join(base_folder_path, method, "{}_{}_{}_summary_importance*".format(a2, method, urban)))[0]
                            

# Set urban column variable, which will be used to group rows
urban_group_column = "urban"

# Set area column variable, which will be used to group rows
area_group_column = "area"

# Set column name used to hold the full feature output names in the Pearson
# dataframe
feature_column_pearson = "x_var"

# Set column name used to hold the absolute value of the mean importance
mean_absval_column = "mean-absoluteval"

# Set column name used to hold the full feature output names in the importance
# dataframe
feature_column_importance = "Feature_Index"


print("\n\nProcessing Pearson's r results...")
# Create empty dictionary to hold processed Pearson results
pearson_dict = dict()

# Create empty list to hold dataframes (can be used if want to concatenate and
# export combined dataframes)
pearson_df_list = []

# Iterate through each area key in the files dictionary under the Pearson key
for area in files_dict["Pearson"]:
    
    # Check if population analysis is specified
    if pop_anal:
        # Call function to create dataframe
        df = create_data_frame(df_list = pearson_df_list, files_corpus = files_dict["Pearson"], area = (area_group_column, area))
        
        # Call function to split full feature output names
        df = split_feature_names(df = df, feature_column_name = feature_column_pearson)

        # Summarize results and add to Pearson dictionary under the area key
        ## full_5: top 5 full feature outputs by absolute value of Pearson's r
        ## feature-freq_5: top 5 most common features within the top 200
        ##                 features sorted by Pearson's r
        pearson_dict[area] = {"full_5": df.sort_values(by = ["abs_r"], ascending = False).head(200)[[feature_column_pearson, "r", "abs_r"]].head(6).set_index(feature_column_pearson),
                              "feature-freq_5": df.sort_values(by = ["abs_r"], ascending = False).head(200).groupby(["feature"]).count().sort_values(by = feature_column_pearson, ascending = False)[[feature_column_pearson]].rename(columns = {feature_column_pearson: "count"}).head(6)}
    
    # Otherwise, OSM analysis is specified
    else:
    
        # Create empty subdictionary with area as key
        pearson_dict[area] = dict()
        
        # Iterate through each urban attribute
        for urban in urban_attributes_list:
        
            # Call function to create dataframe
            df = create_data_frame(df_list = pearson_df_list, files_corpus = files_dict["Pearson"][area], urban = (urban_group_column, urban))
            
            # Call function to split full feature output names
            df = split_feature_names(df = df, feature_column_name = feature_column_pearson)

            # Summarize results and add to Pearson dictionary under the area
            # and urban attribute keys
            ## full_5: top 5 full feature outputs by absolute value of
            ##         Pearson's r
            ## feature-freq_5: top 5 most common feature within the top 200
            ##                 features sorted by Pearson's r
            pearson_dict[area][urban] = {"full_5": df.sort_values(by = ["abs_r"], ascending = False).head(200)[[feature_column_pearson, "r", "abs_r"]].head(6).set_index(feature_column_pearson),
                                         "feature-freq_5": df.sort_values(by = ["abs_r"], ascending = False).head(200).groupby(["feature"]).count().sort_values(by = feature_column_pearson, ascending = False)[[feature_column_pearson]].rename(columns = {feature_column_pearson: "count"}).head(6)}


print("Processing importance results...")
# Create empty dictionary to hold processed Importance results
importance_dict = dict()

# Check if population analysis is specified
if pop_anal:
    
    # Create empty list to hold dataframes (can be used to concatenate and
    # export combined dataframes)
    importance_df_list = []
    
# Otherwise, OSM analysis is specified and pass
else:
    pass

# Iterate through each method
for method in methods_list:
    
    # Check if population analysis is not specified (OSM is specified)
    if not pop_anal:
        
        # Create empty list to hold dataframes (can be used to concatenate and
        # export combined dataframes)
        importance_df_list = []
        importance_25_df_list = []
    
    # Otherwise, population analysis is specified and pass
    else:
        pass
    
    # Create empty subdictionary with method as key
    importance_dict[method] = dict()
        
    # Iterate through each area key in the files dictionary under the method
    # and Importance keys
    for area in files_dict[method]["Importance"]:
        
        # Check if population analysis is specified
        if pop_anal:
            
            # Call function to create dataframe
            df = create_data_frame(df_list = importance_df_list, files_corpus = files_dict[method]["Importance"], area = (area_group_column, area))
            
            # Create empty subdictionary with method and area as keys
            importance_subdict = importance_dict[method][area] = dict()
            
            # Call function to subset and process dataframe and to summarize
            # the results by the various groups
            df, df_fo, df_f, importance_subdict = subset_group_clean(df = df, importance_subdict = importance_subdict, feature_column_name = feature_column_importance, mean_absval_column = mean_absval_column, urban_group_column = "", area_group_column = area_group_column)
            
            # Update the subdictionary with the dictionary produced from the
            # previous function (which has the summarized results)
            importance_dict[method][area] = importance_subdict
            
            # Delete variable
            del importance_subdict
        
        # Otherwise, OSM analysis is specified
        else:
        
            # Create empty subdictionary with method and area as keys
            importance_dict[method][area] = dict()
            
            # Iterate through each urban attribute
            for urban in urban_attributes_list:
                
                # Call function to create dataframe
                df = create_data_frame(df_list = importance_df_list, files_corpus = files_dict[method]["Importance"][area], urban = (urban_group_column, urban), area = (area_group_column, area))
                
                # Create empty subdictionary with method, area, and urban
                # attribute as keys
                importance_subdict = importance_dict[method][area][urban] = dict()
                
                # Call function to subset and process dataframe and to
                # summarize the results by the various groups
                df, df_fo, df_f, importance_subdict = subset_group_clean(df = df, importance_subdict = importance_subdict, feature_column_name = feature_column_importance, mean_absval_column = mean_absval_column, urban_group_column = urban_group_column, area_group_column = area_group_column)
                
                # Update the subdictionary with the dictionary produced from
                # the previous function (which has the summarized results)
                importance_dict[method][area][urban] = importance_subdict
                
                # Delete variable
                del importance_subdict
                
                # Get the top 25 full feature outputs by absolute value of
                # mean importance value (or coefficient) and append to list
                importance_25_df_list.append(df.sort_values(by = [mean_absval_column], ascending = False).head(25))
            
    # Concatenate dataframe of all values
    df_c_importance = pd.concat(importance_df_list, ignore_index = True)
    
    # Check if population analysis is not specified (OSM is specified)
    if not pop_anal:
        
        # Concatenate dataframe consisting of the top 25 full feature outputs
        df_c_importance_25 = pd.concat(importance_25_df_list, ignore_index = False)

        # Create subdictionary to hold overall importance processed results
        all_importance_sub_dict = importance_dict[method]["all"] = dict()

        # Call function to split full feature output names
        df_c_importance = split_feature_names(df = df_c_importance, feature_column_name = feature_column_importance)
        
        # Get top 5 most common features from all full feature outputs
        all_importance_sub_dict["feature-freq_5-all"] = {"all": df_c_importance.groupby([area_group_column, "feature"]).count().sort_values(by = [area_group_column, feature_column_importance], ascending = False)[[feature_column_importance]].rename(columns = {feature_column_importance: "count"}).groupby(area_group_column).head(6).reset_index().set_index(area_group_column)}
        
        #  Get top 5 most common features from the top 25 full feature outputs
        all_importance_sub_dict["feature-freq_5-top25"] = {"top-25": df_c_importance_25.groupby([area_group_column, "feature"]).count().sort_values(by = [area_group_column, feature_column_importance], ascending = False)[[feature_column_importance]].rename(columns = {feature_column_importance: "count"}).groupby(area_group_column).head(6).reset_index().set_index(area_group_column)}
    
    # Otherwise, population analysis is specified and pass
    else:
        pass


print("Processing statistics results...")
# Create empty dictionary to hold processed statistics results
statistics_dict = dict()

# Iterate through each method
for method in methods_list:
    
    # Create empty list to hold dataframes
    statistics_df_list = []
    
    # Iterate through each area key in the files dictionary under the method
    # and Statistics keys
    for area in files_dict[method]["Statistics"]:
        
        # Call function to create dataframe
        df = create_data_frame(df_list = statistics_df_list, files_corpus = files_dict[method]["Statistics"], area = (area_group_column, area))
        
    # Concatenate dataframes together
    df_c_statistics = pd.concat(statistics_df_list, ignore_index = True)
    
    # Set the index to the area
    df_c_statistics.set_index(area_group_column, inplace = True)
    
    # Add combined dataframe to Statistics dictionary under the method key
    statistics_dict[method] = df_c_statistics
  

# Export dataframes in dictionary to Excel file
with pd.ExcelWriter(os.path.join(base_folder_path, "summarized_{}_results.xlsx".format(analysis)), engine = "xlsxwriter") as writer:

    print("\n\nExporting processed statistics results...")
    # Iterate through each key and value in Statistics dictionary
    for sheet, frame in statistics_dict.items():
        
        # Write to sheet
        frame.to_excel(writer, sheet_name = "stats_{}".format(sheet))
        
    print("Exporting processed importance results...")
    # Iterate through each key (methods) and value in Importance dictionary
    for sheet, frame in importance_dict.items(): # Keys are methods
        
        # Set start column and start row, used for determining the column
        # and the row where the dataframe will start
        start_column = 0
        start_row = 0
        
        # Iterate through each subkey (areas) and value under the method key
        # in the Importance dictionary
        for sheet2, frame2 in importance_dict[sheet].items():
            
            # Check if population analysis is specified
            if pop_anal:
                
                # Call function to export dataframes onto one sheet
                second_start_row, start_column = one_sheet_excel(result = "importance_{}".format(sheet), input_df = importance_dict[sheet], sheet_a = "", sheet_b = sheet2, start_row = start_row, start_column = start_column)
            
            # Otherwise, OSM analysis is specified
            else:
            
                # Iterate through each subkey (urban attribute) and value under
                # the area key in the Importance dictionary
                for sheet3, frame3 in importance_dict[sheet][sheet2].items():
            
                    # Call function to export dataframes onto one sheet
                    second_start_row, start_column = one_sheet_excel(result = "importance_{}".format(sheet), input_df = importance_dict[sheet][sheet2], sheet_a = sheet2, sheet_b = sheet3, start_row = start_row, start_column = start_column)
                
                # Reset start column
                start_column = 0
                
                # Update start row number for second start row
                start_row = second_start_row
            
            
    print("Exporting processed Pearson's r results...")
    # Set start column and start row, used for determining the column and
    # the row where the dataframe will start
    start_column = 0
    start_row = 0
    
    # Iterate through each key (area) and value in Importance dictionary
    for sheet, frame in pearson_dict.items():
        
        # Check if population analysis is specified
        if pop_anal:
            
            # Call function to export dataframes onto one sheet
            second_start_row, start_column = one_sheet_excel(result = "pearson", input_df = pearson_dict, sheet_a = "", sheet_b = sheet, start_row = start_row, start_column = start_column)
        
        # Otherwise, OSM analysis is specified
        else:
            
            # Iterate through each subkey (urban attribute) and value under
            # the area key in the Importance dictionary
            for sheet2, frame2 in pearson_dict[sheet].items():
            
                # Call function to export dataframes onto one sheet
                second_start_row, start_column = one_sheet_excel(result = "pearson", input_df = pearson_dict[sheet], sheet_a = sheet, sheet_b = sheet2, start_row = start_row, start_column = start_column)
            
            # Reset start column
            start_column = 0
            
            # Update start row number for second start row
            start_row = second_start_row
    
    # Save file
    writer.save()


print("\n\nDone.")