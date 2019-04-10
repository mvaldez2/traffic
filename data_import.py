import os
import glob

path = 'T:\SR2\logs\processed'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]
print(result)
#loop through result and add to same dataframe