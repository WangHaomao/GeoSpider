#-*- encoding: utf-8 -*-
import redis
from copy import deepcopy
from scrapy import cmdline, crawler

from geospider.control.spider_controller import SpiderController
from geospider.spiders.news_spider import NewsSpider
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017')
db_name = 'news'
db = client[db_name]


def start():
    #conn_table = db['task']
    #print conn_table.find_one({'_id': ObjectId('591eb2df9c1da9154b001832')}).get('starturls')

    b = deepcopy(NewsSpider)
    b.name='bbb'
    b.redis_key = "start_urls"
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # r.sadd("myspider:start_urls", 'http://news.qq.com/')
    r.lpush("start_urls", 'http://news.sohu.com/')
    r.lpush("start_urls", "http://news.qq.com/")
    cmdline.execute("scrapy crawl bbb".split())

    # process = CrawlerProcess(get_project_settings())
    # process.crawl(news_spider)
    # process.start()  # the script will block here until the crawling is finished

def pause():
    cmdline.execute("".split())

if __name__ == '__main__':
    start()

