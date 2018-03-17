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

class flash(scrapy.Spider):
	name = 'flash'
	domain = 'http://www.shopkins-games.com/'
	history = []

	def __init__(self):
		pass
	
	def start_requests(self):
		init_url  = 'http://www.shopkins-games.com/'
		yield scrapy.Request(url=init_url, callback=self.parse) 
		# yield scrapy.Request(url="https://www.games-kids.com/files/swf/macy-macaron-dress-up-1508340613.swf", callback=self.parse_swf, meta={'title': 'test'})

	def parse(self, response):
		article_list = response.xpath('//article[@class="games"]')
		for article in article_list:
			url = article.xpath('./a/@href').extract_first()
			title = article.xpath('./a/@title').extract_first()
			image = article.xpath('.//img/@src').extract_first()
			yield scrapy.Request(url=url, callback=self.parse_detail, meta={'title':title, 'image':image })

	def parse_detail(self, response):
		swf_url = response.xpath('.//embed/@src').extract_first()
		if swf_url:
			pass
			yield scrapy.Request(url=swf_url, callback=self.parse_swf, meta={'title': response.meta['title']})
			yield scrapy.Request(url=response.meta['image'], callback=self.parse_image, meta={'title': response.meta['title']})
		else :
			swf_obj_url = response.xpath('.//object/@data').extract_first()
			if swf_obj_url:
				yield scrapy.Request(url=swf_url, callback=self.parse_swf, meta={'title': response.meta['title']})
				yield scrapy.Request(url=response.meta['image'], callback=self.parse_image, meta={'title': response.meta['title']})
			else :
				pass

	def parse_swf(self, response):
		newpath = 'flash_games/'+response.meta['title']
		if not os.path.exists(newpath):
		    os.makedirs(newpath)
		with open('flash_games/'+response.meta['title']+'/'+response.meta['title']+'.swf', 'wb') as f:
				f.write(response.body)

	def parse_image(self, response):
		newpath = 'flash_games/'+response.meta['title']
		if not os.path.exists(newpath):
		    os.makedirs(newpath)
		with open('flash_games/'+response.meta['title']+'/'+response.meta['title']+'.jpg', 'wb') as f:
				f.write(response.body)		