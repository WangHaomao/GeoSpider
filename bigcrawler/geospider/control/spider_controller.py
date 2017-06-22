#-*- encoding: utf-8 -*-
import redis
from copy import deepcopy

import time
from bson import ObjectId
from scrapy import cmdline
import pymongo

from geospider.spiders.news_spider import NewsSpider
from geospider.utils.mongodb_helper import connect_mongodb, TaskDao
from geospider.utils.time_util import compare_time


def init(taskid):
    # client = pymongo.MongoClient('mongodb://localhost:27017')
    # db_name = 'news'
    # db = client[db_name]
    # task = db.task.find_one({'_id': ObjectId(taskid)})
    # client.close()

    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    task = taskdao.find_by_id(taskid)

    temp = None
    if "news"==task['webtype']:
        temp = deepcopy(NewsSpider)
        temp.name = taskid
        temp.redis_key = taskid+":start_urls"

    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    allowed_domains = []
    for url in task['starturls']:
        r.lpush(taskid+":start_urls", url)
        allowed_domains.append(url.split('/')[2])
    temp.allowed_domains = allowed_domains



def run(taskid):
    cmdline.execute(("scrapy crawl "+taskid).split())

def wait(taskid):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db_name = 'news'
    db = client[db_name]
    task = db.task.find_one({'_id': ObjectId(taskid)})
    starttime = task['starttime']
    endtime = task['endtime']
    client.close()
    flag = False
    while(flag is False):
        flag = compare_time(time.strftime("%Y/%m/%d %H:%M"), starttime, endtime)
        time.sleep(60)
    if flag is True:
        task['status'] = 'running'
        db.task.save(task)
        run(taskid)



def delete(taskid):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.delete(taskid+":requests")
    r.delete(taskid + ":start_urls")
    r.delete(taskid + ":dupefilter")

    client = pymongo.MongoClient('mongodb://localhost:27017')
    db_name = 'news'
    db = client[db_name]
    task = db.task.find_one({'_id': ObjectId(taskid)})

    endtime = time.strftime("%Y/%m/%d %H:%M")
    task['endtime']=endtime
    db.task.save(task)
    client.close()



def scan():
    pass
