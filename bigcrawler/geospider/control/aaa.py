#-*- encoding: utf-8 -*-
import redis
from copy import deepcopy

import sys
from scrapy import cmdline

from geospider.spiders.blog_spider import BlogSpider
from geospider.spiders.news_spider import NewsSpider
import pymongo

from geospider.spiders.shop_main_spider import ShopMainSpider

client = pymongo.MongoClient('mongodb://192.168.1.115:27017')
db_name = 'geospider'
db = client[db_name]

def start():
    #conn_table = db['task']
    #print conn_table.find_one({'_id': ObjectId('591eb2df9c1da9154b001832')}).get('starturls')

    b = deepcopy(ShopMainSpider)
    b.name='jd01'
    b.redis_key = "jd01:start_urls"
    r = redis.Redis(host='192.168.1.115', port=6379, db=0)
    # r.sadd("myspider:start_urls", 'http://news.qq.com/')
    r.lpush("jd01:start_urls", "https://www.jd.com/")
    # r.lpush("aaa:start_urls", "http://news.sohu.com/")
    b.allowed_domains=["jd.com"]
    cmdline.execute("scrapy crawl jd01 --nolog".split())

    # process = CrawlerProcess(get_project_settings())
    # process.crawl(news_spider)
    # process.start()  # the script will block here until the crawling is finished

def pause():
    cmdline.execute("".split())

if __name__ == '__main__':
    import os

    # sys.path.append('/opt/graphite/webapp/')
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphite.local_settings")

    start()
    # r = redis.Redis(host='192.168.1.115', port=6379, db=0)
    # # r.sadd("myspider:start_urls", 'http://news.qq.com/')
    # r.lpush("jd01:start_urls", "https://www.jd.com/")
    # project_dir = os.path.dirname(os.path.abspath(__file__))
    # print project_dir
