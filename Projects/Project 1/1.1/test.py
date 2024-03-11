import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

#Reading data from the file
data = pd.read_csv("Advertising.csv")

#Setting input and output arrays
x_arr = data["radio"].to_numpy().reshape(-1,1)
y_arr = data["sales"].to_numpy()

#Initialzing the model and fitting the model with the defined arrays
model = LinearRegression()
model.fit(x_arr,y_arr)

#Defining the coeffiecients and intercepts
coefficients = model.coef_[0]
intercept = model.intercept_

#Setting the budget as per the problem and predicting outcome
budget = 23
estimated_sales = model.predict([[budget]])

#Printing the necessary outputs
print ("Estimated Sales (in $ Millions):", "{:.4f}".format(estimated_sales[0]))
print ("Linear Model Coefficient (Slope):", "{:.4f}".format(coefficients))
print ("Linear Model Coefficient (Intercept):", "{:.4f}".format(intercept))

#Plotting a scatter plot for the given data and outputs with the best fit curve
plt.scatter(x_arr,y_arr, color='red', label='Data Points')
plt.plot(x_arr,model.predict(x_arr), color='blue', label='Best Fit Curve (Line)')
plt.xlabel('Radio Marketing')
plt.ylabel('Sales')
plt.title('Linear Regression curve for the Radio Marketing vs Sales')
plt.legend()
plt.grid()
plt.show()