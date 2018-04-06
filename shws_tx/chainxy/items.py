# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
	facility_name = Field()
	status = Field()
	type_of_facility = Field()
	site_link = Field()
	location = Field()
	latitude = Field()
	longitude = Field()
	site_phase = Field()
	hazard_ranking_score = Field()
	contaminants = Field()
	state_superfund_registry_status = Field()
	media_affected = Field()
	tceq_region = Field()
	funded_by = Field()
	contacts = Field()
	records_repositories = Field()
	tceq_central_file_room = Field()
	site_details = Field()
	

