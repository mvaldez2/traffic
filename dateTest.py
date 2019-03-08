# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 21:19:20 2019

@author: kabut
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:54:17 2019

@author: mvaldez2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


pd.options.display.max_columns = 50
    
    
file = 'Mish_2016_2_24_to_3_3.csv' #download the huge file
f_signals = 'signals.csv'
f_event_codes = 'event_codes.csv'

#turn files into dataframes
event_codes = pd.read_csv(f_event_codes)
signals = pd.read_csv(f_signals)
data = pd.read_csv(file)

data.sort_values("timestamp", inplace=True)



data['timestamp'] = pd.to_datetime(data.timestamp) #converts timestamp to datetime object
data['Signal'] = data['SignalID'].map(signals.set_index('SignalID')['Signal']) #adds signalid name column
data['event'] = data['EventCodeID'].map(event_codes.set_index('code')['desc']) #adds event name column



data.event.value_counts() #get the occurrences of events
#data.event.value_counts().plot(kind='bar', figsize=(30,15)) #plot

# Print the datatype of data_array to the shell

print(data.head())



#-----------
car_count = data.loc[data.EventCodeID==82, :] #dataframe of occurrences of the detector being on

car_count['Time'] = car_count.timestamp.dt.time #time column



car_count.timestamp.value_counts().sort_index()

car_count.set_index('timestamp', drop=False, inplace=True)
car_count.groupby(pd.Grouper(key='timestamp', freq='15min')).count().plot(kind='bar', y='SignalID', figsize=(10,5)) #number of occurrences in a 15min interval

car_count.timestamp.dt.hour.value_counts().sort_index() #number of occurrences in an hour






#how to loop through dataframe
#for index, row in data.iterrows():
#    print(row['timestamp'], row['Signal'])

#trying to get the duration of an event     
signal = data.loc[data.SignalID==327685, :] #gets one signal 




cycle = signal.loc[signal['EventCodeID'].isin([1,7,8,9,10,11])] #light phases in the signal

lane = cycle.loc[(signal['Param'] == 6)] #gets lane on a signal
#figure out lane signal pattern  

dur = lane.timestamp.diff()
lane['duration'] = dur.dt.seconds.div(60,fill_value=0)
lane.plot(x='timestamp', y='duration', style='o', figsize=(10,5))
