# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import logging
from datetime import datetime
import json
import psycopg2
import scrapy
from _datetime import timedelta


class HomedyPipeline:
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
        if not adapter.get('posted_author'):
            logging.log(logging.ERROR, "Missing posted_author in " + item['url'])
            raise DropItem("Missing posted_author in ", item['url'])
        if not adapter.get('phone'):
            logging.log(logging.ERROR, "Missing phone in " + item['url'])
            raise DropItem("Missing phone in ", item['url'])
        if not adapter.get('posted_date'):
            logging.log(logging.ERROR, "Missing posted_date in " + item['url'])
            raise DropItem("Missing posted_date in ", item['url'])
        if not adapter.get('expired_date'):
            logging.log(logging.ERROR, "Missing expired_date in " + item['url'])
            raise DropItem("Missing expired_date in ", item['url'])
        if not adapter.get('item_code'):
            logging.log(logging.ERROR, "Missing item_code in " + item['url'])
            raise DropItem("Missing item_code in ", item['url'])
        if not adapter.get('post_type'):
            logging.log(logging.ERROR, "Missing post_type in " + item['url'])
            raise DropItem("Missing post_type in ", item['url'])

        # Handle null optional data:
        if not adapter.get('policy'):
            adapter['policy'] = None
        if not adapter.get('latitude'):
            adapter['latitude'] = None
        if not adapter.get('longitude'):
            adapter['longitude'] = None

        # Handling area, price if having "-" or ",":
        if adapter['area'].find("-") != -1:
            # logging.log(logging.ERROR, "Multiple areas in " + item['url'] + " price = " + item['price'])
            # raise DropItem("Multiple areas in ", item['url'], " price = ", item['price'])
            area = adapter['area']
            area = area[area.find("-")+1:]
            adapter['area'] = " ".join(adapter['area'].split())

        if adapter['price'].find("-") != -1:
            # logging.log(logging.ERROR, "Multiple prices in " + item['url'] + " price = " + item['price'])
            # raise DropItem("Multiple prices in ", item['url'], " price = ", item['price'])
            price = adapter['price']
            price = price[price.find("-")+1:]
            adapter['price'] = " ".join(adapter['price'].split())

        # Price format:
        price = adapter['price']
        comma_idx = price.find(",")
        if comma_idx != -1:
            new_str = ''

            for i in range(len(price)):
                if i == comma_idx:
                    new_str = new_str + "."
                else:
                    new_str = new_str + price[i]
            
            adapter['price'] = new_str
        
        # Handle item's content:
        adapter['url'] = " ".join(adapter['url'].split())
        adapter['content'] = " ".join(adapter['content'].split())
        adapter['price'] = " ".join(adapter['price'].split())
        adapter['area'] = " ".join(adapter['area'].split())
        adapter['posted_author'] = " ".join(adapter['posted_author'].split())
        adapter['phone'] = " ".join(adapter['phone'].split())
        adapter['posted_date'] = " ".join(adapter['posted_date'].split())
        adapter['expired_date'] = " ".join(adapter['expired_date'].split())
        adapter['item_code'] = " ".join(adapter['item_code'].split())
        adapter['post_type'] = " ".join(adapter['post_type'].split())
        
        return item

class CheckDuplicateItemsPipeline:
    def __init__(self):
        self.item_lst = []

        # f = open('sample_data_hcm.jl', encoding='utf-8')
        # for line in f:
        #     data = json.loads(line)
        #     self.item_lst.append(data['item_code'])

        # f.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['item_code'] in self.item_lst:
            logging.log(logging.ERROR, "Duplicated item in " + item['url'])
            raise DropItem("Duplicated item in " + item['url'])
        else:
            self.item_lst.append(adapter['item_code'])
            return item

class PriceValidationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter['price']
        
        if price.find("Triệu") != -1:
            area = adapter['area']
            area_value = float(area)
            price_value = float(price[0:price.find("T")])
            total_price = price_value * area_value / 1000.0
            adapter['price'] = str(total_price) + " Tỷ"
            return item
        else:
            return item

class HandlingStringDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        adapter['area'] = float(adapter['area'])
        adapter['price'] = float(adapter['price'][0:adapter['price'].find(" ")])

        # Handle posted_date:
        posted_date = adapter['posted_date']
        number = 0
        num_days = 0
        for s in posted_date.split(" "):
            if s.isdigit():
                number = int(s)
            elif s == "ngày":
                num_days = number
            elif s == "tuần":
                num_days = 7 * number
            elif s == "tháng":
                num_days = 30 * number
            else:
                num_days = 0
        adapter['posted_date'] = (datetime.today() - timedelta(days=num_days)).strftime("%d/%m/%Y")

        adapter['posted_date'] = datetime.strptime(adapter['posted_date'], "%d/%m/%Y")
        adapter['expired_date'] = datetime.strptime(adapter['expired_date'], "%d/%m/%Y")

        # Optional data:
        # if adapter['facade'] is not None:
        #     adapter['facade'] = float(adapter['facade'][0:adapter['facade'].find(" ")])
        # if adapter['entrance'] is not None:
        #     adapter['entrance'] = float(adapter['entrance'][0:adapter['entrance'].find(" ")])
        # if adapter['number_of_floors'] is not None:
        #     adapter['number_of_floors'] = int(adapter['number_of_floors'][0:adapter['number_of_floors'].find(" ")])
        # if adapter['number_of_bedrooms'] is not None:
        #     adapter['number_of_bedrooms'] = int(adapter['number_of_bedrooms'][0:adapter['number_of_bedrooms'].find(" ")])
        # if adapter['number_of_toilets'] is not None:
        #     adapter['number_of_toilets'] = int(adapter['number_of_toilets'][0:adapter['number_of_toilets'].find(" ")])

        # extract data from item['location']:
        # splitted_location = adapter['post_type'].split(" ")
        # district_lst = ["Bình Tân", "Bình Thạnh", "Gò Vấp", "Phú Nhuận", "Tân Bình", "Tân Phú", "Thủ Đức", "Bình Chánh", "Cần Giờ", "Củ Chi", "Hóc Môn", "Nhà Bè"]

        # for content in splitted_location:
        #     tmp = content.split(" ", 1)

        #     if tmp[0] == "Dự":
        #         adapter['project_name'] = tmp[1].split(" ", 1)[1]
        #     if tmp[0] == "Đường":
        #         adapter['street'] = tmp[1]
        #     if tmp[0] in ("Phường", "Xã"):
        #         adapter['ward'] = tmp[1]
        #     if tmp[0] in ("Quận", "Huyện"):
        #         adapter['district'] = tmp[1]
        # else:
        #     # if content in district_lst:
        #     #     adapter['district'] = content
        #     # else:
        #     #     adapter['province'] = content
        #     adapter['district'] = splitted_location[-2]
        #     adapter['province'] = splitted_location[-1]

        # set null for non-existed value:
        if not adapter.get('project_name'):
            adapter['project_name'] = None
        if not adapter.get('street'):
            adapter['street'] = None
        if not adapter.get('ward'):
            adapter['ward'] = None
        if not adapter.get('district'):
            adapter['district'] = None
        if not adapter.get('province'):
            adapter['province'] = None

        # # handling latitude & longitude:
        # if adapter.get('latitude'):
        #     res = adapter['latitude']
        #     latitude = res[res.find("q="):res.find(",")]
        #     longitude = res[res.find(",")+1:res.find("&")]

        #     latitude = float(''.join(x for x in latitude if x.isdigit() or x == '.'))
        #     longitude = float(longitude)

        # format value:
        adapter['latitude'] = "{:5.10f}".format(adapter['latitude'])
        adapter['longitude'] = "{:5.10f}".format(adapter['longitude'])

        # else:
        #     adapter['latitude'] = None
        #     adapter['longitude'] = None

        return item