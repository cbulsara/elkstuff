#!/usr/bin/python2.7

#---------------------------------------
#parse_incidents.py
#
#Scripting necessary to sanitize and
#format CSV output from a ServiceNOW
#incident report and make it ingestible
#by ElasticSearch.
#---------------------------------------


import pandas as pd
import sys
import datetime

def durationHours(df):
    return df.apply(lambda x: x / 3600)



def main():
    #Check for args
    if len(sys.argv) == 1:
        print "No args passed"
        quit()

    filename = sys.argv[1]

    df = pd.read_csv(filename)
    df['calendar_duration'] = durationHours(df['calendar_duration'])
    print df['calendar_duration']

    f = filename.split("_")
    outfile = f[0] + "_parsed_" + f[1]
    
    df.to_csv(outfile, index=False)

main()

