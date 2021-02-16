# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import logging

class LandCrawlerPipeline:
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
        if not adapter.get('location'):
            logging.log(logging.ERROR, "Missing location in " + item['url'])
            raise DropItem("Missing location in ", item['url'])
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
        # if not adapter.get('image_urls'):
        #     raise DropItem("Missing image_urls in {item}")
        
        # Handle item's content:
        adapter['url'] = " ".join(adapter['url'].split())
        adapter['content'] = " ".join(adapter['content'].split())
        adapter['price'] = " ".join(adapter['price'].split())
        adapter['area'] = " ".join(adapter['area'].split())
        adapter['location'] = " ".join(adapter['location'].split())
        adapter['posted_author'] = " ".join(adapter['posted_author'].split())
        adapter['phone'] = " ".join(adapter['phone'].split())
        adapter['posted_date'] = " ".join(adapter['posted_date'].split())
        adapter['expired_date'] = " ".join(adapter['expired_date'].split())
        adapter['item_code'] = " ".join(adapter['item_code'].split())
        
        return item

class PriceValidationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter['price']
        
        if price.find("triệu/m²") != -1:
            area = adapter['area']
            area_value = float(area[0:area.find("m")])
            price_value = float(price[0:price.find("t")])
            total_price = price_value * area_value / 1000.0
            adapter['price'] = str(total_price) + " tỷ"
            return item
        else:
            return item

class ImageProcessingPipeline(ImagesPipeline):
    def get_media_request(self, item, info):

        # Check if existed image_urls:
        if len(item['image_urls']) != 0:
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)
        else:
            return item

    def item_completed(self, results, item, info):
        image_paths = []
        # results returns a list of tuples (success, file_info)
        # Typical example of a tuple in results:
        """[
            (
                True,
                {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
                'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
                'url': 'http://www.example.com/files/product1.pdf',
                'status': 'downloaded'}
            ),
            (
                False,
                Failure(...)
            )
        ]"""
        for success, file_info in results:
            if success:
                image_paths.append(file_info['path'])
            else:
                raise DropItem("No images in {item}")
        
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item

            
            