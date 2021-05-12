# import necessary libraries:
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

from models.prepareData import preprocessData

df_data = pd.read_csv('data_thesis/data_2.csv', skipfooter=1, engine='python')

# select specific cols:
df_data = df_data[['transaction_type', 'property_type', 'area', 'price', 'addr_street', 'addr_ward', 'addr_district', 'addr_city']]

# select specific area:
df_data = df_data[
                (df_data['transaction_type'] == 'bán') &
                (df_data['property_type'] == 'nhà riêng') &
                (df_data['addr_street'] == 'đường minh khai') &
                (df_data['addr_ward'] == 'phường minh khai') &
                (df_data['addr_district'] == 'hai bà trưng') &
                (df_data['addr_city'] == 'hà nội')
                ]

# check if data is null:
df_data.isnull()

# drop null values:
df_data = df_data.dropna()

# sort values by created date
df_data = df_data.sort_values(by=['created_date'])

# Drop duplicates:    
df_data = df_data.drop_duplicates(subset='area', keep='last', inplace=False)

# scale data:


# divide train - test:
train, test = train_test_split(df_data, test_size=0.2)

# Sort data by area column:
train = train.sort_values(by=['area'])
test = test.sort_values(by=['area'])

