import pandas as pd
import numpy as np
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Step 1: Read Data and Clean
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv")
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv")

# Replace 0 values with NaN
load_data.replace(0, np.nan, inplace=True)
temp_data.replace(0, np.nan, inplace=True)

# Initialize list to store results
results = []

# Step 2: Iterate Over Combinations
for zone_id in load_data['zone_id'].unique():
    for station_id in temp_data['station_id'].unique():
        # Step 3: Match Dates
        merged_data = pd.merge(load_data[load_data['zone_id'] == zone_id], 
                               temp_data[temp_data['station_id'] == station_id], 
                               on=['year', 'month', 'day'])
        
        if merged_data.empty:
            continue
        
        # Step 4: Calculate Differences and Ratios
        for i in range(1, 25):
            load_col = f'h{i}_x'
            temp_col = f'h{i}_y'
            diff_load_col = f'diff_load_{i}'
            diff_temp_col = f'diff_temp_{i}'
            ratio_col = f'ratio_{i}'
            
            # Calculate differences, considering NaN values
            merged_data[diff_load_col] = merged_data[load_col] - merged_data[load_col].shift(1)
            merged_data[diff_temp_col] = merged_data[temp_col] - merged_data[temp_col].shift(1)
            
            # Replace NaN differences with 0
            merged_data.loc[merged_data[diff_load_col].isnull(), diff_load_col] = 0
            merged_data.loc[merged_data[diff_temp_col].isnull(), diff_temp_col] = 0
            
            # Calculate ratio
            merged_data[ratio_col] = merged_data[diff_temp_col] / merged_data[diff_load_col]
        
        # Step 5: Aggregate Ratios
        merged_data['average_ratio'] = merged_data[[f'ratio_{i}' for i in range(1, 25)]].mean(axis=1, skipna=True)
        
        # Step 6: Separate Positive and Negative Ratios
        positive_ratios = merged_data[merged_data['average_ratio'] > 0]['average_ratio'].tolist()
        negative_ratios = merged_data[merged_data['average_ratio'] < 0]['average_ratio'].tolist()
        
        # Step 7: Calculate Percentages
        total_count = len(merged_data)
        positive_percentage = (len(positive_ratios) / total_count) * 100
        negative_percentage = (len(negative_ratios) / total_count) * 100
        
        # Add results to list
        results.append({'Zone ID': zone_id,
                        'Station ID': station_id,
                        'Positive Percentage': positive_percentage,
                        'Negative Percentage': negative_percentage})

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Export results to CSV file
results_df.to_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Code/results.csv", index=False)

print("Results exported to results.csv")