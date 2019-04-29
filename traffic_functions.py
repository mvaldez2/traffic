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
file = '2019-04-03.csv' 
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
data['date'] = data['Timestamp'].dt.date
data['date'] = data['date'].astype('str')
data['time'] = data['Timestamp'].dt.time


print(data[['date', 'Signal', 'event','Param']])

#sets signal from dataframe
#data : dataframe
#signal_name: name of signal
#ex: set_signal(data,"CR6 @ CR17")
def set_signal(data, signal_name):
    return data.loc[data.Signal==signal_name, :]

#sets date from dataframe
#data : dataframe
#selected_date: selected date
#ex: set_date(data,"2019-04-03")
def set_date(data, selected_date):
    return data.loc[data.date==selected_date, :]  

#sets range of dates from dataframe
#data : dataframe
#start: start date
#end: end date
#ex: date_range(data,"2019-04-03", "2019-04-09")
def date_range(data, start, end):
    return data.loc[(data.date==start) | (data.date==end)]

#sets range of time from dataframe
#data : dataframe
#start: start time
#end: end time
#ex: time_range(data,"7:00", "12:00")
def time_range(data, start, end):
    return data.set_index('Timestamp').between_time(start,end).reset_index()
    
#-------------------------Counts-----------------------------------------------
#returns bar graph of traphic density of a signal per 15 min
#data : dataframe
#signal_name: name of signal
#ex: traffic(data,"CR6 @ CR17")
def traffic(data, signal_name):
    signal = data.loc[data.Signal==signal_name, :]
    vehicle_count = signal.loc[signal.EventCodeID==82, :] #dataframe of occurrences of the detector being on
    vehicle_count['Time'] = vehicle_count.Timestamp.dt.time #time column 
    vehicle_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
    vehicle_count.set_index('Timestamp', drop=False, inplace=True)
    group = vehicle_count.groupby(pd.Grouper(key='Timestamp', freq='15min')) #groups occurrences in a 15min interval
    group.count().plot(title=signal_name, kind='bar', y='event', figsize=(15,5))
    
 #------------------------ light cycles ---------------------------------------- 
#returns graph of cycle lengths in seconds for traffic lights 
#data : dataframe
#signal_name: name of signal
#phase: phase of traffic light
#ex: cycle_length(data,"CR6 @ CR17", 7)
def cycle_length(data, signal_name, phase):
    signal = data.loc[data.Signal==signal_name, :]
    cycle = signal.loc[(signal['EventCodeID'].isin([1,7,10,11])) & (signal['Param'] == phase)] #light phases in the signal
    dur = cycle.Timestamp.diff() #time difference between rpw below
    cycle['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    cycle['duration'].shift(+1)
    print(cycle[['Timestamp','event','duration']])
    
    #green cycle
    green_cycle = cycle.loc[signal['EventCodeID'].isin([1])] #finds green light events
    green_cycle.plot(title='Green Cycle', x='Timestamp', y='duration', figsize=(15,5), color='g')
    
    #yellow cycle
    yellow_cycle = cycle.loc[signal['EventCodeID'].isin([10])] #finds yellow light events
    yellow_cycle.plot(title='Yellow Cycle',x='Timestamp', y='duration', figsize=(15,5), color='y')
    
    #red cycle
    red_cycle = cycle.loc[signal['EventCodeID'].isin([11])] #finds red light events
    red_cycle.plot(title='Red Cycle',x='Timestamp', y='duration', figsize=(15,5), color='r')

 #---------------- Compare detection systems -----------------------------------
#returns graph that compares the activty of a loop detector and a pod detector
#data : dataframe
#signal_name: name of signal
#loop: loop detector
#pod: pod detectpr
#ex: compare(data,"CR6 @ CR17", 33, 8)    
def compare(data, signal_name, loop, pod):
    compare = data.loc[(data['EventCodeID'].isin([81,82])) & (data.signal==signal_name)] #finds when detectors are on and off
    print(compare[['Timestamp','event','Param']])
    plt.figure(figsize=(15,5))
    
    loops = compare.loc[compare.Param == loop,:] #gets loop detectors
    dur = loops.Timestamp.diff() #time difference between row below
    loops['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    loops['duration'].shift(+1)
    
    pods = compare.loc[compare.Param == pod,:] #gets pod detectors
    dur = pods.Timestamp.diff() #time difference between row below
    pods['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    pods['duration'].shift(+1)    
    
    step(loops.Timestamp, loops.event) #graphs on/off of loop detectors
    step(pods.Timestamp, pods.event) #graphs on/off of pod detectors
    show()
   

#----------------------- IN PROGRESS ---------------------------------------
 #--------------------- Green Arrival ----------------------------------- 
#graph green and not green (binary)
#for green arrival we would have to check if the detector is on during the time period that the light was green
#only use loops #5
#add 5 seconds
time = time_range(data, '16:00', '16:25')
green = time.loc[time['EventCodeID'].isin([1, 7]) & (time.Param==7)]
det = time.loc[time['EventCodeID'].isin([82]) & (time.Param.isin([5, 30]))]
arrival = green.append(det)
arrival.sort_values("Timestamp", inplace=True)    
print(arrival[['time','event','Param']])

#----------------- Split Failure ---------------------------------------------- 
#check loop 1
#if detector is on after red end clearence its a split failure   
lights = time.loc[time['EventCodeID'].isin([1, 7, 10, 11]) & (time.Param==7)]
detectors = time.loc[time['EventCodeID'].isin([81,82]) & (time.Param.isin([26, 35]))]
split = lights.append(detectors)
split.sort_values("Timestamp", inplace=True)    

with pd.option_context('display.max_rows',None):
    print(split[['time','event','Param']])
    
  
        
    
    
    
    
    
    
    
    
    
    
        