import matplotlib.pyplot as plt
import numpy as np

#Generation of distribution range for two sets
x1 = np.linspace(-550, 310, 10)
x2 = np.linspace(-153,1080, 10)

#Generation of mean 
m1 = np.mean(x1)
m2 = np.mean(x2)

#Generation of Standard Deviation
s1 = np.std(x1)
s2 = np.std(x2)

#Printing Mean and Standard Deviation for both the different sets of values to indicate the difference between them
print("Mean 1 =", m1)
print("Mean 2 =", m2)
print("Standard Deviation 1 =", s1)
print("Standard Deviation 2 =", s2)

#Gaussian Distribution formula for two sets of standard deviations
gd1 = 1 / (np.sqrt(2 * np.pi) * s1 ** 2) * np.exp(-((x1-m1) ** 2) / (2 * s1 ** 2))
gd2 = 1 / (np.sqrt(2 * np.pi) * s2 ** 2) * np.exp(-((x2-m2) ** 2) / (2 * s2 ** 2))

#Plot and plot properties
plt.plot(x1, gd1, marker='o', label=f'PDF plot for Std Dev = {s1:.2f}')
plt.plot(x2, gd2, marker='D', label=f'PDF plot for Std Dev = {s2:.2f}')

plt.title("Gaussian Distribuiton for two sets of values for standard deviations")
plt.grid(color = 'Green', linestyle = '--')
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.legend(shadow = True, loc = "upper right")


plt.show()
