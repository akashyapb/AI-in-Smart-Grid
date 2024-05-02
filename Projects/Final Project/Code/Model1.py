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

# Step 3: Sample Validation
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

# Step 5: Train-Test Split
X = merged_data.drop(columns=['zone_id', 'year', 'month', 'day', 'Best Station ID'])
y = merged_data.drop(columns=['year', 'month', 'day', 'Best Station ID', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23', 'h24'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Model Training
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 7: Model Evaluation
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
mean_cv_score = np.mean(cv_scores)
print("Mean Cross-Validation Score:", mean_cv_score)

y_pred = model.predict(X_test)
overall_deviation = mean_squared_error(y_test, y_pred)
print("Overall Deviation:", overall_deviation)
print()

# Step 8: Calculate Top 10 Prediction Errors
# Calculate predictions for test data
y_test_pred = model.predict(X_test)

# Calculate relative percentage error
relative_percentage_error = 100 * (y_test.values - y_test_pred) / y_test.values

# Create DataFrame for prediction errors
prediction_errors = pd.DataFrame({
    'zone': X_test['zone_id'],
    'year': X_test['year'],
    'month': X_test['month'],
    'day': X_test['day'],
    'hour': np.arange(1, 25).repeat(len(X_test)),  # Repeat each hour for each row in X_test
    'predicted_load': y_test_pred.flatten(),  # Flatten y_test_pred to match shape of y_test
    'true_load': y_test.values.flatten(),
    'relative_percentage_error': relative_percentage_error.flatten()
})

# Sort by magnitude of Relative Percentage Error in decreasing order
top_10_errors = prediction_errors.copy()
top_10_errors['relative_percentage_error'] = np.abs(prediction_errors['relative_percentage_error'])  # Take absolute values for sorting
top_10_errors = top_10_errors.nlargest(10, 'relative_percentage_error')

# Display top 10 errors
print("\nTop 10 Prediction Errors:")
print(top_10_errors[['zone', 'year', 'month', 'day', 'hour', 'predicted_load', 'true_load', 'relative_percentage_error']])

#Measure the overall execution time
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Overall Execution Time: {execution_time:0.4f} seconds")
print()