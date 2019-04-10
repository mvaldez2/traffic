# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:54:40 2019

@author: mvaldez2
"""

import pandas as pd
from scipy.stats import ks_2samp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import step, show

pd.options.display.max_columns = 50

#-------------------- Importing data ------------------------------------------    
file = 'ECH_2015_01_15_data.csv' 
f_signals = 'signals.csv'
f_event_codes = 'event_codes.csv'

#turn files into dataframes
event_codes = pd.read_csv(f_event_codes)
signals = pd.read_csv(f_signals)
data = pd.read_csv(file)

data.sort_values("Timestamp", inplace=True)



data['Timestamp'] = pd.to_datetime(data.Timestamp) #converts Timestamp to datetime object
data['Signal'] = data['SignalID'].map(signals.set_index('SignalID')['Signal']) #adds signalid name column
data['event'] = data['EventCodeID'].map(event_codes.set_index('code')['desc']) #adds event name column
#data['day'] = data['Timestamp'].dt.day_name() #used for larger data
data['hour'] = data['Timestamp'].dt.hour
data['minute'] = np.where(data['Timestamp'].dt.minute > 55 , 45, 0)
data['date'] = data['Timestamp'].dt.date
data['date'] = data['date'].astype('str')

def set_signal(data, signal_name):
    return data.loc[data.Signal==signal_name, :]
 
def set_day(data, selected_day):
    return data.loc[data.date==selected_day, :]    
    

def traffic_per15(data):
    car_count = data.loc[data.EventCodeID==82, :] #dataframe of occurrences of the detector being on
    car_count['Time'] = car_count.Timestamp.dt.time #time column 
    car_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
    car_count.set_index('Timestamp', drop=False, inplace=True)
    car_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count().plot(title='Detector Counts',kind='bar', y='SignalID', figsize=(10,15)) #number of occurrences in a 15min interval
    
    
        