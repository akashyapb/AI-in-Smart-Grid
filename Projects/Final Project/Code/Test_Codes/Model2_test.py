import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import time
from itertools import product

# Measure overall execution time
start_time = time.perf_counter()

# Suppress warnings
import warnings
warnings.filterwarnings("ignore", message="It seems that frozen modules are being used", category=UserWarning)
warnings.filterwarnings("ignore", message="Debugger warning", category=UserWarning)

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

# Step 5: Train-Test Split
X = merged_data.drop(columns=['zone_id', 'year', 'month', 'day', 'Best Station ID'])
y = merged_data.drop(columns=['year', 'month', 'day', 'Best Station ID', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23', 'h24'])

# Step 6: Model Training
model = RandomForestRegressor(n_estimators=100, max_depth=7, n_jobs=-1)
model.fit(X, y)

# Step 7: Predict Load for 1st Week of June
# Generate all combinations of zone_id, year, month, and day for the 1st week of June 2008
zones = merged_data['zone_id'].unique()
dates = [(2008, 6, day) for day in range(1, 8)]
combinations = list(product(zones, *zip(*dates)))

# Create DataFrame with all combinations
june_data = pd.DataFrame(combinations, columns=['zone_id', 'year', 'month', 'day'])

# Rename 'Zone ID' column to 'zone_id' in zone_to_station DataFrame
june_data.rename(columns={'Zone ID': 'zone_id'}, inplace=True)

# Ensure 'zone_id' column exists in june_data
if 'zone_id' not in june_data.columns:
    print("Warning: 'zone_id' column not found in june_data.")

# Rename 'Zone ID' column to 'zone_id' in zone_to_station DataFrame
zone_to_station.rename(columns={'Zone ID': 'zone_id'}, inplace=True)
zone_to_station.rename(columns={'Best Station ID': 'station_id'}, inplace = True)

# Merge with zone_to_station data
print(zone_to_station.head())
print(june_data.head())
if not zone_to_station.empty:
    june_data = pd.merge(june_data, zone_to_station, on='zone_id', how='inner')
else:
    print("Warning: 'zone_to_station' DataFrame is empty.")

# Merge with temperature data
june_data = pd.merge(june_data, temp_data, on=['station_id', 'year', 'month', 'day'], how='inner')

# Remove unnecessary columns
june_data.drop(columns=['station_id'], inplace=True)

# Predict load for 1st week of June
june_predictions = model.predict(june_data.drop(columns=['zone_id', 'year', 'month', 'day']))

# Create DataFrame for predictions
june_predictions_df = june_data[['zone_id']].copy()
june_predictions_df['Predicted Load'] = june_predictions

# Export predictions to CSV
june_predictions_df.to_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Code/june_predictions.csv", index=False)

#Measure the overall execution time
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Overall Execution Time: {execution_time:0.4f} seconds")






# Step 9: Calculate Top 10 Prediction Errors
# Calculate predictions for test data
y_test_pred = model.predict(X_test)

# Calculate relative percentage error
relative_percentage_error = 100 * (y_test.values.flatten() - y_test_pred) / y_test.values.flatten()

# Create DataFrame for prediction errors
prediction_errors = pd.DataFrame({
    'zone_id': X_test['zone_id'],
    'year': X_test['year'],
    'month': X_test['month'],
    'day': X_test['day'],
    'Predicted Load': y_test_pred,
    'True Load': y_test.values.flatten(),
    'Relative Percentage Error': relative_percentage_error
})

# Sort by magnitude of Relative Percentage Error in decreasing order
top_10_errors = prediction_errors.nlargest(10, 'Relative Percentage Error', key=abs)

# Display top 10 errors
print("\nTop 10 Prediction Errors:")
print(top_10_errors)