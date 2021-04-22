import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt

def getData():
    # Get home data from CSV file
    dataFile = None
    if os.path.exists('home_data.csv'):
        print("-- home_data.csv found locally")
        dataFile = pd.read_csv('home_data.csv', skipfooter=1, engine='python')

    return dataFile

data = getData()
print(data.head())

askprice = np.array(data['askprice'])
plt.plot(askprice)
plt.show()

if data is not None:
    # Selection few attributes
    attributes = list(
        [
            'num_bed',
            'year_built',
            'num_room',
            'num_bath',
            'living_area',
        ]
    )
    # Vector price of house
    Y = data['askprice']
    # Vector attributes of house
    X = data[attributes]
    # Split data to training test and testing test
    X_train, X_test, Y_train, Y_test = train_test_split(np.array(X), np.array(Y), test_size=0.2)

def linearRegressionModel(X_train, Y_train, X_test, Y_test):
    linear = linear_model.LinearRegression()
    # Training process
    linear.fit(X_train, Y_train)
    # Evaluating the model
    score_trained = linear.score(X_test, Y_test)

    return score_trained

print(linearRegressionModel(X_train, Y_train, X_test, Y_test))