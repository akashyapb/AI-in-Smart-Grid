import pandas as pd
import matplotlib.pyplot as plt

# Initialize values for x, y, and z from the dataset
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv")
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv")

#Merge filtered data from the two documents for the date filtering
merged_data = pd.merge(load_data, temp_data, on = ['day', 'month', 'year'])

#Initialize a list to store the percentages for each zone_id and station_id combination
#percentages = []

#Iterate over unique zone_id and station_id combinations:
for zone_id in merged_data['zone_id'].unique():
    for station_id in merged_data['station_id'].unique():
        filtered_data = merged_data[(merged_data['zone_id'] == zone_id) & (merged_data['station_id'] == station_id)]

#List to store differences
load_diff = []
temp_diff = []
ratios = []

#Iterate of each row in the merged data
for _, row in filtered_data.iterrows():
    #Initilizing tx and ty along with lz and ly values respectively
    tx = row['h1_x']
    ty = row['h2_x']
    
    lx = row['h1_y']
    ly = row['h2_y']
    
    #Lists to store the differences of each current row
    row_load_diff = []
    row_temp_diff = []
    
    #List to store ratios for each row
    #ratios = []
    
    #Temperature and Load Calculation Iteration
    for i in range(1, 25):
        try:
            #Calculate load and temperature differences
            row_load_diff.append(row[f'h{i+1}_x'] - row[f'h{i}_x'])
            row_temp_diff.append(row[f'h{i+1}_y'] - row[f'h{i}_y'])
            
            #Update x and y based on the next set of h values
            tx, ty = ty, row[f'h{i+2}_y']
            lx, ly = ly, row[f'h{i+2}_x']

            #Append the load and temperature differences for the current row to the overall lists
            load_diff.append(row_load_diff)
            temp_diff.append(row_temp_diff)
            
            #Calculate the ratio for the current row
            row_match_ratio = [row_temp_diff[j] / row_load_diff[j] if row_load_diff[j] != 0 else 0 for j in range(len(row_load_diff))]
            ratios.append(row_match_ratio)
            
        except KeyError:
            break

#Calculate the overall average of temp differences for current combination
overall_average_temp_diff = [sum(temp_diff[j] for temp_diff in temp_diff) / len(temp_diff) for j in range(len(temp_diff[0]))]

#Calculate the overall average of load differences for current combination
overall_average_load_diff = [sum(load_diff[j] for load_diff in load_diff) / len(load_diff) for j in range(len(load_diff[0]))]

#Calculate the ratio for each row
#for i in range(len(load_diff)):
#    row_match_ratio = [temp_diff[i][j] / load_diff[i][j] if load_diff[i][j] != 0 else 0 for j in range(len(load_diff[i]))]
#    ratios.append(row_match_ratio)    
        
#Calculate the overall average ratio for each element
overall_average_ratios = [sum(ratios[j] for ratios in ratios) / len(ratios) for j in range(len(ratios[0]))]

#Printing the Overall Average Ratio
print("Overall Average Ratios:")
print(overall_average_ratios)

#Lists to store positive and negative values
positive_values = []
negative_values = []

#Finding and storing positive and negative values and their corresponding iteration count
for i, match_ratio in enumerate(ratios, start = 1):
    for j, val in enumerate(match_ratio, start = 1):
        if val > 0:
            positive_values.append((i, j, val))
        elif val < 0:
            negative_values.append((i, j, val))
            
#Calculating percentages
total_positives = len(positive_values)
total_negatives = len(negative_values)

if total_positives + total_negatives > 0:
    positive_percentage = (total_positives / (total_positives + total_negatives)) * 100
    negative_percentage = (total_negatives / (total_positives + total_negatives)) * 100
else:
    positive_percentage = 0
    negative_percentage = 0                   

# Printing the results for the current combination
print(f"Zone ID: {zone_id}, Station ID: {station_id}, Positive Percentage: {positive_percentage}, Negative Percentage: {negative_percentage}")
#Append the percentages to the list
#percentages.append({'Zone_id': zone_id, 'Station_id': station_id, 'Positive Percentages': positive_percentage, 'Negative Percentages': negative_percentage})
#Printing the Positive percentages and Negative percentages
#for percentage in percentages:
#    print(f"Zone ID: {zone_id}, Station ID: {station_id}, Positive Percentages: {positive_percentage}, Negative Percentages: {negative_percentage}")
    
#Plotting the load and temperature differences
plt.plot(overall_average_load_diff, label = f'Zone {zone_id}, Station {station_id} - Load Differences')
plt.xlabel("Iteration")
plt.ylabel("Difference")
plt.title("Load Differences")
plt.legend()
plt.show()

#Plotting the Temperature Differences
plt.plot(overall_average_temp_diff, label = f'Zone {zone_id}, Station {station_id} - Temperature Differences')
plt.xlabel("Iteration")
plt.ylabel("Difference")
plt.title("Temperature Differences")
plt.legend()
plt.show()

#Plotting the Ratio
plt.plot(overall_average_ratios, label = 'Ratio')
plt.xlabel('Iteration')
plt.ylabel('Ratio')
plt.title('Ratio of Temperature Differences to Load Differences')
plt.legend()
plt.show()    