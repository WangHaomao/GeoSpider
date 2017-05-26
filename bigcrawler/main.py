# -*- encoding: utf-8 -*-
from scrapy import cmdline
import redis

# activate_this = '/home/kui/work/python/env/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
# r = redis.Redis(host='127.0.0.1', port=6379, db=0)
# r.lpush('myspider:start_urls', 'http://news.sohu.com/')   #添加
# cmdline.execute("scrapy crawl news".split())

def add():
	return 'aaa'

# redis-cli lpush myspider:start_urls http://google.com
