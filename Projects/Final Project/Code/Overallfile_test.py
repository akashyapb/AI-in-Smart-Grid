import pandas as pd
import matplotlib.pyplot as plt

# Initialize values for x, y, and z from the dataset
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv")
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv")

#Step 2
# Filtering row absed on zone_id and station_id
load_data_filtered = load_data[(load_data['zone_id'] == 1)]
temp_data_filtered = temp_data[(temp_data['station_id'] == 1)]

#Merge filtered data from the two documents for the date filtering
merged_data = pd.merge(load_data_filtered, temp_data_filtered, on = ['day', 'month', 'year'])

#Step 1
#List to store differences
load_diff = []
temp_diff = []

#Iterate of each row in the merged data
for _, row in merged_data.iterrows():
    #Initilizing tx, ty, tz along with lz, ly and lz values respectively
    tx = row['h1_x']
    ty = row['h2_x']
    tz = row['h3_x']
    
    lx = row['h1_y']
    ly = row['h2_y']
    lz = row['h3_y']
    
    #Lists to store the differences of each current row
    row_load_diff = []
    row_temp_diff = []
    
    #Temperature and Load Calculation Iteration
    for i in range(1, 25):
        try:
            #Calculate load and temperature differences
            row_load_diff.append(row[f'h{i+1}_x'] - row[f'h{i}_x'])
            row_temp_diff.append(row[f'h{i+1}_y'] - row[f'h{i}_y'])
            
            #Update x, y and z based on the next set of h values
            tx, ty, tz = ty, tz, row[f'h{i+3}_y']
            lx, ly, lz = ly, lz, row[f'h{i+3}_x']
        
        except KeyError:
            break
    
    #Append the load and temperature differences for the current row to the overall lists
    load_diff.append(row_load_diff)
    temp_diff.append(row_temp_diff)

#Calculate the overall average of temp differences
overall_average_temp_diff = [sum(temp_diff[i] for temp_diff in temp_diff) / len(temp_diff) for i in range(len(temp_diff[0]))]

#Calculate the overall average of load differences
overall_average_load_diff = [sum(load_diff[i] for load_diff in load_diff) / len(load_diff) for i in range(len(load_diff[0]))]
    
#Step 3
#List to store ratios for each row
ratios = []

#Calculate the ratio for each row
for i in range(len(load_diff)):
    row_match_ratio = [temp_diff[i][j] / load_diff[i][j] if load_diff[i][j] != 0 else 0 for j in range(len(load_diff[i]))]
    ratios.append(row_match_ratio)    
        
#Step 4 = Satisfied
#Step 5
#Calculate the overall average ratio for each element
overall_average_ratios = [sum(match_ratio[i] for match_ratio in ratios) / len(ratios) for i in range(len(ratios[0]))]

#Printing the Overall Average Ratio
print("Overall Average Ratios:")
print(overall_average_ratios)

#Step 6
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
            
#Step 7
#Calculating percentages
total_positives = len(positive_values)
total_negatives = len(negative_values)

if total_positives + total_negatives > 0:
    positive_percentage = (total_positives / (total_positives + total_negatives)) * 100
    negative_percentage = (total_negatives / (total_positives + total_negatives)) * 100
else:
    positive_percentage = 0
    negative_percentage = 0                   

#Printing the Positive percentages and Negative percentages
print("Positive Percentage:")
print(positive_percentage)
print("Negative Percentage:")
print(negative_percentage)
    
#Step 8
#Plotting the load and temperature differences
plt.plot(overall_average_load_diff, label = 'Overall Average Load Differences')
plt.xlabel("Iteration")
plt.ylabel("Difference")
plt.title("Load Differences")
plt.legend()
plt.show()

#Plotting the Temperature Differences
plt.plot(overall_average_temp_diff, label = 'Overall Average Temperature Differences')
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