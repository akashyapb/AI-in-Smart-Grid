import pandas as pd
import numpy as np

temperature_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv")
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv")

#Iterate over each Temperature Station
for station in temperature_data.columns[3:]:
    #Iterate over each Load Zone
    for zone in load_data.columns[3:]:
        #Calculate the correlation between temperature and load data for the current station and zone
        correlation = temperature_data[station].corr(load_data[zone])
        
        #Print the Correlation for the current station and zone combination
        print(f"Correlation between {zone} and {station}: {correlation}")
        
#Iterate over each row of the temperature data
for temp_row in temperature_data.itertuples():
    #Iterate over each row of the load data
    for load_row in load_data.itertuples():
        #Compare the day, month and year values
        if temp_row.day == load_row.day and temp_row.month == load_row.month and temp_row.year == temp_row.year:
            #Map the Temperature and Load data for each hour of the day
            for hour in range(1, 25):
                temperature = temp_row[hour + 4] #Since the temperature data starts from column 5
                load = load_data[hour + 4] #Since the load data starts from column 5
                
#Creating a dictionary to store the average ratio for each combination
average_ratios = {}

#Iterate of each row of the temperature data
for temp_row in temperature_data.itertuples():
    #Iterate over each row of the load data
    for load_row in load_data.itertuples():
        #Comparing the day, month and year values
        if temp_row.day == load_row.day and temp_row.month == load_row.month and temp_row.year == load_row.year:
            #Mapping the temperature data to the load data for each hour of the day
            for hour in range(1, 25):
                temperature = temp_row[hour + 4] #Since the temperature data starts from column 5
                load = load_row[hour + 4] #Since the load data starts from column 5
                
                #Calculating the ratio between temperature and load
                ratio = temperature / load
                
                #Fetching the combination of load zone and temperature station
                combination = f"{temp_row.zone}-{load_row.station}"
                
                #Update the average ratio of the current combination
                if combination in average_ratios:
                    average_ratios[combination].append(ratio)
                else:
                    average_ratios[combination] = [ratio]
                    
#Calculating the average ratio of each combination of zone and station
for combination, ratios in average_ratios.items():
    average_ratio = np.mean(ratios)
    print(f"Combination: {combination}, Average Ratio: {average_ratio}")     
    
              