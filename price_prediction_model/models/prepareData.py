import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def getData(post_type, street, ward, district):
    # db connection:
    conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")

    query = """
        SELECT post_type, area, price, street, ward, district, posted_date
        FROM bds_realestatedata 
        WHERE
            post_type = '{post_type}' AND
            area IS NOT NULL AND
            price IS NOT NULL AND
            posted_date IS NOT NULL AND
            street = '{street}' AND
            ward = '{ward}' AND
            district = '{district}';
    """.format(post_type=post_type, street=street, ward=ward, district=district)
    
    data = pd.read_sql_query(query, con=conn)

    # close db connection:
    conn.close()

    return data

def calcMinimumMaximum(vals):
    q1 = vals.quantile(0.25)
    q3 = vals.quantile(0.75)
    iqr = q3 - q1

    minimum = q1 - 1.5 * iqr
    maximum = q3 + 1.5 * iqr

    return minimum, maximum

def preprocessData(data):

    # sort data in post_date order:
    # data = data.sort_values(by=['posted_date'])

    # Drop duplicates:    
    # data = data.drop_duplicates(subset='area', keep='last', inplace=False)

    # Instead of drop duplicates try calc and use its mean value:
    data = data.groupby(['area'], as_index=False).mean()

    # sort data by area:
    data = data.sort_values(by=['area'])

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
    # area_upper_bound = data['area'].quantile(0.8)
    # area_lower_bound = data['area'].quantile(0.1)
    # price_upper_bound = data['price'].quantile(0.8)
    # price_lower_bound = data['price'].quantile(0.1)

    # data = data[
    #     (data['area'] < area_upper_bound) &
    #     (data['area'] > area_lower_bound) &
    #     (data['price'] < price_upper_bound) &
    #     (data['price'] > price_lower_bound)
    # ]

    # USE IQR instead to detect outlier
    # while True:
    #     area_minimum, area_maximum = calcMinimumMaximum(data['area'])
    #     if (data['area'] > area_minimum).all() and (data['area'] < area_maximum).all():
    #         break
    #     else:
    #         data = data[(data['area'] > area_minimum) & (data['area'] < area_maximum)]

    # while True:
    #     price_minimum, price_maximum = calcMinimumMaximum(data['price'])
    #     if (data['price'] > price_minimum).all() and (data['price'] < price_maximum).all():
    #         break
    #     else:
    #         data = data[(data['price'] > price_minimum) & (data['price'] < price_maximum)]

    area_minimum, area_maximum = calcMinimumMaximum(data['area'])
    data = data[(data['area'] > area_minimum) & (data['area'] < area_maximum)]

    price_minimum, price_maximum = calcMinimumMaximum(data['price'])
    data = data[(data['price'] > price_minimum) & (data['price'] < price_maximum)]


    area_mean = np.mean(data['area'])

    price_mean = np.mean(data['price'])
    price_std = np.std(data['price'])

    # data = data[~(data['area'] < 10)]
    # data = data[~(data['price'] > 200)]

    data = data[~( (data['area'] < area_mean) & (data['price'] > price_mean) )]
    data = data[~( (data['area'] > area_mean) & (data['price'] < price_mean - price_std) )]


    # smooth data:

    # convolve:
    # kernel_size = 10
    # kernel = np.ones(kernel_size) / kernel_size

    # data['area'] = np.convolve(np.array(data['area']), kernel, mode='same')
    # data['price'] = np.convolve(np.array(data['price']), kernel, mode='same')

    # moving average:
    # data['area'] = data['area'].rolling(window=5).mean()
    # data['price'] = data['price'].rolling(window=5).mean()
    # data = data.dropna()

    return data

def scaleData(data):

    if data is not None:

        # scale data with log transform:

        log_transform_area = (data['area']+1).transform(np.log)
        log_transform_price = (data['price']+1).transform(np.log)
        log_transform_data = pd.DataFrame({'post_type': data['post_type'], 'area': log_transform_area, 'price': log_transform_price, 'street': data['street'], 'ward': data['ward'], 'district': data['district'], 'posted_date': data['posted_date']})

        # new_data['log(x - min(x) + 1)'] = (data['area'] - data['area'].min() + 1).transform(np.log)
        
        print("Data after using log transformation: ")
        print(log_transform_data.head())

        return log_transform_data

    else:
        return None

def convertData(data):
    # Selection few attributes
    attributes = ['area']
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

        train, test = train_test_split(data, test_size=0.2)
        return train, test
    else:
        return None, None