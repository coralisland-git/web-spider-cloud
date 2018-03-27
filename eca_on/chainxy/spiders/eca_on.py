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

import textract

import pdb

class eca_on(scrapy.Spider):

	name = 'eca_on'

	domain = 'http://www.gisapplication.lrc.gov.on.ca/'

	history = []

	header = {

		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

		"Accept-Encoding":"gzip, deflate, br",

		"Content-Type":"application/x-www-form-urlencoded",

		"Upgrade-Insecure-Requests":"1",

		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
	
	}

	def __init__(self):
		pass
	
	# start scraper

	def start_requests(self):

		init_url  = 'https://www.accessenvironment.ene.gov.on.ca'

		formdata = {

			"username":"public",

			"username1":"public"
		}

		# sign in with credentials into website.
		yield scrapy.Request(url=init_url, callback=self.parse)

		# yield scrapy.FormRequest(url=init_url, callback=self.parse, formdata=formdata, headers=self.header, method="post")

	def parse(self, response):


		pdf = 'https://www.accessenvironment.ene.gov.on.ca/instruments/4505-6EHQZ7-14.pdf'

		text = textract.process(pdf)

		pdb.set_trace()
		# go into lookup_view page

		# yield scrapy.Request(url="https://wise.er.usgs.gov/driller_db/lookup.php?control=lookup_view", callback=self.parse_view)

	def parse_view(self, response):

		# get the country list from the page

		country_list = response.xpath('//select[@name="county_cd"]//option/@value').extract()

		for country in country_list[1:]:

			url = "https://wise.er.usgs.gov/driller_db/match.php"

			formdata = {

				"control":"match_view",

				"county_cd":str(country)
			}
			
			# go into each country page

			yield scrapy.FormRequest(url=url, formdata=formdata, headers=self.header, method="post", callback=self.parse_list)

	def parse_list(self, response):

		# get the list of wells from the page

		loc_list = response.xpath('//table/tr')

		for loc in loc_list[1:]:

			item = ChainItem()

			url = self.domain + loc.xpath('.//a/@href').extract_first()

			item['well_id'] = self.validate(''.join(loc.xpath('.//td[1]//text()').extract()))

			item['well_depth'] = self.validate(''.join(loc.xpath('.//td[3]//text()').extract()))

			item['well_yield'] = self.validate(''.join(loc.xpath('.//td[4]//text()').extract()))

			item['use_type'] = self.validate(''.join(loc.xpath('.//td[5]//text()').extract()))

			item['date_well_completed'] = self.validate(''.join(loc.xpath('.//td[2]//text()').extract()))

			item['date_completed'] = self.validate(''.join(loc.xpath('.//td[2]//text()').extract()))

			item['remarks'] = self.validate(''.join(loc.xpath('.//td[6]//text()').extract()))

			# go into well detail page.

			yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

	def parse_detail(self, response):

		detail = response.xpath('//table//tr//td[@colspan="3"]//tr')

		item = response.meta['item']

		contractor_data = self.eliminate_space(detail[0].xpath('.//text()').extract())

		if len(contractor_data) >3 :

			item['contractor_name'] = contractor_data[3]

			item['contractor_number'] = contractor_data[2]

		driller_data = self.eliminate_space(detail[1].xpath('.//text()').extract())

		if len(driller_data) > 2:

			item['driller_name'] = driller_data[2]

			item['driller_number'] = driller_data[1]

		pump_data = self.eliminate_space(detail[2].xpath('.//text()').extract())

		if len(pump_data) > 2:

			item['pump_installer_name'] = pump_data[2]

			item['pump_installer_number'] = pump_data[1]

		try:
			item['country'] = self.eliminate_space(detail[3].xpath('.//text()').extract())[1]
		except:
			pass

		try:
			item['fraction'] = self.eliminate_space(detail[3].xpath('.//text()').extract())[3] + self.eliminate_space(detail[3].xpath('.//text()').extract())[4]
		except:
			pass
		
		item['section'] = ''
		
		item['township'] = ''
		
		item['range'] = ''
		
		geolocation = self.eliminate_space(detail[4].xpath('.//text()').extract())

		if len(geolocation) > 2:

			item['longitude'] = geolocation[1]
			
			item['latitude'] = geolocation[3]
		
		yield item

	# validate value for eliminate space, wordwrap, etc 

	def validate(self, item):

		try:

			return item.strip().replace('\n', '').replace('\t','').replace('\r', '')

		except:

			pass

	# select items which are not blank from the list

	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp
