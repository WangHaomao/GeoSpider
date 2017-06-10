from scrapy import Request
from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'test'
    redis_key = 'myspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = ['sohu.com']#filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        a_list = response.xpath(
            "//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        for a in a_list:
            href = ''.join(a.xpath("./@href").extract()).strip()
            text = ''.join(a.xpath("./text()").extract()).strip()
            print (href+" "+text)
            #yield Request(url=href, callback=self.parse)
