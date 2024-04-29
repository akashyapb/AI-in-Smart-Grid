import pandas as pd

# Step 1: Read Data
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv")
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv")

# Step 2: Iterate Over Combinations
for zone_id in load_data['zone_id'].unique():
    for station_id in temp_data['station_id'].unique():
        # Step 3: Match Dates
        merged_data = pd.merge(load_data[load_data['zone_id'] == zone_id], 
                               temp_data[temp_data['station_id'] == station_id], 
                               on=['year', 'month', 'day'])
        
        if merged_data.empty:
            continue
        
        print(f"Processing Zone ID: {zone_id}, Station ID: {station_id}")
        
        # Step 4: Calculate Ratios and Percentages
        valid_ratios = []
        for i in range(1, 25):
            load_col = f'h{i}_x'
            temp_col = f'h{i}_y'
            
            # Check for zero values in raw data before calculating differences
            if (merged_data[load_col] == 0).any() or (merged_data[temp_col] == 0).any():
                print(f"Zero values found in raw data for hour {i}, skipping...")
                continue
            
            diff_load = merged_data[load_col] - merged_data[load_col].shift(1)
            diff_temp = merged_data[temp_col] - merged_data[temp_col].shift(1)
            
            # Check for zero values in differences for this hour
            if diff_load.iloc[i-1] == 0 or diff_temp.iloc[i-1] == 0:
                print(f"Zero value found in differences for hour {i}, skipping...")
                continue
            
            ratio = diff_temp / diff_load
            valid_ratios.extend(ratio)
        
        # Step 5: Calculate Percentages
        if not valid_ratios:
            print("No valid ratios without zero values, setting percentages to 0...")
            positive_percentage = 0
            negative_percentage = 0
        else:
            positive_ratio_count = sum(ratio > 0 for ratio in valid_ratios)
            negative_ratio_count = sum(ratio < 0 for ratio in valid_ratios)
            total_valid_ratios = len(valid_ratios)
            
            positive_percentage = (positive_ratio_count / total_valid_ratios) * 100
            negative_percentage = (negative_ratio_count / total_valid_ratios) * 100
        
        # Step 6: Display Results
        print(f"Zone ID: {zone_id}, Station ID: {station_id}")
        print(f"Positive Percentage: {positive_percentage:.2f}%")
        print(f"Negative Percentage: {negative_percentage:.2f}%")
        print("-" * 30)
