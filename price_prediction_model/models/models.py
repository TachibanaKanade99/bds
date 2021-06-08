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

# Linear Regression Model:
def linearRegressionModel(X_train, Y_train):
    model = linear_model.LinearRegression()

    # Training process
    model.fit(X_train, Y_train)

    return model

# Lasso Model using L1 Regularization:
def lassoRegressionModel(X_train, Y_train, alpha, normalize=True, max_iter=2000, tol=0.001):
    model = linear_model.Lasso(alpha=alpha, normalize=normalize, max_iter=max_iter, tol=tol)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# Ridge Regression using L2 Regularization:
def ridgeRegressionModel(X_train, Y_train, alpha, normalize=True, max_iter=2000):
    model = linear_model.Ridge(alpha=alpha, normalize=normalize, max_iter=max_iter)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# K-Nearest Neighbors:
def nearestNeighbors(data):

    # convert dataframe into numpy array:
    X = data.to_numpy()
    n_neighbors = 3

    # Apply NN:

    # if len(data) in range(30, 50):
    #     n_neighbors = 10
    # elif len(data) in range(50, 80):
    #     n_neighbors = 15
    # elif len(data) in range(80, 100):
    #     n_neighbors = 20
    # elif len(data) in range(100, 150):
    #     n_neighbors = 25
    # elif len(data) in range(150, 175):
    #     n_neighbors = 30
    # else:
    #     n_neighbors = 35

    # print("Number of neighbors: {}".format(n_neighbors))

    neighbors = NearestNeighbors(n_neighbors=n_neighbors, algorithm='brute', metric='euclidean')
    neighbors.fit(X)

    # find distances of a point to its neighbors:
    distances, indexes = neighbors.kneighbors(X)

    # locate outlier by index:
    outlier_indexes = np.where(distances.mean(axis=1) > distances.mean())
    outlier_values = data.iloc[outlier_indexes]
    
    # drop outliers:
    data = data.drop(outlier_values.index)

    print("\nOutliers detected by K-Nearest Neighbors")
    # plot outliers removed:
    plt.scatter(data['area'], data['price'], color='blue', label='inliers')
    plt.scatter(outlier_values['area'], outlier_values['price'], color='red', label='outliers')
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.xlabel('area')
    plt.ylabel('price')
    plt.show()

    return data

# Local Outlier Factor:
def localOutlierFactor(data):

    # convert dataframe into numpy array:
    X = data.to_numpy()
    n_neighbors = 18

    isNeighbors = LocalOutlierFactor(n_neighbors=n_neighbors, algorithm='brute', metric='euclidean').fit_predict(X)
    
    # locate outliers by index:
    outlier_indexes = np.where(isNeighbors == -1)
    outlier_values = data.iloc[outlier_indexes]

    # drop outliers:
    data = data.drop(outlier_values.index)

    print("\nOutliers detected by Local Outlier Factor")
    # plot outliers removed:
    plt.scatter(data['area'], data['price'], color='blue', label='inliers')
    plt.scatter(outlier_values['area'], outlier_values['price'], color='red', label='outliers')
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.xlabel('area')
    plt.ylabel('price')
    plt.show()

    return data


# ElasticNet using both L1 and L2 Regularization:
def elasticNetRegressionModel(X_train, Y_train, alpha=0.01, max_iter=2000, l1_ratio=0.5, tol=0.001):
    model = linear_model.ElasticNet(alpha=alpha, max_iter=max_iter, l1_ratio=l1_ratio, tol=tol)

    # Training process:
    model.fit(X_train, Y_train)

    return model

# RANSAC Regression:
def RANSACRegressionModel(X_train, Y_train, random_state=0):
    model = linear_model.RANSACRegressor(random_state=random_state)

    # Training process:
    model.fit(X_train, Y_train)

    return model

def polynomialTransform(dataset, degree):
    polynomial_features = PolynomialFeatures(degree=degree)
    dataset_poly = polynomial_features.fit_transform(dataset)
    return dataset_poly

def calcRMSE(model, X, Y):
    return np.sqrt(mean_squared_error(Y, model.predict(X)))

