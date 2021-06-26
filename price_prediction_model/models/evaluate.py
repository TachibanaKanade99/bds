import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import QuantileTransformer, PowerTransformer, FunctionTransformer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error

from models.prepareData import getData, convertData, divideData, preprocessData, scaleData
from models.models import linearRegressionModel, polynomialRegression, nearestNeighbors, localOutlierFactor

import unidecode
from joblib import dump

def evaluateModel(_post_type):

    # Database Connection:
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
    cur = conn.cursor()

    # Execute SQL query:

    cur.execute("SELECT post_type, street, ward, district, COUNT(id) FROM bds_realestatedata WHERE street IS NOT NULL AND ward IS NOT NULL AND district IS NOT NULL AND post_type = %s GROUP BY post_type, street, ward, district HAVING COUNT(id) > %s;", ( _post_type, 40 ) )
    item_lst = cur.fetchall()

    for item in item_lst:
        post_type = item[0]
        street = item[1]
        ward = item[2]
        district = item[3]
        
        data = getData(post_type, street, ward, district)

        data = data[~(data['area'] < 10)]
        data = data[~(data['price'] > 200)]

        # transform data into log1p
        data['area'] = (data['area']).transform(np.log1p)
        data['price'] = (data['price']).transform(np.log1p)
        
        # preprocessing data:
        data = preprocessData(data)

        if len(data) > 30:
            print("\n\n")
            print("Sample data in {street}, {ward}, {district}".format(street=street, ward=ward, district=district))
            print("--------------------------------------------------------")
            print(data.head())
            print("--------------------------------------------------------")
            print("Data Length: ", len(data))

            # data = nearestNeighbors(data, 2)
            data = localOutlierFactor(data, 10)

            # divide data into train, validate, test data:
            train_data, test_data = train_test_split(data, test_size=0.3, random_state=4)
            test_data, validate_data = train_test_split(test_data, test_size=0.5, random_state=4)
        
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
                X, Y = convertData(data)
                X_train, Y_train = convertData(train_data)
                X_test, Y_test = convertData(test_data)
                X_validate, Y_validate = convertData(validate_data)

                # transform data:

                # use Quantile Transformer:
                # X_train = QuantileTransformer(n_quantiles=len(X_train), output_distribution='uniform').fit_transform(X_train)
                # Y_train = QuantileTransformer(n_quantiles=len(Y_train), output_distribution='uniform').fit_transform(Y_train)

                # X_test = QuantileTransformer(n_quantiles=len(X_test), output_distribution='uniform').fit_transform(X_test)
                # Y_test = QuantileTransformer(n_quantiles=len(X_test), output_distribution='uniform').fit_transform(Y_test)

                # X_validate = QuantileTransformer(n_quantiles=len(X_validate), output_distribution='uniform').fit_transform(X_validate)
                # Y_validate = QuantileTransformer(n_quantiles=len(Y_validate), output_distribution='uniform').fit_transform(Y_validate)

                # use Power Transform:
                # X_train = PowerTransformer(method='yeo-johnson').fit_transform(X_train)
                # Y_train = PowerTransformer(method='yeo-johnson').fit_transform(Y_train)

                # X_test = PowerTransformer(method='yeo-johnson').fit_transform(X_test)
                # Y_test = PowerTransformer(method='yeo-johnson').fit_transform(Y_test)

                # X_validate = PowerTransformer(method='yeo-johnson').fit_transform(X_validate)
                # Y_validate = PowerTransformer(method='yeo-johnson').fit_transform(Y_validate)

                # Log Transformer:
                # X = FunctionTransformer(np.log).fit_transform(X)
                # Y = FunctionTransformer(np.log).fit_transform(Y)

                # X_train = FunctionTransformer(np.log1p).fit_transform(X_train)
                # Y_train = FunctionTransformer(np.log1p).fit_transform(Y_train)

                # X_test = FunctionTransformer(np.log1p).fit_transform(X_test)
                # Y_test = FunctionTransformer(np.log1p).fit_transform(Y_test)

                # X_validate = FunctionTransformer(np.log1p).fit_transform(X_validate)
                # Y_validate = FunctionTransformer(np.log1p).fit_transform(Y_validate)

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
                plt.figure(figsize=(7, 4))
                plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
                plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
                plt.scatter(X_validate, Y_validate, marker='o', color='green', label='validate_data')
                plt.plot(X_train, Y_train_pred, color='black', label='train_model')
                plt.legend(bbox_to_anchor=(1,1), loc="upper left")
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
                poly_model, degree, validate_rmse = polynomialRegression(X_train, Y_train, X_validate, Y_validate, X_test, Y_test)

                # transform X and X_test:
                polynomial_features = PolynomialFeatures(degree=degree)
                X_train_poly = polynomial_features.fit_transform(X_train)
                X_test_poly = polynomial_features.fit_transform(X_test)

                # Try predicting Y
                Y_train_poly_pred = poly_model.predict(X_train_poly)

                # Plot model:
                plt.figure(figsize=(7, 4))
                plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
                plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
                plt.scatter(X_validate, Y_validate, marker='o', color='green', label='validate_data')
                plt.plot(X_train, Y_train_poly_pred, color='black', label='train_model')
                plt.legend(bbox_to_anchor=(1,1), loc="upper left")
                plt.tight_layout()
                plt.xlabel('area')
                plt.ylabel('price')
                plt.show()

                print("Polynomial Regression with degree = {}\n".format(degree))
                # Polynomial Model coefficient and intercept:
                print("Polynomial model coefficient:")
                print(poly_model.coef_)
                print("Polynomial model intercept: {}\n".format(poly_model.intercept_))

                # poly_model rmse:
                # print("Polynomial Model RMSE on train data: {}".format(train_rmse))
                print("Polynomial Model RMSE on validate data: {}".format(validate_rmse))
                # print("Polynomial Model RMSE on test data: {}".format(test_rmse))

                # score the model with test data:

                # Linear score:
                print("\n")

                linear_train_r2_score = linear_model.score(X_train, Y_train)
                print("Linear Model score on train dataset: ", linear_train_r2_score)
                
                linear_test_r2_score = linear_model.score(X_test, Y_test)
                print("Linear Model score on test dataset: ", linear_test_r2_score)

                # Poly score:
                print("\n")

                poly_train_r2_score = poly_model.score(X_train_poly, Y_train)
                print("Poly Model score on train dataset: ", poly_train_r2_score)

                poly_test_r2_score = poly_model.score(X_test_poly, Y_test)
                print("Poly Model score on test dataset: ", poly_test_r2_score)


                # Save model after training:
                # calc cross validation score of linear to compare with poly for best model selection
                linear_cv = np.mean(cross_val_score(linear_model, X, Y, cv=5))
                poly_cv = np.mean(cross_val_score(poly_model, X, Y, cv=5))

                best_r2_score = linear_test_r2_score if linear_test_r2_score > poly_test_r2_score else poly_test_r2_score
                best_model = linear_model if (linear_cv > poly_cv and linear_test_r2_score > poly_test_r2_score) else poly_model
                best_degree = 1 if linear_cv > poly_cv else degree

                print(linear_cv)
                print(poly_cv)

                # remove "dấu":
                post_type = unidecode.unidecode(post_type.lower().replace(" ", ""))
                street = unidecode.unidecode(street.lower().replace(" ", ""))
                ward = unidecode.unidecode(ward.lower().replace(" ", ""))
                district = unidecode.unidecode(district.lower().replace(" ", ""))
                model_name = post_type + "_" + street + "_" + ward + "_" + district

                if best_r2_score > 0.7:
                    # Save model:
                    if model_name != 'bannharieng_3/2_14_10':
                        dump((best_model, best_degree), 'trained/' + model_name + ".joblib")

        else:
            print("Length data in {street}, {ward}, {district} is {length}".format(street=street, ward=ward, district=district, length=len(data)))

    # Close connection:
    cur.close()
    conn.close()
