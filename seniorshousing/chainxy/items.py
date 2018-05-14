# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):

    CompanyName = Field()

    FirstName = Field()

    LastName = Field()

    City = Field()

    State = Field()

    WebSite = Field()

    Link = Field()