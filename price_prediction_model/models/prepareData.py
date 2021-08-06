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

    # check if data is existed:
    if len(data) <= 0:
        data = None

    return data

# def getData(post_type, district):
#     # db connection:
#     conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")

#     query = """
#         SELECT post_type, area, price, district, posted_date
#         FROM bds_realestatedata 
#         WHERE
#             post_type = '{post_type}' AND
#             area IS NOT NULL AND
#             price IS NOT NULL AND
#             posted_date IS NOT NULL AND
#             district = '{district}';
#     """.format(post_type=post_type, district=district)
    
#     data = pd.read_sql_query(query, con=conn)

#     # close db connection:
#     conn.close()

#     # check if data is existed:
#     if len(data) <= 0:
#         data = None

#     return data

def calcMinimumMaximum(vals):
    q1 = vals.quantile(0.25)
    q3 = vals.quantile(0.75)
    iqr = q3 - q1

    minimum = q1 - 1.5 * iqr
    maximum = q3 + 1.5 * iqr

    return minimum, maximum
    # return q1, q3

# percentiles's method:
def calcPercentiles(vals):
    min_val = vals.quantile(0.05)
    max_val = vals.quantile(0.95)

    return min_val, max_val

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
    # area_upper_bound = data['area'].quantile(0.95)
    # area_lower_bound = data['area'].quantile(0.05)
    # price_upper_bound = data['price'].quantile(0.95)
    # price_lower_bound = data['price'].quantile(0.05)

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
    # price_minimum, price_maximum = calcMinimumMaximum(data['price'])
    # data = data[(data['price'] > price_minimum) & (data['price'] < price_maximum)]

    # part_data = data['price'][:len(data)//5]
    # price_minimum, price_maximum = calcMinimumMaximum(part_data)
    # data_1 = data[:len(data)//5][(part_data > price_minimum) & (part_data < price_maximum)]

    # part_data = data['price'][len(data)//5:len(data)*2//5]
    # price_minimum, price_maximum = calcMinimumMaximum(part_data)
    # data_2 = data[len(data)//5:len(data)*2//5][(part_data > price_minimum) & (part_data < price_maximum)]

    # part_data = data['price'][len(data)*2//5:len(data)*3//5]
    # price_minimum, price_maximum = calcMinimumMaximum(part_data)
    # data_3 = data[len(data)*2//5:len(data)*3//5][(part_data > price_minimum) & (part_data < price_maximum)]

    # part_data = data['price'][len(data)*3//5:len(data)*4//5]
    # price_minimum, price_maximum = calcMinimumMaximum(part_data)
    # data_4 = data[len(data)*3//5:len(data)*4//5][(part_data > price_minimum) & (part_data < price_maximum)]

    # part_data = data['price'][len(data)*4//5:]
    # price_minimum, price_maximum = calcMinimumMaximum(part_data)
    # data_5 = data[len(data)*4//5:][(part_data > price_minimum) & (part_data < price_maximum)]

    # data = pd.concat([data_1, data_2, data_3, data_4, data_5], ignore_index=True)

    num_of_parts = 5
    max_value = data['area'].iloc[len(data)-1]
    min_value = data['area'].iloc[0]
    frame_value = (max_value - min_value) / num_of_parts

    # divide dataframe into smaller frames according to the their max and min value so number of rows in each small dataframe may be different: 
    frames_data = [ data[(data['area'] >= i*frame_value+min_value) & (data['area'] <= (i+1)*frame_value+min_value)].copy() for i in range(0, num_of_parts)]
    frames_data[-1] = frames_data[-1].append(data[data['area'] > num_of_parts*frame_value+min_value])

    # Apply quantile into smaller frames
    for i in range(len(frames_data)):
        price_minimum, price_maximum = calcPercentiles(frames_data[i]['price'])
        frames_data[i] = frames_data[i][(frames_data[i]['price'] > price_minimum) & (frames_data[i]['price'] < price_maximum)]
    
    data = pd.concat(frames_data, ignore_index=True)
    
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