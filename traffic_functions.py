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
data['date'] = data['Timestamp'].dt.date
data['date'] = data['date'].astype('str')
data['time'] = data['Timestamp'].dt.time


print(data[['date', 'Signal', 'event','Param']])

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
    car_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count().plot(title=signal,kind='bar', y='SignalID', figsize=(25,15)) #number of occurrences in a 15min interval
    
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
    green_cycle = lane.loc[s['EventCodeID'].isin([1,7])] #finds green light events
    green_cycle.plot(title='Green Cycle', x='Timestamp', y='duration', figsize=(35,15), color='g')
    green_cycle.duration.describe() #5 number summary of green cycle length
    green_cycle.loc[green_cycle.duration>green_cycle.duration.mean(), :] #times the duration is greater than average
    
    #yellow cycle
    yellow_cycle = lane.loc[s['EventCodeID'].isin([10])] #finds yellow light events
    yellow_cycle.plot(title='Yellow Cycle',x='Timestamp', y='duration', figsize=(35,15), color='y')
    yellow_cycle.duration.describe() #5 number summary of yellow cycle length
    yellow_cycle.loc[yellow_cycle.duration>yellow_cycle.duration.mean(), :] #times the duration is greater than average
    
    #red cycle
    red_cycle = lane.loc[s['EventCodeID'].isin([11])] #finds red light events
    red_cycle.plot(title='Red Cycle',x='Timestamp', y='duration', figsize=(35,15), color='r')
    red_cycle.duration.describe() #5 number summary of red cycle length
    red_cycle.loc[red_cycle.duration>red_cycle.duration.mean(), :] #times the duration is greater than average

 #---------------- Compare detection systems -----------------------------------    
def compare(data, signal, det1, det2):
   
    compare = data.loc[data['EventCodeID'].isin([81,82])] #finds when detectors are on and off
    #graph a comparison between parameters when the detector is on and off
    #pd.value_counts(compare['Param']).plot.bar(figsize=(35,15))
    print(compare[['Timestamp','event','Param']])
    #we need the more info on the parameters to compare
    plt.figure(figsize=(35,15))
    #plt.gca().invert_yaxis()
    compare_det = compare.loc[compare.Param==det1]
    compare_det2 = compare.loc[compare.Param==det2]
    step(compare_det.Timestamp, compare_det.event) #looks like on and off are flipped in the graph labels
    step(compare_det2.Timestamp, compare_det2.event)
    show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        