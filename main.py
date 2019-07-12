# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:54:40 2019
Main file that contains the functions to analyze the data
@author: mvaldez2
"""

import pandas as pd
from scipy.stats import ks_2samp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import step, show
from tkinter.filedialog import askopenfilename
  
file = askopenfilename() #get imported data
data = pd.read_csv(file) #turn file into dataframe
data['Timestamp'] = pd.to_datetime(data.Timestamp)


'''
sets time period
data : dataframe
start_date: start date
end_time: end date
start: start time
end: end time
usage:
    If you want to set a time period from the dataset you can set the function 
    to a variable and use that as the data parameter for the rest of the functions
    ex:
        df = time_period(data, "2019-04-29", "2019-04-30", "2:00", "4:00")
        traffic(df,"CR6 @ CR17", 15)
'''
def time_period(data, start_date, end_date, start_time, end_time):
    data.loc[(data.date==start_date) | (data.date==end_date)]
    return data.set_index('Timestamp').between_time(start_time,end_time).reset_index()
   

#-------------------------Counts-----------------------------------------------
'''
#returns bar graph of traffic density of a signal per 15 min
data : dataframe
signal_name: name of signal
freq: frequency in minutes
ex: traffic(data,"CR6 @ CR17", 15)
'''
def traffic(data, signal_name, freq):
    signal = data.loc[data.Signal==signal_name, :]
    vehicle_count = signal.loc[signal.EventCodeID==82, :] #dataframe of occurrences of the detector being on
    vehicle_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
    vehicle_count.set_index('Timestamp', drop=False, inplace=True)
    group = vehicle_count.groupby(pd.Grouper(key='Timestamp', freq= str(freq)+'min')) #groups occurrences in a 15min interval
    group.count().plot(title=signal_name, kind='bar', y='event', figsize=(15,5), colormap='Paired')

'''
returns bar graph of traffic density of a lane on a signal per 15 min 
data : dataframe
signal_name: name of signal
freq: frequency in minutes
*args: parameters to get the phase of the signal 
ex: traffic(data,"CR6 @ CR17, 15, 25, 40")
'''
def traffic_lane(data, signal_name, freq, *lane):
    signal = data.loc[data.Signal==signal_name, :]
    vehicle_count = signal.loc[(signal.EventCodeID==82) & (signal['Param'].isin(lane))] #dataframe of occurrences of the detector being on
    vehicle_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
    vehicle_count.set_index('Timestamp', drop=False, inplace=True)
    group = vehicle_count.groupby(pd.Grouper(key='Timestamp', freq= str(freq)+'min')) #groups occurrences in a 15min interval
    group.count().plot(title=signal_name, kind='bar', y='event', figsize=(15,5), colormap='Paired')
    
#------------------------ light cycles ---------------------------------------- 
'''
returns graph of cycle lengths in seconds for traffic lights 
data : dataframe
signal_name: name of signal
phase: phase of traffic light
ex: cycle_length(data,"CR6 @ CR17", 2)
'''
def cycle_length(data, signal_name, phase):
    signal = data.loc[data.Signal==signal_name, :]
    cycle = signal.loc[(signal['EventCodeID'].isin([1,7,10,11])) & (signal['Param'] == phase)] #light phases in the signal
    dur = cycle.Timestamp.diff() #time difference between row below
    cycle['duration'] = dur.dt.total_seconds().fillna(0).shift(-1)
    cycle['duration'].shift(+1)
    print(cycle[['Timestamp','event','duration']])
    
    #green cycle
    green_cycle = cycle.loc[signal['EventCodeID'].isin([1,7])] #finds green light events
    green_cycle.plot(title='Green Cycle', x='Timestamp', y='duration', figsize=(15,5), color='g')
    
    #yellow cycle
    yellow_cycle = cycle.loc[signal['EventCodeID'].isin([10])] #finds yellow light events
    yellow_cycle.plot(title='Yellow Cycle',x='Timestamp', y='duration', figsize=(15,5), color='y')
    
    #red cycle
    red_cycle = cycle.loc[signal['EventCodeID'].isin([11])] #finds red light events
    red_cycle.plot(title='Red Cycle',x='Timestamp', y='duration', figsize=(15,5), color='r')
    

#---------------- Compare detection systems -----------------------------------
'''
returns graph that compares the activity of a loop detector and a pod detector
data : dataframe
signal_name: name of signal
loop: loop detector
pod: pod detectpr
ex: compare(data,"CR6 @ CR17", 33, 8, '04:30', '04:35')
'''    
def compare(data, signal_name, loop, pod, start, end):
    data = data.set_index('Timestamp').between_time(start,end).reset_index()
    compare = data.loc[(data['EventCodeID'].isin([81,82])) & (data.Signal==signal_name)] #finds when detectors are on and off
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
   

#----------------- Split Failure ---------------------------------------------- 
#check loop 1
'''
returns graph that finds the amount of split failures on a given lane
data : dataframe
signal_name: name of signal
phase: phase of traffic light
*dets: vehicle detectors on the same lane
ex: split_failure(data, "CR6 @ CR17", 4, 25, 40)
''' 
def split_failure(data, signal_name, phase, *dets):
    data = data.loc[data.Signal==signal_name, :]
    lights = data.loc[data['EventCodeID'].isin([1, 7, 10, 11]) & (data.Param==phase)] #get light events and phase
    detectors = data.loc[data['EventCodeID'].isin([81,82]) & (data.Param.isin(dets))] #get detectors that are on the same lane
    split = lights.append(detectors)
    split.sort_values("Timestamp", inplace=True)    
    pattern = np.asarray([11, 81]) #split failure pattern
    n_obs = len(pattern)
    split['split_failure'] = (split['EventCodeID']
                           .rolling(window=n_obs , min_periods=n_obs)
                           .apply(lambda x: (x==pattern).all())
                           .astype(bool)             
                           .shift(-1 * (n_obs - 1))  
                           .fillna(False)            
                           ) #counts the occurrences of the pattern
    split_count = split.loc[split.split_failure==True, :] #dataframe of occurrences of the detector being on
    split_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
    split_count.set_index('Timestamp', drop=False, inplace=True)
    group = split_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count() #groups occurrences in a 15min interval
    group.plot(title="Split Failures", kind='bar', y='event', stacked=True, figsize=(15,5), colormap='Paired')    
    group.plot.bar(stacked=True, figsize=(15,5));