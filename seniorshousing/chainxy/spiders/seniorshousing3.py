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
from selenium import webdriver
from lxml import html
import pdb

class seniorshousing3(scrapy.Spider):

	name = 'seniorshousing3'

	domain = 'https://www.seniorshousing.org'

	history = []

	def __init__(self):
		pass
	
	def start_requests(self):

		init_url  = 'https://www.seniorshousing.org/members-bio.php?level=3'

		yield scrapy.Request(url=init_url, callback=self.parse) 


	def parse(self, response):

		records = response.xpath('//table[@height="100px"]')

		for record in records:

			detail = self.eliminate_space(record.xpath('.//text()').extract())

			try:

				item = ChainItem()

				item['Link'] = response.url

				item['CompanyName'] = detail[0]

				if '.' in detail[1]:

					fl = detail[1].split('.')

				else:

					fl = detail[1].split(' ')

				item['FirstName'] = self.validate(fl[0])

				item['LastName'] = self.validate(fl[1])

				item['WebSite'] = ''

				if len(detail) > 2:

					if 'com' in detail[2].lower() or 'www' in detail[2].lower() or '.' in detail[2]:
						
						item['WebSite'] = detail[2]

					else :					

						cs = detail[2].split(',')

						item['City'] = self.validate(cs[0]);

						item['State'] = self.validate(cs[1]);

					if len(detail) > 3 and item['WebSite'] == '':

						item['WebSite'] = detail[3]

				yield item

			except:

				pdb.set_trace()


		pagenations = response.xpath('//a[contains(@href, "/members-bio.php?page=")]')

		for pagenation in pagenations:

			if 'next' in pagenation.xpath('./img/@src').extract_first():

				url = self.domain + pagenation.xpath('./@href').extract_first()

				yield scrapy.Request(url, callback=self.parse)


	def validate(self, item):
		try:
			return item.strip().replace('\n', '').replace('\t','').replace('\r', '')
		except:
			pass

	def eliminate_space(self, items):
	    tmp = []
	    for item in items:
	        if self.validate(item) != '':
	            tmp.append(self.validate(item))
	    return tmp
