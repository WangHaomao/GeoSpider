# -*- encoding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from example.items import Profile
import re
from scrapy.dupefilters import RFPDupeFilter
from scrapy.spiders import CrawlSpider,Rule
from scrapy_redis.spiders import RedisCrawlSpider

class YouyuanSpider(RedisCrawlSpider):
    name = 'youyuan'
    #allowed_domains = ['youyuan.com']
    redis_key = 'myspider:start_urls'
    # 有缘网的列表页
    #start_urls = ['http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1/']
    pattern = re.compile(r'[0-9]')

    # 提取列表页和Profile资料页的链接形成新的request保存到redis中等待调度
    profile_page_lx = LinkExtractor(allow=('http://www.youyuan.com/\d+-profile/'))

    page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p\d+/'))

    rules = (

        Rule(page_lx, callback='parse_list_page', follow=True),
        Rule(profile_page_lx, callback='parse_profile_page', follow=False),

    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(YouyuanSpider, self).__init__(*args, **kwargs)

    # 处理列表页，其实完全不用的，就是留个函数debug方便
    def parse_list_page(self, response):
        print "Processed  list %s" % (response.url,)
        #print response.body
        self.profile_page_lx.extract_links(response)

        pass

    # 处理Profile资料页，得到我们要的Profile
    def parse_profile_page(self, response):
        print "Processing profile %s" % response.url

        profile = Profile()
        profile['header_url'] = self.get_header_url(response)
        profile['username'] = self.get_username(response)
        profile['monologue'] = self.get_monologue(response)
        profile['pic_urls'] = self.get_pic_urls(response)
        profile['age'] = self.get_age(response)
        profile['source'] = 'youyuan'
        profile['source_url'] = response.url

        #print "Processed profile %s" % response.url

        yield profile


    # 提取头像地址
    def get_header_url(self, response):
        header = response.xpath('//dl[@class="personal_cen"]/dt/img/@src').extract()
        if len(header) > 0:
            header_url = header[0]
        else:
            header_url = ""
        return header_url.strip()

    # 提取用户名
    def get_username(self, response):
        usernames = response.xpath('//dl[@class="personal_cen"]/dd/div/strong/text()').extract()
        if len(usernames) > 0:
            username = usernames[0]
        else:
            username = ""
        return username.strip()

    # 提取内心独白
    def get_monologue(self, response):
        monologues = response.xpath('//ul[@class="requre"]/li/p/text()').extract()
        if len(monologues) > 0:
            monologue = monologues[0]
        else:
            monologue = ""
        return monologue.strip()

    # 提取相册图片地址
    def get_pic_urls(self, response):
        pic_urls = []
        data_url_full = response.xpath('//li[@class="smallPhoto"]/@data_url_full').extract()
        if len(data_url_full) <= 1:
            pic_urls.append("");
        else:
            for pic_url in data_url_full:
                pic_urls.append(pic_url)

        if len(pic_urls) <= 1:
            return ""
        return '|'.join(pic_urls)

    # 提取年龄
    def get_age(self, response):
        age_urls = response.xpath('//dl[@class="personal_cen"]/dd/p[@class="local"]/text()').extract()
        if len(age_urls) > 0:
            age = age_urls[0]
        else:
            age = ""

        age_words = re.split(' ', age)
        if len(age_words) <= 2:
            return "0"
        #20岁
        age = age_words[2][:-1]
        if self.pattern.match(age):
            return age
        return "0"