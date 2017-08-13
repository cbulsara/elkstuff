#!/usr/bin/python2.7

#---------------------------------------
#parse_sep.py
#
#Scripting necessary to sanitize and
#format CSV output from SEPM such that 
#it is ingestible by Elasticsearch. 
#Contains SEP-specific stuff, indicated
#in comments. If using as a template for
#other parsing functions be sure to take
#SEP-specific stuff out or modify it.
#---------------------------------------


import pandas as pd
import sys

#Define the column names that we want to keep and in what order
keep_cols = ['Computer_Name', 'Measure_Date', 
            'Pattern_Date', 'Operating_System', 'Client_Version',
            'Policy_Serial', 'HI_Status', 'Status',
            'Auto_Protect_On', 'Worst_Detection', 
            'Last_Scan_Time', 'Antivirus_engine_On',
            'Download_Insight_On', 'SONAR_On', 'Tamper_Protection_On',
            'Intrusion_Prevention_On', 'IE_Browser_Protection_On',
            'Firefox_Browser_Protection_On', 'Early_Launch_Antimalware_On',
             'Server_Name', 'MAC_Address1']

#---------------------------------------

def addMeasureDate(df):
    measure_date = raw_input("Enter measurement date as MM/DD/YYYY: ")
    df.insert(0, 'Measure_Date', measure_date)

def pruneColumns(df):
    df = df[keep_cols]
    return df

def pruneDate(df):
    col = raw_input("Enter name of date column to be pruned down to MM/DD/YYYY: ")
    df[col].replace('Never', '', inplace=True)                                          ##SEP-specific: Elasticsearch can't handle text in date fields, so replace 'Never' (never scanned) with nothing
    df[col] = df[col].map(lambda x: str(x).split(" ")[0])                               ##SEP-specific: Some date fields in SEPM will be formated MM/DD/YYYY + other junk separated by a space
                                                                                                        #We want to get rid of everything after MM/DD/YYYY using space as delimeter
def joinCMDB(left_frame):
    user_input = raw_input("Join with CMDB file [Y/N]: ").upper()

    if user_input == "Y":
        cmdb_path = raw_input("Enter path/filename of CMDB file: ")
        right_frame = pd.read_csv(cmdb_path)

        df = left_frame.merge(right_frame, how='outer', left_on='Computer_Name', right_on='name', indicator=True)
    else:
        print("Not joining.")
    return df

#-----------------------------------------, 
#Main
#
#
#-----------------------------------------

#Check for args
if len(sys.argv) == 1:
    print "No args passed"
    quit()

for i in sys.argv[1:]:
    
    print("****" + i + "****")

    df = pd.read_csv(i)
    
    addMeasureDate(df)

    df = pruneColumns(df)

    pruneDate(df)

    df = joinCMDB(df)

    newfilename = raw_input("Enter name of output file: ")
    df.to_csv(newfilename, index=False)
