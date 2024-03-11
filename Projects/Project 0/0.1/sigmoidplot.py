import matplotlib.pyplot as plt
import numpy as np

#Range of sigmoid plot definition
r1 = -6
r2 = 6

#Generation of evenly spaced points within the range defined
x = np.linspace(r1,r2,100)

#Sigmoid function formula
y = 1/(1+np.exp(-x))

#Plot and plot properties
plt.plot(x, y)

plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title(f"Sigmoid Plot from {r1:.1f} to {r2:.1f}") #f-string is used to fetch data from the defined variables
plt.grid(color = 'Red', linestyle = '--')

plt.show()