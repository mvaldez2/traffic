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
    
    
file = 'sample_2.csv' 
f_signals = 'signals.csv'
f_event_codes = 'event_codes.csv'

#turn files into dataframes
event_codes = pd.read_csv(f_event_codes)
signals = pd.read_csv(f_signals)
data = pd.read_csv(file)

data.sort_values("Timestamp", inplace=True)



data['Timestamp'] = pd.to_datetime(data.Timestamp) #converts timestamp to datetime object
data['Signal'] = data['SignalID'].map(signals.set_index('SignalID')['Signal']) #adds signalid name column
data['event'] = data['EventCodeID'].map(event_codes.set_index('code')['desc']) #adds event name column



data.event.value_counts() #get the occurrences of events
#data.event.value_counts().plot(kind='bar', figsize=(30,15)) #plot

# Print the datatype of data_array to the shell

print(data.head())



#-----------
car_count = data.loc[data.EventCodeID==82, :] #dataframe of occurrences of the detector being on

car_count['Time'] = car_count.Timestamp.dt.time #time column



car_count.Timestamp.value_counts().sort_index()

car_count.set_index('Timestamp', drop=False, inplace=True)
car_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count().plot(kind='bar', y='SignalID', figsize=(30,15)) #number of occurrences in a 15min interval

car_count.Timestamp.dt.hour.value_counts().sort_index() #number of occurrences in an hour






#how to loop through dataframe
#for index, row in data.iterrows():
#    print(row['Timestamp'], row['Signal'])

#trying to get the duration of an event     
signal = data.loc[data.Signal=='CR 4 @ CR 17', :] 
dur = signal.Timestamp.diff()
signal['duration'] = dur.dt.seconds.div(60, fill_value=0)
signal.plot(x='Timestamp', y='duration', style='o', figsize=(30,15))


