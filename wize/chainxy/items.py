# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
	well_id = Field()
	well_depth = Field()
	well_yield = Field()
	use_type = Field()
	contractor_name = Field()
	contractor_number = Field()
	driller_name = Field()
	driller_number = Field()
	pump_installer_name = Field()
	pump_installer_number = Field()
	date_well_completed = Field()
	country = Field()
	fraction = Field()
	section = Field()
	township = Field()
	range = Field()
	longitude = Field()
	latitude = Field()
