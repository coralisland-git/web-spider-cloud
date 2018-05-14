# from __future__ import unicode_literals
import scrapy
import json
import csv
import os
import scrapy
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
from selenium import webdriver
from lxml import html
import random
import pdb

class zillowProxy(scrapy.Spider):

	name = 'zillowProxy'

	domain = 'https://www.zillow.com'

	proxy_list = []

	def __init__(self):

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/data/proxy list.txt'

		with open(file_path, 'rb') as text:

			content = text.readlines()

		for proxy in content :

			proxy = proxy.replace('\n', '')

			proxy = 'http://' + proxy

			self.proxy_list.append(proxy)
		
	
	def start_requests(self):

		count = 0

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/data/HC_ALL_SFR.csv'

		with open(file_path, 'rb') as csvfile:

			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

			for row in spamreader:

				if count >= 1:

					item = ChainItem()

					item['Folio'] = row[0].replace('"', '')

					item['Pin'] = row[1].replace('"', '')

					item['Owner'] = row[2].replace('"', '')

					item['Site_Addr'] = row[3].replace('"', '')

					item['Site_City'] = row[4].replace('"', '')

					item['Site_State'] = row[5].replace('"', '')

					item['Site_Zip'] = row[6].replace('"', '')

					url  = 'https://www.zillow.com/homes/'+item['Site_Addr'].replace(' ', '+')+',-'+item['Site_City'].replace(' ', '-')+',-'+item['Site_State']+'-'+item['Site_Zip']+'_rb/'
					
					yield scrapy.Request(url= url, callback=self.parse, meta={'item' : item, 'url' : url}, dont_filter=True) 

				count += 1


	def parse(self, response):

		if 'captcha' in response.url.lower():

			yield scrapy.Request(url=response.meta['url'], callback=self.parse, meta={'item' : response.meta['item'], 'url' : response.meta['url'], 'proxy' : random.choice(self.proxy_list)}, dont_filter=True) 

		else :

			try:

				item = response.meta['item']

				detail = self.eliminate_space(response.xpath('//header[@class="zsg-content-header addr"]/h3//span[@class="addr_bbs"]//text()').extract())

				try:

					item['Bed'] = float(detail[0].lower().replace('bed', '').replace('s', '').strip())

				except :

					item['Bed'] = 0

				try:

					item['Bath'] = float(detail[1].lower().replace('bath', '').replace('s', '').strip())

				except:

					item['Bath'] = 0

				try:

					item['Square_Footage'] = float(detail[2].lower().replace('sqft','').replace('s', '').strip().replace(',',''))

				except :

					item['Square_Footage'] = 0

				try:

					market = self.validate(''.join(response.xpath('//div[contains(@class, "home-summary-row")]')[0].xpath('.//text()').extract()))

					if 'sale' in market.lower():

						item['Mark'] = 'Yes'

					else : 

						item['Mark'] = 'No'	

					if item['Mark'] == 'Yes':

						item['Zestimate'] = float(self.validate(''.join(response.xpath('//div[contains(@class, "home-summary-row")]')[2].xpath('./span[2]//text()').extract())).replace(',', '').replace('$', ''))

					else :

						item['Zestimate'] = float(self.validate(''.join(response.xpath('//div[contains(@class, "home-summary-row")]')[1].xpath('./span[2]//text()').extract())).replace(',','').replace('$', ''))

				except :

					item['Mark'] = ''

					item['Zestimate'] = 0
					
				yield item

			except : 

				pdb.set_trace()


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass

	def eliminate_space(self, items):

		tmp = []

		for item in items:

			if self.validate(item) != '':

				tmp.append(self.validate(item))

		return tmp