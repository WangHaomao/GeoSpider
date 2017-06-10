# -*- encoding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from geospider.news.arcticle_parser import *
from geospider.items import News

import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
class NewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'news'
    redis_key = 'news:start_urls'

    # rules = (
    #     # follow all links
    #     Rule(LinkExtractor(), callback='parse', follow=True),
    # )
    allowed_domains = [
        'news.sohu.com'
    ]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        print("***********************************************************8")
        #print(domain)
        #self.allowed_domains = filter(None, domain.split(','))
        super(NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield Request(url=response.url, callback=self.parse_page)

    def parse_page(self, response):
        a_list = response.xpath(
            "//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        #print("href:%s num:%d" % (response.url, len(a_list)))
        for a in a_list:
            item_href = ''.join(a.xpath("./@href").extract()).strip()
            item_text = ''.join(a.xpath("./text()").extract()).strip()
            # for k, v in dict.items():
            # 5为一个阈值，当value小于5时为导航页，当value大于5时视为新闻详情页
            #print("parse_page:%s %s" % (item_text, item_href))
            flag = is_acricle_page_by_url_and_text(item_href, item_text)
            if flag:
                # print("b:"+item_text+" "+item_href)
                yield Request(url=item_href, callback=self.parse_acticle)
            else:
                # print("a:"+item_text+" "+item_href)
                yield Request(url=item_href, callback=self.parse_page)


    def parse_acticle(self, response):
        print("parse_acticle:"+response.url)
        html = get_html(response.url)
        origin_content = filter_tags(html, True)
        title = get_title(html)
        time = get_time_by_url(response.url)
        keywords = get_keywords(html)
        content = get_content(origin_content)
        url_num = len(get_all_url(html))

        flag = is_acricle_page_by_allinfo(html,title,time,keywords,content,url_num)

        if flag:
            print("parse successful......%s"%(response.url))
            item = News()
            item['url'] = str(response.url)
            item['title'] = str(title)
            item['time'] = str(time)
            item['keywords'] = str(keywords)
            item['acticle'] = str(content)
            item['taskid'] = str(self.name)
            yield item
            yield Request(url=response.url, callback=self.parse_page)
        else:
            print("parse failure......%s" % (response.url))
            yield Request(url=response.url, callback=self.parse_page)

