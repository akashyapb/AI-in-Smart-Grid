from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier

#Loading and initializing the dataset
data = load_breast_cancer()
ftr = data.data
trgt = data.target

#Splitting the datasets into Training, Validation and Testing
ftr_train_val, ftr_test, trgt_train_val, trgt_test = train_test_split(ftr, trgt, test_size = 0.2, random_state = 19)

#Printing the number of samples in original dataset and split subsets
print("The Total number of samples in the Wisconsin Breast Cancer Dataset is: \n")
print(len(ftr))

print("The number of samples in the Training and Validation Dataset is: \n")
print(len(ftr_train_val))

print("The number of samples in the Testing Dataset is: \n")
print(len(ftr_test))

#Creating a MultiLayer Perceptron Classifier 
mlp = MLPClassifier(hidden_layer_sizes =(100, 100), max_iter = 1000, random_state = 53)

#Performing Cross Validation
cv_scores = cross_val_score(mlp, ftr_train_val, trgt_train_val, cv = 10)

#Printing the performance of the MLP
print("Cross Validation Scores: \n")
print(cv_scores)

print("Average Score of Cross Validation: \n")
print(cv_scores.mean())