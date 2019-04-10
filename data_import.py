import os
import glob
import numpy as np
import pandas as pd

path = 'T:\SR2\logs\processed'
extension = 'csv'
os.chdir(path) #gets path

    
appended_data = [] #list to store all the data
for infile in glob.glob('*.{}'.format(extension)): #loops through the folder of csv files
    data = pd.read_csv(infile, skiprows=8, header=None) #gets csv file and turns it into a dataframe
    appended_data.append(data) #adds dataframe to list

appended_data = pd.concat(appended_data) #appends all dataframes in list and creates one large dataframe
appended_data.columns = ['Timestamp', 'EventCodeID', 'Param'] #adds labels
appended_data.insert(loc=0, column='SignalID', value='64AC68A9-A856-4401-A2BF-04F329887DDC')
# write DataFrame to an excel sheet 
appended_data.to_csv('C:/Users/transpo/Downloads/traffic-master/traffic-master/appended.csv', index=False) #imports to csv to easily integrate into our script