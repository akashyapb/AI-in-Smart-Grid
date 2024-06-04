import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
import warnings
import time

#Measure overall execution time
start_time = time.perf_counter()

# Suppress warnings
warnings.filterwarnings("ignore")

# Step 1: Data Loading
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Load_history_final.csv")
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Temp_history_final.csv")
combined_results = pd.read_csv("combined_results.csv")

# Step 2: Data Preprocessing
# Replace 0 values with NaN
load_data.replace(0, np.nan, inplace=True)
temp_data.replace(0, np.nan, inplace=True)

# Remove rows with NaN values
load_data.dropna(inplace=True)
temp_data.dropna(inplace=True)

# Step 3: Data Correlation
# Extract unique zone IDs and corresponding best station IDs from combined_results
zone_to_station = combined_results.drop_duplicates(subset=['Zone ID'])[['Zone ID', 'Best Station ID']]

# Step 4: Data Merging
# Merge load_data and temp_data based on zone_id and station_id
merged_data = pd.merge(load_data, zone_to_station, left_on='zone_id', right_on='Zone ID', how='inner')
merged_data.drop(columns=['Zone ID'], inplace=True)  # Drop redundant column

# Step 5: Sample Validation
# Choose a few random samples from merged_data and cross-check with combined_results.csv
# For example, select 5 random rows and validate the mapping
sample_rows = merged_data.sample(n=5, random_state=42)
print("\nSample Validation:")
for index, row in sample_rows.iterrows():
    # Check if 'station_id' is present in the row
    if 'station_id' in row:
        station_id = row['station_id']
    else:
        # Use the correct column name if it's different
        station_id = row['Best Station ID']
    
    zone_id = row['zone_id']
    # Ensure 'Zone ID' is used if 'zone_id' is not present in row
    if 'zone_id' in row:
        zone_id = row['zone_id']
    else:
        zone_id = row['Zone ID']
        
    best_station_id = zone_to_station[zone_to_station['Zone ID'] == zone_id]['Best Station ID'].values[0]
    print(f"Zone ID: {zone_id}, Station ID: {station_id}, Best Station ID: {best_station_id}")
print()

# Step 6: Train-Test Split
X = merged_data.drop(columns=['zone_id', 'year', 'month', 'day', 'Best Station ID'])
y = merged_data[['h1']]  # Select one of the hour columns for training

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Model Training
model = LogisticRegression()
model.fit(X_train, y_train.values.ravel())  # Convert y_train to 1D array using ravel()

# Step 8: Model Evaluation
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
mean_cv_score = np.mean(cv_scores)
print("Mean Cross-Validation Score:", mean_cv_score)

y_pred = model.predict(X_test)
overall_deviation = mean_squared_error(y_test, y_pred)
print("Overall Deviation:", overall_deviation)
print()

#Measure the overall execution time
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Overall Execution Time: {execution_time:0.4f} seconds")
print()