#!/usr/bin/env python
# coding: utf-8


###############################################################################
# CONTEXTUAL FEATURES REGRESSION
# using Random Forest Regressor or Elastic Net Regularized Regression
# with population density or OSM urban attributes as dependent variables
# 3-4_regression_spfeas-analysis.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University
# Portions of script based on work by Robert Harrison
# Portions of script created with assistance from Michael Mann

# This script is part 2 of 2, using the CSV files from part 1.
# The script builds a model using elastic net regularized regression (ENR)
# or random forest regression (RFR), with population or OSM urban attributes
# as the dependent variables and contextual features as the independent
# variables.

# """text""" Replace placeholder text with relevant text
###############################################################################


# Import modules
import pandas as pd
import numpy as np
from statistics import mean
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
from sklearn.linear_model import ElasticNetCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import time

# Start timer
start_time = time.time()


def import_correlation(y, image_type):
    '''This function imports the scaled dependent and independent variables.'''
    
    print("\n\n=============================================\n\n")
    print("IMPORTING CSV")
    
    # Create file name
    # Change as necessary to import files *
    scaled_csv = image_type + "_" + y + "_scaled_csv.csv"
    print("Importing {}...".format(scaled_csv))
    
    # Convert csv to dataframe
    scaled_df = pd.read_csv(scaled_csv, index_col=0)
    # print(scaled_df.head())
    
    # Set x and y variables
    x_vars = list(scaled_df.columns[1:])
    y_var = scaled_df.columns[0]
    
    # Return variables for next function 
    return x_vars, y_var, scaled_df


