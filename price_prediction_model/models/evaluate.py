import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import QuantileTransformer, PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from models.prepareData import getData, convertData, divideData, preprocessData, scaleData
from models.models import linearRegressionModel, polynomialRegression

def evaluateModel(post_type):

    # Database Connection:
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
    cur = conn.cursor()

    # Execute SQL query:

    cur.execute("SELECT post_type, street, ward, district, COUNT(id) FROM bds_realestatedata WHERE street IS NOT NULL AND ward IS NOT NULL AND district IS NOT NULL AND post_type = %s GROUP BY post_type, street, ward, district HAVING COUNT(id) > %s;", ( post_type, 170 ) )
    item_lst = cur.fetchall()

    for item in item_lst:
        street = item[1]
        ward = item[2]
        district = item[3]

        # print("----------------------------------------------------")
        # print("Model Evaluation for {} in {}".format(post_type, district))
        # print("----------------------------------------------------")
        # print("\n")
        
        data = getData(post_type, street, ward, district)

        # preprocessing data:
        data = preprocessData(data)

        print("Sample data: ")
        print("--------------------------------------------------------")
        print(data.head())
        print("--------------------------------------------------------")
        print("Data Length: ", len(data))

        # divide data into train, validate, test data:
        train_data, test_data = train_test_split(data, test_size=0.2)
        train_data, validate_data = train_test_split(train_data, test_size=0.2)
        
        # Train model with train_data:
        if train_data is not None and test_data is not None and validate_data is not None:

            # Sort data by area column:
            train_data = train_data.sort_values(by=['area'])
            test_data = test_data.sort_values(by=['area'])
            validate_data = validate_data.sort_values(by=['area'])

            print("\nTrain data length: ", len(train_data))
            print("Test data length: ", len(test_data))
            print("Validate data length: ", len(validate_data))

            # Manipulate data:
            X_train, Y_train = convertData(train_data)
            X_test, Y_test = convertData(test_data)
            X_validate, Y_validate = convertData(validate_data)

            # transform data:

            # use Quantile Transformer:
            # X_train = QuantileTransformer(n_quantiles=len(X_train)-1, output_distribution='uniform').fit_transform(X_train)
            # Y_train = QuantileTransformer(n_quantiles=len(Y_train)-1, output_distribution='uniform').fit_transform(Y_train)

            # X_test = QuantileTransformer(n_quantiles=len(X_test)-1, output_distribution='uniform').fit_transform(X_test)
            # Y_test = QuantileTransformer(n_quantiles=len(X_test)-1, output_distribution='uniform').fit_transform(Y_test)

            # X_validate = QuantileTransformer(n_quantiles=len(X_validate)-1, output_distribution='uniform').fit_transform(X_validate)
            # Y_validate = QuantileTransformer(n_quantiles=len(Y_validate)-1, output_distribution='uniform').fit_transform(Y_validate)

            # use Power Transform:
            X_train = PowerTransformer(method='yeo-johnson').fit_transform(X_train)
            Y_train = PowerTransformer(method='yeo-johnson').fit_transform(Y_train)

            X_test = PowerTransformer(method='yeo-johnson').fit_transform(X_test)
            Y_test = PowerTransformer(method='yeo-johnson').fit_transform(Y_test)

            X_validate = PowerTransformer(method='yeo-johnson').fit_transform(X_validate)
            Y_validate = PowerTransformer(method='yeo-johnson').fit_transform(Y_validate)

            # find model by using linear regression:
            linear_model = linearRegressionModel(X_train, Y_train)

            # find Y by using linear model predict:
            Y_train_pred = linear_model.predict(X_train)
            Y_test_pred = linear_model.predict(X_test)

            # Calculate RMSE on train and test data:
            train_linear_rmse = np.sqrt(mean_squared_error(Y_train, Y_train_pred))
            test_linear_rmse = np.sqrt(mean_squared_error(Y_test, Y_test_pred))

            print("\nLinear Regression Model: ")
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
            print("Linear model coefficient: {}".format(linear_model.coef_))
            print("Linear model intercept: {}".format(linear_model.intercept_))

            # linear_model rmse:
            print("Linear model rmse on train data: {}".format(train_linear_rmse))
            print("Linear model rmse on test data: {}".format(test_linear_rmse))
            print("\n\n")

            # find model by using polynomial regression:
            poly_model, degree, validate_rmse, test_rmse = polynomialRegression(X_train, Y_train, X_test, Y_test, X_validate, Y_validate)

            # transform X and X_test:
            polynomial_features = PolynomialFeatures(degree=degree)
            X_train_poly = polynomial_features.fit_transform(X_train)
            X_test_poly = polynomial_features.fit_transform(X_test)

            # Try predicting Y
            Y_train_poly_pred = poly_model.predict(X_train_poly)
            Y_test_poly_pred = poly_model.predict(X_test_poly)

            # Plot model:
            plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
            plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
            plt.plot(X_train, Y_train_poly_pred, color='green', label='train_model')
            # plt.plot(X_test, Y_test_poly_pred, color='purple', label='test_model')
            plt.legend()
            plt.tight_layout()
            plt.xlabel('area')
            plt.ylabel('price')
            plt.show()

            print("Polynomial Regression with degree = {}".format(degree))
            # Polynomial Model coefficient and intercept:
            print("Polynomial model coefficient:")
            print(poly_model.coef_)
            print("Polynomial model intercept: {}".format(poly_model.intercept_))

            # poly_model rmse:
            print("Polynomial Model RMSE on validate data: {}".format(validate_rmse))
            print("Polynomial Model RMSE on test data: {}".format(test_rmse))

            # score the model with test data:

            # Linear score:
            print("\n")
            print("Linear Model score on train dataset: ", linear_model.score(X_train, Y_train))
            print("Linear Model score on test dataset: ", linear_model.score(X_test, Y_test))

            # Poly score:
            print("\n")
            print("Poly Model score on train dataset: ", poly_model.score(X_train_poly, Y_train))
            print("Poly Model score on test dataset: ", poly_model.score(X_test_poly, Y_test))

    # Close connection:
    cur.close()
    conn.close()
