import pymongo
import logging
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.settings import Settings


class MongoDBPipeline(object):
    def __init__(self):
        self.url = settings['MONGO_URI']
        self.db = settings['MONGO_DATABASE']
        self.col = settings['MONGO_COLLECTION']
        connection = pymongo.MongoClient(self.url)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if not data:
                err_msg += 'Missing %s of poem from %s\n' % (field, item['url'])
        if err_msg:
            raise DropItem(err_msg)
        self.collection.insert(dict(item))
        logging.debug('Item written to MongoDB database %s/%s' % (self.db, self.col))
        return item