#!/usr/bin/python2.7

#---------------------------------------
#parse_tasks.py
#
#Scripting necessary to sanitize and
#format CSV output from a ServiceNOW
#task report and make it ingestible
#by ElasticSearch.
#---------------------------------------


import pandas as pd
import sys
import datetime as dt

def durationHours(start, end, date_format_in):
    date1 = dt.datetime.strptime(start, date_format_in)
    date2 = dt.datetime.strptime(end, date_format_in)

    delta = date2 - date1

    return delta.seconds / 60 / 60


def main():
    #Check for args
    if len(sys.argv) == 1:
        print "No args passed"
        quit()

    filename = sys.argv[1]

    df = pd.read_csv(filename)
    
    date_format_in = '%Y-%m-%d %H:%M:%S'
    df['duration'] = df.apply(lambda x: durationHours(x['sys_created_on'], x['closed_at'], date_format_in), axis=1)

    f = filename.split("_")
    outfile = f[0] + "_parsed_" + f[1]
    
    df.to_csv(outfile, index=False)


main()

