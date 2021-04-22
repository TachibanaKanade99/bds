# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random

# Selenium:
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

from scrapy.http.response.html import HtmlResponse
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import socket
import socks
import time
from stem import Signal
from stem.control import Controller

class LandCrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LandCrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumDownloaderMiddleware:

    # Scrapy middleware for handling the requests using Selenium:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options = EdgeOptions()
        # options.use_chromnium = True
        # options.add_argument('headless')
        # options.add_argument('window-size=1200x600')
        options.add_argument('no-sandbox')
        options.add_argument('no-default-browser-check')
        options.add_argument('disable-gpu')
        options.add_argument('disable-default-apps')
        options.add_argument('disable-extensions')
        options.add_argument('incognito')

        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')
        
        # window chrome web driver:
        self.driver = webdriver.Chrome('D:\\Tuan_Minh\\bds\\bds_crawler\\batdongsancomvn\\chromedriver.exe', options=options)

        # linux chrome webdriver:
        # self.driver = webdriver.Chrome('/media/tuanminh/DATA/Tuan_Minh/bds/bds_crawler/batdongsancomvn/chromedriver_linux', options=options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})

        # self.driver = Edge('D:\\Tuan_Minh\\bds\\bds_crawler\\batdongsancomvn\\msedgedriver.exe', options=options)
        # self.driver.minimize_window()

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware
        
    
    def process_request(self, request, spider):
        if not request.meta.get('selenium', False):
            return request

        self.driver.get(request.url)
        self.driver.implicitly_wait(random.uniform(1.0, 3.0))
        # map_locator = self.driver.find_element(By.XPATH, '//*[@id="product-detail-web"]/div[@class="detail-product"]//div[@class="map"]/iframe/@src')
        # WebDriverWait(self.driver, timeout=5).until(expected_conditions.visibility_of_element_located(map_locator))

        body = str.encode(self.driver.page_source)
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8')

    def spider_closed(self):
        # Shutdown driver when spider closed:
        self.driver.quit()


def new_tor_identity():
    with Controller.from_port(port=9151) as controller:
        controller.authenticate(password='361975Warcraft')
        controller.signal(Signal.NEWNYM)

class ProxyMiddleware(HttpProxyMiddleware):
    def process_response(self, request, response, spider):
        # Get a new identity depending on the response
        if response.status != 200:
            new_tor_identity()
            return request
        return response

    def process_request(self, request, spider):
        # Set the Proxy
        # A new identity for each request
        # Comment out if you want to get a new Identity only through process_response
        new_tor_identity()
        request.meta['proxy'] = 'http://127.0.0.1:8118'