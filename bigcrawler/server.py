# -*- encoding: utf-8 -*-
import redis

rc = redis.Redis(host='127.0.0.1')

ps = rc.pubsub()

ps.subscribe(['crawler'])  #订阅两个频道，分别是foo，或bar

for item in ps.listen():

    if item['type'] == 'message':
        print item['data']