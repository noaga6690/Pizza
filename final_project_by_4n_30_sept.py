# -*- coding: utf-8 -*-
"""Final_Project_by_4N_30_sept.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NN68lfHWiAtbtY8RnZG6ur3oXS-cmL3Y
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Importing dataset and libraries"""

import pandas as pd
import numpy as np

file_path = '/content/drive/MyDrive/Final_Project_DS29/Dataset/pizza_v2.csv'
pizza_data = pd.read_csv('/content/drive/MyDrive/Final_Project_DS29/Dataset/pizza_v2.csv')

pizza_data.head(15)

"""# Data Cleaning"""

# checking the null value in the dataset
pizza_data.isnull().sum()

pizza_data.rename({'price_cad':'price'}, axis=1, inplace=True)

# Convert price and diameter to numeric
pizza_data['price'] = pd.to_numeric(pizza_data['price'].str.replace('$', ''), errors='coerce')
pizza_data['diameter'] = pd.to_numeric(pizza_data['diameter'].str.replace(' inch', ''), errors='coerce')

pizza_data.head()

# converting the Canadian currency to Rupiah
# def convert(value):
    # return value*11404
# pizza_data['price'].apply(convert)
pizza_data.head()

pizza_data.info()

"""# EDA

## EDA for Numerical Data
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Set up the matplotlib figure
plt.figure(figsize=(14, 6))

# Plot the distribution of price
plt.subplot(1, 2, 1)
sns.histplot(pizza_data['price'], bins=20, kde=True)
plt.title('Distribution of Pizza Prices')
plt.xlabel('Price (CAD)')
plt.ylabel('Frequency')

# Plot the distribution of diameter
plt.subplot(1, 2, 2)
sns.histplot(pizza_data['diameter'], bins=20, kde=True)
plt.title('Distribution of Pizza Diameter')
plt.xlabel('Diameter (inches)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Scatter plot of price vs diameter
plt.figure(figsize=(8, 6))
sns.scatterplot(x=pizza_data['diameter'], y=pizza_data['price'])
plt.title('Scatter Plot of Price vs Diameter')
plt.xlabel('Diameter (inches)')
plt.ylabel('Price (CAD)')
plt.show()

"""## EDA for Categorical Data"""

# Frequency of each category
categorical_columns = ['company', 'topping', 'variant', 'size', 'extra_sauce', 'extra_cheese', 'extra_mushrooms']
categorical_freq = pizza_data[categorical_columns].apply(lambda x: x.value_counts()).T.stack()

categorical_freq

# Set up the matplotlib figure
plt.figure(figsize=(14, 6))

# Plot the distribution of topping
plt.subplot(1, 2, 1)
sns.countplot(y = pizza_data['topping'])

# Plot the distribution of variant
plt.subplot(1, 2, 2)
sns.countplot(y = pizza_data['variant'])

plt.tight_layout()
plt.show()

# Set up the matplotlib figure
plt.figure(figsize=(12, 6))

# Plot the distribution of extra sauce
plt.subplot(1, 2, 1)
sns.countplot(y = pizza_data['extra_sauce'])

# Plot the distribution of extra cheese
plt.subplot(1, 2, 2)
sns.countplot(y = pizza_data['extra_cheese'])

plt.tight_layout()
plt.show()

# Set up the matplotlib figure
plt.figure(figsize=(12, 6))

# Plot the distribution of extra mushrooms
plt.subplot(1, 2, 1)
sns.countplot(y = pizza_data['extra_mushrooms'])

# Plot the distribution of pizza diameter
plt.subplot(1, 2, 2)
sns.countplot(y = pizza_data['diameter'])

plt.tight_layout()
plt.show()

sns.boxplot(y='topping', x='price', data=pizza_data)

sns.boxplot(y='variant', x='price', data=pizza_data)

"""# Data Preprocessing

## Label Encoding
"""

from sklearn.preprocessing import LabelEncoder
cat_cols=pizza_data.select_dtypes(include=['object']).columns
cat_cols

en=LabelEncoder()
for i in cat_cols:
    pizza_data[i]=en.fit_transform(pizza_data[i])

pizza_data.head()

"""# Store Feature Matric in X and Target in Y"""

# Extract features (X) and target (y) variables
X = pizza_data.drop('price', axis=1)
y = pizza_data['price']

"""# Split the Data into Train and Test"""

from sklearn.model_selection import train_test_split

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""# Modeling

