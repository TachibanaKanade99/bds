import scrapy
from homedy.items import HomedyItem
import logging
from datetime import datetime

import js2xml
import lxml.etree
from parsel import Selector

class HomedySpider(scrapy.Spider):
    name = 'homedy_spider'
    allowed_domains = ['homedy.com']
    start_urls = [
        'https://homedy.com/ban-nha-dat-tp-ho-chi-minh?sort=new',
    ]

    # log format:
    # configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logfile/log_' + datetime.now().strftime('%d%m%Y%H%M%S') + '.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def parse(self, response):
        # for item in response.xpath('//div[@id="MainPage"]/div[@class="content"]/div[@class="tab-content"]/div[@class=" product-item"]'):
        #     item_url = "https://homedy.com/" + item.xpath('./div[@class="product-item-top"]/a').attrib["href"]
        #     yield scrapy.Request(item_url, callback=self.parse_item, cb_kwargs=dict(item_url=item_url))
        yield scrapy.Request('https://homedy.com/can-ban-dat-ta-quang-buu-quan-8-gia-159-ty-90m2-bao-so-gan-truong-hoc-cho-cong-vien-kd-tot-es1334705', callback=self.parse_item, cb_kwargs=dict(item_url='https://homedy.com/can-ban-dat-ta-quang-buu-quan-8-gia-159-ty-90m2-bao-so-gan-truong-hoc-cho-cong-vien-kd-tot-es1334705'))

        # next_page:
        # next_page = response.xpath('//div[@class="page-nav"]/ul/li[@class="active"]/following-sibling::*')

        # if next_page.get() is not None:
        #     nextpage_url = response.urljoin(next_page.xpath('./a').attrib["href"])

        #     if nextpage_url != 'https://homedy.com/ban-nha-dat-tp-ho-chi-minh/p5?sort=new':
        #         yield scrapy.Request(nextpage_url, callback=self.parse)

    def parse_item(self, response, item_url):
        item = HomedyItem()

        item['url'] = item_url
        item['content'] = response.xpath('//div[@class="product-detail-top"]/div[1]/div[1]/div[@class="product-detail-top-left"]/h1/text()').get()

        item['item_code'] = response.xpath('//div[@class="product-info"]/span[@class="code"]/text()').get()
        item['posted_date'] = response.xpath('//div[@class="product-info"]/span[@class="date-created"][1]/text()').get()
        item['expired_date'] = response.xpath('//div[@class="product-info"]/span[last()]/text()').get()

        post_type = response.xpath('//div[@class="address"]/a/span/text()').get()

        # Handle null for post_type:
        if post_type is not None:
            if "Đường" in post_type:
                street = post_type[post_type.find("Đường"):]
                item['street'] = street[street.find(" ")+1:]
            if "Phố" in post_type:
                street = post_type[post_type.find("Phố"):]
                item['street'] = street[street.find(" ")+1:]
        else:
            post_type = response.xpath('//div[@class="address"]/a/@title').get()

        location_dict = {
            'Dự': 'project_name',
            'Đường': 'street',
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
                        if tmp[0] == 'Đường':
                            print(tmp)
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
        price_unit = response.xpath('//div[@class="product-detail"]/div[@class="row"][1]/div[contains(@class, "cell-right")]/text()[2]').get()
        price_unit = price_unit[price_unit.find("T"):price_unit.find(" ")]
        
        if price is None or price_unit is None:
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
        xml = lxml.etree.tostring(js2xml.parse(js), encoding='unicode')
        selector = Selector(text=xml)

        latitude = selector.css('var[name="_latitude"] number').attrib["value"]
        item['latitude'] = float(latitude)

        longtitude = selector.css('var[name="_longtitude"] number').attrib["value"]
        item['longitude'] = float(longtitude)

        yield item

        