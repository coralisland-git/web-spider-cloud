# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
    sku = Field()
    brand = Field()
    model = Field()
    desc = Field()
    long_desc = Field()
    image = Field()
    price = Field()
    position = Field()
    ori_com = Field()