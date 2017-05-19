# # Scrapy settings for example project
# #
# # For simplicity, this file contains only the most important settings by
# # default. All the other settings are documented here:
# #
# #     http://doc.scrapy.org/topics/settings.html
# #
# SPIDER_MODULES = ['example.spiders']
# NEWSPIDER_MODULE = 'example.spiders'
#
# USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'
#
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = True
# #SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# #SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# #SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
#
# ITEM_PIPELINES = {
#     'example.pipelines.ExamplePipeline': 300,
#     'scrapy_redis.pipelines.RedisPipeline': 400,
# }
#
# LOG_LEVEL = 'DEBUG'
#
# # Introduce an artifical delay to make use of parallelism. to speed up the
# # crawl.
# DOWNLOAD_DELAY = 1



SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

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
    #'example.pipelines.ExamplePipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
    'example.mongodb_pipelines.MongoDBPipeline': 400,
}

# DOWNLOADER_MIDDLEWARES = {
# #    'cnblogs.middlewares.MyCustomDownloaderMiddleware': 543,
#     'example.middlewares.RandomUserAgent': 1,
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#     #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#     'example.middlewares.ProxyMiddleware': 100,
# }

# The item pipeline serializes and stores the items in this redis key.
#REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# mongodb
# MONGODB_HOST = '127.0.0.1'
# MONGODB_PORT = 27017
# MONGODB_DBNAME = 'youhuan'
# MONGODB_DOCNAME = 'test'
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'news'
MONGO_COLLECTION = 't_news4'

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

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

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