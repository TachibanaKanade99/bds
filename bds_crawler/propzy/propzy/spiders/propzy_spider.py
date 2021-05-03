import scrapy
from propzy.items import PropzyItem
import logging
from datetime import datetime
import psycopg2

import js2xml
import lxml.etree
from parsel import Selector

class PropzySpider(scrapy.Spider):
    name = 'propzy_spider'
    allowed_domains = ['propzy.vn']
    start_urls = [
        'https://propzy.vn/mua/bat-dong-san/hcm?property_type=11&selectprice=2&bed-value&loai=11,13,8,14',
    ]

    # log format:
    # configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logfile/log_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def __init__(self, *arg, **kwargs):
        super(PropzySpider, self).__init__(*arg, **kwargs)

        # open db connection:
        self.conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT url FROM bds_realestatedata WHERE url LIKE '%propzy%';")
        self.item_lst = self.cur.fetchall()

        # close connection:
        self.cur.close()
        self.conn.close()
        
        self.new_lst = []
        for item in self.item_lst:
            self.new_lst.append(item[0])

    def parse(self, response):
        for item in response.xpath('//div[@id="view-as-grid"]/div[contains(@class, "col-md-3")]'):
            item_url = "https://propzy.vn" + item.xpath('./div[contains(@class, "item-listing")]/div[@class="bl-img"]/div[contains(@class, "owl-carousel")]/a').attrib["href"]

            if item_url not in self.new_lst:
                yield scrapy.Request(item_url, callback=self.parse_item, cb_kwargs=dict(item_url=item_url))
            else:
                logging.log(logging.ERROR, "Duplicated item in " + item_url)
                continue

        # next page:
        next_page = response.xpath('//div[@class="pages"]/ul/li/a[contains(@class, "current")]/following::*')

        if next_page.get() is not None:
            nextpage_url = response.urljoin(next_page.xpath('./a').attrib["href"])

            # if nextpage_url != 'https://propzy.vn/mua/bat-dong-san/hcm/p1000?property_type=11&selectprice=2&bed-value&loai=11,13,8,14':
            yield scrapy.Request(nextpage_url, callback=self.parse)

        # url = 'https://propzy.vn/mua/dat-nen/hcm/quan-thu-duc/id337654'
        # yield scrapy.Request(url, callback=self.parse_item, cb_kwargs=dict(item_url=url))

    def parse_item(self, response, item_url):
        item = PropzyItem()
        item['url'] = item_url

        item['content'] = response.xpath('//div[@class="t-detail"]/h1/text()').get()
        
        posted_date = datetime.now().strftime("%d/%m/%Y")
        item['posted_date'] = datetime.strptime(posted_date, "%d/%m/%Y")

        item['location'] = response.xpath('//div[@class="t-detail"]/p[@class="p-address"]/text()').get()
        item['item_code'] = response.xpath('//div[@class="t-detail"]/div[@class="label mb-10"]/span[@class="label-3"]/text()').get()
        
        post_type = response.xpath('//div[@class="breadcrumbs"]/span[@class="item"]/text()').get()
        post_type = " ".join(post_type.split())

        post_type_dict = {
            'Bán chung cư': 'Bán căn hộ chung cư',
            'Bán đất nền dự án': 'Bán đất nền dự án (đất trong dự án quy hoạch)',
            'Bán đất nền': 'Bán đất',
            'Bán nhà riêng': 'Bán nhà riêng'
        }
        post_type_keys_lst = list(post_type_dict.keys())

        if post_type in post_type_keys_lst:
            item['post_type'] = post_type_dict[post_type]

        # handle price:
        price = response.xpath('//div[@class="t-detail"]/p[@class="p-price-n"]/text()').get()
        price = " ".join(price.split())

        if price == 'Đã bán':
            price = response.xpath('//div[@class="t-detail"]/p[@class="p-price-n"]/span[@class="average-price"]/text()').get()
        
        item['price'] = price
        
        for content in response.xpath('//div[@class="bl-parameter-listing"]/ul/li'):
            type = content.xpath('./span[@class="sp-text"]/text()').get()
            data = content.xpath('./span[@class="sp-info"]/text()').get()
            if type == "Phòng ngủ":
                item['number_of_bedrooms'] = data
            elif type == "Phòng tắm":
                item['number_of_toilets'] = data
            elif type == "Diện tích":
                item['area'] = data
            elif type == "Hướng":
                item['orientation'] = data

        # images:
        
        image_urls = []
        
        # first image:
        for img in  response.xpath('//div[@class="div-hover"]/div[contains(@class, "item")]'):
            # only 1 picture:
            img_src = img.xpath('./a[contains(@class, "img")]/img/@src').get()
            
            if img_src is not None:
                image_urls.append(img_src)
            else:
                # 3 images:
                imgs_row = img.xpath('./div[@class="row row-img"]')
                # if len(imgs_row) > 0:
                for img_url in imgs_row.xpath('./div[contains(@class, "col-padding")]'):
                    img_item = img_url.xpath('./div[@class="item"]').get()

                    if img_item is not None:
                        img_src = img_url.xpath('./div[@class="item"]/a/img/@src').get()
                        image_urls.append(img_src)
                    
                    # default: 5 images
                    else:
                        imgs_row = img_url.xpath('./div[@class="row row-img"]')
                        print("Length: ", len(imgs_row.xpath('./div[contains(@class, "col-padding")]')))
                        for img_url in imgs_row.xpath('./div[contains(@class, "col-padding")]'):
                            img_src = img_url.xpath('./div[@class="item"]/a/img/@src').get()
                            image_urls.append(img_src)

        item['image_urls'] = image_urls

        # project name:
        project_name_lst = response.xpath('//div[@id="tab-project"]/div[contains(@class, "tab-content")]/div[@class="d-info-overview title"]/text()').getall()

        if len(project_name_lst) > 0:
            project_name = project_name_lst[1]
            project_name = " ".join(project_name.split())
            item['project_name'] = project_name

        # latitude & longitude:
        js = response.xpath('//div[@id="fb-root"]/following-sibling::*/text()').get()
        if js is not None:
            xml = lxml.etree.tostring(js2xml.parse(js), encoding='unicode')
            selector = Selector(text=xml)

            latitude = selector.xpath('//property[@name="latitude"]/number').attrib["value"]
            item['latitude'] = float(latitude)

            longtitude = selector.xpath('//property[@name="longitude"]/number').attrib["value"]
            item['longitude'] = float(longtitude)

        yield item
