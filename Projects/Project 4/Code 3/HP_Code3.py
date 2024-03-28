from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

data = load_diabetes()

#Selecting the no. of hyperparameters 
ftr = data.data[: , :9]
trgt = data.target

#Shuffle the dataset before the split
ftr, trgt = shuffle(ftr, trgt, random_state = 42)

# Split data into training/validation (80%) and test (20%) sets
ftr_train_val, ftr_test, trgt_train_val, trgt_test = train_test_split(ftr, trgt, test_size = 0.2, random_state = 79)

# Further split training/validation set into training and validation sets
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train_val, trgt_train_val, test_size = 0.2, random_state = 13)

# Printing the number of samples in the original dataset and split subsets
print("The Total number of samples in the Diabetes Dataset is: \n")
print(len(ftr))

print("The number of samples in the Training Dataset is: \n")
print(len(ftr_train))

print("The number of samples in the Validation Dataset is: \n")
print(len(ftr_val))

print("The number of samples in the Testing Dataset is: \n")
print(len(ftr_test))

#Creating the Random Forest Classifier Instance and training the model on the Training Data
rfr = RandomForestRegressor(random_state = 25)
rfr.fit(ftr_train, trgt_train)

#Validating and printing the model on the validation dataset
val_predictions = rfr.predict(ftr_val)
mse = mean_squared_error(trgt_val, val_predictions)
print("Mean Squared Error on the Validation dataset:", mse)

#Testing the Model on the test set
test_predictions = rfr.predict(ftr_test)
mse_test = mean_squared_error(trgt_test, test_predictions)
print("Mean Squared Error on the Test Set:", mse_test)

#Listing the top 10 incorrect predications from the test set
incorrect = abs(test_predictions - trgt_test)
incorrect_idx = incorrect.argsort()[::-1][:10]
print("Top 10 Examples from the test set where the predictions have been incorrect:\n")
for i in incorrect_idx:
    print("Example:", i+1)
    print("Features:", ftr_test[i])
    print("True Label:", trgt_test[i])
    print("Predicted Label:", test_predictions[i])
    print("Prediction Error:", incorrect[i])
    print()