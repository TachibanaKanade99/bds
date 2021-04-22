import psycopg2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

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
    return prepareData(data)

def prepareData(data):
    factor = 3
    area_upper_bound = data['area'].mean() + data['area'].std() * factor
    area_lower_bound = data['area'].mean() - data['area'].std() * factor
    price_upper_bound = data['price'].mean() + data['price'].std() * factor
    price_lower_bound = data['price'].mean() - data['price'].std() * factor

    data = data[
        (data['area'] < area_upper_bound) &
        (data['area'] > area_lower_bound) &
        (data['price'] < price_upper_bound) &
        (data['price'] > price_lower_bound)
    ]

    print("Data length after removing outliners: ", len(data))
    return data

def prepareData(data):

    # remove outliner:
    factor = 3
    area_upper_bound = data['area'].mean() + data['area'].std() * factor
    area_lower_bound = data['area'].mean() - data['area'].std() * factor
    price_upper_bound = data['price'].mean() + data['price'].std() * factor
    price_lower_bound = data['price'].mean() - data['price'].std() * factor

    data = data[
        (data['area'] < area_upper_bound) &
        (data['area'] > area_lower_bound) &
        (data['price'] < price_upper_bound) &
        (data['price'] > price_lower_bound)
    ]

    print("Data length after removing outliners: ", len(data))

    # log transform:
    log_transform_area = (data['area']+1).transform(np.log)
    log_transform_price = (data['price']+1).transform(np.log)
    log_transform_data = pd.DataFrame({'area': log_transform_area, 'price': log_transform_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district']})

    # new_data['log(x - min(x) + 1)'] = (data['area'] - data['area'].min() + 1).transform(np.log)

    return log_transform_data

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