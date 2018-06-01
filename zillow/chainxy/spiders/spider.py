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

from selenium import webdriver

from pyvirtualdisplay import Display

import random

from lxml import etree

import time

import MySQLdb

import sys

import pdb


class spider(scrapy.Spider):

	name = 'spider'

	domain = 'https://www.zillow.com'

	proxy_list = []

	choice = ''

	def __init__(self):

		# self.driver = webdriver.Chrome("./chromedriver")

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/data/proxy list.txt'

		with open(file_path, 'rb') as text:

			content = text.readlines()

		for proxy in content :

			proxy = proxy.replace('\n', '')

			proxy = 'http://' + proxy

			self.proxy_list.append(proxy)


		self.headers = [

			"folio", "pin", "owner", "owner_addr", "owner_city", "owner_state", "owner_zip", "site_addr", "site_city", "site_state", "site_zip", "bed", "bath", "square_footage", "zestimate", "active", "icomps", "redfin", "trulia"

		]


		db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="zillow_db")       

		self.cur = db.cursor()


	def start_requests(self):

		yield scrapy.Request(self.domain, callback=self.parse_case,  meta={'proxy' : random.choice(self.proxy_list) }, dont_filter=True)

		# yield scrapy.Request(url='https://www.trulia.com/', callback=self.parse_trulia)


	def parse_case(self, response):

		print("""
--------- Options ---------

	0 : Csv

	1 : Zillow

	2 : Icomps

	3 : Redfin

	4 : Trulia
---------------------------
			""")
		
		self.choice = raw_input(' Select : ')

		try:

			self.choice = int(self.choice)

		except:

			self.choice = -1


		if self.choice == 0:

			yield scrapy.Request(self.domain, callback=self.parse_csv, meta={'proxy' : random.choice(self.proxy_list) }, dont_filter=True)

		elif self.choice == 1:

			sql = "select * from parcel_estimate where zestimate is NULL or zestimate='0' or zestimate='' or bed='' or bed is NULL or bath='' or bath is NULL or square_footage='' or square_footage is NULL"

			self.cur.execute(sql)

			rows = self.cur.fetchall()

			for row in rows:

				item = ChainItem()

				for ind in range(0, len(row)-1):

					item[self.headers[ind].title()] = row[ind+1]

				url  = 'https://www.zillow.com/homes/'+item['Site_Addr'].replace(' ', '+')+',-'+item['Site_City'].replace(' ', '-')+',-'+item['Site_State']+'-'+item['Site_Zip']+'_rb/'

				yield scrapy.Request(url= url, callback=self.parse_zillow, meta={'item' : item, 'url' : url, 'proxy' : random.choice(self.proxy_list) }, dont_filter=True) 

		elif self.choice == 2:

			sql = "select * from parcel_estimate where icomps is NULL or icomps='0' or icomps=''"

			self.cur.execute(sql)

			rows = self.cur.fetchall()

			for row in rows:

				item = ChainItem()

				for ind in range(0, len(row)-1):

					item[self.headers[ind].title()] = row[ind+1]

				url = 'https://icomps.com/'

				headers = {

					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

					'Accept-Encoding':'gzip, deflate, br',

					'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryEA6WIdnFYAG0Pxrw',

					'Upgrade-Insecure-Requests':'1'

				}

				formdata = {

					'address' : item['Site_Addr'] + ', ' + item['Site_City'] + ', ' + item['Site_State']

				}

				yield scrapy.FormRequest(url, callback=self.parse_icomps, formdata=formdata , method='POST', meta={ 'item' : item, 'proxy' : random.choice(self.proxy_list)}, dont_filter=True)

		elif self.choice == 3:

			sql = "select * from parcel_estimate where redfin is NULL or redfin='0' or redfin=''"

			self.cur.execute(sql)

			rows = self.cur.fetchall()

			for row in rows:

				item = ChainItem()

				for ind in range(0, len(row)-1):

					item[self.headers[ind].title()] = row[ind+1]

				url = 'https://www.redfin.com/stingray/do/location-autocomplete?location='+item['Site_Addr']+'&start=0&count=10&v=2&market=social&al=1&iss=false&ooa=true'

				yield scrapy.Request(url, callback=self.parse_redfin, meta={ 'item' : item , 'proxy' : random.choice(self.proxy_list) }, dont_filter=True)

		elif self.choice == 4:

			print(' ~~~~ Warning! : Trulia has not been implemeted yet. ~~~')

		else:

			print(' ~~~~ Warning! : invalid format ~~~')


	def parse_csv(self, response):

		count = 0

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/data/HC_ALL_SFR.csv'

		with open(file_path, 'rb') as csvfile:

			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

			for row in spamreader:

				if count >= 1:

					item = ChainItem()

					for ind in range(0, len(row)):

						item[self.headers[ind].title()] = row[ind].replace('"', '')

					sql = "select * from parcel_estimate where folio=%s" %item['Folio']

					self.cur.execute(sql)

					rows = self.cur.fetchall()

					if len(rows) == 0:
				
						yield item

				count += 1


	def parse_zillow(self, response):

		if 'captcha' in response.url.lower():

			yield scrapy.Request(url=response.meta['url'], callback=self.parse_zillow, meta={'item' : response.meta['item'], 'url' : response.meta['url'], 'proxy' : random.choice(self.proxy_list)}, dont_filter=True) 

		else :

			try:

				item = response.meta['item']

				detail = self.eliminate_space(response.xpath('//header[@class="zsg-content-header addr"]/h3//span[@class="addr_bbs"]//text()').extract())

				item['Bed'] = detail[0].lower().replace('bed', '').replace('s', '').strip()

				item['Bath'] = float(detail[1].lower().replace('bath', '').replace('s', '').strip())

				item['Square_Footage'] = float(detail[2].lower().replace('sqft','').replace('s', '').strip().replace(',',''))

				try:

					market = self.validate(''.join(response.xpath('//div[contains(@class, "home-summary-row")]')[0].xpath('.//text()').extract()))

					if 'sale' in market.lower() or 'sold' in market.lower():

						item['Active'] = 'Yes'

					else : 

						item['Active'] = 'No'	

					if item['Active'] == 'Yes':

						item['Zestimate'] = self.validate(''.join(response.xpath('//div[contains(@class, "home-summary-row")]')[2].xpath('./span[2]//text()').extract())).replace(',', '').replace('$', '')

					else :

						item['Zestimate'] = self.validate(''.join(response.xpath('//div[contains(@class, "home-summary-row")]')[1].xpath('./span[2]//text()').extract())).replace(',','').replace('$', '')

				except :

					item['Active'] = ''

					item['Zestimate'] = ''

				yield item

			except :

				pass


	def parse_icomps(self, response):		

		if 'comparables' in response.body.lower() : 

			print('warning : Icomps.com went down. please try again later.')

		else:

			item = response.meta['item']

			try:

				item['Icomps'] = self.validate(''.join(response.xpath('//p[contains(@class, "green value")]//text()').extract()).split(':')[1].strip().replace('$', '').replace(',',''))

			except :

				item['Icomps'] = ''

			yield item


	def parse_redfin(self, response):

		item = response.meta['item']

		data = response.body.split('&&')

		if len(data) > 1:

			data = data[1]

		try:

			data = json.loads(data)

			matched_addr = data['payload']['exactMatch']['name']

			url = 'https://www.redfin.com'+data['payload']['exactMatch']['url']

			if item['Site_Addr'].lower() == matched_addr.lower():

				yield scrapy.Request(url=url, callback=self.parse_redfin_detail, meta={ 'item' : item, 'proxy' : random.choice(self.proxy_list) }, dont_filter=True)

		except :

			pass


	def parse_redfin_detail(self, response):

		item = response.meta['item']

		try:

			item['Redfin'] = self.validate(''.join(response.xpath('//div[@class="info-block avm"]//div[@class="statsValue"]//text()').extract()).replace('$', '').replace(',',''))

		except :

			item['Redfin'] = ''

		yield item


	# def parse_trulia(self, response):

	# 	display = Display(visible=0, size=(800, 600))

	# 	display.start()

	# 	self.driver.get("https://www.trulia.com/")

	# 	self.driver.set_window_position(-10000,0)

	# 	# try:

	# 	# 	self.driver.find_element_by_id('searchBox').send_keys('706 BLOOMINGFIELD DR')

	# 	# 	self.driver.find_element_by_class_name('css-16gf7cf').click()

	# 	# 	# time.sleep(1)

	# 	# 	source = self.driver.page_source.encode("utf8")

	# 	# 	tree = etree.HTML(source)

	# 	# 	# item = response.meta['item']

	# 	# 	item = {}

	# 	# 	item['trulia'] = self.validate(''.join(tree.xpath('//div[contains(@class, "pan ptxsXxsVisible ptlSmlVisible")]//div[@class="mvn"]//text()')).replace('$', '').replace(',','')).split(' ')[0]

	# 	# 	self.driver.get("https://www.trulia.com/")

	# 	# except :

	# 	# 	item['trulia'] = ''

	
	# 	pdb.set_trace()

	# 	yield item

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