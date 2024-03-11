import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#Loading dataset, initializzing and splitting into training, validation and testing
data = load_breast_cancer()
ftr = data.data
trgt = data.target
ftr_train, ftr_test, trgt_train, trgt_test = train_test_split(ftr, trgt, test_size = 0.05, random_state = 50)
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train, trgt_train, test_size = 0.5, random_state = 25)

#Creation of Decision Tree regression model and fitting the data
dtr = DecisionTreeRegressor()
dtr.fit(ftr_train, trgt_train)

#Obtaining the feature importances of 5 best features
imp = dtr.feature_importances_
top_indices = np.argsort(imp)[-5:][::-1]
top_features = data.feature_names[top_indices]
feature_scores = imp[top_indices]

#Calculating model efficiency score
score = dtr.score(ftr_val, trgt_val)

# Get all feature scores
all_feature_scores = dtr.feature_importances_

print("All Features:")
for feature, scr in zip(data.feature_names, all_feature_scores):
    print(f"{feature}: {scr}")

#Printing the results
print("\nModel Efficiency score:", score)
print("\nThe best 5 features are:")
for feature, scr in zip(top_features, feature_scores):
    print(f"{feature} : {scr}")
    
#Applying the test data to the model and printing the final score
final_score = dtr.score(ftr_test, trgt_test)
print("\nFinal Score:", final_score)    