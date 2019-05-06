# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:10:42 2019

@author: mvaldez2
"""

import pandas as pd
import os

#-------------------- Importing data ------------------------------------------    
file = '2019_04_29.csv' 
f_signals = 'signals.csv'
f_event_codes = 'event_codes.csv'

#turn files into dataframes
event_codes = pd.read_csv(f_event_codes)
signals = pd.read_csv(f_signals)
data = pd.read_csv(file)
data.rename(columns={'Event Type':'EventCodeID'}, inplace=True)
data.rename(columns={'Parameter':'Param'}, inplace=True)
data.sort_values("Timestamp", inplace=True)

#set because we only have enough info to evluate one signal. 
#this can be removed to use for  all signals, but will not be useful until we have detector associations for all signals
data.insert(loc=0, column='SignalID', value='64AC68A9-A856-4401-A2BF-04F329887DDC') 

data['Timestamp'] = pd.to_datetime(data.Timestamp) #converts Timestamp to datetime object
data['Signal'] = data['SignalID'].map(signals.set_index('SignalID')['Signal']) #adds signalid name column
data['event'] = data['EventCodeID'].map(event_codes.set_index('code')['desc']) #adds event name column
data['date'] = data['Timestamp'].dt.date
data['date'] = data['date'].astype('str')
data['time'] = data['Timestamp'].dt.time

path = os.path.dirname(os.path.realpath(__file__))


#data.to_csv('C:/Users/transpo/Downloads/traffic-master/traffic-master/appended.csv', index=False) #imports to csv to easily integrate into our script