import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error

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

# Display the shape of the datasets after preprocessing
print("Shape of load_data after preprocessing:", load_data.shape)
print("Shape of temp_data after preprocessing:", temp_data.shape)

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
