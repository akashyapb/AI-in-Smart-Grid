import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

#Loading dataset, initializzing and splitting into training, validation and testing
data = load_breast_cancer()
ftr = data.data
trgt = data.target
ftr_train, ftr_test, trgt_train, trgt_test = train_test_split(ftr, trgt, test_size = 0.2, random_state = 50)
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train, trgt_train, test_size = 0.25, random_state = 25)

#Scaling the features
scaler = StandardScaler()
ftr_train_scaled = scaler.fit_transform(ftr_train)
ftr_val_scaled = scaler.transform(ftr_val)
ftr_test_scaled = scaler.transform(ftr_test)

#Creation of Logistic regression model and fitting the data
lr = LogisticRegression(penalty = 'l1', solver = 'liblinear')
lr.fit(ftr_train_scaled, trgt_train)

#Obtaining the Logistic Regression coeffiencents of 5 best features
coef = np.abs(lr.coef_)
top_indices = np.argsort(coef)[0][-5:][::-1]
top_features = data.feature_names[top_indices]
feature_score = coef[0][top_indices]

#Plotting the graph for 3 features that do a good job
good_ftr_indices = top_indices[:3]
good_ftr_names = data.feature_names[good_ftr_indices]
good_ftr_scores = coef[0][good_ftr_indices]

plt.figure(figsize = (10,5))
plt.bar(good_ftr_names, good_ftr_scores)
plt.title("Top 3 features that do a good job")
plt.xlabel("Feature")
plt.ylabel("Logistic Regressor Coefficients")

#Adding score value on top of each bar
for i, j in enumerate(good_ftr_scores):
    plt.text(i, j, str(round(j, 2)), ha = 'center', va = 'bottom')

plt.show()
    
#Obtaining the Logistic Regression coeffiencents of 5 worst features
worst_ftr_indices = np.argsort(coef)[0][:3]
worst_ftr_names = data.feature_names[worst_ftr_indices]
worst_ftr_scores = coef[0][worst_ftr_indices]

#Plotting the graph for 3 features that do a worst job
plt.figure(figsize = (10,5))
plt.bar(worst_ftr_names, worst_ftr_scores)
plt.title("Top 3 features that do a Worst job")
plt.xlabel("Feature")
plt.ylabel("Logistic Regressor Coefficients")

#Adding score value on top of each bar
for i, j in enumerate(worst_ftr_scores):
    plt.text(i, j, str(round(j, 2)), ha = 'center', va = 'bottom')

plt.show()
    
#Selecting 5 best features for classification
selected_ftr = data.data[:, top_indices]

#Developing the K Nearest Neighbour Classifier using the best features
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(selected_ftr, trgt)

#Calculating model efficiency score
score = lr.score(ftr_val_scaled, trgt_val)

# Get all feature scores
all_feature_scores = coef[0]

print("All Features:")
for feature, scr in zip(data.feature_names, all_feature_scores):
    print(f"{feature}: {scr}")

#Printing the results
print("\nModel Efficiency score:", score)
print("\nThe best 5 features are:")
for feature, scr in zip(top_features, feature_score):
    print(f"{feature} : {scr}")
    
#Applying the test data to the model and printing the final score
final_score = lr.score(ftr_test_scaled, trgt_test)
print("\nFinal Score:", final_score)

# Applying the test data to the classifier and printing the final score
ftr_test_selected = ftr_test[:, top_indices]
final_score = knn.score(ftr_test_selected, trgt_test)
print("\nFinal score upon KNN Classification", final_score)    

#Classifying examples as benign and malignant based on prediction score
pred = knn.predict(ftr_test_selected)
benign_examples = ftr_test_selected[pred == 0][:3]
malignant_examples = ftr_test_selected[pred == 1][:3]

# Printing example values of benign and malignant cases
print("\nExample Values:")
print("Benign:")
for i in benign_examples:
    print([f"{feature}: {value}" for feature, value in zip(top_features, i)])
print("\nMalignant:")
for i in malignant_examples:
    print([f"{feature}: {value}" for feature, value in zip(top_features, i)])