import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import PolynomialFeatures

# Linear Regression Model:
def linearRegressionModel(X_train, Y_train):
    model = linear_model.LinearRegression()

    # Training process
    model.fit(X_train, Y_train)

    # find Y_pred by model prediction:
    Y_train_pred = model.predict(X_train)

    # Find RMSE of the linear model:
    linear_rmse = np.sqrt(mean_squared_error(Y_train, Y_train_pred))

    return model, linear_rmse

def polynomialTransform(dataset, degree):
    polynomial_features = PolynomialFeatures(degree=degree)
    dataset_poly = polynomial_features.fit_transform(dataset)
    return dataset_poly

def polynomialRegression(X_train, Y_train):

    # degree = 2
    X_train_poly = polynomialTransform(X_train, 2)
    # selected_model, min_rmse = linearRegressionModel(X_train_poly, Y_train)
    selected_model, min_rmse = lassoRegressionModel(X_train_poly, Y_train)
    # selected_model, min_rmse = ridgeRegressionModel(X_train_poly, Y_train)
    selected_degree = 2

    min_degree = 3
    max_degree = 50

    for i in range(min_degree, max_degree+1):
        X_train_poly = polynomialTransform(X_train, i)

        poly_model, rmse = linearRegressionModel(X_train_poly, Y_train)
        poly_model, rmse = lassoRegressionModel(X_train_poly, Y_train)
        # poly_model, rmse = ridgeRegressionModel(X_train_poly, Y_train)

        # Try to select the model with minimum rmse:
        if rmse < min_rmse:
            min_rmse = rmse
            selected_model = poly_model
            selected_degree = i

    return selected_model, min_rmse, selected_degree

# Lasso Model:
def lassoRegressionModel(X_train, Y_train, alpha=1):
    model = linear_model.Lasso(alpha=alpha, max_iter=5000, tol=0.002)

    # Training process:
    model.fit(X_train, Y_train)

    # find Y_pred by model prediction:
    Y_train_pred = model.predict(X_train)

    # Find RMSE of the linear model:
    rmse = np.sqrt(mean_squared_error(Y_train, Y_train_pred))

    return model, rmse

# Ridge Regression:
def ridgeRegressionModel(X_train, Y_train, alpha=1):
    model = linear_model.Ridge(alpha=alpha, normalize=True)

    # Training process:
    model.fit(X_train, Y_train)

    # find Y_pred by model prediction:
    Y_train_pred = model.predict(X_train)

    # Find RMSE of the linear model:
    rmse = np.sqrt(mean_squared_error(Y_train, Y_train_pred))

    return model, rmse

