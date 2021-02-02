# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LandCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
    posted_author = scrapy.Field()
    phone = scrapy.Field()
    posted_date = scrapy.Field()
    expired_date = scrapy.Field()
    item_code = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    pass
