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
import pandas as pd



pd.options.display.max_columns = 50
    

#-------------------- Importing data ------------------------------------------    
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


#-------------------------Counts-----------------------------------------------
car_count = data.loc[data.EventCodeID==82, :] #dataframe of occurrences of the detector being on

car_count['Time'] = car_count.timestamp.dt.time #time column



car_count.timestamp.value_counts().sort_index()

car_count.set_index('timestamp', drop=False, inplace=True)
car_count.groupby(pd.Grouper(key='timestamp', freq='15min')).count().plot(title='Detector Counts',kind='bar', y='SignalID', figsize=(10,5)) #number of occurrences in a 15min interval

car_count.timestamp.dt.hour.value_counts().sort_index() #number of occurrences in an hour





#--------------------------------Analysis--------------------------------------
#how to loop through dataframe
#for index, row in data.iterrows():
#    print(row['timestamp'], row['Signal'])

#trying to get the duration of an event     
signal = data.loc[data.SignalID==327685, :] #gets one signal 

signal.loc[data.EventCodeID==82, :].groupby(pd.Grouper(key='timestamp', freq='D')).count().plot(title='Signal Detector Counts', kind='bar', y='SignalID', figsize=(10,5))

#how do I check the split change for a lane?
split = signal.loc[signal['EventCodeID'].isin([134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149])] #split events
split.groupby(pd.Grouper(key='timestamp', freq='D')).count().plot(title='splits', kind='bar', y='SignalID', figsize=(10,5))

cycle = signal.loc[signal['EventCodeID'].isin([1,7,8,9,10,11])] #light phases in the signal

lane = cycle.loc[(signal['Param'] == 6)] #gets lane on a signal
#figure out lane signal pattern  

dur = lane.timestamp.diff()
lane['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)


#green ccycle length
green_cycle = lane.loc[signal['EventCodeID'].isin([1,7])]
green_cycle.plot(title='Green Cycle', x='timestamp', y='duration', figsize=(10,5), color='g')
green_cycle.duration.describe() #5 number summary of green cycle length
green_cycle.loc[green_cycle.duration>green_cycle.duration.mean(), :] #times the duration is greater than average

#yellow cycle
yellow_cycle = lane.loc[signal['EventCodeID'].isin([8,9])]
yellow_cycle.plot(title='Yellow Cycle',x='timestamp', y='duration', figsize=(10,5), color='y')
yellow_cycle.duration.describe() #5 number summary of yellow cycle length
yellow_cycle.loc[yellow_cycle.duration>yellow_cycle.duration.mean(), :] #times the duration is greater than average

#red cycle
red_cycle = lane.loc[signal['EventCodeID'].isin([10,11])]
red_cycle.plot(title='Red Cycle',x='timestamp', y='duration', figsize=(10,5), color='r')
red_cycle.duration.describe() #5 number summary of red cycle length
red_cycle.loc[red_cycle.duration>red_cycle.duration.mean(), :] #times the duration is greater than average


#graph green and not green (binary)


#for green arrival we would have to check if the detector is on during the time period that the light was green
#do we use correlation somehow? 
#create a function that takes timestamp and timeperiod, then get ocurrences that way