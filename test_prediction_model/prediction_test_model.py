import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model


# convert to array:
# area = np.array(data['area'])
# price = np.array(data['price'])
# plt.scatter(area, price, marker='o')
# plt.show()

def getData():
    street = 'Trần Văn Giàu'
    ward = 'Phạm Văn Hai'
    district = 'Bình Chánh'
    
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
    # cur = conn.cursor()
    query = """
        SELECT area, price, street, ward, district
        FROM bds_realestatedata 
        WHERE
            post_type = 'Bán đất' AND
            area IS NOT NULL AND
            price IS NOT NULL AND
            street = '{street}' AND
            ward = '{ward}' AND
            district = '{district}';
    """.format(street=street, ward=ward, district=district)
    # cur.execute(query)
    # data = cur.fetchall()
    data = pd.read_sql_query(query, con=conn)

    # data info
    print(data.head())
    print("Data length: ", len(data))
    return data

def test_split(data):
    # Selection few attributes
    attributes = list(
        [
            'area',
        ]
    )
    
    # Vector attributes of lands
    X = data[attributes]
    # Vector price of land
    Y = data['price']
    
    # Convert into arr:
    X = np.array(X)
    Y = np.array(Y)
    
    # plt.plot(Y)
    # plt.show()
    
    # Split data to training test and testing test
    # training data : testing data = 80 : 20
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    
    return X_train, X_test, Y_train, Y_test

# Linear Regression Model:
def linearRegressionModel(X_train, Y_train, X_test, Y_test):
    model = linear_model.LinearRegression()

    # Training process
    model.fit(X_train, Y_train)
    
    print("\nLinear Regression Model:")
    # Evaluating the model
    yfit = model.predict(X_test)
    plt.scatter(X_train, Y_train, marker='o')
    plt.plot(X_test, yfit)
    plt.show()
    
    score_trained = model.score(X_test, Y_test)

    return score_trained

# Lasso Model:
def lassoRegressionModel(X_train, Y_train, X_test, Y_test):
    model = linear_model.Lasso(alpha=1.0)

    # Training process:
    model.fit(X_train, Y_train)
    
    print("\nLasso Model:")
    # Evaluating the model
    yfit = model.predict(X_test)
    plt.scatter(X_train, Y_train, marker='o')
    plt.plot(X_test, yfit)
    plt.show()

    # Evaluation the model:
    score_trained = model.score(X_test, Y_test)
    
    return score_trained

data = getData()
X_train, X_test, Y_train, Y_test = test_split(data)

print("Linear Regression training model score: ", linearRegressionModel(X_train, Y_train, X_test, Y_test))
# print("Lasso Regression training model score: ", lassoRegressionModel(X_train, Y_train, X_test, Y_test))