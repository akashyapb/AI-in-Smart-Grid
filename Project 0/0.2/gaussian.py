import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import norm
#import statistics

#Distribution Ranges from 1.1 to 1.2 and 2.1 to 2.2
range1 = [-200,500]
range2 = (-500,300)

#x1 = np.arange(r1, r2, 50)
#x2 = np.arange(r3, r4, 50)

#m1 = statistics.mean(x1)
m1 = sum(range1)/len(range1)
#m2 = statistics.mean(x2)
m2 = sum(range2)/len(range2)

#s1 = statistics.stdev(x1)

#s2 = statistics.stdev(x2)

#plt.plot(x1, norm.pdf(x1, m1, s1), marker = 'o', label = 'PDF plot for range -200 to 500')
#plt.plot(x2, norm.pdf(x2, m2, s2), marker = "D", label = 'PDF plot for range -500 to 300')

#plt.title("Gaussian Distribuiton for two sets of values")
#plt.grid(color = 'Green', linestyle = '--')
#plt.xlabel("X Axis")
#plt.ylabel("Y Axis")
#plt.legend(shadow = True, loc = "upper left")

#plt.show()