def rfr(seed_range, x_vars, y_var, scaled_df, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, y, image_type, dep_var):
    '''This function runs the random forest regression.'''

    print("\n\n=============================================\n\n")
    print("RANDOM FOREST")
    
    # Set dependent variable as a key in the dictionaries
    # Values are results of analysis
    Y_Statistics[y_var] = {}
    Y_Summary_Statistics[y_var] = {}
    
    # Set dependent variable as a key in Models dictionary,
    # used to store each result object
    Models[y_var] = {}
    
    # Set dependent variable as a key in Coefficients dictionary,
    # used to store variables and coefficients as determined by RF regression
    Coefficients[y_var] = {}
    
    # Create empty lists
    in_sample_R2_list = []
    out_of_sample_R2_list = []
    out_of_sample_mse_y_list = []
    out_of_sample_mae_y_list = []
    out_of_sample_mape_y_list = []
    
    print("\n\n")
    
    # Run RF regression for each seed
    for i in seed_range:
        print("Setting random seed to {}...".format(i))
        
        # Set seed
        np.random.seed(i)
        
        # Split the data, with 80% to train and 20% to test
        print("Splitting the data into 80% to train and 20% to test...")
        X_train, X_test, y_train, y_test = train_test_split(scaled_df[x_vars],
                                                            scaled_df[y_var],
                                                            test_size = 0.20)
        
        # Print dimensions of train and test variables
        print("The dimension of the training X values is {}.".format(X_train.shape))
        print("The dimension of the testing X values is {}.".format(X_test.shape))
        print("The dimension of the training Y values is {}.".format(y_train.shape))
        print("The dimension of the testing Y values is {}.".format(y_test.shape))
        

        print("Performing GridSearchCV and RandomForestRegressor...")
        # Set up RandomForestRegressor estimaor
        rf_estimator = RandomForestRegressor(bootstrap = True,
                                             n_jobs = -1,
                                             #random_state = i,
                                             verbose = False)
        
        # Run GridSearchCV with various parameters to optimize for
        # RandomForestRegressor
        # GridSearchCV runs RandomForestRegressor, so no need to take
        # parameters and run RFR again
        gsc = GridSearchCV(estimator = rf_estimator, #RandomForestRegressor(),
                   param_grid = {'n_estimators': [200, 300, 500, 700, 900, 1000],
                                 'min_samples_leaf': [1, 2, 5, 10, 25],
                                 'max_features': ["auto", "sqrt", "log2", 0.33, 0.20, 0.10, None]},
                   cv = 5,
                   scoring = 'neg_mean_squared_error',
                   verbose = False,
                   n_jobs = -1)
        
        # Obtain parameters by fitting training data
        grid_result = gsc.fit(X_train, y_train)
        
        # Obtain random forest regressor and the best estimators
        # This step is optional and only done for clarity.
        # grid_result can also be used to calculate r^2, etc.
        rf_result = grid_result.best_estimator_
        
        # Save model
        joblib.dump(value = rf_result,
                    filename = image_type + "_" + y + "_" + str(i) + "_rfr_" + dep_var + "_model.pkl",
                    compress = 3)
        
        
        best_parameters = grid_result.best_params_
        print("Here are the optimized parameters: ", best_parameters)
        
        # Fit model
        print("Fitting the model...")
        rf_result.fit(X_train,y_train)
        
        # Append the model to the Models dictionary, with seed number as
        # key and print
        Models[y_var][i] = rf_result
        print(rf_result)
        
        # Set variables based on the model "outputs"
        r_squared = rf_result.score(X_train, y_train)
        
        # Create empty dictionary within the existing dictionary, with
        # seed number as key
        Y_Statistics[y_var][i] = {}
        
        # Store the in-sample r^2 score in the output dictionary
        Y_Statistics[y_var][i]['In_Sample_R2'] = r_squared
        
        # Append r^2 to list
        in_sample_R2_list.append(r_squared)
        
        
        # Create dataframe of contextual features and their coefficients as
        # determined by RFR
        # Sort by absolute value of coefficients
        importance_column = "Importance_" + str(i)
        y_df = pd.DataFrame({'Feature': list(X_train.columns),
                             importance_column: rf_result.feature_importances_}).sort_values(importance_column, ascending = False)
        
        # Print top 10 model features and coefficients
        print("Top 10 Model Features and Coefficients")
        print(y_df.head(10))
        print("The dimension of this table is {}.".format(y_df.shape))

        
        # Delete model features whose coefficients are 0 to reduce
        # dataframe clutter (optional)
        '''
        for index, row in y_df.iterrows():
            
            if row['Coefficient'] == 0:
                print("Dropping {} from dataframe...".format(row['Feature']))
                y_df.drop(index, inplace = True)
                
            else:
                print("Keeping {} in dataframe...".format(row['Feature']))
        print("The dimension of this table is now {}.".format(y_df.shape))
        '''

        # Store coefficients in Coefficients dictionary, with seed number as key
        Coefficients[y_var][i] = y_df
        
        print("Testing the model...")
        # Predict y based on X test values
        y_pred = rf_result.predict(X_test)
        
        # Calculate out-of-sample r^2
        # This only uses the test sizes
        out_of_sample_r_squared = rf_result.score(X_test, y_test)
        
        # Calculate ouf-of-sample MSE 
        out_of_sample_mse_y = mse(y_test, y_pred)

        # Calculate ouf-of-sample MAE    
        out_of_sample_mae_y = mae(y_test, y_pred)
        
        # Calculate ouf-of-sample MAPE
        out_of_sample_mape_y = np.mean(abs((y_test - y_pred) / y_test)) * 100
       
        # Print statement of statistics
        print("Out of Sample R2: {:.2f}; Out of Sample MSE: {:.3f}; Out of Sample MAE: {:.3f}; MAPE {:.3f}"
              .format(out_of_sample_r_squared, out_of_sample_mse_y, out_of_sample_mae_y, out_of_sample_mape_y))
        
        # Add out-of-sample r^2, MSE, MAE, and MAPE to dictionary
        Y_Statistics[y_var][i]['Out_of_Sample R2'] = out_of_sample_r_squared
        Y_Statistics[y_var][i]['Out_of_Sample MSE'] = out_of_sample_mse_y
        Y_Statistics[y_var][i]['Out_of_Sample MAE'] = out_of_sample_mae_y
        Y_Statistics[y_var][i]['Out_of_Sample MAPE'] = out_of_sample_mape_y
        
        # Append out-of-sample r^2, MSE, MAE, and MAPE to lists
        out_of_sample_R2_list.append(out_of_sample_r_squared)
        out_of_sample_mse_y_list.append(out_of_sample_mse_y)
        out_of_sample_mae_y_list.append(out_of_sample_mae_y)
        out_of_sample_mape_y_list.append(out_of_sample_mape_y)
        
        # Print statistics for that seed iteration
        print("Here's the results summary for {}, with random seed {}:".format(y_var, i))
        print(Y_Statistics[y_var][i])
        
        print("\n\n---------------------------------------------\n\n")
    
    
    print("Calculating averages...")
    
    # Print out-of-sample r^2 list
    print("Out of sample R2 values:")
    print(out_of_sample_R2_list)
    
    # Calculate minimum, maximum, and average out-of-sample r^2 values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_R2"] = min(out_of_sample_R2_list)
    Y_Summary_Statistics[y_var]["Mean_Out_R2"] = mean(out_of_sample_R2_list)
    Y_Summary_Statistics[y_var]["Max_Out_R2"] = max(out_of_sample_R2_list)

    # Print MSE list
    print("Out of sample MSE values:")
    print(out_of_sample_mse_y_list)
    
    # Calculate minimum, maximum, and average out-of-sample MSE values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_MSE"] = min(out_of_sample_mse_y_list)
    Y_Summary_Statistics[y_var]["Mean_Out_MSE"] = mean(out_of_sample_mse_y_list)
    Y_Summary_Statistics[y_var]["Max_Out_MSE"] = max(out_of_sample_mse_y_list)
    
    # Print MAE list
    print("Out of sample MAE values:")
    print(out_of_sample_mae_y_list)
    
    # Calculate minimum, maximum, and average out-of-sample MAE values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_MAE"] = min(out_of_sample_mae_y_list)
    Y_Summary_Statistics[y_var]["Mean_Out_MAE"] = mean(out_of_sample_mae_y_list)
    Y_Summary_Statistics[y_var]["Max_Out_MAE"] = max(out_of_sample_mae_y_list)
    
    # Print MAPE list
    print("Out of sample MAPE values:")
    print(out_of_sample_mape_y_list)
    
    # Calculate minimum, maximum, and average out-of-sample MAPE values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_MAPE"] = min(out_of_sample_mape_y_list)
    Y_Summary_Statistics[y_var]["Mean_Out_MAPE"] = mean(out_of_sample_mape_y_list)
    Y_Summary_Statistics[y_var]["Max_Out_MAPE"] = max(out_of_sample_mape_y_list)
    
    # Print in-sample r^2 list
    print("In sample R2 values:")
    print(in_sample_R2_list)
    
    # Calculate minimum, maximum, and average in-sample r^2 values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_In_R2"] = min(in_sample_R2_list)
    Y_Summary_Statistics[y_var]["Mean_In_R2"] = mean(in_sample_R2_list)
    Y_Summary_Statistics[y_var]["Max_In_R2"] = max(in_sample_R2_list)
    
    
    # Print statistics for all seeds
    print("Here's the results for {}:".format(y_var))
    print(Y_Statistics[y_var])
    
    print("\n\n#######################\n\n")
    
    # Print summary statistics for all seeds
    print("Here's the summarized results for {}:".format(y_var))
    print(Y_Summary_Statistics[y_var])
    print("\n\n#######################\n\n")


