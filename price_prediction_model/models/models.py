import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn import neighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor

# ignore warnings: =))) 
import warnings

# local libs:
from models.prepareData import convertData

# Linear Regression Model:
def linearRegressionModel(X_train, Y_train, fit_intercept=True, normalize=False):
    model = linear_model.LinearRegression(fit_intercept=fit_intercept, normalize=normalize)

    # Training process
    model.fit(X_train, Y_train)

    return model

class PolynomialRegressionModel:
    def __init__(self, degree=3, coef_=None):
        self.degree = degree
        self.coef_ = coef_
        
    def fit(self, X, Y):
        X_poly = PolynomialFeatures(degree=self.degree).fit_transform(X)
        self.poly_model = linearRegressionModel(X_poly, Y)
        self.coef_ = self.poly_model.coef_
        self.intercept_ = self.poly_model.intercept_
        
    def get_params(self, deep=False):
        return {'coef_': self.coef_}
    
    def set_params(self, coef_=None, random_state=None):
        self.coef_ = coef_
    
    def predict(self, X):
        X_poly = PolynomialFeatures(degree=self.degree).fit_transform(X)
        return self.poly_model.predict(X_poly)
    
    def score(self, X, Y):
        return mean_squared_error(Y, self.predict(X))

# Lasso Model using L1 Regularization:
def lassoRegressionModel(X_train, Y_train, alpha, normalize=False, max_iter=2000, tol=0.001):
    model = linear_model.Lasso(alpha=alpha, fit_intercept=True, normalize=normalize, max_iter=max_iter, tol=tol)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# Ridge Regression using L2 Regularization:
def ridgeRegressionModel(X_train, Y_train, alpha, normalize=False, max_iter=2000, tol=0.001):
    model = linear_model.Ridge(alpha=alpha, fit_intercept=True, normalize=normalize, max_iter=max_iter)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# K-Nearest Neighbors:
def nearestNeighbors(data, n_neighbors):

    # convert dataframe into numpy array:
    X = data.to_numpy()

    neighbors = NearestNeighbors(n_neighbors=n_neighbors, algorithm='brute', metric='euclidean')
    neighbors.fit(X)

    # find distances of a point to its neighbors:
    distances, indexes = neighbors.kneighbors(X)

    # locate outlier by index:
    outlier_indexes = np.where(distances.mean(axis=1) > distances.mean())
    outlier_values = data.iloc[outlier_indexes]
    
    # drop outliers:
    data = data.drop(outlier_values.index)

    # print("\nOutliers detected by K-Nearest Neighbors with n_neighbors = ", n_neighbors)
    # # plot outliers removed:
    # plt.scatter(data['area'], data['price'], color='blue', label='inliers')
    # plt.scatter(outlier_values['area'], outlier_values['price'], color='red', label='outliers')
    # plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    # plt.tight_layout()
    # plt.xlabel('area')
    # plt.ylabel('price')
    # plt.show()

    return data

# Local Outlier Factor:
def localOutlierFactor(data, n_neighbors):

    # convert dataframe into numpy array:
    X = data.to_numpy()

    isNeighbors = LocalOutlierFactor(n_neighbors=n_neighbors, algorithm='brute', metric='euclidean', contamination=0.2).fit_predict(X)
    
    # locate outliers by index:
    outlier_indexes = np.where(isNeighbors == -1)
    outlier_values = data.iloc[outlier_indexes]

    # drop outliers:
    data = data.drop(outlier_values.index)

    # print("\nOutliers detected by Local Outlier Factor with n_neighbors = ", n_neighbors)
    # # plot outliers removed:
    # plt.scatter(data['area'], data['price'], color='blue', label='inliers')
    # plt.scatter(outlier_values['area'], outlier_values['price'], color='red', label='outliers')
    # plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    # plt.tight_layout()
    # plt.xlabel('area')
    # plt.ylabel('price')
    # plt.show()

    return data


# ElasticNet using both L1 and L2 Regularization:
def elasticNetRegressionModel(X_train, Y_train, alpha=0.01, max_iter=2000, l1_ratio=0.5, tol=0.001):
    model = linear_model.ElasticNet(alpha=alpha, max_iter=max_iter, l1_ratio=l1_ratio, tol=tol)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# RANSAC Regression:
def RANSACRegressionModel(data, base_estimator=linear_model.LinearRegression(), random_state=None):

    X_train, Y_train = convertData(data)
    model = linear_model.RANSACRegressor(base_estimator=base_estimator, random_state=random_state)

    # Training process:
    model.fit(X_train, Y_train)

    inlier_mask = model.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)

    outlier_indexes = np.where(outlier_mask==True)
    outlier_values = data.iloc[outlier_indexes]
    data = data.drop(outlier_values.index)

    return data

def polynomialTransform(dataset, degree):
    polynomial_features = PolynomialFeatures(degree=degree)
    dataset_poly = polynomial_features.fit_transform(dataset)
    return dataset_poly

def calcRMSE(model, X, Y):
    return np.sqrt(mean_squared_error(Y, model.predict(X)))

def calcCV(model, X, Y, scoring):
    return np.mean(cross_val_score(model, X, Y, scoring=scoring, cv=5))

