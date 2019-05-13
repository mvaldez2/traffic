Importing Data

1. Use import.py file to process data for main file
    * This script opens a file picker where you choose which file you want to process
    * After the file is processed a new directory called imported is created. 
    This contains the processed file to be used on the main script

Analyzing data

2. Use main.py to analyze the data
    * It opens file picker where you choose your processed file from the imported directory
    * You can now use 6 different functions to analyze the data
    
    * time_period(data, start_date, end_date, start_time, end_time) 
        * If you want to set a time period from the dataset you can set the function 
            to a variable and use that as the data paraemeter for the rest of the functions
            ex:
            df = time_period(data, "2019-04-29", "2019-04-30", "2:00", "4:00")
            traffic(df,"CR6 @ CR17", 15)
    
    * traffic(data, signal_name, freq) returns bar graph of traffic density of a signal per set frequency
        * ex: traffic(data,"CR6 @ CR17", 15)
        
    * traffic_lane(data, signal_name, freq, *lane) returns bar graph of traffic density of a lane on a signal per set frequency
        * ex: traffic_lane(data,"CR6 @ CR17", 15, 25, 40)
        
    * cycle_length(data, signal_name, phase) returns graph of cycle lengths in seconds for traffic lights 
        * ex: cycle_length(data,"CR6 @ CR17", 2)
        
    * compare(data, signal_name, loop, pod, start, end) returns graph that compares the activity of a loop detector and a pod detector
        * ex: compare(data,"CR6 @ CR17", 13, 54, '13:11', '13:13')
        
    * split_failure(data, signal_name, phase, *dets) returns graph that finds the amount of split failures on a given lane
        * ex: split_failure(data, "CR6 @ CR17", 4, 25, 40)
