import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

#Loading the data to the 'data' variable
data = load_diabetes()

#Preparing the feature matrix and the target vector
ftr = pd.DataFrame(data.data, columns = data.feature_names)
target = data.target

#Splitting the data for Training, Validation and Testing
ftr_train, ftr_test, target_train, target_test = train_test_split(ftr, target, test_size = 0.2, random_state = 10)
ftr_train, ftr_val, target_train, target_val = train_test_split(ftr_train, target_train, test_size = 0.5, random_state = 15)

#Creting an instance of the Lasso model and fitting the model to the data
lasso = Lasso()
lasso.fit(ftr_train,target_train)
#lasso.fit(ftr_val,target_val)
#lasso.fit(ftr_test,target_test)

#Obtaining the co-efficients and the corresponding feature names
ftr_coef = pd.Series(lasso.coef_, index = ftr.columns)
print("The score of individual features for disease progression are as follows:")
print(ftr_coef)

#Sorting the obtained feature co-efficients in descending order and selecting the top 5 features
sorted_desc = ftr_coef.abs().sort_values(ascending = False)
best_ftr = sorted_desc[:5].index.to_list()

#Printing the results
print("Top 5 features that best predict disease progression are:")
for i in best_ftr:
    print(i)