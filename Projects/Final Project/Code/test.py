import pandas as pd
import matplotlib.pyplot as plt

# Logic of the function
def x_calc(x, y, z):
    return (y - x) / (z - y)

# Initialize values for x, y, and z from the dataset
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/temp_month1.csv", nrows = 1)
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/load_month1.csv", nrows = 1)

# Extract the row of data
temp_row_data = temp_data.iloc[0]
load_row_data = load_data.iloc[0]

# Initialize x, y, and z with h1, h2, and h3 values respectively
tx = temp_row_data['h1']
ty = temp_row_data['h2']
tz = temp_row_data['h3']

lx = temp_row_data['h1']
ly = temp_row_data['h2']
lz = temp_row_data['h3']

#List creation to store differences
tr_values = []
lr_values = []

diff_values = []

# Temperature and Load Calculation iteration
for i in range(1, 23):
    try:
        tr = x_calc(tx, ty, tz)
        lr = x_calc(lx, ly, lz)
        print(f"tr{i}: {tr}")
        print(f"lr{i}: {lr}")

        # Update x, y, and z based on the next set of h values
        tx = ty
        ty = tz
        tz = temp_row_data[f'h{i+3}']
        
        lx = ly
        ly = lz
        lz = load_row_data[f'h{i+3}']
        
        #Calculating the difference between tr and lr
        diff = tr - lr
        diff_values.append(diff)
        
        #Store the tr and lr values
        tr_values.append(tr)
        lr_values.append(lr)

    except KeyError:
        break
    
#Plotting the tr and lr values
plt.plot(tr_values, label = 'tr')
plt.plot(lr_values, label = 'lr')
plt.xlabel("Iteration")
plt.ylabel("Value")
plt.title("Comparision for tr and lr values")
plt.legend()
plt.show()

#Printing the differences between tr and lr values
print("Differences between tr and lr:", diff_values)