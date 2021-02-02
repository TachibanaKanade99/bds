import scrapy
from land_crawler.items import LandCrawlerItem

class LandSpider(scrapy.Spider):
    name = "example_spider"
    allowed_domains = ['batdongsan.com.vn']

    start_urls = [
        'https://batdongsan.com.vn/ban-dat-dat-nen-tp-hcm/-1/n-30000/-1/-1',
    ]

    def parse(self, response):
        item = LandCrawlerItem()
        for land in response.xpath('//div[@id="product-lists-web"]/div[contains(@class, "product-item clearfix")]'):
            item['content'] = land.xpath('./a/div[2]/h3/span/text()').get()
            item['price'] = land.xpath('./a/div[2]/div[1]/span[@class="price"]/text()').get()
            item['area'] = land.xpath('./a/div[2]/div[1]/span[@class="area"]/text()').get()
            item['location'] = land.xpath('./a/div[2]/div[1]/span[@class="location"]/text()').get()
            yield item

        # next page
        next_page = response.xpath('//div[@class="pagination"]/a[@class="actived"]/following-sibling::*').attrib["href"]

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)