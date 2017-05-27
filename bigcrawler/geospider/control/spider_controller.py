#-*- encoding: utf-8 -*-
import redis
from copy import deepcopy

from bson import ObjectId
from scrapy import cmdline
import pymongo

from geospider.spiders.news_spider import NewsSpider


def init(taskid, type):
    temp = None
    if "news"==type:
        temp = deepcopy(NewsSpider)
        temp.name = taskid
        temp.redis_key = taskid+":start_urls"

    client = pymongo.MongoClient('mongodb://localhost:27017')
    db_name = 'news'
    db = client[db_name]
    task = db.task.find_one({'_id': ObjectId(taskid)})
    client.close()

    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    for url in task['starturls']:
        r.lpush(taskid+":start_urls", url)


def run(taskid):
    cmdline.execute(("scrapy crawl "+taskid).split())

def delete(taskid):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.delete(taskid+":requests")