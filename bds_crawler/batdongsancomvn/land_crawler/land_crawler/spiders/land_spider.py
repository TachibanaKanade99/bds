import scrapy
from land_crawler.items import LandCrawlerItem

class LandSpider(scrapy.Spider):
    name = "land_spider"
    allowed_domains = ['batdongsan.com.vn']

    start_urls = [
        'https://batdongsan.com.vn/ban-dat-dat-nen-tp-hcm/-1/n-30000/-1/-1',
    ]

    def parse(self, response):
        for item in response.xpath('//div[@id="product-lists-web"]/div[contains(@class, "product-item clearfix")]'):
            item_url = "https://batdongsan.com.vn" + item.xpath('./a').attrib["href"]
            yield scrapy.Request(item_url, callback=self.parse_item, cb_kwargs=dict(url=item_url))

        # next page
        # next_page = response.xpath('//div[@class="pagination"]/a[@class="actived"]/following-sibling::*').attrib["href"]

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response, url):
        item = LandCrawlerItem()

        for land_item in response.xpath('//div[@class="form-content"]/div[contains(@class, "main-container clearfix")]'):
            item['url'] = url
            item['content'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/h1[@class="tile-product"]/text()').get()
            item['price'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="short-detail-wrap"]/ul/li[1]/span[@class="sp2"]/text()').get()
            item['area'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="short-detail-wrap"]/ul/li[2]/span[@class="sp2"]/text()').get()
            item['location'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="detail-2 pad-16"]/div[@class="box-round-grey3"]/div[2]/span[2]/text()').get()
            item['posted_author'] = land_item.xpath('./div[@class="main-right"]/div[@class="box-contact"]/div[@class="user"]/div[@class="name"]/text()').get()
            item['phone'] = land_item.xpath('./div[@class="main-right"]/div[@class="box-contact"]/div[@class="user"]/div[@class="phone text-center"]/span/text()').get()
            item['posted_date'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="product-config pad-16"]/ul[@class="short-detail-2 list2 clearfix"]/li[1]/span[@class="sp3"]/text()').get()
            item['expired_date'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="product-config pad-16"]/ul[@class="short-detail-2 list2 clearfix"]/li[2]/span[@class="sp3"]/text()').get()
            item['item_code'] = land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@id="product-detail-web"]/div[@class="detail-product"]/div[@class="product-config pad-16"]/ul[@class="short-detail-2 list2 clearfix"]/li[4]/span[@class="sp3"]/text()').get()

            # crawl image:
            image_urls = []
            for url in land_item.xpath('./div[@class="main-left"]/section[@class="product-detail"]/div[@class="slide-product"]/div[@class="swiper-container gallery-top"]/ul/li'):
                image_url = url.xpath('./div[@class="ioverlay"]/img/@src-lazy').get()
                image_urls.append(image_url)

            item['image_urls'] = image_urls
            yield item