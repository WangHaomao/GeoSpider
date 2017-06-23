# -*- encoding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from geospider.blog.blog_parser import *
from geospider.items import Blog
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from geospider.blog.extract_content import extract_content

from scrapy_redis.spiders import RedisCrawlSpider

import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
from geospider.utils.url_util import is_articel_content_page_blog_and_news


class BlogSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'blog'
    redis_key = 'blog:start_urls'

    # rules = (
    #     # follow all links
    #     Rule(domain_rule, callback='parse_page', follow=True),
    # )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        print("***********************************************************")
        #print(domain)
        #self.allowed_domains = filter(None, domain.split(','))
        # self.allowed_domains=['blog.sina.com.cn']
        super(BlogSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield Request(url=response.url, callback=self.parse_page)

    def parse_page(self, response):
        a_list = response.xpath(
            "//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        #print("href:%s num:%d" % (response.url, len(a_list)))

        for a in a_list:
            item_href = ''.join(a.xpath("./@href").extract()).strip()
            item_text = ''.join(a.xpath("./text()").extract()).strip()
            domain = item_href.split('/')[2]
            #print("domain:%s"%(domain))
            print("'%s'," % (item_href))
            # for k, v in dict.items():
            # 5为一个阈值，当value小于5时为导航页，当value大于5时视为新闻详情页
            #print("parse_page:%s %s" % (item_text, item_href))
            flag = is_articel_content_page_blog_and_news(item_href)

            if flag:
                print(item_href)
                yield Request(url=item_href, callback=self.parse_acticle)
            else:
                # print("a:"+item_text+" "+item_href)
                yield Request(url=item_href, callback=self.parse_page)

    def parse_acticle(self, response):
        print("parse_acticle:"+response.url)
        html = get_html(response.url)
        title = get_title(html)
        time = get_time_by_html(html)
        keywords = get_keywords(html)
        content = extract_content(html)
        url_num = len(get_all_url(html))

        #flag = is_acricle_page_by_allinfo(html,response.url,title,time,keywords,content,url_num)

        #if flag:
        print("parse successful......%s"%(response.url))
        item = Blog()
        item['url'] = str(response.url)
        item['title'] = str(title)
        item['time'] = str(time)
        item['keywords'] = str(keywords)
        item['acticle'] = str(content)
        item['taskid'] = str(self.name)
        yield item
        #yield Request(url=response.url, callback=self.parse_page)

