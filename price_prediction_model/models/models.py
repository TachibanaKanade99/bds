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

    return model

def polynomialTransform(dataset, degree):
    polynomial_features = PolynomialFeatures(degree=degree)
    dataset_poly = polynomial_features.fit_transform(dataset)
    return dataset_poly

def calcRMSE(model, X, Y):
    return np.sqrt(mean_squared_error(Y, model.predict(X)))

def polynomialRegression(X_train, Y_train, X_test, Y_test, X_validate, Y_validate):

    # degree = 2
    X_train_poly = polynomialTransform(X_train, 2)
    # selected_model = linearRegressionModel(X_train_poly, Y_train)
    selected_model = lassoRegressionModel(X_train_poly, Y_train)
    # selected_model = ridgeRegressionModel(X_train_poly, Y_train)
    # selected_model = elasticNetRegressionModel(X_train_poly, Y_train)
    
    # calc rmse on validated data:
    X_validate_poly = polynomialTransform(X_validate, 2)
    min_rmse = calcRMSE(selected_model, X_validate_poly, Y_validate)

    # Choose model with specific degree:
    selected_degree = 2
    # selected_X_train_poly = X_train_poly

    min_degree = 3
    max_degree = 100

    for i in range(min_degree, max_degree+1):
        X_train_poly = polynomialTransform(X_train, i)

        # poly_model = linearRegressionModel(X_train_poly, Y_train)
        poly_model = lassoRegressionModel(X_train_poly, Y_train)
        # poly_model = ridgeRegressionModel(X_train_poly, Y_train)
        # poly_model = elasticNetRegressionModel(X_train_poly, Y_train)

        # calc rmse on validated data:
        X_validate_poly = polynomialTransform(X_validate, i)
        rmse = calcRMSE(poly_model, X_validate_poly, Y_validate)

        # Try to select the model with minimum rmse:
        if rmse < min_rmse:
            min_rmse = rmse
            selected_model = poly_model
            selected_X_train_poly = X_train_poly
            selected_degree = i

    # calc rmse on test data:
    X_test_poly = polynomialTransform(X_test, selected_degree)
    test_rmse = calcRMSE(selected_model, X_test_poly, Y_test)

    # using model with regularization for selected X_degree
    # selected_model, min_rmse = ridgeRegressionModel(selected_X_train_poly, Y_train)

    return selected_model, selected_degree, min_rmse, test_rmse

# Lasso Model using L1 Regularization:
def lassoRegressionModel(X_train, Y_train, alpha=0.005, normalize=True, max_iter=2000, tol=0.001):
    model = linear_model.Lasso(alpha=alpha, normalize=normalize, max_iter=max_iter, tol=tol)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# Ridge Regression using L2 Regularization:
def ridgeRegressionModel(X_train, Y_train, alpha=0.005, normalize=True, max_iter=2000):
    model = linear_model.Ridge(alpha=alpha, normalize=normalize, max_iter=max_iter)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# ElasticNet using both L1 and L2 Regularization:
def elasticNetRegressionModel(X_train, Y_train, alpha=0.01, max_iter=2000, l1_ratio=0.5, tol=0.001):
    model = linear_model.ElasticNet(alpha=alpha, max_iter=max_iter, l1_ratio=l1_ratio, tol=tol)

    # Training process:
    model.fit(X_train, Y_train)

    return model


