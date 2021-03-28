# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomedyItem(scrapy.Item):
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
    post_type = scrapy.Field()
    full_description = scrapy.Field()

    # Option field:
    email = scrapy.Field()
    project_name = scrapy.Field()
    policy = scrapy.Field()
    street = scrapy.Field()
    ward = scrapy.Field()
    district = scrapy.Field()
    province = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    pass
