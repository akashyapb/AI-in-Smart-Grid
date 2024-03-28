from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.utils import shuffle
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data = load_breast_cancer()

#Selecting the no. of hyperparameters 
ftr = data.data[: , :30]
trgt = data.target

#Shuffle the dataset before the split
ftr, trgt = shuffle(ftr, trgt, random_state = 48)

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
gbc = GradientBoostingClassifier(random_state = 29)
gbc.fit(ftr_train, trgt_train)

#Validating and printing the model on the validation dataset
val_predictions = gbc.predict(ftr_val)
print("Accuracy on the Validation set:", accuracy_score(trgt_val, val_predictions))
print("Precision on the Validation set:", precision_score(trgt_val, val_predictions))
print("Recall on the Validation set:", recall_score(trgt_val, val_predictions))
print("F1 Score on the Validation set:", f1_score(trgt_val, val_predictions),"\n")

#Testing the Model on the test set
test_predictions = gbc.predict(ftr_test)
print("Accuracy on the Test Set:", accuracy_score(trgt_test, test_predictions))

#Listing the incorrect predications from the test set
incorrect = [i for i in range(len(ftr_test)) if test_predictions[i] != trgt_test[i]]
print("Examples from the test set where the predictions have been incorrect:\n")
for i in incorrect:
    print("Example:", i+1)
    print("Features:", ftr_test[i])
    print("True Label:", trgt_test[i])
    print("Predicted Label:", test_predictions[i])
    print()