## Models and Metrics Selection
"""

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import xgboost as xgb
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor

# Defining function for each evaluation metric
# R²
def rsqr_score(test, pred):
    """Calculate R squared score

    Args:
        test -- test data
        pred -- predicted data

    Returns:
        R squared score
    """
    r2_ = r2_score(test, pred)
    return r2_


# RMSE
def rmse_score(test, pred):
    """Calculate Root Mean Square Error score

    Args:
        test -- test data
        pred -- predicted data

    Returns:
        Root Mean Square Error score
    """
    rmse_ = np.sqrt(mean_squared_error(test, pred))
    return rmse_


# Print the scores
def print_score(test, pred):
    """Print calculated score

    Args:
        test -- test data
        pred -- predicted data

    Returns:
        print the regressor name
        print the R squared score
        print Root Mean Square Error score
    """

    print(f"- Regressor: {regr.__class__.__name__}")
    print(f"R²: {rsqr_score(test, pred)}")
    print(f"RMSE: {rmse_score(test, pred)}\n")

# Define regression models
linear_model = LinearRegression()
lasso_model = Lasso()
ridge_model = Ridge()
xgb_model = xgb.XGBRegressor(objective ='reg:squarederror')
rf_model = RandomForestRegressor()


# Train models on X_train and y_train
for regr in [linear_model, lasso_model, xgb_model, rf_model]:
    # fit the corresponding model
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)

    # Print the defined metrics above for each classifier
    print_score(y_test, y_pred)

model_names = ['Linear Regression', 'Ridge Regression', 'XGBoost', 'RandomForest']

# Create a 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(9, 7))

model_counter = 0
y_pred_list = []

for row in range(2):
    for col in range(2):
        regr = [linear_model, ridge_model, xgb_model, rf_model][model_counter]

        # Fit the corresponding model
        regr.fit(X_train, y_train)
        y_pred = regr.predict(X_test)
        y_pred_list.append(y_pred)

        # Create a scatterplot for the current model in the current subplot
        sns.scatterplot(x=y_test, y=y_pred, ax=axes[row, col])
        axes[row, col].set_title(f'{model_names[model_counter]}')
        axes[row, col].set_xlabel('True Values')
        axes[row, col].set_ylabel('Predicted Values')
        axes[row, col].plot([min(y_test), max(y_test)],
                            [min(y_test), max(y_test)],
                            color='red', linestyle='--')

        # Increment the model counter
        model_counter += 1

# Adjust layout to prevent overlap of subplots
plt.tight_layout()
plt.show()

"""## Finding Important Features"""

from sklearn import metrics
xgb_model.feature_importances_

imp_fea = pd.Series(xgb_model.feature_importances_, index=X_train.columns)
imp_fea.plot(kind='bar')

"""## Model Optimization

> Hyperparameters tuning will be applied to the model which has the best R2 and RMSE metrics score. In this case the **XGBoost Regression** is the chosen one.
"""

from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

# Define the hyperparameter grid
param_grid = {
    'learning_rate': [0.01, 0.1],
    'n_estimators': [100, 200],
    'max_depth': [3, 4],
    'min_child_weight': [1, 2],
    'gamma': [0, 0.1],
    'subsample': [0.8, 0.9],
    'colsample_bytree': [0.7, 0.8],
}

xgb = XGBRegressor()

# Create a GridSearchCV instance
grid_search = GridSearchCV (estimator=xgb,
                            param_grid=param_grid,
                            scoring='neg_mean_squared_error',
                            cv=3)

# Fit the XGBoost model with GridSearchCV
grid_search.fit(X_train, y_train)

# Get the best hyperparameters for XGBoost
best_xgb = grid_search.best_estimator_
best_params = grid_search.best_params_

# Print the best hyperparameters for XGBoost
print("Best Hyperparameters for XGBoost:", best_params)

# Evaluate the best XGBoost model
y_pred_tuned = best_xgb.predict(X_test)

r2 = r2_score(y_test, y_pred_tuned)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_tuned))
print("--Tuned XGBRegression--")
print("R2 score:", r2)
print("RMSE:", rmse)

"""# Save the Model"""

X = pizza_data.drop('price', axis=1)
y = pizza_data['price']

xgb_model=XGBRegressor()

xgb.fit(X,y)

import joblib
joblib.dump(xgb,'pizza_price_predict')

model = joblib.load('pizza_price_predict')

import pandas as pd
df = pd.DataFrame({
    'company':1,
    'diameter':22,
    'topping':2,
    'variant': 1,
    'size': 3,
    'extra_sauce':1,
    'extra_cheese':1,
    'extra_mushrooms':1,
}, index=[0])

df

model.predict(df)
