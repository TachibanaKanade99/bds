import psycopg2
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

from models.prepareData import getData, convertData, divideData, preprocessData, scaleData
from models.models import linearRegressionModel, polynomialRegression

def evaluateModel(district, post_type):

    # Database Connection:
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
    cur = conn.cursor()

    # Houses:
    print("------------------------------")
    print("Model Evaluation for {} in {}".format(post_type, district))
    print("------------------------------")

    cur.execute("SELECT post_type, street, ward, district, COUNT(id) FROM bds_realestatedata WHERE street IS NOT NULL AND ward IS NOT NULL AND district = %s AND post_type = %s GROUP BY post_type, street, ward, district HAVING COUNT(id) > %s;", ( district, post_type, 25 ) )
    item_lst = cur.fetchall()

    for item in item_lst:
        street = item[1]
        ward = item[2]
        print("\n")
        data = getData(post_type, street, ward, district, conn)

        # preprocessing data:
        # train_data = preprocessData(train_data)
        # test_data = preprocessData(test_data)
        data = preprocessData(data)

        # scale data:
        # train_data = scaleData(train_data)
        # test_data = scaleData(test_data)
        data = scaleData(data)

        # divide data into train and test:
        train_data, test_data = divideData(data)
        
        # Train model with train_data:
        if train_data is not None and test_data is not None:
        # if data is not None:
             # Sort data by area column:
            train_data = train_data.sort_values(by=['area'])
            test_data = test_data.sort_values(by=['area'])
            # data = data.sort_values(by=['area'])

            # Manipulate data:
            # X, Y = convertData(data)
            X, Y = convertData(train_data)
            X_test, Y_test = convertData(test_data)

            print("Train data length: {}".format(len(train_data)))
            print("Test data length: {}".format(len(test_data)))

            print("--------------------------------------------------------")
            print(train_data.head())
            # print(data.head())
            print("--------------------------------------------------------")
            print("Data length: ", len(train_data))
            # print("Data length: ", len(data))

            print("Linear Regression Model: ")
            # find model by using linear regression:
            model, linear_rmse = linearRegressionModel(X, Y)

            # find Y by using linear model predict:
            Y_pred = model.predict(X)
            # Y_test_pred = model.predict(X_test)

            # Plot linear model:
            plt.scatter(X, Y, marker='o', color='blue', label='train_data')
            plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
            plt.plot(X, Y_pred, color='black', label='train_model')
            # plt.plot(X_test, Y_test_pred, color='purple', label='test_model')
            plt.legend()
            plt.tight_layout()
            plt.show()

            # linear_model rmse:
            print("Linear model rmse: {}".format(linear_rmse))

            print("\n\n")

            # find model by using polynomial regression:
            poly_model, poly_rmse, degree = polynomialRegression(X, Y)

            if poly_rmse < linear_rmse:
                print("Polynomial Regression with degree = {}".format(degree))

                # transform X and X_test:
                polynomial_features = PolynomialFeatures(degree=degree)
                X_poly = polynomial_features.fit_transform(X)
                X_test_poly = polynomial_features.fit_transform(X_test)

                # Try predicting Y
                Y_poly_pred = poly_model.predict(X_poly)
                # Y_test_poly_pred = poly_model.predict(X_test_poly)

                # Plot model:
                plt.scatter(X, Y, marker='o', color='blue', label='train_data')
                plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
                plt.plot(X, Y_poly_pred, color='green', label='train_model')
                # plt.plot(X_test, Y_test_poly_pred, color='purple', label='test_model')
                plt.tight_layout()
                plt.legend()
                plt.show()

                # poly_model rmse:
                print("Polynomial Model RMSE: {}".format(poly_rmse))

            # score the model with test data:

            # Linear score:
            print("Linear Model score on train dataset: ", model.score(X, Y))
            print("Linear Model score on test dataset: ", model.score(X_test, Y_test))

            # Poly score:
            print("Poly Model score on train dataset: ", poly_model.score(X_poly, Y))
            print("Poly Model score on test dataset: ", poly_model.score(X_test_poly, Y_test))

    # Close connection:
    cur.close()
    conn.close()