def enr(seed_range, x_vars, y_var, scaled_df, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, y, image_type, dep_var):
    '''This function runs the elastic net regularized regression.'''
    
    print("\n\n=============================================\n\n")
    print("ELASTIC NET REGULARIZED REGRESSION")
    
    # Set dependent variable as a key in the dictionaries
    # Values are results of analysis
    Y_Statistics[y_var] = {}
    Y_Summary_Statistics[y_var] = {}
    
    # Set dependent variable as a key in Models dictionary,
    # used to store each result object
    Models[y_var] = {}
    
    # Set dependent variable as a key in Coefficients dictionary,
    # used to store variables and coefficients as determined by ENR regression
    Coefficients[y_var] = {}
    
    # Create empty lists
    in_sample_R2_list = []
    alpha_list = []
    l1_list = []
    out_of_sample_R2_list = []
    out_of_sample_mse_y_list = []
    out_of_sample_mae_y_list = []
    out_of_sample_mape_y_list = []
    
    print("\n\n")
    
    # Run ENR regression for each seed
    for i in seed_range:
        print("Setting random seed to {}...".format(i))
        
        # Set seed
        np.random.seed(i)
        
        # Set parameters for ElasticNetCV
        enet_result = ElasticNetCV(max_iter = 1e8,
                                   alphas = [0.0005, 0.001, 0.01, 0.03, 0.05, 0.1],
                                   l1_ratio = [.1, .5, .7, .9, .95, .99, 1],
                                   verbose = False,
                                   n_jobs = -1, 
                                   cv = 5, # 5-fold cross validatoin
                                   selection = 'random',
                                   fit_intercept = False)
        
        # Split the data, with 80% to train and 20% to test
        print("Splitting the data into 80% to train and 20% to test...")
        X_train, X_test, y_train, y_test = train_test_split(scaled_df[x_vars],
                                                            scaled_df[y_var],
                                                            test_size = 0.20)
        
        # Print dimensions of train and test variables
        print("The dimension of the training X values is {}.".format(X_train.shape))
        print("The dimension of the testing X values is {}.".format(X_test.shape))
        print("The dimension of the training Y values is {}.".format(y_train.shape))
        print("The dimension of the testing Y values is {}.".format(y_test.shape))
        
        # Fit model
        print("Fitting the model...")
        enet_result.fit(X_train,y_train)
        
        # Save model
        joblib.dump(value = enet_result,
                    filename = image_type + "_" + y + "_" + str(i) + "_enr_" + dep_var + "_model.pkl",
                    compress = 3)
        
        # Append the model to the Models dictionary, with seed number as
        # key and print
        Models[y_var][i] = enet_result
        print(enet_result)
        
        # Set variables based on the model "outputs"
        opt_alpha = enet_result.alpha_
        opt_l1_ratio = enet_result.l1_ratio_
        r_squared = enet_result.score(X_train, y_train)
        
        # Print update to ensure that the script is progressing properly (optional)
        # print("R2: {:.2f}; Alpha: {}; l1_ratio: {}".format(r_squared, opt_alpha, opt_l1_ratio))
        
        # Create empty dictionary within the existing dictionary, with seed
        # number as key
        Y_Statistics[y_var][i] = {}
        
        # Store the in-sample r^2 score, optimal alpha, and l1 ratio values in
        # the output dictionary
        Y_Statistics[y_var][i]['In_Sample_R2'] = r_squared
        Y_Statistics[y_var][i]['Alpha'] = opt_alpha
        Y_Statistics[y_var][i]['l1_ratio'] = opt_l1_ratio
        
        in_sample_R2_list.append(r_squared)
        alpha_list.append(opt_alpha)
        l1_list.append(opt_l1_ratio)
        
        # Create dataframe of contextual features and their coefficients as
        # determined by ENR
        # Sort by absolute value of coefficients
        importance_column = "Importance_" + str(i)
        y_df = pd.DataFrame([i for i in zip(list(scaled_df[x_vars].axes[1]), enet_result.coef_)], 
                            columns = ["Feature", importance_column]).sort_values(importance_column, ascending = False)
        
        # Print top 10 model features and coefficients
        print("Top 10 Model Features and Coefficients")
        print(y_df.head(10))
        print("The dimension of this table is {}.".format(y_df.shape))

        
        # Delete model features whose coefficients are 0 to reduce dataframe
        # clutter (optional)
        '''
        for index, row in y_df.iterrows():
            
            if row['Coefficient'] == 0:
                print("Dropping {} from dataframe...".format(row['Feature']))
                y_df.drop(index, inplace = True)
                
            else:
                print("Keeping {} in dataframe...".format(row['Feature']))
        print("The dimension of this table is now {}.".format(y_df.shape))
        '''

        # Store coefficients in Coefficients dictionary, with seed number as key
        Coefficients[y_var][i] = y_df
        
        print("Testing the model...")
        # Predict y based on X test values
        y_pred = enet_result.predict(X_test)
        
        # Calculate out-of-sample r^2 based
        out_of_sample_r_squared = enet_result.score(X_test,y_test)
        
        # Calculate out-of-sample MSE 
        out_of_sample_mse_y = mse(y_test, y_pred)
        
        # Calculate ouf-of-sample MAE    
        out_of_sample_mae_y = mae(y_test, y_pred)
        
        # Calculate ouf-of-sample MAPE
        out_of_sample_mape_y = np.mean(abs((y_test - y_pred) / y_test)) * 100
        
        # Print statement of statistics
        print("Out of Sample R2: {:.2f}; Out of Sample MSE: {:.3f}; Out of Sample MAE: {:.3f}; MAPE {:.3f}"
              .format(out_of_sample_r_squared, out_of_sample_mse_y, out_of_sample_mae_y, out_of_sample_mape_y))
        
        # Add out-of-sample r^2, MSE, MAE, and MAPE to dictionary
        Y_Statistics[y_var][i]['Out_of_Sample R2'] = out_of_sample_r_squared
        Y_Statistics[y_var][i]['Out_of_Sample MSE'] = out_of_sample_mse_y
        Y_Statistics[y_var][i]['Out_of_Sample MAE'] = out_of_sample_mae_y
        Y_Statistics[y_var][i]['Out_of_Sample MAPE'] = out_of_sample_mape_y
        
        # Append out-of-sample r^2, MSE, MAE, and MAPE to lists
        out_of_sample_R2_list.append(out_of_sample_r_squared)
        out_of_sample_mse_y_list.append(out_of_sample_mse_y)
        out_of_sample_mae_y_list.append(out_of_sample_mae_y)
        out_of_sample_mape_y_list.append(out_of_sample_mape_y)
        
        # Print statistics for that seed iteration
        print("Here's the results summary for {}, with random seed {}:".format(y_var, i))
        print(Y_Statistics[y_var][i])
        
        print("\n\n---------------------------------------------\n\n")    
    
    print("Calculating averages...")
    
    # Print out-of-sample r^2 list
    print("Out of sample R2 values:")
    print(out_of_sample_R2_list)
    
    # Calculate minimum, maximum, and average out-of-sample r^2 values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_R2"] = min(out_of_sample_R2_list)
    Y_Summary_Statistics[y_var]["Mean_Out_R2"] = mean(out_of_sample_R2_list)
    Y_Summary_Statistics[y_var]["Max_Out_R2"] = max(out_of_sample_R2_list)

    # Print out-of-sample MSE list
    print("Out of sample MSE values:")
    print(out_of_sample_mse_y_list)
    
    # Calculate minimum, maximum, and average out-of-sample MSE values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_MSE"] = min(out_of_sample_mse_y_list)
    Y_Summary_Statistics[y_var]["Mean_Out_MSE"] = mean(out_of_sample_mse_y_list)
    Y_Summary_Statistics[y_var]["Max_Out_MSE"] = max(out_of_sample_mse_y_list)

    # Print MAE list
    print("Out of sample MAE values:")
    print(out_of_sample_mae_y_list)
    
    # Calculate minimum, maximum, and average out-of-sample MAE values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_MAE"] = min(out_of_sample_mae_y_list)
    Y_Summary_Statistics[y_var]["Mean_Out_MAE"] = mean(out_of_sample_mae_y_list)
    Y_Summary_Statistics[y_var]["Max_Out_MAE"] = max(out_of_sample_mae_y_list)
    
    # Print MAPE list
    print("Out of sample MAPE values:")
    print(out_of_sample_mape_y_list)
    
    # Calculate minimum, maximum, and average out-of-sample MAPE values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_Out_MAPE"] = min(out_of_sample_mape_y_list)
    Y_Summary_Statistics[y_var]["Mean_Out_MAPE"] = mean(out_of_sample_mape_y_list)
    Y_Summary_Statistics[y_var]["Max_Out_MAPE"] = max(out_of_sample_mape_y_list)
    
    # Print in-sample r^2 list
    print("In sample R2 values:")
    print(in_sample_R2_list)
    
    # Calculate minimum, maximum, and average in-sample r^2 values and
    # add to dictionary
    Y_Summary_Statistics[y_var]["Min_In_R2"] = min(in_sample_R2_list)
    Y_Summary_Statistics[y_var]["Mean_In_R2"] = mean(in_sample_R2_list)
    Y_Summary_Statistics[y_var]["Max_In_R2"] = max(in_sample_R2_list)
    
    # Print alpha list
    print("Alpha values:")
    print(alpha_list)
    
    # Calculate minimum, maximum, and average alpha values and add to dictionary
    Y_Summary_Statistics[y_var]["Min_alpha"] = min(alpha_list)
    Y_Summary_Statistics[y_var]["Mean_alpha"] = mean(alpha_list)
    Y_Summary_Statistics[y_var]["Max_alpha"] = max(alpha_list)
    
    # Print l1 list
    print("L1 values:")
    print(l1_list)
    
    # Calculate minimum, maximum, and average alpha values and add to dictionary
    Y_Summary_Statistics[y_var]["Min_l1"] = min(l1_list)
    Y_Summary_Statistics[y_var]["Mean_l1"] = mean(l1_list)
    Y_Summary_Statistics[y_var]["Max_l1"] = max(l1_list)
    
    
    # Print statistics for all seeds
    print("Here's the results for {}:".format(y_var))
    print(Y_Statistics[y_var])
    
    print("\n\n#######################\n\n")
    # Print summary statistics for all seeds
    print("Here's the summarized results for {}:".format(y_var))
    print(Y_Summary_Statistics[y_var])
    print("\n\n#######################\n\n")


