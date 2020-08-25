#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# COMBINE DATA FROM MULTIPLE COUNTRIES
# 3-1_regression_combine-country-data.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script combines data from multiple countries into one CSV file. If
# files are already combined or do not need to be combined, then this script
# is not necessary.

# Input files should have the same primary key. Input files can be contextual
# features data, population data, etc.

# * Change as necessary
# """text""" Replace placeholder text with relevant text
###############################################################################


# Import module
import pandas as pd

print("Importing CSV files...")
# Read in CSVs for each country, setting first column as the index
df1 = pd.read_csv(r"""csv1.csv""", index_col = 0)
df2 = pd.read_csv(r"""csv2.csv""", index_col = 0)
df3 = pd.read_csv(r"""csv3.csv""", index_col = 0)

# Print shape of all dataframes
print(df1.shape, df2.shape, df3.shape)

print("Concatenating CSV files into one...")
# Combine all dataframes together
df4 = pd.concat([df1, df2, df3], sort=True)

# Print shape of new dataframe
print(df4.shape)

print("Exporting concatenated CSV file...")
# Export new dataframe
df4.to_csv(r"""csv_combined.csv""")

print("\n\nDone")