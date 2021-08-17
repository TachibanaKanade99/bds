from sklearn.model_selection import cross_val_score, KFold
from matplotlib import pyplot as plt

from models.prepareData import getData, preprocessData, convertData, divideData, scaleData
from models.models import linearRegressionModel, PolynomialFeatures, polynomialRegression

# data = getData('Bán đất', 'Vườn Lài', 'An Phú Đông', '12')
# data = getData('Bán đất', 'Ngô Chí Quốc', 'Bình Chiểu', 'Thủ Đức')
# data = getData('Bán đất', 'Nguyễn Văn Tạo', 'Long Thới', 'Nhà Bè')
data = getData('Bán đất', 'Lê Văn Lương', 'Nhơn Đức', 'Nhà Bè')

print("Sample data")
print("--------------------------------------------------------")
print(data.head())
print("--------------------------------------------------------")
print("Data length: ", len(data))

# preprocess data using StandardScaler:
# data = preprocessData(data)
# scaler = StandardScaler()
# attribute = ['area']
# predict_value = ['price']

# data['area'] = scaler.fit_transform(data[attribute])
# data['price'] = scaler.fit_transform(data[predict_value])

# custom preporcess data:
data = preprocessData(data)
data = scaleData(data)

print("\n")
print("Data after after Preprocessing: ")
print("--------------------------------------------------------")
print(data.head())
print("--------------------------------------------------------")
print("Data Length: ", len(data))

# divide data into train and test:
train_data, test_data = divideData(data)

# Sort data by area column:
train_data = train_data.sort_values(by=['area'])
test_data = test_data.sort_values(by=['area'])

print("\nTrain data length: ", len(train_data))
print("Test data length: ", len(test_data))

# convert data into numpy
X, Y = convertData(data)
X_train, Y_train = convertData(train_data)
X_test, Y_test = convertData(test_data)

print("\nLinear Regression Model: ")

# find model by using linear regression:
model, linear_rmse = linearRegressionModel(X_train, Y_train)

# find Y by using linear model predict:
Y_train_pred = model.predict(X_train)
# Y_test_pred = model.predict(X_test)

# Plot linear model:
plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
plt.plot(X_train, Y_train_pred, color='black', label='train_model')
plt.legend()
plt.tight_layout()
plt.xlabel('area')
plt.ylabel('price')
plt.show()

# Linear Model coefficient and intercept:
print("Linear model coefficient: {}".format(model.coef_))
print("Linear model intercept: {}".format(model.intercept_))

# linear_model rmse:
print("Linear model rmse: {}".format(linear_rmse))
print("\n\n")

# find model by using polynomial regression:
poly_model, poly_rmse, degree = polynomialRegression(X_train, Y_train)

print("Polynomial Regression with degree = {}".format(degree))

# transform X and X_test:
polynomial_features = PolynomialFeatures(degree=degree)
X_poly = polynomial_features.fit_transform(X)
X_train_poly = polynomial_features.fit_transform(X_train)
X_test_poly = polynomial_features.fit_transform(X_test)

# Try predicting Y
Y_train_poly_pred = poly_model.predict(X_train_poly)
Y_test_poly_pred = poly_model.predict(X_test_poly)

# Plot model:
plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
plt.plot(X_train, Y_train_poly_pred, color='green', label='train_model')
plt.plot(X_test, Y_test_poly_pred, color='purple', label='test_model')
plt.legend()
plt.tight_layout()
plt.xlabel('area')
plt.ylabel('price')
plt.show()

# Polynomial Model coefficient and intercept:
print("Polynomial model coefficient:")
print(poly_model.coef_)
print("Polynomial model intercept: {}".format(poly_model.intercept_))

# poly_model rmse:
print("Polynomial Model RMSE: {}".format(poly_rmse))

# score the model with test data:

# Linear score:
print("\n")
print("Linear Model score on train dataset: ", model.score(X_train, Y_train))
print("Linear Model score on test dataset: ", model.score(X_test, Y_test))

# Poly score:
print("\n")
print("Poly Model score on train dataset: ", poly_model.score(X_train_poly, Y_train))
print("Poly Model score on test dataset: ", poly_model.score(X_test_poly, Y_test))

# K-fold Cross Validation Score:
kf = KFold(n_splits=5, shuffle=False, random_state=None)
linear_cross_val_score = cross_val_score(model, X_train, Y_train, cv=kf)
print("\nCross Validation Score on Linear Regression: ", linear_cross_val_score)
print("Average score on Linear Regression: ", linear_cross_val_score.mean())

poly_cross_val_score = cross_val_score(poly_model, X_train_poly, Y_train, cv=kf)
print("\nCross Validation Score on Polynomial Regression: ", poly_cross_val_score)
print("Average score on Polynomial Regression: ", poly_cross_val_score.mean())