def calcCV(model, X, Y):
    return np.mean(cross_val_score(model, X, Y, cv=5))

def polynomialRegression(X, Y, X_train, Y_train, X_test, Y_test, X_validate, Y_validate):

    # degree = 2
    X_train_poly = polynomialTransform(X_train, 2)
    selected_poly_model = linearRegressionModel(X_train_poly, Y_train)
    
    # calc rmse on validated data:
    X_validate_poly = polynomialTransform(X_validate, 2)
    min_poly_validate_rmse = calcRMSE(selected_poly_model, X_validate_poly, Y_validate)

    # Choose model with specific degree:
    selected_degree = 2
    selected_X_train_poly = X_train_poly

    min_degree = 3
    max_degree = 100

    for i in range(min_degree, max_degree+1):
        X_train_poly = polynomialTransform(X_train, i)

        poly_model = linearRegressionModel(X_train_poly, Y_train)

        # calc rmse on validated data:
        X_validate_poly = polynomialTransform(X_validate, i)
        validate_rmse = calcRMSE(poly_model, X_validate_poly, Y_validate)

        # Try to select the model with minimum rmse:
        if validate_rmse < min_poly_validate_rmse:
            min_poly_validate_rmse = validate_rmse
            selected_poly_model = poly_model
            selected_X_train_poly = X_train_poly
            selected_degree = i

    print("\nSelected Polynomial Regression with degree = {} and validate RMSE = {}".format(selected_degree, min_poly_validate_rmse))
    
    # Apply Regularization to prevent overfitting on selected Polynomial Regression:
    alphas = [0.00001, 0.00003, 0.00005, 0.00008, 0.0001, 0.0003, 0.0005, 0.0008, 0.001, 0.005, 0.01, 0.02, 0.04, 0.06, 0.1, 1.0, 3.0, 5.0, 10.0, 50.0, 100.0]

    selected_alpha = alphas[0]
    
    warnings.filterwarnings('ignore')
    # selected_regularized_model = ridgeRegressionModel(selected_X_train_poly, Y_train, selected_alpha)
    selected_regularized_model = lassoRegressionModel(selected_X_train_poly, Y_train, selected_alpha)

    X_validate_poly = polynomialTransform(X_validate, selected_degree)
    max_regularized_cv_score = calcCV(selected_regularized_model, X, Y)

    for alpha in alphas[1:]:
        # model = ridgeRegressionModel(selected_X_train_poly, Y_train, alpha)
        model = lassoRegressionModel(selected_X_train_poly, Y_train, alpha)
        cv_score = calcCV(model, X, Y)

        if cv_score > max_regularized_cv_score:
            max_regularized_cv_score = cv_score
            selected_alpha = alpha
            selected_regularized_model = model

    X_validate_poly = polynomialTransform(X_validate, selected_degree)
    regularized_validate_rmse = calcRMSE(selected_regularized_model, X_validate_poly, Y_validate)

    print("Selected Regularized Regression with alpha = {} and validate RMSE = {}".format(selected_alpha, regularized_validate_rmse))

    # Choose between Ridge Regression and Polynomial Regression using cross validation score:
    poly_cv_score = calcCV(selected_poly_model, X, Y)

    print("Polynomial Regression cross validation score: ", poly_cv_score)
    print("Selected Regularized Regression cross validation score: ", max_regularized_cv_score)

    # selected_model = selected_poly_model if poly_cv_score > max_regularized_cv_score else selected_regularized_model
    # selected_validate_rmse = min_poly_validate_rmse if selected_model == selected_poly_model else regularized_validate_rmse
    selected_model = selected_regularized_model
    selected_validate_rmse = regularized_validate_rmse

    # calc rmse on train data:
    train_rmse = calcRMSE(selected_model, selected_X_train_poly, Y_train)

    # calc rmse on test data:
    X_test_poly = polynomialTransform(X_test, selected_degree)
    test_rmse = calcRMSE(selected_model, X_test_poly, Y_test)

    return selected_model, selected_degree, train_rmse, selected_validate_rmse, test_rmse



