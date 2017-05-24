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

class Profile(Item):
    # 提取头像地址
    header_url = Field()
    # 提取相册图片地址
    pic_urls = Field()

    username = Field()
    # 提取内心独白
    monologue = Field()
    age = Field()
    # youyuan
    source = Field()
    source_url = Field()

    crawled = Field()
    spider = Field()

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
    acticle = Field()
    url = Field()

# class ShopItem(Item):
#     navbar = Field()



