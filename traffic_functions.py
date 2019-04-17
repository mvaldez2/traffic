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
#data['day'] = data['Timestamp'].dt.day_name() #used for larger data
data['date'] = data['Timestamp'].dt.date
data['date'] = data['date'].astype('str')
data['time'] = data['Timestamp'].dt.time


print(data[['date', 'Signal', 'event','Param']])

#sets signal to dataframe
#Variables
#data : dataset
#signal_name: name of signal
def set_signal(data, signal_name):
    return data.loc[data.Signal==signal_name, :]
 
def set_day(data, selected_day):
    return data.loc[data.date==selected_day, :]  


def date_range(data, start, end):
    return data.loc[(data.date==start) | (data.date==end)]

def date_range2(data, start, end):
    mask = (data['Timestamp'].dt.hour>start)&(df['Timestamp'].dt.hour<end)
    return data.loc[mask]

def time_range(data, start, end):
    return data.set_index('Timestamp').between_time(start,end).reset_index()
    
#-------------------------Counts-----------------------------------------------
def traffic(data, signal):
    s = data.loc[data.Signal==signal, :]
    car_count = s.loc[s.EventCodeID==82, :] #dataframe of occurrences of the detector being on
    car_count['Time'] = car_count.Timestamp.dt.time #time column 
    car_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
    car_count.set_index('Timestamp', drop=False, inplace=True)
    car_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count().plot(title=signal,kind='bar', y='SignalID', figsize=(15,5)) #number of occurrences in a 15min interval
    
 #------------------------ light cycles ----------------------------------------   
def cycle_length(data, signal, phase):
    s = data.loc[data.Signal==signal, :]
    cycle = s.loc[s['EventCodeID'].isin([1,7,10,11])] #light phases in the signal
    lane = cycle.loc[(s['Param'] == phase)] #gets lane on a signal
    dur = lane.Timestamp.diff() #time difference between rpw below
    lane['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    lane['duration'].shift(+1)
    print(lane[['Timestamp','event','duration']])
    #green cycle
    green_cycle = lane.loc[s['EventCodeID'].isin([1])] #finds green light events
    green_cycle.plot(title='Green Cycle', x='Timestamp', y='duration', figsize=(15,5), color='g')
    green_cycle.duration.describe() #5 number summary of green cycle length
    green_cycle.loc[green_cycle.duration>green_cycle.duration.mean(), :] #times the duration is greater than average
    
    #yellow cycle
    yellow_cycle = lane.loc[s['EventCodeID'].isin([10])] #finds yellow light events
    yellow_cycle.plot(title='Yellow Cycle',x='Timestamp', y='duration', figsize=(15,5), color='y')
    yellow_cycle.duration.describe() #5 number summary of yellow cycle length
    yellow_cycle.loc[yellow_cycle.duration>yellow_cycle.duration.mean(), :] #times the duration is greater than average
    
    #red cycle
    red_cycle = lane.loc[s['EventCodeID'].isin([11])] #finds red light events
    red_cycle.plot(title='Red Cycle',x='Timestamp', y='duration', figsize=(15,5), color='r')
    red_cycle.duration.describe() #5 number summary of red cycle length
    red_cycle.loc[red_cycle.duration>red_cycle.duration.mean(), :] #times the duration is greater than average

 #---------------- Compare detection systems -----------------------------------    
def compare(data, signal, loop, pod):
   
    compare = data.loc[data['EventCodeID'].isin([81,82])] #finds when detectors are on and off
    #graph a comparison between parameters when the detector is on and off
    #pd.value_counts(compare['Param']).plot.bar(figsize=(35,15))
    print(compare[['Timestamp','event','Param']])
    #we need the more info on the parameters to compare
    plt.figure(figsize=(15,5))
    
    #plt.gca().invert_yaxis()
    loops = compare.loc[compare.Param == loop,:]
    dur = loops.Timestamp.diff() #time difference between rpw below
    loops['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    loops['duration'].shift(+1)
    pods = compare.loc[compare.Param == pod,:]
    dur = pods.Timestamp.diff() #time difference between rpw below
    pods['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    pods['duration'].shift(+1)    
    step(loops.Timestamp, loops.event) #looks like on and off are flipped in the graph labels
    step(pods.Timestamp, pods.event)
    show()
    
    #find duration of error for both 
    lp = compare.loc[(compare.Param == pod) | (compare.Param == loop)]
    diff = lp.loc[lp['EventCodeID'].isin([82])]
    dur = diff.Timestamp.diff() #time difference between rpw below
    diff['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    diff['duration'].shift(+1)
    print(diff[['Timestamp','Param', 'duration']])
    

    
    
    
 #--------------------- Green Arrival ----------------------------------- 
#graph green and not green (binary)
#for green arrival we would have to check if the detector is on during the time period that the light was green
#only use loops 5
 #add 5 seconds
time = time_range(data, '15:00', '15:25')
green = time.loc[time['EventCodeID'].isin([1, 7]) & (time.Param==7)]
det = time.loc[time['EventCodeID'].isin([82]) & (time.Param.isin([5, 30]))]
arrival = green.append(det)
arrival.sort_values("Timestamp", inplace=True)    
print(arrival[['time','event','Param']])

#----------------- Split Failure ----------------------------------------------    
lights = time.loc[time['EventCodeID'].isin([1, 7, 10, 11]) & (time.Param==7)]
detectors = time.loc[time['EventCodeID'].isin([81,82]) & (time.Param.isin([5, 6, 9, 26, 30, 31, 33]))]
split = lights.append(detectors)
split.sort_values("Timestamp", inplace=True)    

with pd.option_context('display.max_rows',None):
    print(split[['time','event','Param']])
    
def split_failures():    
    for index, row in split.iterrows():
        #get vvent
        #get next event
        #if light is red count detectors until light is green
        print(row['time'], row['event'])    
        
    
    
    
    
    
    
    
    
    
    
        