def output_excel(image_type, y_var, Y_Statistics, y_summary_statistic_dictionary_list, Y_Summary_Statistics, Coefficients, method):
    '''This function converts summarized statistics to Excel files
    for easier viewing.'''

    print("\n\n=============================================\n\n")
    print("CONVERT TO EXCEL")
    
    # Iterate through each y variable's statistics (R^2, MSE, etc) to
    # create one Excel file
    print("Working on each seed for each variable's statistics...")
    for key in Y_Statistics:
        
        # Create empty list
        seed_output_list = []
        
        # Extract seed values (which are dictionaries) from the y variable key
        y_stat_key = Y_Statistics[key]
        
        # Iterate through each seed in the extracted dictionary
        for seed_key in y_stat_key:
            
            # Extract values from the seed key
            seed_key_elements = y_stat_key[seed_key]
            
            # Convert extracted values to dataframe
            seed_key_df = pd.DataFrame(seed_key_elements, index = [seed_key])
            
            # Append dataframe to list
            seed_output_list.append(seed_key_df)
        
        # Print list (optional)
        # print(seed_output_list)

        # Merge all the dataframes in the list
        seed_df = pd.concat(seed_output_list)
    
        # Print dataframe
        print("Here's the merged dataframe that will be converted to an Excel spreadsheet:")
        print(seed_df)
        
        # Convert to Excel spreadsheet
        # Optional
        print("Converting to Excel...")
        seed_df.to_excel(excel_writer = image_type + "_" + method + "_" + key + "_seed_output.xlsx",
                         header = True,
                         index = True,
                         index_label = "seed")
        
    
    # Iterate through each y variable
    print("Working on each seed for each variable's coefficients...")
    for key in Coefficients:
        
        # Extract seed values (which are dictionaries) from the y variable key
        coefficient_key = Coefficients[key]
        
        # Create empty list that will be used to store coefficients for each seed
        seed_coefficient_df_list = []
        
        # Iterate through each seed in the extracted dictionary
        for seed_key in coefficient_key:
            
            # Extract values from the seed key
            seed_key_coefficient_elements = coefficient_key[seed_key]
            
            # Convert extracted values to dataframe
            seed_coefficient_df = pd.DataFrame(seed_key_coefficient_elements).set_index("Feature")
            print(seed_coefficient_df.head(5))
            
            # Apend each seed's coefficients to list
            seed_coefficient_df_list.append(seed_coefficient_df)

            # Convert to Excel spreadsheet (optional)
            '''
            print("Converting to Excel...")
            seed_coefficient_df.to_excel(excel_writer = image_type + "_" + method + "_" + key + "_" + str(seed_key) + "_importance.xlsx",
                                         header = True,
                                         index = True,
                                         index_label = "Feature_Index")
            '''

        # Concatenate all seed dataframes
        print("Concatenating dataframes...")
        merged_coefficient_df = pd.concat(seed_coefficient_df_list, axis = 1, sort = True)
        print(merged_coefficient_df.head(5))
        
        # Calculate minimum, mean, and maximum for dataframe by row and convert them to dataframes
        print("Calculating statistics...")
        merged_coefficient_df["mean"] = merged_coefficient_df.mean(axis = 1)
        merged_coefficient_df["min"] = merged_coefficient_df.min(axis = 1) # Be careful, this will pull from df which now includes mean
        merged_coefficient_df["max"] = merged_coefficient_df.max(axis = 1) # Ibid.
        
        # Sort by mean
        merged_coefficient_df = merged_coefficient_df.sort_values("mean", ascending = False)
        
        # Save to Excel
        print("Converting to Excel...")
        merged_coefficient_df.to_excel(excel_writer = image_type + "_" + method + "_" + key + "_summary_importance.xlsx",
                                       header = True,
                                       index = True,
                                       index_label = "Feature_Index")
        
    # Call the dictionary within each key, converts it to a dataframe, and
    # appends it to a list
    print("Working on summary statistics for each variable...")
    for key in Y_Summary_Statistics:
        
        # Extract values (which are dictionaries) from the y variable key
        y_sum_stat_key = Y_Summary_Statistics[key]
        
        # Convert extracted values to daaframe
        y_sum_stat_key_df = pd.DataFrame(y_sum_stat_key, index = [key])
        
        # Append dataframe to list
        y_summary_statistic_dictionary_list.append(y_sum_stat_key_df)

    # Print list (optional)        
    # print(y_summary_statistic_dictionary_list)
    
    # Merge all the dataframes in the list
    y_summary_statistic_df = pd.concat(y_summary_statistic_dictionary_list)
    
    # Print dataframe
    print("Here's the merged dataframe that will be converted to an Excel spreadsheet:")
    print(y_summary_statistic_df)
    
    # Convert to Excel spreadsheet
    print("Converting to Excel...")
    y_summary_statistic_df.to_excel(excel_writer = image_type + "_" + method + "_y_summary_stats.xlsx",
                                    header = True,
                                    index = True,
                                    index_label = "y_variable")
    
    # Return variables
    return seed_df, y_summary_statistic_df
    
    
