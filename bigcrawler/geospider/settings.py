SPIDER_MODULES = ['geospider.spiders']
NEWSPIDER_MODULE = 'geospider.spiders'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Default requests serializer is pickle, but it can be changed to any module
# with loads and dumps functions. Note that pickle is not compatible between
# python versions.
# Caveat: In python 3.x, the serializer must return strings keys and support
# bytes as values. Because of this reason the json or msgpack module will not
# work by default. In python 2.x there is no such issue and you can use
# 'json' or 'msgpack' as serializers.
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# Don't cleanup redis queues, allows to pause/resume crawls.
#SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# Alternative queues.
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).
#SCHEDULER_IDLE_BEFORE_CLOSE = 10

# Store scraped item in redis for post-processing.
ITEM_PIPELINES = {
    #'spiderController.pipelines.ExamplePipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
    'geospider.mongodb_pipelines.MongoDBPipeline': 400,
}

DOWNLOADER_MIDDLEWARES = {
#    'cnblogs.middlewares.MyCustomDownloaderMiddleware': 543,
#     'spiderController.middlewares.RandomUserAgent': 1,
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#     #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#     'spiderController.middlewares.ProxyMiddleware': 100,
}

# The item pipeline serializes and stores the items in this redis key.
#REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '192.168.1.114'
REDIS_PORT = 6379
SUBSCRIBE = 'crawler'

LOCAL_HOST = '192.168.1.114'

# mongodb
# MONGODB_HOST = '127.0.0.1'
# MONGODB_PORT = 27017
# MONGODB_DBNAME = 'youhuan'
# MONGODB_DOCNAME = 'test'
MONGO_URI = 'mongodb://192.168.1.114:27017/'
MONGO_DATABASE = 'geospider'
MONGO_COLLECTION = 'news'

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
#REDIS_URL = 'redis://user:pass@hostname:9001'

# Custom redis client parameters (i.e.: socket timeout, etc.)
#REDIS_PARAMS  = {}
# Use custom redis client class.
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

# If True, it uses redis' ``SPOP`` operation. You have to use the ``SADD``
# command to add URLs to the redis queue. This could be useful if you
# want to avoid duplicates in your start urls list and the order of
# processing does not matter.
#REDIS_START_URLS_AS_SET = False

# Default start urls key for RedisSpider and RedisCrawlSpider.
#REDIS_START_URLS_KEY = '%(name)s:start_urls'

# Use other encoding than utf-8 for redis.
#REDIS_ENCODING = 'latin1'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

LOG_LEVEL= 'DEBUG'

# LOG_FILE ='log.txt'

# PROXIES = [
#     {'ip_port': '175.163.236.167:80', 'user_pass': ''},
#     {'ip_port': '121.204.165.247:8118', 'user_pass': ''},
#     {'ip_port': '125.89.39.191:8118', 'user_pass': ''},
#     {'ip_port': '116.211.143.11:80', 'user_pass': ''},
#     {'ip_port': '60.178.87.10:808', 'user_pass': ''},
#     {'ip_port': '180.170.102.218:8118', 'user_pass': ''},
#     {'ip_port': '60.21.132.218:63000', 'user_pass': ''},
#     {'ip_port': '114.230.41.127:808', 'user_pass': ''},
#     {'ip_port': '218.4.101.130:83', 'user_pass': ''},
#     {'ip_port': '49.86.62.162:808', 'user_pass': ''},
#     {'ip_port': '122.228.179.178:80', 'user_pass': ''},
#     {'ip_port': '183.78.183.156:82', 'user_pass': ''}
# ]

# REDIS_START_URLS_KEY = '%(name):start_urls'
# REDIS_REQUESTS_KEY='%(name):requests'
# REDIS_DUPEFILTER_KEY='%(name):dupefilter'
