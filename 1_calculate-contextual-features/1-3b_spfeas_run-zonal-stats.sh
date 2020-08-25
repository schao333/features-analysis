#!/bin/bash

#SBATCH -p defq
#SBATCH -J zonal_stats
#SBATCH --export=NONE
#SBATCH -t 1-00:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=stevenchao@gwu.edu


export PATH="/groups/engstromgrp/anaconda3/bin:$PATH"
source activate Ryan_CondaEnvP2.7


###############################################################################
# RUN ZONAL STATISTICS
# 1-3b_spfeas_run-zonal-stats.py

# Created by: Steven Chao
# Fall 2019
# The George Washington University

# This script calculates the zonal statistics for the contextual feature
# outputs by running the Python script 1-3a_spfeas_zonal-stats.py.
###############################################################################


# Run the Python script
python 1-3a_spfeas_zonal-stats.py
