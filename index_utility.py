#!/usr/bin/python2.7

#---------------------------------------
#index_utility.py
#
# Accepts CSV files bound for 
# elasticsearch as arguments. For each
# one, it interrogates the user for
# field types. It outputs 2 files: a
# text file with ready-to-paste index
# specification for use in a curl PUT
# transaction to build an index, and a
# CSV file with column names and field 
# types, useful for pasting into CONF
# files and the like.
#---------------------------------------
import csv
import sys
import pandas as pd

#define acceptable input as elasticsearch field typess
acceptable_inputs = ['text', 'keyword', 'long', 'integer',
                        'short', 'byte', 'double', 'float',
                        'date', 'boolean', 'binary',
                        'integer_range', 'float_range',
                        'double_range', 'date_range',
                        'object', 'nested', 'geo_point',
                        'geo_shape', 'ip', 'completion',
                        'token_count', 'murmur3', 'mapper-attachments']

#Write preamble and headers + types in a format ingestible by elasticsearch via a curl PUT.
#An easy way to use this is to copy the contents of the output file, paste it into the Kibana dev tools
#console, clean it up, append PUT [index name] to the top, and send
def writeIndex(headers, types):
    #Append mandatory preamble with timestamp and version
    outbuffer = []
    outbuffer.append("{")
    outbuffer.append("\t" + '"mappings": {')
    outbuffer.append("\t\t" + '"logs": {')
    outbuffer.append("\t\t\t" + '"properties": {')
    outbuffer.append("\t\t\t\t" + '"@timestamp": {')
    outbuffer.append("\t\t\t\t\t" + '"type": "date"')
    outbuffer.append("\t\t\t\t" + "},")
    outbuffer.append("\t\t\t\t" + '"@version": {')
    outbuffer.append("\t\t\t\t\t" + '"type": "string"')
    outbuffer.append("\t\t\t\t" + '},')

    #Zip the header and types lists, iterate and append to outbuffer with appropriate formatting.
    for h, t in zip(headers,types):
        outbuffer.append("\t\t\t\t" + '"' + h + '"' + ": {")
        outbuffer.append("\t\t\t\t\t" + '"type":' + ' "' + t + '"')
        outbuffer.append("\t\t\t\t" + "},")
    #Eliminate the final trailing comma
    outbuffer[-1] = outbuffer[-1].replace(",", "")
    #Append closing braces
    outbuffer.append("\t\t\t" + '}')
    outbuffer.append("\t\t" + '}')
    outbuffer.append("\t" + '}')
    outbuffer.append('}')

    #Write buffer to file
    filename = raw_input("Path/name of output text file: ")

    textfile = open(filename, 'wb')
    for s in outbuffer:
        textfile.write(s + "\n")
    textfile.close()

#------------------------------------------------------
#Main
#
#Iterate through csv files passed on the command line.
#For each column, poll the user for field type.
#Call WriteIndex to write headers and field types to
#a text file in a format ingestible by elasticsearch via
#a curl PUT. Also write headers out to a CSV file for
#debug, and also to copy and paste into CONF files.
#------------------------------------------------------


#Argument check
if len(sys.argv) == 1:
    print "No args passed"
    quit()

#Iterate through CSV files passed on the command line.
for i in sys.argv[1:]:
    
    headersout = []                                                     #headers list
    typesout = []                                                       #field types list

    #Read CSV file and load the first row into the list of headers.
    f = pd.read_csv(i)
    headersout = list(f)

    #For each header, poll user for field types
    print("Please enter the desired data type for each column.")
    print acceptable_inputs
    for h in list(f):
        while True:
            column_type = raw_input("Enter data type of " + h + ": ")
            try:
                column_type = column_type.lower()
            except ValueError:
                continue
            if column_type in acceptable_inputs:                        #compare user input against list of elasticsearch field types, throw exceptions
                typesout.append(column_type)
                break
            else:
                print("Invalid Entry")
    
    writeIndex(headersout,typesout)                                     #write headers to file for debug and CONF file use
    filename =  i.split(".")[0] + "_headers.csv"                        #we have to use csv.writer instead of pandas in order to 
    with open(filename, 'wb') as csvfile:                               #get field names wrapped in "QUOTES"
        w = csv.writer(csvfile, quoting=csv.QUOTE_ALL, quotechar='"')   #most ELK CONF files need field names wrapped in quotes
        w.writerow(headersout)
        w.writerow(typesout)



