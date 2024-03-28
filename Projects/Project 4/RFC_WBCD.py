from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.utils import shuffle
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data = load_breast_cancer()

#Shuffle the dataset before the split
ftr, trgt = shuffle(data.data, data.target, random_state = 48)

# Split data into training/validation (80%) and test (20%) sets
ftr_train_val, ftr_test, trgt_train_val, trgt_test = train_test_split(ftr, trgt, test_size = 0.2, random_state = 50)

# Further split training/validation set into training and validation sets
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train_val, trgt_train_val, test_size = 0.5, random_state = 64)

# Printing the number of samples in the original dataset and split subsets
print("The Total number of samples in the Wisconsin Breast Cancer Dataset is: \n")
print(len(ftr))

print("The number of samples in the Training Dataset is: \n")
print(len(ftr_train))

print("The number of samples in the Validation Dataset is: \n")
print(len(ftr_val))

print("The number of samples in the Testing Dataset is: \n")
print(len(ftr_test))

#Creating the Random Forest Classifier Instance and training the model on the Training Data
rfc = RandomForestClassifier(random_state = 39)
rfc.fit(ftr_train, trgt_train)

#Validating and printing the model on the validation dataset
val_predictions = rfc.predict(ftr_val)
print("Accuracy on the Validation set:", accuracy_score(trgt_val, val_predictions))
print("Precision on the Validation set:", precision_score(trgt_val, val_predictions))
print("Recall on the Validation set:", recall_score(trgt_val, val_predictions))
print("F1 Score on the Validation set:", f1_score(trgt_val, val_predictions),"\n")

#Testing the Model on the test set
test_predictions = rfc.predict(ftr_test)
print("Accuracy on the Test Set:", accuracy_score(trgt_test, test_predictions))