# -*- coding: utf-8 -*-
import scrapy


class ModeSpider(scrapy.Spider):
    name = "mode"
    allowed_domains = ["https://www.baidu.com"]
    start_urls = ['http://www.baidu.com/']
    # level 1 一般是首页
    def parse(self, response):
        pass
