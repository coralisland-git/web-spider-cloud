# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):

    Folio = Field()

    Pin = Field()

    Owner = Field()

    Owner_Addr = Field()

    Owner_City = Field()

    Owner_State = Field()

    Owner_Zip = Field()

    Site_Addr = Field()

    Site_City = Field()

    Site_State = Field()

    Site_Zip = Field()

    Bed = Field()

    Bath = Field()

    Square_Footage = Field()

    Zestimate = Field()

    Active = Field()

    Icomps = Field()

    Redfin = Field()

    Trulia = Field()