# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:44:02 2019

@author: mvaldez2
"""

import pandas as pd
from scipy.stats import ks_2samp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import step, show
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
output_file('simple_timeseries_plot.html')


pd.options.display.max_columns = 50

#-------------------- Importing data ------------------------------------------    
file = '2019-04-03.csv' 
f_signals = 'signals.csv'
f_event_codes = 'event_codes.csv'

#turn files into dfframes
event_codes = pd.read_csv(f_event_codes)
signals = pd.read_csv(f_signals)
df = pd.read_csv(file)

df.sort_values("Timestamp", inplace=True)

df['Timestamp'] = pd.to_datetime(df.Timestamp) #converts Timestamp to datetime object
df['Signal'] = df['SignalID'].map(signals.set_index('SignalID')['Signal']) #adds signalid name column
df['event'] = df['EventCodeID'].map(event_codes.set_index('code')['desc']) #adds event name column
df['date'] = df['Timestamp'].dt.date
df['date'] = df['date'].astype('str')
df['time'] = df['Timestamp'].dt.time


print(df[['date', 'Signal', 'event','Param']])

vehicle_count = df.loc[df.EventCodeID==82, :] #dataframe of occurrences of the detector being on
vehicle_count['Time'] = vehicle_count.Timestamp.dt.time #time column 
vehicle_count.Timestamp.value_counts().sort_index() #sorts data by timestamp 
vehicle_count.set_index('Timestamp', drop=False, inplace=True)
group = vehicle_count.groupby(pd.Grouper(key='Timestamp', freq='15min')).count() #groups occurrences in a 15min interval

source = ColumnDataSource(group)

p = figure(x_axis_type='datetime')

p.line(x='Timestamp', y='EventCodeID', line_width=2, source=source, legend='Vehicle')

p.yaxis.axis_label = 'Vehicle Counts'

show(p)