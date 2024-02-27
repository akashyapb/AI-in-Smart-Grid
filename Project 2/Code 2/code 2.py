from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer

#Initialzing the dataset
data = load_breast_cancer()

#Assigning features and target to the dataset
x = data.data
y = data.target

#Splitting ratios
train = 0.7
val = 0.15
test = 0.15

#Splitting the dataset for training and temporary set
x_train, x_temp, y_train, y_temp = train_test_split(x, y, train_size = train, random_state = 40)

#Splitting the remaining dataset into validation and testing set
x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size = 0.5, random_state = 40)

#Printing the shapes of the resulting datasets to confirm the split
print("Training set shape:", x_train.shape, y_train.shape)
print("Validation set shape:", x_val.shape, y_val.shape)
print("Testing set shape:", x_test.shape, y_test.shape)