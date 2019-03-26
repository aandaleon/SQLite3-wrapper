# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:26:45 2019
#Solution to example python queries
#Run this program with: python practice_python_queries/Angela_solution_to_query_example.py --genenames practice_python_queries/genenames.txt
@author: Angela
"""

import argparse
import numpy as np
import sqlite3
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--genenames", type = str, action = "store", dest = "genenames", required = False, default = "genenames.txt", help = "File containing gene names.") #"practice_python_queries/genenames.txt"
args = parser.parse_args()

path = "db/gtex_v7_Whole_Blood_imputed_europeans_tw_0.5_signif.db" #which .db are we querying?
genenames = np.loadtxt(args.genenames, dtype = str, ndmin = 1) #load in list of gene names you want to query
conn = sqlite3.connect(path) #open connection to db file
c = conn.cursor()
data = [] #start a list of lists to store data in (only have one dataframe to store this all in)

for genename in genenames:
    c.execute("select gene, cv_R2_avg from extra where genename = '" + genename + "';") #what are the names of these genes (starting w/ ENSG)?
    for row in c:
        gene = row[0]
        cv_R2_avg = row[1] #what's its cv R2 average?
    c.execute("select rsid, weight from weights where gene = '" + gene + "'") #what SNPs are in the file and what are their rsids and weights?
    for row in c:
        rs = row[0]
        weight = row[1]
        data.append([rs, weight, genename, cv_R2_avg])
        
data = pd.DataFrame(data) #make list of lists into dataframe
data.columns = ["rs", "weight", "genename", "cv_R2_avg"] #give column names so user knows what they're looking at
data.to_csv("practice_python_queries/rs_weights_genename_cv2R2avg.csv", index = False) #write to .csv
