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

class spl_il(scrapy.Spider):

	name = 'spl_il'

	history = []

	header = {

		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

		"Accept-Encoding":"gzip, deflate",

		"Content-Type":"application/x-www-form-urlencoded",

		"Cookie":"ASP.NET_SessionId=vrfv0545mp1hijnnt5ebdtic",

		"Host":"tier2.iema.state.il.us",

		"Origin":"http://tier2.iema.state.il.us",

		"Referer":"http://tier2.iema.state.il.us/FOIAHazmatSearch/",

		"Upgrade-Insecure-Requests":"1",

		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
	
	}

	def __init__(self):
		pass
	
	# start scraper

	def start_requests(self):

		init_url  = 'http://tier2.iema.state.il.us/FOIAHazmatSearch/Default.aspx'

		formdata = {

			"__VIEWSTATE":"/wEPDwUKMTU2OTAyMTExMg9kFgICBw9kFgYCAQ8PFgIeBFRleHQFDkluY2lkZW50TnVtYmVyZGQCAw8PFgIfAAUDQVNDZGQCEw9kFgICCQ88KwALAGRkVViZWL3l2ApCjLUqaBl+G3Y+cQM=",
			
			"__VIEWSTATEGENERATOR":"DB5F18E0",
			
			"__EVENTVALIDATION":"/wEWCAK1yPSQAQKvhL6CCwLQ38TuBALwpJ3cBgLv7ITZAgLg2ZN+AsKGtEYCpZ/z7gqvmEyNyb2OR+cCmzE41bIiPMYdzQ==",
			
			"txtNumber":"%",
			
			"btnSearch":"Search"

		}

		# sign in with credentials into website.

		yield scrapy.FormRequest(url=init_url, callback=self.parse, formdata=formdata, headers=self.header, method="post")

	def parse(self, response):

		loc_list = response.xpath('//table[@id="dgResults"]//tr')

		for loc in loc_list[1:-1]:

			url = "http://tier2.iema.state.il.us/FOIAHazmatSearch/HazmatDetails.aspx?RptNum="+loc.xpath('.//a/text()').extract_first()

			yield scrapy.Request(url, callback=self.parse_detail, headers=self.header, method="get")


	def parse_detail(self, response):

		pdb.set_trace()

		item = ChainItem()



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
