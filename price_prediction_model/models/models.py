import matplotlib.pyplot as plt
from sklearn import linear_model

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