# This is the main function that calls the other functions
def main(image_type, dep_var, method = "rfr"):
    '''This is the main function that runs the script and calls the other
    functions.'''
    
    # Create empty dictionaries
    Y_Statistics = {}
    Y_Summary_Statistics = {}
    Models = {}
    Coefficients = {}
    
    # Create empty list
    y_summary_statistic_dictionary_list = []
    
    # Set random seed
    # NB: If range, does not include the last number
    # NB: If one number or a series of numbers, put in a list using [] *
    seed_range = range(1, 101)
    
    # Select dependent variables based on user specification
    if dep_var.lower() == "pop":
        
        # Choose population variable names
        dep_var_list = ["pop_density_m"]
        
    elif dep_var.upper() == "OSM":
        
        # Choose OSM variable names
        dep_var_list = ["BUILD_DEN", "BUILTUP_AREA", "BUILTUP_DEN_PRCNT", "COUNT_BUILD", "RD_AREA", "RD_DEN", "RD_LENGTH", "SUM_BUILD_AREA"]
    
    else:
        
        # Raise error if dependent variable not specified
        raise Exception("Specify the dependent variable!")
    
    # For loop iterates through each CSV file
    for y in dep_var_list:
        
        # Import CSV file
        x_vars, y_var, scaled_df = import_correlation(y, image_type)
        
        # Select method based on user specification
        if method == "rfr":

            # Run RF regression
            rfr(seed_range, x_vars, y_var, scaled_df, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, y, image_type, dep_var)
        
        elif method == "enr":

            # Run ENR regression
            enr(seed_range, x_vars, y_var, scaled_df, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, y, image_type, dep_var)
        
        else:
            
            # Raise error if method not specified
            raise Exception("Select either ENR or RFR as a method!")

    # Export to Excel spreadsheets
    seed_df, y_summary_statistic_df = output_excel(image_type, y_var, Y_Statistics, y_summary_statistic_dictionary_list, Y_Summary_Statistics, Coefficients, method)
    
    print("\n\n=============================================\n\n")
    
    # Return variables
    # return y_dict, Y_Statistics, Y_Summary_Statistics, Models, Coefficients, seed_df, y_summary_statistic_df


