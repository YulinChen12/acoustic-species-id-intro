#!/usr/bin/env python
# coding: utf-8

# In[174]:


import pandas as pd
import numpy as np
# The function takes in csv path and output a new csv file with a stratified
# random sample of the original csv. Should return True/False if the stratified csv file was
# successful
def stratified_sample(input_path,output_path):
    #try if the stratified csv file is successful
    try:
        #read the csv file
        audio = pd.read_csv(input_path,dtype=str)
        
        # Two variables that make sure that the audiomoths are 46.1 megabytes and 1-minute long for reference
        reference_file_size = 46080360
        duration = 60
        
        #Two data cleanning concepts,store duration as float and FileSize as int to make easier 
        #comparion in the future
        audio["Duration"] = audio["Duration"].astype(float)
        audio["FileSize"] = audio["FileSize"].astype(int)
        
        #Create a new column called Hour 
        audio["Hour"] = pd.to_datetime(audio['StartDateTime'],dayfirst=True).dt.hour
        
        #Filtering the audio dataframe with the condition that the audiomoths are 46.1 megabytes and 1-minute long
        filter_data = audio[(audio['FileSize'] == reference_file_size ) & (audio['Duration'] >= duration)& (audio['Duration'] < duration+1)]
        
        #Audiomoths with some problems,excluing those.
        excluded_Audiomoth = ['AM-21', 'AM-19', 'AM-8', 'AM-28']
        included_Audiomoth = filter_data[~filter_data['AudioMothCode'].isin(excluded_Audiomoth)]
        
        #Filtering the inclued audiomoth dataframe with the condition that if an 
        # Audiomoth device has enough clips(24 clips for each hour)
        enough_clips_audiomoth = included_Audiomoth.groupby('AudioMothCode').filter(lambda x: x['Hour'].nunique() == 24)
        
        combined_data = pd.DataFrame()
        
        #Loop through each inclued audiomoth in the dataframe.
        for Audio_device in enough_clips_audiomoth['AudioMothCode'].unique():
            #sub dataframe with each inclued audiomoth
            device_data = enough_clips_audiomoth[enough_clips_audiomoth['AudioMothCode'] == Audio_device]
            
            #Find valid audio clips for all 24 hours
            for hour in range(24): 
                # sub dataframe for each hour of each audiomoth
                hour_data = device_data[device_data['Hour'] == hour]
                if not hour_data.empty:
                    #if not empty,randomly choose one clip for this current hour
                    sample = hour_data.sample(n=1, random_state=1)
                    #add that clip into the combined dataframe
                    combined_data = pd.concat([combined_data, sample], ignore_index=True)
        #save the dataframe into a csv file.
        combined_data.to_csv(output_path)
        return True
    #catch if the strafied is not successful
    except Exception as fail:
        return False