def polynomialRegression(X_train, Y_train, X_validate, Y_validate):

    # degree = 2
    X_train_poly = polynomialTransform(X_train, 2)
    selected_poly_model = linearRegressionModel(X_train_poly, Y_train)
    
    # calc rmse on validate data:
    X_validate_poly = polynomialTransform(X_validate, 2)
    min_poly_rmse = calcRMSE(selected_poly_model, X_validate_poly, Y_validate)

    # Choose model with specific degree:
    selected_degree = 2
    # selected_X_train_poly = X_train_poly

    min_degree = 3
    max_degree = 100

    for i in range(min_degree, max_degree+1):
        X_train_poly = polynomialTransform(X_train, i)
        poly_model = linearRegressionModel(X_train_poly, Y_train)

        # calc rmse on validate data:
        X_validate_poly = polynomialTransform(X_validate, i)
        rmse = calcRMSE(poly_model, X_validate_poly, Y_validate)

        # Try to select the model with minimum rmse:
        if rmse < min_poly_rmse:
            min_poly_rmse = rmse
            selected_poly_model = poly_model
            # selected_X_train_poly = X_train_poly
            selected_degree = i

    print("\nSelected Polynomial Regression with degree = {} and RMSE = {}".format(selected_degree, min_poly_rmse))

    return selected_poly_model, "Polynomial Regression", selected_degree
    
def regularizedRegression(degree, X_train, Y_train, X_validate, Y_validate):

    # Apply Regularization to prevent overfitting on selected Polynomial Regression:
    
    # Alpha Hyperparameter list:
    alphas = [0.00001, 0.00003, 0.00005, 0.00008, 0.0001, 0.0003, 0.0005, 0.0008, 0.001, 0.005, 0.01, 0.02, 0.04, 0.06, 0.1, 1.0, 3.0, 5.0, 10.0, 50.0, 100.0]

    selected_ridge_alpha = alphas[0]
    selected_lasso_alpha = alphas[0]

    # Transform X_train with degree:
    X_train_poly = polynomialTransform(X_train, degree)
    
    warnings.filterwarnings('ignore')
    ridge_model = linear_model.Ridge(alpha=selected_ridge_alpha, fit_intercept=True, normalize=False, max_iter=2000, tol=0.001)
    lasso_model = linear_model.Lasso(alpha=selected_lasso_alpha, fit_intercept=True, normalize=False, max_iter=2000, tol=0.001)

    max_ridge_cv_score = calcCV(ridge_model, X_train_poly, Y_train, 'r2')
    # print("Ridge Regression with alpha = {} and cv_score = {}".format(alphas[0], max_ridge_cv_score))
    max_lasso_cv_score = calcCV(lasso_model, X_train_poly, Y_train, 'r2')

    for alpha in alphas[1:]:
        ridge_model = linear_model.Ridge(alpha=alpha, fit_intercept=True, normalize=False, max_iter=2000, tol=0.001)
        lasso_model = linear_model.Lasso(alpha=alpha, fit_intercept=True, normalize=False, max_iter=2000, tol=0.001)
        
        ridge_cv_score = calcCV(ridge_model, X_train_poly, Y_train, 'r2')
        # print("Ridge Regression with alpha = {} and cv_score = {}".format(alpha, ridge_cv_score))
        lasso_cv_score = calcCV(lasso_model, X_train_poly, Y_train, 'r2')

        if ridge_cv_score > max_ridge_cv_score:
            max_ridge_cv_score = ridge_cv_score
            selected_ridge_alpha = alpha

        if lasso_cv_score > max_lasso_cv_score:
            max_lasso_cv_score = lasso_cv_score
            selected_lasso_alpha = alpha

    # fit Ridge and Lasso model with selected alpha:
    ridge_model = ridgeRegressionModel(X_train_poly, Y_train, selected_ridge_alpha)
    lasso_model = lassoRegressionModel(X_train_poly, Y_train, selected_lasso_alpha)

    X_validate_poly = polynomialTransform(X_validate, degree)

    # Ridge and Lasso CV score:
    print("Ridge max CV score: ", max_ridge_cv_score)
    print("Lasso max CV score: ", max_lasso_cv_score)

    # Ridge RMSE on validate data:
    ridge_rmse = calcRMSE(ridge_model, X_validate_poly, Y_validate)
    print("Ridge Regression with alpha = {} and RMSE = {}".format(selected_ridge_alpha, ridge_rmse))

    # Lasso RMSE on validate data:
    lasso_rmse = calcRMSE(lasso_model, X_validate_poly, Y_validate)
    print("Lasso Model with alpha = {} and RMSE = {}".format(selected_lasso_alpha, lasso_rmse))

    # Choose regularized model by its R2 score:

    if max_lasso_cv_score > max_ridge_cv_score:
        selected_regularized_model = lasso_model
        regularized_name = "Lasso Regression"
        regularized_cv_score = max_lasso_cv_score
    else:
        selected_regularized_model = ridge_model
        regularized_name = "Ridge Regression"
        regularized_cv_score = max_ridge_cv_score

    print("Selected Regularization Model is ", regularized_name)

    return selected_regularized_model, regularized_name, regularized_cv_score


