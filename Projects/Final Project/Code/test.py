import pandas as pd
import matplotlib.pyplot as plt

# Initialize values for x, y, and z from the dataset
temp_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/temp_month1.csv", nrows = 1)
load_data = pd.read_csv("/Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/AI-in-Smart-Grid/Projects/Final Project/load_month1.csv", nrows = 1)

# Extract the row of data
temp_row_data = temp_data.iloc[0]
load_row_data = load_data.iloc[0]

# Initialize tx, ty, and tz along with lx, ly, and lz values respectively
tx = temp_row_data['h1']
ty = temp_row_data['h2']
tz = temp_row_data['h3']

lx = load_row_data['h1']
ly = load_row_data['h2']
lz = load_row_data['h3']

#Lists to store differences
load_diff = []
temp_diff = []
ratio = []

# Temperature and Load Calculation iteration
for i in range(1, 25):
    try:
        #Calculate load and temperature differences
        load_diff.append(load_row_data[f'h{i+1}'] - load_row_data[f'h{i}'])
        temp_diff.append(temp_row_data[f'h{i+1}'] - temp_row_data[f'h{i}'])
        
        #Calculate Ratio
        if load_diff[-1] != 0:
            ratio.append(temp_diff[-1] / load_diff[-1])
        else:
            ratio.append(0)    

        # Update x, y, and z based on the next set of h values
        tx = ty
        ty = tz
        tz = temp_row_data[f'h{i+3}']
        
        lx = ly
        ly = lz
        lz = load_row_data[f'h{i+3}']

    except KeyError:
        break

#Printing the Load and Temperature differences along with Ratio
print("Load Differences:", load_diff)
print("Temperature Differences:", temp_diff)
print("Ratio:", ratio)

#Array to store positive and negative values
positive_values = []
negative_values = []

#Finding and storing positive and negative values and their corresponding iteration count
for i, val in enumerate(ratio):
    if val > 0:
        positive_values.append((i+1, val))
    elif val < 0:
        negative_values.append((i+1, val))
        
#Calculating percentages
positive_percentage = len(positive_values) / len (ratio) * 100
negative_percentage = len(negative_values) / len (ratio) * 100
    
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
plt.plot(ratio, label = 'Ratio')
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