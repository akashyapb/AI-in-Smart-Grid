import pandas as pd
import matplotlib.pyplot as plt

# Initialize values for x, y, and z from the dataset
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/temp_month1.csv")
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/load_month1.csv")

# Filtering row absed on zone_id and station_id
load_data_filtered = load_data[(load_data['zone_id'] == 1)]
temp_data_filtered = temp_data[(temp_data['station_id'] == 1)]

#Merge filtered data from the two documents for the date filtering
merged_data = pd.merge(load_data_filtered, temp_data_filtered, on = ['day', 'month', 'year'])

#Lists to store differences
load_diff = []
temp_diff = []
ratios = []

# Iterate over each row in the merged data
for _, row in merged_data.iterrows():
        #Initialize tx, ty, and tz along with lx, ly, and lz values respectively
        tx = row['h1_x']
        ty = row['h2_x']
        tz = row['h3_x']
        
        lx = row['h1_y']
        ly = row['h2_y']
        lz = row['h3_y']
        
#Temperature and Load Calculation Iteration
for i in range(1, 25):
    try:
        #Calculate load and temperature differences
        load_diff.append(row[f'h{i+1}_x'] - row[f'h{i}_x'])
        temp_diff.append(row[f'h{i+1}_y'] - row[f'h{i}_y'])

        # Update x, y, and z based on the next set of h values  
        tx, ty, tz = ty, tz, row[f'h{i+3}_y']
        lx, ly, lz = ly, lz, row[f'h{i+3}_x']

    except KeyError:
        break

#Calculate the ratio for the current match
match_ratio = [temp_diff[i] / load_diff[i] if load_diff[i] != 0 else 0 for i in range(len(load_diff))]

#Append the match ratios to the list of ratios
ratios.append(match_ratio)

#Calculating the overall average ratio for each element across all rows
overall_average_ratios = [sum(match_ratio[i] for match_ratio in ratios) / len(ratios) for i in range(len(match_ratio))]

#Printing the overall average ratio
print("Overall Average Ratio:", overall_average_ratios)

#Printing the Load and Temperature differences along with Ratio
print("Load Differences:", load_diff)
print("Temperature Differences:", temp_diff)

#Array to store positive and negative values
positive_values = []
negative_values = []

#Finding and storing positive and negative values and their corresponding iteration count
for match_ratio in ratios:
    for i, val in enumerate(match_ratio):
        if val > 0:
            positive_values.append((i+1, val))
        elif val < 0:
            negative_values.append((i+1, val))
        
#Calculate the total number of positive and negative values
total_positive = sum(len([val for val in match_ratio if val > 0]) for match_ratio in ratios)
total_negative = sum(len([val for val in match_ratio if val > 0]) for match_ratio in ratios)

#Calculating percentages
if len(ratios) > 0:
    positive_percentage = (total_positive / (total_positive + total_negative)) * 100
    negative_percentage = (total_negative / (total_positive + total_negative)) * 100
else:
    positive_percentage = 0
    negative_percentage = 0    
    
#Plotting the load and temperature differences
plt.plot(load_diff, label = 'Load Differences')
plt.xlabel("Iteration")
plt.ylabel("Difference")
plt.title("Load Differences")
plt.legend()
plt.show()

#Plotting the Temperature Differences
plt.plot(temp_diff, label = 'Temperature Differences')
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

#Printing the positive and negative values
print("Positive Differences:")
for i, val in positive_values:
    print("Iteration:", i, "Value:", val)

print("Negative Differences:")
for i, val in negative_values:
    print("Iteration:", i, "Value:", val)
    
#Printing the percentages
print("Percentage of Positive Values:", positive_percentage)
print("Percentage of Negative Values:", negative_percentage)