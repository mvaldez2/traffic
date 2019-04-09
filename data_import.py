import os
import glob
import numpy as np

path = 'T:\SR2\logs\processed'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]

#loop through result and add to same dataframe


    
appended_data = []
for infile in glob.glob('*.{}'.format(extension)):
    data = pd.read_csv(infile, error_bad_lines=False)
    # store DataFrame in list
    appended_data.append(data)
# see pd.concat documentation for more info
appended_data = pd.concat(appended_data)
# write DataFrame to an excel sheet 
