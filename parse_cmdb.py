#!/usr/bin/python2.7

#---------------------------------------
#parse_sep.py
#
#Scripting necessary to sanitize output
#from SNOW CMDB and prep it for joining 
#with SEPM and other outputs.
#---------------------------------------


import pandas as pd
import sys

#Define the column names that we want to keep and in what order
keep_cols = ['name', 'u_friendly', 'short_description',
                'model_id', 'serial_number']

#Define the column names we want to change to
rename_cols = ['cmdb_name', 'cmdb_friendly', 'cmdb_shortdescription',
                'cmdb_model_id', 'cmdb_serial']

#----------------------------------------
#pruneColumns(df)
#
#Limit columns in the passed dataframe to
#those specified in keep_cols. Return
#pruned dataframe.
#---------------------------------------- 
def pruneColumns(df):
    df = df[keep_cols]
    return df
                                                                                                       

#-----------------------------------------
# concatWorkstationsServers(df1, df2)
# 
# Concatenate lists of Workstations and
# Servers out of SNOW CMDB. Assumes same
# column names in both lists. Returns
# concatenated dataframe, or None if user
# decides not to concat.
#-----------------------------------------                                                                                                       #We want to get rid of everything after MM/DD/YYYY using space as delimeter
def concatWorkstationsServers(df1, df2):
    user_input = raw_input("Concatenate servers and workstations? [Y/N]: ").upper()

    if user_input == "Y":
        frames = [df1, df2]
        df = pd.concat(frames)
        return df    
    else:
        print("Not concatenating.")
    return None

#----------------------------------------
# renameColumns(df)
# 
# Rename columns to titles specified in
# rename_cols. Return dataframe with 
# renamed columns.
#----------------------------------------
def renameColumns(df):
    for a, b in zip(keep_cols, rename_cols):
        df.rename(columns={a: b}, inplace=True)
    
    return df

#-----------------------------------------, 
#Main
#
#
#-----------------------------------------

#Check for args
if len(sys.argv) != 3:
    print "Utility takes 2 args: workstation and server CSVs."
    quit()

  
print("****" + sys.argv[1] + "****")
print("****" + sys.argv[2] + "****")

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])
    
df1 = pruneColumns(df1)
df2 = pruneColumns(df2)

df3 = concatWorkstationsServers(df2, df2)

df3 = renameColumns(df3)

if not (df3 is None):
    newfilename = raw_input("Enter name of output file: ")
    df3.to_csv(newfilename, index=False)
else:
    df1.to_csv(sys.argv[1] + ".new", index=False)
    df2.to_csv(sys.argv[2] + ".new", index=False)