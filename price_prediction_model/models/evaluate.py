import psycopg2

from models.prepareData import getData, splitData
from models.models import linearRegressionModel

def evaluateModel(district, post_type):

    # Database Connection:
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
    cur = conn.cursor()

    # Houses:
    print("------------------------------")
    print("Model Evaluation for {} in {}".format(post_type, district))
    print("------------------------------")

    cur.execute("SELECT post_type, street, ward, district, COUNT(id) FROM bds_realestatedata WHERE street IS NOT NULL AND ward IS NOT NULL AND district = %s AND post_type = %s GROUP BY post_type, street, ward, district HAVING COUNT(id) > %s;", ( district, post_type, 10 ) )
    item_lst = cur.fetchall()

    for item in item_lst:
        street = item[1]
        ward = item[2]
        print("\n")
        data = getData(post_type, street, ward, district, conn)
        X_train, X_test, Y_train, Y_test = splitData(data)

        score = linearRegressionModel(X_train, Y_train, X_test, Y_test)
        print("Linear Regression training model score: ", score, "\n")

    # Close connection:
    cur.close()
    conn.close()
