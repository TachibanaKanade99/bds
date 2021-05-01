from numpy.lib import polynomial
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures

def getData(post_type, street, ward, district):
    
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
    # cur = conn.cursor()
    query = """
        SELECT area, price, street, ward, district
        FROM bds_realestatedata 
        WHERE
            post_type = '{}' AND
            area IS NOT NULL AND
            price IS NOT NULL AND
            street = '{}' AND
            ward = '{}' AND
            district = '{}';
    """.format(post_type, street, ward, district)
    
    # cur.execute(query)
    # data = cur.fetchall()
    data = pd.read_sql_query(query, con=conn)

    return prepareData(data)
    # return data

def prepareData(data):
    
    # Drop duplicates:    
    data.drop_duplicates(subset='area', keep='first', inplace=True)
    
    # Sort data by area column:
    data = data.sort_values(by=['area'])

    # use percentiles to remove outliers:
    area_upper_bound = data['area'].quantile(0.95)
    area_lower_bound = data['area'].quantile(0.05)
    price_upper_bound = data['price'].quantile(0.95)
    price_lower_bound = data['price'].quantile(0.05)

    data = data[
        (data['area'] < area_upper_bound) &
        (data['area'] > area_lower_bound) &
        (data['price'] < price_upper_bound) &
        (data['price'] > price_lower_bound)
    ]

#     Use log transformation to scale data:

    log_transform_area = (data['area']+1).transform(np.log)
    log_transform_price = (data['price']+1).transform(np.log)
    log_transform_data = pd.DataFrame({'area': log_transform_area, 'price': log_transform_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district']})

    print("--------------------------------------------------------")
    print(log_transform_data.head())
    print("--------------------------------------------------------")
    print("Log Transformation Data length: ", len(log_transform_data))

    return log_transform_data

def splitData(data):
    # Selection few attributes
    attributes = ['area',]
    predict_val = ['price']
    
    # Vector attributes of lands
    X = data[attributes]
    # Vector price of land
    Y = data[predict_val]
    
    # Convert into arr:
    X = np.array(X)
    Y = np.array(Y)
    
    # Split data to training test and testing test
    # training data : testing data = 80 : 20
    # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
    # return X_train, X_test, Y_train, Y_test
    
    return X, Y

# Linear Regression Model:
def linearRegressionModel(X, Y):
    model = linear_model.LinearRegression()

    # Training process
    model.fit(X, Y)
    
    # return model coefficient, intercept:
    return model

# Polynomial Regression:
def polynomialRegression(degree):
    polynomial_features = PolynomialFeatures(degree=degree)
    X_poly = polynomial_features.fit_transform(X)

    # calc linear regression again:
    poly_model = linearRegressionModel(X_poly, Y)
    return poly_model, X_poly

def degree_test(degree):
    print("\n\nUse polynomial regression with degree = {}: \n\n".format(degree))
    
    # Call polynomial regression
    poly_model, X_poly = polynomialRegression(degree)
    
    poly_model_coef = poly_model.coef_
    poly_model_intercept = poly_model.intercept_
    Y_poly_pred = poly_model.predict(X_poly)
    
    print("Model coefficient: ", poly_model_coef)
    print("Model intercept: ", poly_model_intercept)
    
    # print("Model: y = {} + {}x + {}x^2 + {}".format(model_coef[0], model_coef[1], model_coef[2], model_intercept))

    # Plot model:
    plt.scatter(X, Y)
    # plt.plot(X, poly_model_coef[0] + poly_model_coef[1]*X + poly_model_coef[2]*pow(X, 2) + poly_model_intercept, color='red')
    plt.plot(X, Y_poly_pred, color='green')
    plt.show()

    # Find root mean square error of model between Y_predict and Y
    rmse = np.sqrt(mean_squared_error(Y, Y_poly_pred))
    print("Root Mean Square Error: ", rmse)

    return poly_model, rmse

# Data:
post_type = 'Bán đất'
street = 'Đoàn Nguyễn Tuấn'
ward = 'Quy Đức'
district = 'Bình Chánh'

data = getData(post_type, street, ward, district)
X, Y = splitData(data)

model = linearRegressionModel(X, Y)
model_coef = model.coef_
model_intercept = model.intercept_
Y_pred = model.predict(X)

""" 
y = ax1 + b
[a] is coefficient
b is intercept
"""

print("Model coefficient: ", model_coef)
print("Model intercept ", model_intercept)

# Plot model:
plt.scatter(X, Y)
# plt.plot(X, model_coef*X + model_intercept, color='y')
plt.plot(X, Y_pred, color='yellow')
plt.show()

# Find root mean square error of model between Y_predict and Y
linear_rmse = np.sqrt(mean_squared_error(Y, Y_pred))
print("Root Mean Square Error: ", linear_rmse)

min_rmse = linear_rmse
selected_model = linear_model
degree = 1
for i in range(2, 11):
    poly_model, rmse = degree_test(i)
    if rmse < min_rmse:
        min_rmse = rmse
        selected_model = poly_model
        degree = i
print("\n\nMin rmse: {} with model with degree: {}".format(min_rmse, degree))