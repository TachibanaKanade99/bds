# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropzyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()
    content = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
    posted_date = scrapy.Field()
    item_code = scrapy.Field()
    image_urls = scrapy.Field()
    post_type = scrapy.Field()


    # Optional fields:
    project_name = scrapy.Field()
    street = scrapy.Field()
    ward = scrapy.Field()
    district = scrapy.Field()
    province = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    number_of_bedrooms = scrapy.Field()
    number_of_toilets = scrapy.Field()
    orientation = scrapy.Field()
    
    pass
