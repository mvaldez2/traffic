# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:54:17 2019

@author: mvaldez2
"""
import pandas as pd
from scipy.stats import ks_2samp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import step, show

pd.options.display.max_columns = 50

#-------------------- Importing data ------------------------------------------    
file = 'ECH_2015_01_15_data.csv' #download the huge file
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


data.event.value_counts() #get the occurrences of events
#data.event.value_counts().plot(kind='bar', figsize=(30,15)) #plot

#-------------------------Counts-----------------------------------------------
car_count = data.loc[data.EventCodeID==82, :] #dataframe of occurrences of the detector being on

car_count['Time'] = car_count.Timestamp.dt.time #time column



car_count.Timestamp.value_counts().sort_index() #sorts data by timestamp

car_count.set_index('Timestamp', drop=False, inplace=True)
car_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count().plot(title='Detector Counts',kind='bar', y='SignalID', figsize=(35,15)) #number of occurrences in a 15min interval


car_count.Timestamp.dt.hour.value_counts().sort_index() #number of occurrences in an hour



#_______________________________ Analysis _____________________________________
#how to loop through dataframe
#for index, row in data.iterrows():
#    print(row['Timestamp'], row['Signal'])

     
signal = data.loc[data.Signal=='CR6 @ CR17', :] #gets one signal 
#signal.loc[data.EventCodeID==82, :].groupby(pd.Grouper(key='Timestamp', freq='D')).count().plot(title='Signal Detector Counts', kind='bar', y='SignalID', figsize=(10,5))


cycle = signal.loc[signal['EventCodeID'].isin([1,7,8,9,10,11])] #light phases in the signal

lane = cycle.loc[(signal['Param'] == 6)] #gets lane on a signal
#figure out lane signal pattern  

dur = lane.Timestamp.diff() #time difference between rpw below
lane['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)



#------------------------ light cycles ----------------------------------------
#green cycle 
green_cycle = lane.loc[signal['EventCodeID'].isin([1,7])] #finds green light events
green_cycle.plot(title='Green Cycle', x='Timestamp', y='duration', figsize=(35,15), color='g')
green_cycle.duration.describe() #5 number summary of green cycle length
green_cycle.loc[green_cycle.duration>green_cycle.duration.mean(), :] #times the duration is greater than average

#yellow cycle
yellow_cycle = lane.loc[signal['EventCodeID'].isin([8,9])] #finds yellow light events
yellow_cycle.plot(title='Yellow Cycle',x='Timestamp', y='duration', figsize=(35,15), color='y')
yellow_cycle.duration.describe() #5 number summary of yellow cycle length
yellow_cycle.loc[yellow_cycle.duration>yellow_cycle.duration.mean(), :] #times the duration is greater than average

#red cycle
red_cycle = lane.loc[signal['EventCodeID'].isin([10,11])] #finds red light events
red_cycle.plot(title='Red Cycle',x='Timestamp', y='duration', figsize=(35,15), color='r')
red_cycle.duration.describe() #5 number summary of red cycle length
red_cycle.loc[red_cycle.duration>red_cycle.duration.mean(), :] #times the duration is greater than average


#---------------------- arrival on green --------------------------------------

#graph green and not green (binary)
#for green arrival we would have to check if the detector is on during the time period that the light was green
#we would need the parameter for detector on to know which phase we are checkin 


    


#---------------- Compare detection systems -----------------------------------
hour = signal.loc[signal.hour==3,:] #finds events occurring at a certain hour of the day
compare = hour.loc[hour['EventCodeID'].isin([81,82])] #finds when detectors are on and off
#graph a comparison between parameters when the detector is on and off
#pd.value_counts(compare['Param']).plot.bar(figsize=(35,15))
test = ks_2samp(compare.count(), car_count.count())



#we need the more info on the parameters to compare
plt.figure(figsize=(35,15))
plt.ylim(81, 82.5)
compare_det = compare.loc[compare.Param==27,:]
compare_det2 = compare.loc[compare.Param==20,:]
step(compare_det.Timestamp, compare_det.EventCodeID,compare_det2.Timestamp, compare_det2.EventCodeID)
show()



#--------------------- Split Failures -----------------------------------------
#For split failure we have to see if there's a phase call when the light turns red
plt.figure(figsize=(35,15))
splitf = signal.loc[signal['EventCodeID'].isin([10,43,44])] #finds when the light turns red and the phase calls
split_lane = splitf.loc[(splitf['Param'] == 6) & (splitf.hour==3)] #finds time of day and phase
step(split_lane.Timestamp, split_lane.EventCodeID)
splits = split_lane[['Timestamp','event']] #just view timestamp and event

