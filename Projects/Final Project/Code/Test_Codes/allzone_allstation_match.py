import pandas as pd
import numpy as np

#Read data from CSV files
load_data = pd.read_csv('/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv')
temp_data = pd.read_csv('/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv')

#Initializing empty lists to store results
positive_percentages = []
negative_percentages = []

#Iterating over each combination of zone_id and station_id
for zone_id in range(1, 21):
    for station_id in range(1, 10):
        #Filter the data based on Zone_id and Station_id
        load_filtered = load_data[(load_data['zone_id'] == zone_id)]
       
        temp_filtered = temp_data[(temp_data['station_id'] == station_id)]
        
        #Merge the filtered data based on date
        merged_data = pd.merge(load_filtered, temp_filtered, on = ['year', 'month', 'day'])
        
        #Calculate the differences between the consecutive values
        load_diff = merged_data.iloc[:, 4:28].diff(axis = 1)
        temp_diff = merged_data.iloc[:, 28:52].diff(axis = 1)
        
        #Divide the corresponding values from temp_diff by load_diff
        ratios = temp_diff / load_diff
        
        #Calculate the average of the ratios
        average_ratios = ratios.mean(axis = 1)
        
        #Seperate positive and negative values
        positive_values = average_ratios[average_ratios > 0]
        negative_values = average_ratios[average_ratios < 0]
        
        #Calculate the percentages
        positive_percentage = (len(positive_values) / len(average_ratios)) * 100
        negative_percentage = (len(negative_values) / len(average_ratios)) * 100
        
        #Append the percentages to the respective lists
        positive_percentages.append(positive_percentage)
        negative_percentages.append(negative_percentage)
        
#Print the positive and negative percentages for each combination
#for i in range(len(positive_percentages)):
print(f"Combination: Zone_id: {zone_id}, Station_id: {station_id}")    
print(f"Positive Percentage = {positive_percentages}%, Negative Percentage = {negative_percentages}%")
print()
            
        