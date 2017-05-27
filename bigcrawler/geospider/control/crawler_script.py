# This snippet can be used to run scrapy spiders independent of scrapyd or the scrapy command line tool and use it from a script.
#
# The multiprocessing library is used in order to work around a bug in Twisted, in which you cannot restart an already running reactor or in this case a scrapy instance.
#
# [Here](http://groups.google.com/group/scrapy-users/browse_thread/thread/f332fc5b749d401a) is the mailing-list discussion for this snippet.

# !/usr/bin/python
import os

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'gewspider.settings')  # Must be at the top before other imports

import logging
from scrapy import signals, project
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue


class CrawlerScript():
    def __init__(self):
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'geospider'):
            self.crawler.install()
        self.crawler.configure()
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _item_passed(self, item):
        self.items.append(item)

    def _crawl(self, queue, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        if spider:
            self.crawler.queue.append_spider(spider)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)

    def crawl(self, spider):
        queue = Queue()
        p = Process(target=self._crawl, args=(queue, spider,))
        p.start()
        p.join()
        return queue.get(True)


# Usage
if __name__ == "__main__":

    """
    This example runs spider1 and then spider2 three times. 
    """
    items = list()
    crawler = CrawlerScript()
    items.append(crawler.crawl('news'))

    print items