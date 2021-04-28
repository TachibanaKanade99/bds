# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from re import split
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
# from scrapy.pipelines.images import ImagesPipeline
import logging
from datetime import datetime
# import json
import psycopg2
# import scrapy


class PropzyPipeline:
    def process_item(self, item, spider):
        return item

class CheckCrawledDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not adapter.get('url'):
            logging.log(logging.ERROR, "Missing url in " + item['url'])
            raise DropItem("Missing url in ", item['url'])
        if not adapter.get('content'):
            logging.log(logging.ERROR, "Missing content in " + item['url'])
            raise DropItem("Missing content in ", item['url'])
        if not adapter.get('price'):
            logging.log(logging.ERROR, "Missing price in " + item['url'])
            raise DropItem("Missing price in ", item['url'])
        if not adapter.get('area'):
            logging.log(logging.ERROR, "Missing area in " + item['url'])
            raise DropItem("Missing area in ", item['url'])
        if not adapter.get('item_code'):
            logging.log(logging.ERROR, "Missing item_code in " + item['url'])
            raise DropItem("Missing item_code in ", item['url'])
        if not adapter.get('post_type'):
            logging.log(logging.ERROR, "Missing post_type in " + item['url'])
            raise DropItem("Missing post_type in ", item['url'])

        # Handle nullable data:
        if not adapter.get('project_name'):
            adapter['project_name'] = None
        if not adapter.get('orientation'):
            adapter['orientation'] = None
        if not adapter.get('latitude'):
            adapter['latitude'] = None
        if not adapter.get('longitude'):
            adapter['longitude'] = None
        if adapter['number_of_bedrooms'] == '--':
            adapter['number_of_bedrooms'] = None
        if adapter['number_of_toilets'] == '--':
            adapter['number_of_toilets'] = None

        # Handle space in data:
        adapter['url'] = " ".join(adapter['url'].split())
        adapter['content'] = " ".join(adapter['content'].split())
        adapter['price'] = " ".join(adapter['price'].split())
        adapter['area'] = " ".join(adapter['area'].split())
        adapter['item_code'] = " ".join(adapter['item_code'].split())
        adapter['post_type'] = " ".join(adapter['post_type'].split())

        # Handle comma in area:
        area = adapter['area']
        area_comma_idx = area.find(",")
        if area_comma_idx != -1:
            new_area = ''

            for i in range(len(area)):
                if i == area_comma_idx:
                    new_area = new_area + "."
                else:
                    new_area = new_area + area[i]

            adapter['area'] = new_area

        # Handle comma in price:
        price = adapter['price']
        price_comma_idx = price.find(",")
        if price_comma_idx != -1:
            new_price = ''

            for i in range(len(price)):
                if i == price_comma_idx:
                    new_price = new_price + "."
                else:
                    new_price = new_price + price[i]
            
            adapter['price'] = new_price

        # Handle "Đã bán" in price:
        # if price == 'Đã bán':
        #     logging.log(logging.ERROR, "Missing price in " + item['url'])
        #     raise DropItem("Missing price in ", item['url'])

        return item

class PriceValidationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter['price']
        area = adapter['area']
        area_value = float(area[0:area.find("m")])
        price_value = float(price[0:price.find(" ")])

        if price.find("triệu/m²") != -1:
            converted_price = price_value * area_value / 1000.0
            adapter['price'] = str(converted_price) + " tỷ"
            return item
        elif price.find("nghìn/m²") != -1:
            converted_price = price_value * area_value / 1000000.0
            adapter['price'] = str(converted_price) + " tỷ"
            return item
        elif price.find("triệu") != -1:
            converted_price = price_value / 1000.0
            adapter['price'] = str(converted_price) + " tỷ"
            return item
        else:
            return item

class CheckDuplicatedItemsPipeline:
    def __init__(self):
        self.item_lst = []

        # get item_code from database:
        conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
        cur = conn.cursor()
        
        cur.execute("SELECT item_code from bds_realestatedata WHERE url LIKE '%propzy%'")
        item_code_lst = cur.fetchall()

        # close connection:
        cur.close()
        conn.close()

        for item in item_code_lst:
            self.item_lst.append(item[0])

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['item_code'] in self.item_lst:
            logging.log(logging.ERROR, "Duplicated item in " + item['url'])
            raise DropItem("Duplicated item in " + item['url'])
        else:
            self.item_lst.append(adapter['item_code'])
        
        return item

class HandlingStringDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adapter['area'] = float(adapter['area'][0:adapter['area'].find("m")])
        adapter['price'] = float(adapter['price'][0:adapter['price'].find(" ")])
        adapter['item_code'] = adapter['item_code'][adapter['item_code'].find(" ")+1:]

        if adapter['number_of_bedrooms'] is not None:
            adapter['number_of_bedrooms'] = int(adapter['number_of_bedrooms'])
        if adapter['number_of_toilets'] is not None:
            adapter['number_of_toilets'] = int(adapter['number_of_toilets'])


        # handle street, ward, district:
        adapter['province'] = "Hồ Chí Minh"
        splitted_location = adapter['location'].split(',')

        # remove space in splitted_location:
        for i in range(len(splitted_location)):
            splitted_location[i] = " ".join(splitted_location[i].split())

        location_dict = {
            'phố': 'street',
            'đường': 'street',
            'phường': 'ward',
            'xã': 'ward',
            'quận': 'district',
            'huyện': 'district',
        }
        location_keys_lst = list(location_dict.keys())

        for sub in splitted_location:
            tmp = sub.split(" ", 1)
            tmp_prefix = tmp[0].lower()
            tmp_value = tmp[1]

            if tmp_prefix in location_keys_lst:
                adapter[location_dict[tmp_prefix]] = tmp_value

        return item

class PostgreSQLPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
        self.cur = self.conn.cursor()

    # def open_spider(self, spider):
    #     self.cur.execute("SELECT url FROM bds_realestatedata;")
    #     self.item_lst = self.cur.fetchall()

    def close_spider(self, spider):
        # close cursor
        self.cur.close()
        # close connection
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # if len(self.item_lst) > 0:
        #     for i in self.item_lst:
        #         if adapter['url'] == i[0]:
        #             logging.log(logging.ERROR, "Duplicated item in " + item['url'])
        #             raise DropItem("Duplicated item in " + item['url'])
        
        try:
            self.cur.execute("""
                INSERT INTO bds_realestatedata (
                    url, 
                    content,
                    price, 
                    area, 
                    location, 
                    posted_date, 
                    item_code, 
                    image_urls,  
                    orientation, 
                    district, 
                    province, 
                    street, 
                    ward, 
                    post_type, 
                    project_name,
                    number_of_bedrooms,
                    number_of_toilets,
                    latitude,
                    longitude
                ) 
                VALUES ( 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )""", 
                (
                    adapter['url'], 
                    adapter['content'], 
                    adapter['price'], 
                    adapter['area'], 
                    adapter['location'],  
                    adapter['posted_date'], 
                    adapter['item_code'], 
                    adapter['image_urls'], 
                    adapter['orientation'], 
                    adapter['district'], 
                    adapter['province'], 
                    adapter['street'], 
                    adapter['ward'], 
                    adapter['post_type'], 
                    adapter['project_name'],
                    adapter['number_of_bedrooms'],
                    adapter['number_of_toilets'],
                    adapter['latitude'],
                    adapter['longitude']
                )
            )
            self.conn.commit()
        except:
            self.conn.rollback()
        return item
