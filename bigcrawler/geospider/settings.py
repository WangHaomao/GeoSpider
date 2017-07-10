SPIDER_MODULES = ['geospider.spiders']
NEWSPIDER_MODULE = 'geospider.spiders'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

ITEM_PIPELINES = {
    #'spiderController.pipelines.ExamplePipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
    'geospider.mongodb_pipelines.MongoDBPipeline': 400,
}

DOWNLOADER_MIDDLEWARES = {
      'geospider.middlewares.RotateUserAgentMiddleware':123
}

REDIS_HOST = '192.168.1.130'
REDIS_PORT = 6379
SUBSCRIBE = 'crawler'

LOCAL_HOST = '192.168.1.130'

# STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'
STATS_CLASS = 'geospider.statscol.graphite.RedisGraphiteStatsCollector'
GRAPHITE_HOST = '123.207.230.48'
GRAPHITE_PORT = 2003
MONGO_URI = 'mongodb://192.168.1.130/'
MONGO_DATABASE = 'geospider'
MONGO_COLLECTION = 'news'
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

LOG_LEVEL= 'DEBUG'
import logging
logging.getLogger('cluster.matrix').setLevel(logging.WARNING)
logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)
