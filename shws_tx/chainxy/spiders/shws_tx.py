# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from lxml import etree

from lxml import html

import pdb

class shws_tx(scrapy.Spider):

	name = 'shws_tx'

	domain = 'https://www.tceq.texas.gov'

	history = []

	def __init__(self):
		pass
	
	# start scraper

	def start_requests(self):

		init_url  = 'https://www.tceq.texas.gov/remediation/superfund/state/'

		yield scrapy.Request(init_url, callback=self.parse_state)		

	
	def parse_state(self, response):

		state_list = response.xpath('//div[@class="entries"]//article[@class="entry"]//a[contains(@class, "state-published")]/@href').extract()

		for state in state_list:

			yield scrapy.Request(state, callback=self.parse_related_list, dont_filter=True)

		try:

			next_bt = response.xpath('//ul[@class="pagination"]//li[@class="next"]//a/@href').extract_first()

			if next_bt:

				yield scrapy.Request(next_bt, callback=self.parse_state, dont_filter=True)
		except:

			pass


	def parse_related_list(self, response):

		related_list = response.xpath('//ul[@class="visualNoMarker"]//a/@href').extract()

		for related in related_list:

			yield scrapy.Request(related, callback=self.parse_topic_list, dont_filter=True)


	def parse_topic_list(self, response):

		topic_list = response.xpath('//div[@id="topics"]//div[@class="topic"]//a/@href').extract()

		for topic in topic_list:

			yield scrapy.Request(topic, callback=self.parse_detail, dont_filter=True)


	def parse_detail(self, response):

		item = ChainItem()

		detail = self.eliminate_space(response.xpath('//section[@class="portletContent"]//text()').extract())

		item['facility_name'] = ' '.join(self.eliminate_space(response.xpath('//h1[@class="documentFirstHeading"]//text()').extract()))

		item['status'] = ' '.join(self.eliminate_space(response.xpath('//div[@class="documentDescription description"]//text()').extract()))

		item['type_of_facility'] = self.get_value('type of facility', detail)

		item['site_link'] = response.url

		item['location'] = self.get_value('location', detail)

		item['latitude'] = self.get_value('latitude', detail)

		item['longitude'] = self.get_value('longitude', detail)

		item['site_phase'] = self.get_value('site phase', detail)

		item['hazard_ranking_score'] = self.get_value('hazard ranking score', detail)

		item['contaminants'] = self.get_value('contaminants at time of hrs', detail)

		item['state_superfund_registry_status'] = self.get_value('state superfund registry status', detail)

		item['media_affected'] = self.get_value('media affected', detail)

		item['tceq_region'] = self.get_value('tceq region', detail)

		item['funded_by'] = self.get_value('funded by', detail)

		item['contacts'] = self.get_value_bulk('contact information', 'superfund program contact', detail)

		item['records_repositories'] = self.get_value_bulk('young branch library', 'tceq central file room', detail)

		item['tceq_central_file_room'] = self.get_value_bulk('tceq central file room', 'end', detail)

		item['site_details'] = ' '.join(response.xpath('//div[@id="parent-fieldname-text"]//text()').extract())

		if item['facility_name']+item['site_link'] not in self.history:

			self.history.append(item['facility_name']+item['site_link'])

			yield item


	def validate(self, item):

		try:

			return item.strip().replace('\n', '').replace('\t','').replace('\r', '').replace(':', '')

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp


	def get_value(self, arg, items):

		val = ''

		for ind in range(0, len(items)):

			if arg.lower() in items[ind].lower():

				try:

					val = items[ind+1]

				except:

					pass

		return val


	def get_value_bulk(self, arg1, arg2, items):

		val = ''

		index = 0

		for ind in range(0, len(items)):

			if arg1.lower() in items[ind].lower():

				try:

					index = ind

					break

				except:

					pass

		if arg2 == 'end':

			for ind in range(index, len(items)):

				val += items[ind] + ' '

		else:

			for ind in range(index, len(items)):

				if arg2.lower() in items[ind].lower():

					try:

						break
					
					except:

						pass

				else :

					val += items[ind] + ' '

		return val

