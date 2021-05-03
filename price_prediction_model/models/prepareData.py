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

    return data

def preprocessData(data):

    # Drop duplicates:    
    data = data.drop_duplicates(subset='area', keep='first', inplace=False)

    # remove outliner:

    # use standard deviation:
    # factor = 3
    # area_upper_bound = data['area'].mean() + data['area'].std() * factor
    # area_lower_bound = data['area'].mean() - data['area'].std() * factor
    # price_upper_bound = data['price'].mean() + data['price'].std() * factor
    # price_lower_bound = data['price'].mean() - data['price'].std() * factor

    # data = data[
    #     (data['area'] < area_upper_bound) &
    #     (data['area'] > area_lower_bound) &
    #     (data['price'] < price_upper_bound) &
    #     (data['price'] > price_lower_bound)
    # ]
    
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

    if len(data) > 15:
        return data
    else:
        return None

def scaleData(data):

    if data is not None:

        # scale data with log transform:

        log_transform_area = (data['area']+1).transform(np.log)
        log_transform_price = (data['price']+1).transform(np.log)
        log_transform_data = pd.DataFrame({'post_type': data['post_type'], 'area': log_transform_area, 'price': log_transform_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district']})

        # print("--------------------------------------------------------")
        # print(log_transform_data.head())
        # print("--------------------------------------------------------")
        # print("Log Transformation Data length: ", len(log_transform_data))

        # new_data['log(x - min(x) + 1)'] = (data['area'] - data['area'].min() + 1).transform(np.log)
        # print("Data after using log transformation: ")
        # print(log_transform_data.head())

        # normalize data:
        # normalize_area = (data['area'] - data['area'].min()) / (data['area'].max() - data['area'].min())
        # normalize_price = (data['price'] - data['price'].min()) / (data['price'].max() - data['price'].min())
        # normalize_data = pd.DataFrame({'post_type': data['post_type'], 'area': normalize_area, 'price': normalize_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district']})

        # print("Data after using normalization: ")
        # print(normalize_data.head())

        # print("Data for street {}, ward {}, district {}".format(normalize_data['street'][0], normalize_data['ward'][0], normalize_data['district'][0]))

        return log_transform_data
        # return normalize_data

    else:
        return None

def convertData(data):
    # Selection few attributes
    attributes = ['area',]
    predict_val = ['price']
    
    # Vector attributes of lands
    X = data[attributes]
    # Vector price of land
    Y = data[predict_val]

    # convert into array
    X = np.array(X)
    Y = np.array(Y)
    
    return X, Y

def divideData(data):
    if data is not None:
        # Split data to training test and testing test
        # training data : testing data = 80 : 20

        # print(data['price'])
        # print("Number of price instances by class: {}".format(np.bincount(data['price'])))
        # train, test = train_test_split(data, test_size=0.2, random_state=42, stratify=data['price'].astype(int))
        train, test = train_test_split(data, test_size=0.2)
        
        return train, test
    else:
        return None, None