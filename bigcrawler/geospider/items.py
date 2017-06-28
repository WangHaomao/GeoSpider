# -*- encoding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import pymongo

class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()

class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()

class Cloth(Item):
    title = Field()
    link = Field()
    price = Field()
    comment = Field()
    original_price = Field()
    referer = Field()

class News(Item):
    title = Field()
    keywords = Field()
    time = Field()
    article = Field()
    url = Field()
    taskid = Field()

class Blog(Item):
    title = Field()
    keywords = Field()
    time = Field()
    article = Field()
    url = Field()
    taskid = Field()

# class ShopItem(Item):
#     navbar = Field()

class ECommerceSiteCrawlerItem(Item):
    pass


