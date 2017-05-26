# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class ShopMainSpider(scrapy.Spider):
    name = "shopspider"
    # allowed_domains = ["https://www.baidu.com"]
    start_urls = [  'http://www.dangdang.com/',
                    'https://taobao.com',]

    def parse(self, response):
        print response.url
        soup = BeautifulSoup(response.text,"lxml")
        print soup.find_all("a")

