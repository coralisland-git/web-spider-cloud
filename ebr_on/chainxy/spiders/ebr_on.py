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

import getpass

import datetime

import pdb



class ebr_on(scrapy.Spider):

	name = 'ebr_on'

	domain = 'http://www.ebr.gov.on.ca'

	history = []
	
	date_start = '2017/10/01'
	
	date_end = '2018/03/25'

	header = {

		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

		"Accept-Encoding":"gzip, deflate",

		"Content-Type":"application/x-www-form-urlencoded",

		"Referer":"http://www.ebr.gov.on.ca/ERS-WEB-External/searchNoticePost.do",

		"Upgrade-Insecure-Requests":"1",

		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

	}

	def __init__(self):
		pass
	
	# start scraper

	def start_requests(self):

		self.date_start = raw_input('Date Start : ')

		self.date_end = raw_input('Date End : ')

		now = datetime.datetime.now()

		if self.date_start == '':

			self.date_start = str(int(now.year)-3) + '/' + now.strftime('%m') + '/' + now.strftime('%d')

		if self.date_end == '':

			self.date_end = str(now.year) + '/' + now.strftime('%m') + '/' + now.strftime('%d')

		init_url  = 'http://www.ebr.gov.on.ca/ERS-WEB-External/searchNoticePost.do'

		formdata = {

			"shouldReset":"true",

			"oldTimePeriod":"3",

			"oldTimeFlag":"TRUE",

			"ClearAllData":"FALSE",

			"multimedia":"false",

			"lioMapSelectionXMLString": "",

			"LIO_MAP_ACTION":"LIO_MAP_ACTION_DATA_NO",

			"language":"en",

			"erbRegistryNumber":"",

			"lioSearchType":"0",

			"lioText":"",

			"timePeriod":"-1",

			"lastOrFromTo":"1",

			"dateStart": self.date_start,

			"dateEnd": self.date_end,

			"numberOfRecords":"100",

			"sortBy":"20006",

			"sortOrder":"1",

			"actionType":"Search"

		}

		# sign in with credentials into website.

		yield scrapy.FormRequest(url=init_url, callback=self.parse, formdata=formdata, headers=self.header, method="post", dont_filter=True)

	
	def parse(self, response):

		page_list = self.eliminate_space(response.xpath('//div[@id="div_pagination"]//text()').extract())

		for page in page_list:

			try:

				url = 'http://www.ebr.gov.on.ca/ERS-WEB-External/searchNoticePost.do'

				formdata = {
					
					"isPopulateSearchNoticeForm":"true",
					
					"shouldReset":"true",
					
					"multimedia":"false",
					
					"lastOrFromTo":"1",
					
					"timePeriod":"-1",
					
					"dateStart": self.date_start,

					"dateEnd": self.date_end,
					
					"numberOfRecords":"100",
					
					"sortBy":"20006",
					
					"sortOrder":"1",
					
					"lioSearchType":"0",
					
					"page":page,
					
					"language":"en",
				
				}

				yield scrapy.FormRequest(url=url, callback=self.parse_page, formdata=formdata, headers=self.header, method="post", dont_filter=True)

			except:

				pass


		pagenation_list = response.xpath('//a[@class="searchResultN"]')

		next_page = ''

		for pagenation in pagenation_list:

			if 'next' in pagenation.xpath('./text()').extract_first().lower():

				next_page = pagenation.xpath('./@href').extract_first().split('(')[1][:-1]

		
		if next_page != '':

			url = 'http://www.ebr.gov.on.ca/ERS-WEB-External/searchNoticePost.do'

			formdata = {
				
				"isPopulateSearchNoticeForm":"true",
				
				"shouldReset":"true",
				
				"multimedia":"false",
				
				"lastOrFromTo":"1",
				
				"timePeriod":"-1",
				
				"dateStart": self.date_start,

				"dateEnd": self.date_end,
				
				"numberOfRecords":"100",
				
				"sortBy":"20006",
				
				"sortOrder":"1",
				
				"lioSearchType":"0",
				
				"page": next_page,
				
				"language":"en"
			
			}

			yield scrapy.FormRequest(url=url, callback=self.parse, formdata=formdata, headers=self.header, method="post", dont_filter=True)

	def parse_page(self, response):

		loc_list = response.xpath('//table[@class="searchResult"]//tr[@valign="top"]')

		for loc in loc_list:

			try:

				url = self.domain + loc.xpath('.//a[@class="searchResultLink"]/@href').extract_first()

				item = ChainItem()

				item['ministry_reference_number'] = self.validate(''.join(loc.xpath('.//td[2]//text()').extract()))

				item['ebr_registry_number'] = self.validate(''.join(loc.xpath('.//td[1]//text()').extract()))

				item['notice_type'] = self.validate(''.join(loc.xpath('.//td[4]//text()').extract()))

				item['notice_date'] = self.validate(''.join(loc.xpath('.//td[5]//text()').extract())) 

				yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})
			
			except:

				pass

	
	def parse_detail(self, response):

		data = response.xpath('//span[@class="notice-content-sub"]')

		item = response.meta['item']

		detail = response.xpath('//div[@aria-labelledby="h1_notice"]//span[@class="notice-content-sub"]')

		try:
			item['instrument_type'] = self.validate(''.join(detail[1].xpath('.//text()').extract()))

			item['company_name'] = self.validate(''.join(detail[0].xpath('.//text()').extract()[0:1]))

			item['proposal_address'] = self.validate(''.join(detail[0].xpath('.//text()').extract()[1:]))

		except:

			pass

		ebrs = self.eliminate_space(response.xpath('//div[@aria-label="EBR Registry Number:"]//text()').extract())

		for ind in range(0, len(ebrs)):

			if 'date proposal loaded' in ebrs[ind].lower():

				item['proposal_date'] = ebrs[ind+1]

		item['related_locations'] = self.validate(''.join(response.xpath('//div[contains(@aria-label, "Location(s) Related to")]//div[@class="notice-content"]//text()').extract()))
		
		yield item

	# validate value for eliminate space, wordwrap, etc 

	def validate(self, item):

		try:

			return item.strip().replace('\n', '').replace('\t','').replace('\r', '').replace('  ', '')

		except:

			pass

	# select items which are not blank from the list

	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp
