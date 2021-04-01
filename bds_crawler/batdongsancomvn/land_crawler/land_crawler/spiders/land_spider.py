import scrapy
from land_crawler.items import LandCrawlerItem
import logging
# from scrapy.utils.log import configure_logging
from datetime import datetime
import psycopg2

# Selenium:
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import psycopg2

class LandSpider(scrapy.Spider):
    name = "land_spider"
    allowed_domains = ['batdongsan.com.vn']

    # start_urls = [
        # 'https://batdongsan.com.vn/ban-dat-dat-nen/-1/n-100000/-1/-1',
        # 'http://quotes.toscrape.com',
        # 'https://batdongsan.com.vn/ban-dat-dat-nen-tp-hcm/-1/n-100000/-1/-1'
        # 'https://batdongsan.com.vn/ban-dat-tp-hcm/-1/n-30000/-1/-1',
        # 'https://batdongsan.com.vn/ban-dat-nen-du-an-tp-hcm/-1/n-30000/-1/-1',
    # ]

    # log format:
    # configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logfile/log_' + datetime.now().strftime('%d%m%Y%H%M%S') + '.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def start_requests(self):
        # url='https://batdongsan.com.vn/nha-dat-ban-tp-hcm/-1/n-100000/-1/-1'
        url='https://batdongsan.com.vn/nha-dat-ban-tp-hcm/-1/n-100000/-1/-1/p235'
        yield scrapy.Request(url=url, callback=self.parse, meta={'selenium': True}, dont_filter=True)
        # item_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-truong-quoc-dung-phuong-8-13-prj-newton-residence/ban-gap-novaland-2pn-full-noi-that-cuc-dep-lh-0973034874-pr28541296'
        # yield scrapy.Request(item_url, callback=self.parse_item, meta={'selenium': True}, cb_kwargs=dict(item_url=item_url))

    def parse(self, response):

        # open db connection:
        conn = psycopg2.connect(database="real_estate_data", user="postgres", password="361975Warcraft")
        cur = conn.cursor()
        cur.execute("SELECT url FROM bds_realestatedata WHERE url LIKE '%batdongsan%';")
        item_lst = cur.fetchall()
        
        new_lst = []
        for item in item_lst:
            new_lst.append(item[0])

        for item in response.xpath('//div[@id="product-lists-web"]/div[contains(@class, "product-item clearfix")]'):
            item_url = "https://batdongsan.com.vn" + item.xpath('./a').attrib["href"]

            if item_url not in new_lst:
                yield scrapy.Request(item_url, callback=self.parse_item, meta={'selenium': True}, cb_kwargs=dict(item_url=item_url))
            else:
                logging.log(logging.ERROR, "Duplicated item in " + item_url)
                continue
        
        # next page
        next_page = response.xpath('//div[@class="pagination"]/a[@class="actived"]/following-sibling::*')

        if next_page.get() is not None:
            nextpage_url = response.urljoin(next_page.attrib["href"])
            yield scrapy.Request(nextpage_url, callback=self.parse, meta={'selenium': True})
        
        # close logging
        # handlers = logging.handlers[:]
        # for handler in handlers:
        #     handler.close()
        #     logging.removeHandler(handler)

    def parse_item(self, response, item_url):
        item = LandCrawlerItem()

        for land_item in response.xpath('//div[@class="form-content"]/div[contains(@class, "main-container clearfix")]'):
            item['url'] = item_url
            item['content'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/h1[@class="tile-product"]/text()').get()
            
            item['price'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="short-detail-wrap"]/ul/li[1]/span[@class="sp2"]/text()').get()
            item['area'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="short-detail-wrap"]/ul/li[2]/span[@class="sp2"]/text()').get()

            # Optional information:

            # item['post_type'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="detail-2 pad-16"]/div[@class="box-round-grey3"]/div[1]/span[2]/text()').get()
            # item['location'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="detail-2 pad-16"]/div[@class="box-round-grey3"]/div[2]/span[2]/text()').get()

            for post_info in land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="detail-2 pad-16"]/div[@class="box-round-grey3"]/div'):
                post_name = post_info.xpath('./span[1]/text()').get()
                post_content = post_info.xpath('./span[2]/text()').get()

                if post_name == 'Loại tin đăng:':
                    item['post_type'] = post_content
                elif post_name == 'Địa chỉ:':
                    item['location'] = post_content
                elif post_name == 'Mặt tiền:':
                    item['facade'] = post_content
                elif post_name == 'Đường vào:':
                    item['entrance'] = post_content
                elif post_name == 'Pháp lý:':
                    item['policy'] = post_content
                elif post_name == 'Hướng nhà:':
                    item['orientation'] = post_content
                elif post_name == 'Hướng ban công:':
                    item['balcony_orientation'] = post_content
                elif post_name == 'Số tầng:':
                    item['number_of_floors'] = post_content
                elif post_name == 'Số phòng ngủ:':
                    item['number_of_bedrooms'] = post_content
                elif post_name == 'Số toilet:':
                    item['number_of_toilets'] = post_content
                elif post_name == 'Nội thất:':
                    item['furniture'] = post_content

            item['posted_author'] = land_item.xpath('./div[@class="main-right"]/div[@class="box-contact"]/div[@class="user"]/div[@class="name"]/text()').get()
            item['phone'] = land_item.xpath('./div[@class="main-right"]/div[@class="box-contact"]/div[@class="user"]/div[@class="phone text-center"]/span').attrib["raw"]

            # Check if existed email:
            email_item =  land_item.xpath('./div[@class="main-right"]/div[@class="box-contact"]/div[@class="user"]/div[@class="mail btn-border-grey text-center"]/a[@id="email"]')

            if email_item.get() is not None:
                item['email'] = email_item.attrib["data-email"]
        
            item['posted_date'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="product-config pad-16"]/ul[@class="short-detail-2 list2 clearfix"]/li[1]/span[@class="sp3"]/text()').get()
            item['expired_date'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="product-config pad-16"]/ul[@class="short-detail-2 list2 clearfix"]/li[2]/span[@class="sp3"]/text()').get()
            item['item_code'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="product-config pad-16"]/ul[@class="short-detail-2 list2 clearfix"]/li[4]/span[@class="sp3"]/text()').get()

            # Latitude & longitude:
            item['latitude'] = response.xpath('//*[@id="product-detail-web"]/div[@class="detail-product"]//div[@class="map"]/iframe/@src').get()

            # crawl image:
            image_urls = []
            for url in land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@class="slide-product"]/div[contains(@class, "swiper-container gallery-top")]/ul/li'):
                image_url = url.xpath('./div[@class="ioverlay"]/img/@src-lazy').get()
                image_urls.append(image_url)

            item['image_urls'] = image_urls
            yield item