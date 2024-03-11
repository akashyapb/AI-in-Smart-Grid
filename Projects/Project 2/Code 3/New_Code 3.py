from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#Loading dataset, initializzing and splitting into training, validation and testing
data = load_breast_cancer()
ftr = data.data
trgt = data.target
ftr_train, ftr_test, trgt_train, trgt_test = train_test_split(ftr, trgt, test_size = 0.4, random_state = 50)
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train, trgt_train, test_size = 0.5, random_state = 25)

#Scaling the features
scaler = StandardScaler()
ftr_train_scaled = scaler.fit_transform(ftr_train)
ftr_val_scaled = scaler.transform(ftr_val)
ftr_test_scaled = scaler.transform(ftr_test)

#Creation of Lasso regression model and fitting the data
lasso = Lasso(alpha = 0.4)
lasso.fit(ftr_train_scaled, trgt_train)

#Obtaining the lasso coeffiencents of 5 best features
coef = lasso.coef_
top_indices = coef.argsort()[-5:][::-1]
top_features = data.feature_names[top_indices]
feature_score = coef[top_indices]

#Calculating model efficiency score
score = lasso.score(ftr_val_scaled, trgt_val)

# Get all feature scores
all_feature_scores = coef

print("All Features:")
for feature, scr in zip(data.feature_names, all_feature_scores):
    print(f"{feature}: {scr}")

#Printing the results
print("\nModel Efficiency score:", score)
print("\nThe best 5 features are:")
for feature, scr in zip(top_features, feature_score):
    print(f"{feature} : {scr}")
    
#Applying the test data to the model and printing the final score
final_score = lasso.score(ftr_test_scaled, trgt_test)
print("\nFinal Score:", final_score)    