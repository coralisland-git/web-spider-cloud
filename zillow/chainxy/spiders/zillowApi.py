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
import pdb

class zillowApi(scrapy.Spider):

	name = 'zillowApi'

	domain = 'http://www.shopkins-games.com/'

	history = []

	def __init__(self):
		
		pass
	
	def start_requests(self):

		count = 0

		with open('data/HC_ALL_SFR.csv', 'rb') as csvfile:

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

					url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1geoanay8ej_3tnpx&address='+item['Site_Addr']+'&citystatezip='+item['Site_City'] + '+' + item['Site_State']
					
					yield scrapy.Request(url= url, callback=self.parse, meta={'item' : item}) 

				count += 1


	def parse(self, response):

		try:

			item = response.meta['item']

			item['Bed'] = int(float(response.body.split('<bedrooms>')[1].split('</bedrooms>')[0].strip().replace(',', '')))

			item['Bath'] = int(float(response.body.split('<bathrooms>')[1].split('</bathrooms>')[0].strip().replace(',', '')))

			item['Square_Footage'] = int(response.body.split('<finishedSqFt>')[1].split('</finishedSqFt>')[0].strip().replace(',', ''))

			item['Zestimate'] = int(response.body.split('<amount currency="USD">')[1].split('</amount>')[0].strip().replace(',', ''))

			if 'lastSoldDate' in response.body:

				item['Mark'] = 'Yes'	

			else :

				item['Mark'] = 'No'	
				
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