import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from sklearn.feature_selection import RFECV
from sklearn.metrics import mean_squared_error

#Loading the diabetes dataset onto the data variable and setting up the feature and tareget
data = load_diabetes()
ftr = pd.DataFrame(data.data, columns = data.feature_names)
trgt = data.target

#Splitting the dataset into Training, Validation and Test
ftr_train, ftr_test, trgt_train, trgt_test = train_test_split(ftr, trgt, test_size = 0.3, random_state = 42)
ftr_train, ftr_val, trgt_train, trgt_val = train_test_split(ftr_train, trgt_train, test_size = 0.25, random_state = 42)

#Initializing and training the Decision Tree Regressor Model
model = LogisticRegression()

#Performing feature selection using Recurve feature elemination with cross validation
selector = RFECV(estimator = model)
selector.fit(ftr_train, trgt_train)

#Tranforming the training and validation sets with selected features
ftr_train_selected = selector.transform(ftr_train)
ftr_val_selected = selector.transform(ftr_val)

#Training the model with the selected features
model.fit(ftr_train_selected, trgt_train)

#Evaluating the model on the trained dataset using the validation set
ftr_val_selected = selector.transform(ftr_val)
trgt_pred_val = model.predict(ftr_val_selected)
mse_val = mean_squared_error(trgt_val, trgt_pred_val)

#trgt_pred_val = model.predict(ftr_val)
#mse_val = mean_squared_error(trgt_val, trgt_pred_val)
print("Mean Squared Error (Validation):")
print(mse_val)

#Obtianing the selected feature indices and feature names
selected_ftr_indices = selector.get_support(indices = True)
selected_ftr = ftr.columns[selected_ftr_indices]

#Selected features for predicting disease progression
print("Selected features for predicting disease progression:")
print(selected_ftr)