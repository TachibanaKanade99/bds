# import necessary libraries:
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

from models.prepareData import convertData
from models.models import linearRegressionModel, polynomialRegression

df_data = pd.read_csv('data_thesis/data_2.csv', skipfooter=1, engine='python')

# select specific cols:
df_data = df_data[['transaction_type', 'property_type', 'area', 'price', 'addr_street', 'addr_ward', 'addr_district', 'addr_city']]

# select specific area:
df_data = df_data[
                (df_data['transaction_type'] == 'bán') &
                (df_data['property_type'] == 'nhà riêng') &
                (df_data['addr_street'] == 'đường minh khai') &
                (df_data['addr_ward'] == 'phường minh khai') &
                (df_data['addr_district'] == 'hai bà trưng') &
                (df_data['addr_city'] == 'hà nội')
                ]

# check if data is null:
df_data.isnull()

# drop null values:
df_data = df_data.dropna()

# sort values by created date
df_data = df_data.sort_values(by=['created_date'])

# Drop duplicates:    
df_data = df_data.drop_duplicates(subset='area', keep='last', inplace=False)

# scale data:
df_data['area'] = (df_data['area']+1).transform(np.log)
df_data['price'] = (df_data['price']+1).transform(np.log)

# divide train - test:
train, test = train_test_split(df_data, test_size=0.2)

# Sort data by area column:
train = train.sort_values(by=['area'])
test = test.sort_values(by=['area'])

X_train, Y_train = convertData(train)
X_test, Y_test = convertData(test)

# find model by using linear regression:
model, linear_rmse = linearRegressionModel(X_train, Y_train)

# find Y by using linear model predict:
Y_train_pred = model.predict(X_train)
# Y_test_pred = model.predict(X_test)

# Plot linear model:
plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
plt.plot(X_train, Y_train_pred, color='black', label='train_model')
# plt.plot(X_test, Y_test_pred, color='purple', label='test_model')
plt.legend()
plt.tight_layout()
plt.xlabel('area')
plt.ylabel('price (tr/m2)')
plt.show()

# Linear Model coefficient and intercept:
print("Linear model coefficient: {}".format(model.coef_))
print("Linear model intercept: {}".format(model.intercept_))

# linear_model rmse:
print("Linear model RMSE: {}".format(linear_rmse))

poly_model, poly_rmse, degree = polynomialRegression(X_train, Y_train)
print("Polynomial Regression with degree = {}".format(degree))

# transform X and X_test:
polynomial_features = PolynomialFeatures(degree=degree)
X_train_poly = polynomial_features.fit_transform(X_train)
X_test_poly = polynomial_features.fit_transform(X_test)

# Try predicting Y
Y_train_poly_pred = poly_model.predict(X_train_poly)
# Y_test_poly_pred = poly_model.predict(X_test_poly)

# Plot model:
plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
plt.plot(X_train, Y_train_poly_pred, color='green', label='train_model')
# plt.plot(X_test, Y_test_poly_pred, color='purple', label='test_model')
plt.legend()
plt.tight_layout()
plt.xlabel('area')
plt.ylabel('price (tr/m2)')
plt.show()

# Polynomial Model coefficient and intercept:
print("Polynomial model coefficient: {}".format(poly_model.coef_))
print("Polynomial model intercept: {}".format(poly_model.intercept_))

# poly_model rmse:
print("Polynomial Model RMSE: {}".format(poly_rmse))

# score the model with test data:

# Linear score:
print("\n\n")
print("Linear Model score on train dataset: ", model.score(X_train, Y_train))
print("Linear Model score on test dataset: ", model.score(X_test, Y_test))

# Poly score:
print("\n")
print("Poly Model score on train dataset: ", poly_model.score(X_train_poly, Y_train))
print("Poly Model score on test dataset: ", poly_model.score(X_test_poly, Y_test))

