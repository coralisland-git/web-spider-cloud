# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):

	ministry_reference_number = Field()

	ebr_registry_number = Field()

	company_name = Field()

	instrument_type = Field()
	
	notice_type = Field()

	notice_date = Field()

	proposal_date = Field()

	proposal_address = Field()

	related_locations = Field()

