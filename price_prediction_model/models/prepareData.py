import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

    return prepareData(data)

def prepareData(data):

    # find duplicates:
    # print(data)
    # print(data.duplicated(subset='area'))
    data.drop_duplicates(subset='area', keep='first', inplace=True)

    # remove outliner:

    # use standard deviation:
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
    
    # use percentiles:
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

    if len(data) > 10:
        # log transform:
        log_transform_area = (data['area']+1).transform(np.log)
        log_transform_price = (data['price']+1).transform(np.log)
        log_transform_data = pd.DataFrame({'post_type': data['post_type'], 'area': log_transform_area, 'price': log_transform_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district']})

        # new_data['log(x - min(x) + 1)'] = (data['area'] - data['area'].min() + 1).transform(np.log)
        # print("Data after using log transformation: ")
        # print(log_transform_data.head())

        # normalize data:
        # normalize_area = (log_transform_data['area'] - log_transform_data['area'].min()) / (log_transform_data['area'].max() - log_transform_data['area'].min())
        # normalize_price = (log_transform_data['price'] - log_transform_data['price'].min()) / (log_transform_data['price'].max() - log_transform_data['price'].min())
        # normalize_data = pd.DataFrame({'post_type': data['post_type'], 'area': normalize_area, 'price': normalize_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district']})

        # print("Data after using normalization: ")
        # print(normalize_data.head())

        # print("Data for street {}, ward {}, district {}".format(normalize_data['street'][0], normalize_data['ward'][0], normalize_data['district'][0]))
        print("--------------------------------------------------------")
        print(log_transform_data.head())
        print("--------------------------------------------------------")
        print("Data length: ", len(log_transform_data))

        return log_transform_data
    else:
        return None

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