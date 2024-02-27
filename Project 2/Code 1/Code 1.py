import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.feature_selection import f_regression

#Loading the diabetes dataset
diabetes = load_diabetes()

#Obtaining the feature and target data
ft = diabetes.data
trgt = diabetes.target

#Computing scores from regression for strong linear and non-linear and weak relationship
scores, x = f_regression(ft, trgt)

#Fetching the indices for the 3 types of relationships based on score
str_l_idx = scores.argmax()
str_nl_idx = scores.argsort()[-2]
wk_idx = scores.argmin()

#Plot 1: One feature with strong linear relationship with Disease progression
plt.scatter(ft[:, str_l_idx], trgt)
plt.xlabel('Feature {}'.format(str_l_idx))
plt.ylabel("Disease Progression")
plt.title('Feature with Strong Linear Relationship')
plt.show()

#Plot 2: One feature with strong non-linear relationship with Disease progression
plt.scatter(ft[:, str_nl_idx], trgt)
plt.xlabel('Feature {}'.format(str_nl_idx))
plt.ylabel("Disease Progression")
plt.title('Feature with Strong Non-Linear Relationship')
plt.show()

#Plot 3: One feature with Weak relationship with Disease progression
plt.scatter(ft[:, wk_idx], trgt)
plt.xlabel('Feature {}'.format(wk_idx))
plt.ylabel("Disease Progression")
plt.title('Feature with Weak Relationship')
plt.show()