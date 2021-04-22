import scrapy
from homedy.items import HomedyItem
import logging
from datetime import datetime
import psycopg2

import js2xml
import lxml.etree
from parsel import Selector

class HomedySpider(scrapy.Spider):
    name = 'homedy_spider'
    allowed_domains = ['homedy.com']
    start_urls = [
        'https://homedy.com/ban-nha-dat-tp-ho-chi-minh-gia-tren-300-trieu?sort=new',
    ]

    # log format:
    # configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logfile/log_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def __init__(self, *arg, **kwargs):
        super(HomedySpider, self).__init__(*arg, **kwargs)

        # open db connection:
        self.conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT url FROM bds_realestatedata WHERE url LIKE '%homedy%';")
        self.item_lst = self.cur.fetchall()

        # close connection:
        self.cur.close()
        self.conn.close()
        
        self.new_lst = []
        for item in self.item_lst:
            self.new_lst.append(item[0])

    def parse(self, response):

        for item in response.xpath('//div[@id="MainPage"]/div[@class="content"]/div[@class="tab-content"]/div[@class=" product-item"]'):
            item_url = "https://homedy.com/" + item.xpath('./div[@class="product-item-top"]/a').attrib["href"]

            if item_url not in self.new_lst:
                yield scrapy.Request(item_url, callback=self.parse_item, cb_kwargs=dict(item_url=item_url))
            else:
                logging.log(logging.ERROR, "Duplicated item in " + item_url)
                continue
        # url = 'https://homedy.com/ban-can-82m2-hoang-kim-the-gia-gia-re-235-ty-so-hong-thanh-toan-700tr-o-ngay-es960493'
        # yield scrapy.Request(url, callback=self.parse_item, cb_kwargs=dict(item_url=url))

        # next_page:
        next_page = response.xpath('//div[@class="page-nav"]/ul/li[@class="active"]/following-sibling::*')

        if next_page.get() is not None:
            nextpage_url = response.urljoin(next_page.xpath('./a').attrib["href"])

            # if nextpage_url != 'https://homedy.com/ban-nha-dat-tp-ho-chi-minh-gia-tren-300-trieu/p2?sort=new':
            yield scrapy.Request(nextpage_url, callback=self.parse)

    def parse_item(self, response, item_url):
        item = HomedyItem()

        item['url'] = item_url
        item['content'] = response.xpath('//div[@class="product-detail-top"]/div[1]/div[1]/div[@class="product-detail-top-left"]/h1/text()').get()

        item['item_code'] = response.xpath('//div[@class="product-info"]/span[@class="code"]/text()').get()
        item['posted_date'] = response.xpath('//div[@class="product-info"]/span[@class="date-created"][1]/text()').get()
        item['expired_date'] = response.xpath('//div[@class="product-info"]/span[last()]/text()').get()

        post_type = response.xpath('//div[@class="address"]/a/span/text()').get()

        # Handle null for post_type:
        if post_type is None:
            post_type = response.xpath('//div[@class="address"]/a/text()').get()

        # fu*ck again =.=:
        if post_type is not None:

            if "Đường" in post_type:
                street = post_type[post_type.find("Đường"):]
                item['street'] = street[street.find(" ")+1:]
            if "Phố" in post_type:
                street = post_type[post_type.find("Phố"):]
                item['street'] = street[street.find(" ")+1:]
            if "Phường" in post_type:
                ward = post_type[post_type.find("Phường"):]
                item['ward'] = ward[ward.find(" ")+1:]
            if "Xã" in post_type:
                ward = post_type[post_type.find("Xã"):]
                item['ward'] = ward[ward.find(" ")+1:]
            if "Quận" in post_type:
                district = post_type[post_type.find("Quận"):]
                item['district'] = district[district.find(" ")+1:]
            if "Huyện" in post_type:
                district = post_type[post_type.find("Huyện"):]
                item['district'] = district[district.find(" ")+1:]

            location_dict = {
                'Dự': 'project_name',
                'Đường': 'street',
                'Phố': 'street',
                'Phường': 'ward',
                'Xã': 'ward',
                'Quận': 'district',
                'Huyện': 'district',
                'TP': 'province'
            }
            location_keys_lst = list(location_dict.keys())

            for content in response.xpath('//div[@class="address"]/span'):
                text = content.xpath('./text()').get()
                tmp = text.split(" ", 1)

                if tmp[0] == "": # Fuck
                    tmp = tmp[1].split(" ", 1)

                for key in location_keys_lst:
                    if tmp[0] == key:
                        if tmp[0] == 'Dự':
                            item[location_dict[key]] = tmp[1].split(" ", 1)[1]
                        else:
                            # if tmp[0] == 'Đường':
                            #     print(tmp)
                            item[location_dict[key]] = tmp[1]
                
                # if tmp[0] == "": # Fuck
                #     second_tmp = tmp[1].split(" ", 1)

                #     for key in location_keys_lst:
                #         if second_tmp[0] == key:
                #             if second_tmp[0] == 'Dự':
                #                 item[location_dict[key]] = second_tmp[1].split(" ", 1)[1]
                #             else:
                #                 item[location_dict[key]] = second_tmp[1]

            post_type_dict = {
                'Bán Căn hộ chung cư': 'Bán căn hộ chung cư',
                'Bán Căn hộ': 'Bán căn hộ chung cư',
                'Bán Bất động sản khác': 'Bán loại bất động sản khác',
                'Bán Nhà biệt thự, liền kề': 'Bán nhà biệt thự, liền kề (nhà trong dự án quy hoạch)',
                'Bán Nhà phố thương mại Shophouse': 'Bán nhà mặt phố',
                'Bán Nhà mặt phố': 'Bán nhà mặt phố',
                'Bán Nhà riêng': 'Bán nhà riêng',
                'Bán Đất': 'Bán đất',
                'Bán Đất nền dự án': 'Bán đất nền dự án (đất trong dự án quy hoạch)'
            }
            post_type_keys_lst = list(post_type_dict.keys())

            for key in post_type_keys_lst:
                if key in post_type:
                    item['post_type'] = post_type_dict[key]

        price = response.xpath('//div[@class="product-detail"]/div[@class="row"][1]/div[contains(@class, "cell-right")]/span/text()').get()

        if price is None:
            price = response.xpath('//div[@class="product-detail"]/div[@class="row"][1]/div[contains(@class, "cell-right")]/em/text()').get()

        price_unit = response.xpath('//div[@class="product-detail"]/div[@class="row"][1]/div[contains(@class, "cell-right")]/text()[2]').get()
        price_unit = price_unit[price_unit.find("T"):price_unit.find(" ")]
        
        if price == 'Thương lượng':
            item['price'] = price
        elif price is None or price_unit is None:
            item['price'] = None
        else:
            item['price'] = price + " " + price_unit

        item['area'] = response.xpath('//div[@class="product-detail"]/div[@class="row"][2]/div[contains(@class, "cell-right")]/span/text()').get()

        # Full description:
        texts = response.xpath('//div[@class="description readmore"]//p/text()').extract()
        item['full_description'] = [text.strip().replace('"', '').replace("'", "").replace("’", "") for text in texts if text.strip()]

        item['posted_author'] = response.xpath('//div[@class="info-agency"]/div[1]/a/@title').get()
        item['phone'] = response.xpath('//a[@class="btn mobile mobile-counter pc-mobile-number"]/@data-mobile').get()

        # Latitude & Longitude:
        js = response.xpath('//div[@id="modal_street_view"]/following-sibling::*/text()').get()
        if js is not None:
            xml = lxml.etree.tostring(js2xml.parse(js), encoding='unicode')
            selector = Selector(text=xml)

            latitude = selector.css('var[name="_latitude"] number').attrib["value"]
            item['latitude'] = float(latitude)

            longtitude = selector.css('var[name="_longtitude"] number').attrib["value"]
            item['longitude'] = float(longtitude)


        # image:
        image_urls = []
        first_image = response.xpath('//div[@class="image-view"]/div[@class="container"]/div[@class="image-carousel owl-carousel owl-theme"]/div[contains(@class, "image-default")]/a').attrib["href"]
        image_urls.append(first_image)

        for other in response.xpath('//div[@class="image-view"]/div[@class="container"]/div[@class="image-carousel owl-carousel owl-theme"]/div[contains(@class, "image-item")]/div[@class="item"]'):
            image_url = other.xpath('./div[@class="animate-box"]/a').attrib["href"]
            image_urls.append(image_url)

        item['image_urls'] = image_urls

        # get project name:
        project_name_component = response.xpath('//div[@class="product-project"]/div[@class="product-project-bg"]')

        if project_name_component.get() is not None:
            project_name = project_name_component.xpath('./div[@class="project"]/div[@class="project-detail"]/div[contains(@class, "item")]/div[@class="info"]/a/text()').get()
            item['project_name'] = " ".join(project_name.split())

        yield item

        