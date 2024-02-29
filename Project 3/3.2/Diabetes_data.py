from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.utils import shuffle
from sklearn.neural_network import MLPRegressor

#Loading the Dataset
data = load_diabetes()

#Shuffling and inilializing the sub-datasets
ftr, trgt = shuffle(data.data, data.target, random_state = 33)

# Splitting the datasets into Training/Validation and Testing
ftr_train_val, ftr_test, trgt_train_val, trgt_test = train_test_split(ftr, trgt, test_size = 0.2, random_state = 82)

# Further splitting the Training/Validation set into Training and Validation sets
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train_val, trgt_train_val, test_size = 0.1, random_state = 80)

# Printing the number of samples in the original dataset and split subsets
print("The Total number of samples in the Wisconsin Breast Cancer Dataset is: \n")
print(len(ftr))

print("The number of samples in the Training Dataset is: \n")
print(len(ftr_train))

print("The number of samples in the Validation Dataset is: \n")
print(len(ftr_val))

print("The number of samples in the Testing Dataset is: \n")
print(len(ftr_test))

# Performing Cross Validation on the training and validation dataset
cv_scores = cross_val_score(MLPRegressor(), ftr_train_val, trgt_train_val, cv = 10)

# Printing the performance of the Cross Validation
print("Cross Validation Scores: \n")
print(cv_scores)

print("Average Score of Cross Validation: \n")
print(cv_scores.mean())

#Creating a MultiLayer Perceptron Regressor 
mlp = MLPRegressor(hidden_layer_sizes =(1000, 500), max_iter = 1500, random_state = 53)

# Training the MLP Regressor on the training dataset
mlp.fit(ftr_train, trgt_train)

# Evaluating the MLP Regressor on the training dataset
training_score = mlp.score(ftr_train, trgt_train)

# Evaluating the MLP Regressor on the validation dataset
validation_score = mlp.score(ftr_val, trgt_val)

# Evaluating the MLP Regressor on the testing dataset
test_score = mlp.score(ftr_test, trgt_test)

# Printing the scores for the MLP Regressor
print("Training Score: \n")
print(training_score)

print("Validation Score: \n")
print(validation_score)

print("Test Score: \n")
print(test_score)