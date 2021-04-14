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

# Database Connection:
conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
cur = conn.cursor()

def getData(post_type, street, ward, district, conn):
    # cur = conn.cursor()
    query = """
        SELECT post_type, area, price, street, ward, district
        FROM bds_realestatedata 
        WHERE
            post_type = '{post_type}' AND
            area IS NOT NULL AND
            price IS NOT NULL AND
            street = '{street}' AND
            ward = '{ward}' AND
            district = '{district}';
    """.format(post_type=post_type, street=street, ward=ward, district=district)
    # cur.execute(query)
    # data = cur.fetchall()
    data = pd.read_sql_query(query, con=conn)

    # data info
    print(data.head())
    print("Data length: ", len(data))
    return data

def splitData(data):
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
    
    # Evaluating the model
    print("\nLinear Regression Model:")
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
    
    # Evaluating the model
    print("\nLasso Model:")
    yfit = model.predict(X_test)
    plt.scatter(X_train, Y_train, marker='o')
    plt.plot(X_test, yfit)
    plt.show()

    # Evaluation the model:
    score_trained = model.score(X_test, Y_test)
    
    return score_trained


# Houses:
print("------------------------------")
print("Model Evaluation for Houses")
print("------------------------------")

cur.execute("SELECT post_type, street, ward, district, COUNT(id) FROM bds_realestatedata WHERE street IS NOT NULL AND ward IS NOT NULL AND district = %s AND post_type = %s GROUP BY post_type, street, ward, district HAVING COUNT(id) > %s;", ( 'Tân Phú', 'Bán nhà riêng', 10 ) )
item_lst = cur.fetchall()

for item in item_lst:
    post_type = item[0]
    street = item[1]
    ward = item[2]
    district = item[3]
    print("\n")
    data = getData(post_type, street, ward, district, conn)
    X_train, X_test, Y_train, Y_test = splitData(data)

    score = linearRegressionModel(X_train, Y_train, X_test, Y_test)
    print("Linear Regression training model score: ", score, "\n")

# Lands:
print("------------------------------")
print("Model Evaluation for Lands")
print("------------------------------")

cur.execute("SELECT post_type, street, ward, district, COUNT(id) FROM bds_realestatedata WHERE street IS NOT NULL AND ward IS NOT NULL AND district = %s AND post_type = %s GROUP BY post_type, street, ward, district HAVING COUNT(id) > %s;", ( 'Tân Phú', 'Bán đất', 10 ) )
item_lst = cur.fetchall()

for item in item_lst:
    post_type = item[0]
    street = item[1]
    ward = item[2]
    district = item[3]
    print("\n")
    data = getData(post_type, street, ward, district, conn)
    X_train, X_test, Y_train, Y_test = splitData(data)

    score = linearRegressionModel(X_train, Y_train, X_test, Y_test)
    print("Linear Regression training model score: ", score, "\n")

# Close connection:
cur.close()
conn.close()