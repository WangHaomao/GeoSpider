# -*- encoding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import Request
from geospider.news.news_parser_old import *
from geospider.items import News
import sys
class ShopSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'shopspider'
    redis_key = 'myspider:start_urls'
    # allowed_domains = ['news.qq.com']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ShopSpider, self).__init__(*args, **kwargs)

    # 解析首页,获取navbar
    def parse(self, response):
        pass



