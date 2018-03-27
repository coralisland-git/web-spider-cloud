# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):

	log_number = Field()

	log_number_link = Field()

	fac_id = Field()

	site_name = Field()

	address = Field()

	city = Field()

	zip_code = Field()

	county = Field()

	summary_information = Field()

	site_name_ = Field()

	received_data = Field()

	address_1 = Field()

	address_2 = Field()

	status = Field()

	tank_type = Field()

	county = Field()

	file_status = Field()

	site_type = Field()

	ust_facility_id = Field()

	project_manager = Field()

	cause_of_release = Field()

	source_of_release = Field()

	discovery_method = Field()

	media_effected = Field()

	contaminants_released = Field()

	delineate_soil = Field()

	ground_water = Field()

	soil_delineated_release = Field()

	stopped_date = Field()

	cleanup_start_date = Field()

	cleanup_end_date = Field()


	work_reported = Field() 

	reported_date = Field()
	

	file_name = Field()

	file_link =	Field()

	category = Field()

	file_size_mb = Field()

	upload_date = Field()


