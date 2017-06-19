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
class BlogSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'blog'
    redis_key = 'blog:start_urls'

    domain_rule = LinkExtractor(allow=(r'https://s.taobao.com/search?\S+'))

    # rules = (
    #     # follow all links
    #     Rule(domain_rule, callback='parse_page', follow=True),
    # )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        print("***********************************************************8")
        for i in self.allowed_domains:
            print(i)
        #print(domain)
        #self.allowed_domains = filter(None, domain.split(','))
        super(BlogSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield Request(url=response.url, callback=self.parse_page)

    def parse_page(self, response):
        a_list = response.xpath(
            "//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        # print("href:%s num:%d" % (response.url, len(a_list)))
        for a in a_list:
            item_href = ''.join(a.xpath("./@href").extract()).strip()
            item_text = ''.join(a.xpath("./text()").extract()).strip()
            domain = item_href.split('/')[2]
            #print("domain:%s"%(domain))
            flag = 0
            for i in self.allowed_domains:
                if i not in domain:
                    flag = 1
                    break
            if flag==1:
                # print("该url不在域名内")
                continue

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


    def parse_acticle(self, url):
        # print("parse_acticle:"+response.url)
        html = get_html(url)
        title = get_title(html)
        time = get_time_by_url(url)
        keywords = get_keywords(html)
        content = extract_content(html)
        url_num = len(get_all_url(html))

        flag = is_acricle_page_by_allinfo(html,url,title,time,keywords,content,url_num)

        if flag:
            print("parse successful......%s"%(url))
            item = Blog()
            item['url'] = str(url)
            item['title'] = str(title)
            item['time'] = str(time)
            item['keywords'] = str(keywords)
            item['acticle'] = str(content)
            item['taskid'] = str(self.name)
            yield item
            #print(item)
            #yield Request(url=response.url, callback=self.parse_page)
        # else:
        #     print("parse failure......%s" % (response.url))
        #     yield Request(url=response.url, callback=self.parse_page)

