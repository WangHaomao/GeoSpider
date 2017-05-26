# -*- encoding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import Request
from spiderController.news.model import *
from spiderController.items import News
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class NewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'news'
    redis_key = 'myspider:start_urls'
    allowed_domains = ['news.qq.com']

    # rules = (
    #     # follow all links
    #     Rule(LinkExtractor(), callback='parse', follow=True),
    # )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        a_list = response.xpath("//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        dict = {}
        for a in a_list:
            key_href = ''.join(a.xpath("./@href").extract()).strip()
            dict[key_href] = ''.join(a.xpath("./text()").extract()).strip()
        for k, v in dict.items():
            #5为一个阈值，当value小于5时为导航页，当value大于5时视为新闻详情页
            if len(v) <= 5:
                yield Request(url=k, callback=self.parse)
            else:
                yield Request(url=k, callback=self.parse_detail)

    def parse_item_url(self, response):
        pass

    def parse_detail(self, response):
        ctthtml = getcontentfromweb(response.url)
        soup = filter_tags(ctthtml)
        soup2 = filter_ul_tags(soup)
        title = gettitle(soup)
        time = gettime(soup)
        keywords = getkeywords(soup)
        origin_content = get_origin_content(soup2)
        content = getcontent1(origin_content)
        if len(content) < 10 or content is None:
            origin_content = get_origin_content(soup)
            content = getcontent1(origin_content)
        if content is not None and content != '' and time is not None and title != '' and title is not None:
            # print content
            item = News()
            item['url'] = str(response.url).encode("utf-8")
            item['title'] = str(title).encode("utf-8")
            item['time'] = str(time).encode("utf-8")
            item['keywords'] = str(keywords).encode('utf-8')
            item['acticle'] = str(content).decode("utf-8")
            yield item
        yield Request(url=response.url, callback=self.parse)
