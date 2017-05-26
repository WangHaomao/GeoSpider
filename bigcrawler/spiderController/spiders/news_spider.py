from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider

from spiderController.news.model import *
from spiderController.items import News
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class NewsSpider(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'oldnews'
    redis_key = 'myspider:start_urls'
    allowed_domains = ['news.qq.com']

    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        #title, time, keywords, content = run(response.url)
        url_list = []
        url_list.append(response.url)
        for url in url_list:
            ctthtml = None
            try:
                ctthtml = getcontentfromweb(url)
            except:
                continue;
            soup = filter_tags(ctthtml)
            soup2 = filter_ul_tags(soup)
            url_list2 = get_all_url(soup)
            url_list.extend(url_list2)

            title = gettitle(soup)
            # print title
            # print "==========="
            time = gettime(soup)
            # print time
            # print "==========="
            keywords = getkeywords(soup)
            # print keywords
            # print "============"
            origin_content = get_origin_content(soup2)
            content = getcontent1(origin_content)
            # if len(content) < 10 or content is None:
            #     origin_content = get_origin_content(soup)
            #     content = getcontent1(origin_content)
            if content is not None and content != '' and time is not None and title!='' and title is not None:
                # print content
                item = News()
                item['url'] = str(url).encode("utf-8")
                item['title'] = str(title).encode("utf-8")
                item['time'] = str(time).encode("utf-8")
                item['keywords'] = str(keywords).encode('utf-8')
                item['acticle'] = str(content).decode("utf-8")
                yield item