# Run script
# Image type is the country, dependent variable is either "pop" or "OSM",
# and method is either "enr" or "rfr"

main(image_type = """sl""", dep_var = "OSM", method = "enr")
main(image_type = """blz""", dep_var = "OSM", method = "enr")
main(image_type = """gh""", dep_var = "OSM", method = "enr")
main(image_type = """sl-blz-gh""", dep_var = "OSM", method = "enr")

main(image_type = """sl""", dep_var = "OSM", method = "rfr")
main(image_type = """blz""", dep_var = "OSM", method = "rfr")
main(image_type = """gh""", dep_var = "OSM", method = "rfr")
main(image_type = """sl-blz-gh""", dep_var = "OSM", method = "rfr")

main(image_type = """sl""", dep_var = "pop", method = "enr")
main(image_type = """blz""", dep_var = "pop", method = "enr")
main(image_type = """gh""", dep_var = "pop", method = "enr")
main(image_type = """sl-blz-gh""", dep_var = "pop", method = "enr")

main(image_type = """sl""", dep_var = "pop", method = "rfr")
main(image_type = """blz""", dep_var = "pop", method = "rfr")
main(image_type = """gh""", dep_var = "pop", method = "rfr")
main(image_type = """sl-blz-gh""", dep_var = "pop", method = "rfr")


print("Done.")

# Stop timer and print total time in seconds
end_time = time.time()
print("{} seconds".format(end_time - start_time))