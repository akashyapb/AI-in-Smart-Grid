import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import warnings
import time
from itertools import product

# Measure overall execution time
start_time = time.perf_counter()

# Suppress warnings
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

#print(load_data.head())
#print(combined_results.head())
# Rename 'Zone ID' column to 'zone_id' in combined_results DataFrame
combined_results.rename(columns={'Zone ID': 'zone_id'}, inplace=True)
# Step 3: Data Merging
# Merge load_data and temp_data based on zone_id
merged_data = pd.merge(load_data, combined_results, on='zone_id', how='inner')

# Step 4: Train-Test Split
X = merged_data.drop(columns=['zone_id', 'year', 'month', 'day', 'Best Station ID'])
y = merged_data[['year', 'month', 'day', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23', 'h24']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Model Training and Prediction for Each Hour
hourly_predictions = {}
for hour in range(1, 25):
    model = RandomForestRegressor(n_estimators=100, max_depth=7, n_jobs=-1)
    model.fit(X_train, y_train[f'h{hour}'])
    y_pred = model.predict(X_test)
    hourly_predictions[f'h{hour}'] = y_pred

# Step 6: Combine Hourly Predictions for Entire Population
population_predictions = pd.DataFrame(hourly_predictions)

# Step 7: Export Predictions to CSV
population_predictions.to_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/Code/population_predictions.csv", index=False)

# Measure the overall execution time
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Overall Execution Time: {execution_time:0.4f} seconds")