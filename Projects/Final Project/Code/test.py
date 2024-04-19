import pandas as pd

# Logic of the function
def x_calc(x, y, z):
    return (y - x) / (z - y)

# Initialize values for x, y, and z from the dataset
data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/temp_month1.csv", nrows=1)

# Extract the row of data
row_data = data.iloc[0]

# Initialize x, y, and z with h1, h2, and h3 values respectively
x = row_data['h1']
y = row_data['h2']
z = row_data['h3']

# Calculation iteration
for i in range(1, 23):
    try:
        r = x_calc(x, y, z)
        print(f"r{i}: {r}")

        # Update x, y, and z based on the next set of h values
        x = y
        y = z
        z = row_data[f'h{i+3}']
    except KeyError:
        break