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
f_signals = 'signals.csv'
f_event_codes = 'event_codes.csv'

#turn files into dataframes
event_codes = pd.read_csv(f_event_codes)
signals = pd.read_csv(f_signals)

appended_data.rename(columns={'Event Type':'EventCodeID'}, inplace=True)
appended_data.rename(columns={'Parameter':'Param'}, inplace=True)
appended_data.sort_values("Timestamp", inplace=True)

#set because we only have enough info to evluate one signal. 
#this can be removed to use for  all signals, but will not be useful until we have detector associations for all signals
appended_data.insert(loc=0, column='SignalID', value='64AC68A9-A856-4401-A2BF-04F329887DDC') 

appended_data['Timestamp'] = pd.to_datetime(appended_data.Timestamp) #converts Timestamp to datetime object
appended_data['Signal'] = appended_data['SignalID'].map(signals.set_index('SignalID')['Signal']) #adds signalid name column
appended_data['event'] = appended_data['EventCodeID'].map(event_codes.set_index('code')['desc']) #adds event name column
appended_data['date'] = appended_data['Timestamp'].dt.date
appended_data['date'] = appended_data['date'].astype('str')
appended_data['time'] = appended_data['Timestamp'].dt.time
path = os.path.dirname(os.path.realpath(__file__))
date = appended_data.date[0]

outdir = path + '/imported'
if not os.path.exists(outdir):
    os.mkdir(outdir)

full_path = os.path.join(outdir, 'appended.csv') 


data.to_csv(full_path) #imports to csv to easily integrate into our script
