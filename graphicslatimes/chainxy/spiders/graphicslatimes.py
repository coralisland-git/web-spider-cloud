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

class graphicslatimes(scrapy.Spider):
	name = 'graphicslatimes'
	domain = 'http://www.shopkins-games.com/'
	history = []

	def __init__(self):
		pass
	
	def start_requests(self):
		init_url  = 'http://graphics.latimes.com/soft-story-apartments-needing-retrofit/'
		yield scrapy.Request(url=init_url, callback=self.parse) 

	def parse(self, Response):
		pdb.set_trace()
		loc_list = Response.xpath('//table//a')
			

		# https://secure.in.gov/Apps/dnr/DOWOS/WebResource.axd?d=zd6FVKQYzRUGe_5KYiX-j08Z2PpME0X9IjgvQa6iABaQMMP_bBI3X5GORKtQwgPDIdItdwy8zObWwAnVmlY7qUp7JdU1&t=636271527501517547
		# https://secure.in.gov/Apps/dnr/DOWOS/WebResource.axd?d=zd6FVKQYzRUGe_5KYiX-j08Z2PpME0X9IjgvQa6iABaQMMP_bBI3X5GORKtQwgPDIdItdwy8zObWwAnVmlY7qUp7JdU1&t=636271527501517547