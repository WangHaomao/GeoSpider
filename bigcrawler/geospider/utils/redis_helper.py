# -*- encoding: utf-8 -*-
import redis

def connect_redis():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return r

class URLManager(object):
    def __init__(self, redis):
        self.redis = redis

    def delete_task(self, taskid):
        self.redis.delete(taskid+":requests")
        self.redis.delete(taskid + ":start_urls")
        self.redis.delete(taskid + ":dupefilter")

    def insert_url(self, taskid, url):
        self.redis.lpush(taskid + ":start_urls", url)