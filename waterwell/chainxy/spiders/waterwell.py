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

import time

import pdb



class waterwell(scrapy.Spider):

	name = 'waterwell'

	domain = 'https://secure.in.gov/'

	header = {

		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

		"Accept-Encoding":"gzip, deflate, br",

		"Content-Type":"application/x-www-form-urlencoded",

		"Upgrade-Insecure-Requests":"1",

		"Origin":"https://secure.in.gov",

		"Referer":"https://secure.in.gov/apps/dnr/dowos/WaterWell.aspx",

		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
	}

	def __init__(self):

		# load selenium driver

		self.driver = webdriver.Chrome("./chromedriver")
	
	def start_requests(self):

		init_url  = 'https://secure.in.gov/apps/dnr/dowos/WaterWell.aspx'

		yield scrapy.Request(url=init_url, callback=self.parse)

	def parse(self, response):

		self.driver.get("https://secure.in.gov/apps/dnr/dowos/WaterWell.aspx")

		self.driver.find_element_by_id('mstr_cphUserItems_txtMaxNumRows').send_keys('300000')

		self.driver.find_element_by_id('mstr_cphUserItems_ddlQSearch').send_keys('County')

		self.driver.find_element_by_id('mstr_cphUserItems_btnSearchGo').click()

		time.sleep(5)

		source = self.driver.page_source.encode("utf8")

		tree = etree.HTML(source)

		count = len(tree.xpath('//table//tr//a'))

		for ind in range(0, count):

			self.driver.find_elements_by_xpath('//table//tr//a')[ind].click()

			time.sleep(6)

			source = self.driver.page_source.encode("utf8")

			tree = etree.HTML(source)
			
			item = ChainItem()

			item['owner_contractor'] = self.validate(''.join(tree.xpath('//span[@id="lblOwnType"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="Label89"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="Label90"]//text()')))
			
			item['name'] = self.validate(''.join(tree.xpath('//span[@id="lblOwnName"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="lblDrillName"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="lblOperName"]//text()')))
			
			item['address'] = self.validate(''.join(tree.xpath('//span[@id="lblOwnAddr"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="lblDrillAddr"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="lblOperLic"]//text()')))
			
			item['telephone'] = self.validate(''.join(tree.xpath('//span[@id="lblOwnPhone"]//text()'))) + '-' + self.validate(''.join(tree.xpath('//span[@id="lblDrillPhone"]//text()'))) + '-' + ' '

			item['reference_number'] = self.validate(''.join(tree.xpath('//span[@id="lblRefNum"]//text()')))

			item['driving_dircetion_to_well'] = self.validate(''.join(tree.xpath('//span[@id="lblDriving"]//text()')))

			item['date_completed'] = self.validate(''.join(tree.xpath('//span[@id="lblDateCompleted"]//text()')))

			item['well_use'] = self.validate(''.join(tree.xpath('//span[@id="lblWellUse"]//text()')))

			item['drilling_method'] = self.validate(''.join(tree.xpath('//span[@id="lblWellDrillMethod"]//text()')))

			item['pump_type'] = self.validate(''.join(tree.xpath('//span[@id="lblWellPumpType"]//text()')))

			item['depth'] = self.validate(''.join(tree.xpath('//span[@id="lblWellDepth"]//text()')))

			item['pump_setting_depth'] = self.validate(''.join(tree.xpath('//span[@id="lblWellPumpDepth"]//text()')))

			item['water_quality'] = self.validate(''.join(tree.xpath('//span[@id="lblWellQuality"]//text()')))

			item['casing_length'] = self.validate(''.join(tree.xpath('//span[@id="lblCasingLength"]//text()')))

			item['casing_mateiral'] = self.validate(''.join(tree.xpath('//span[@id="lblCasingMaterial"]//text()')))

			item['casing_diameter'] = self.validate(''.join(tree.xpath('//span[@id="lblCasingDia"]//text()')))

			item['screen_length'] = self.validate(''.join(tree.xpath('//span[@id="lblScreenLength"]//text()')))

			item['screen_material'] = self.validate(''.join(tree.xpath('//span[@id="lblScreenMaterial"]//text()')))

			item['screen_diameter'] = self.validate(''.join(tree.xpath('//span[@id="lblScreenDia"]//text()')))

			item['slot_size']  = self.validate(''.join(tree.xpath('//span[@id="lblScreenSlot"]//text()')))

			item['type_of_test'] = self.validate(''.join(tree.xpath('//span[@id="lblTypeTest"]//text()')))

			item['test_rate'] = self.validate(''.join(tree.xpath('//span[@id="lblTestRate"]//text()')))

			item['bail_test_rate'] = self.validate(''.join(tree.xpath('//span[@id="lblBailTestRate"]//text()')))

			item['drawdown'] = self.validate(''.join(tree.xpath('//span[@id="lblDrawdown"]//text()')))

			item['static_water_level'] = self.validate(''.join(tree.xpath('//span[@id="lblStaticLevel"]//text()')))

			item['bailer_drawdown'] = self.validate(''.join(tree.xpath('//span[@id="lblBailerDrawdown"]//text()')))

			item['material'] = self.validate(''.join(tree.xpath('//span[@id="lblGroutMaterial"]//text()')))

			item['depth_2'] = self.validate(''.join(tree.xpath('//span[@id="lblSealDepth"]//text()')))

			item['installation_method'] = self.validate(''.join(tree.xpath('//span[@id="lblSealMethod"]//text()')))

			item['number_of_bags_used'] = self.validate(''.join(tree.xpath('//span[@id="lblGroutBags"]//text()')))

			item['sealing_material'] = self.validate(''.join(tree.xpath('//span[@id="lblSealMaterial"]//text()')))

			item['well_abandonment_depth'] = self.validate(''.join(tree.xpath('//span[@id="lblSealDepth"]//text()')))

			item['installation_method_2'] = self.validate(''.join(tree.xpath('//span[@id="lblSealMethod"]//text()')))

			item['number_of_bags_used_2'] = self.validate(''.join(tree.xpath('//span[@id="lblSealBags"]//text()')))

			item['county'] = self.validate(''.join(tree.xpath('//span[@id="lblCounty"]//text()')))

			item['township'] = self.validate(''.join(tree.xpath('//span[@id="lblTownship"]//text()')))

			item['range'] = self.validate(''.join(tree.xpath('//span[@id="lblRange"]//text()')))

			item['section'] = self.validate(''.join(tree.xpath('//span[@id="lblSection"]//text()')))

			item['topo_map'] = self.validate(''.join(tree.xpath('//span[@id="lblTopoMap"]//text()')))

			item['grant'] = self.validate(''.join(tree.xpath('//span[@id="lblGrant"]//text()')))

			item['field_located_by'] = self.validate(''.join(tree.xpath('//span[@id="lblFieldBy"]//text()')))

			item['field_located_on'] = self.validate(''.join(tree.xpath('//span[@id="lblFieldOn"]//text()')))

			item['courthouse_location_by'] = self.validate(''.join(tree.xpath('//span[@id="lblCourthouseBy"]//text()')))

			item['courthouse_location_on'] = self.validate(''.join(tree.xpath('//span[@id="lblCourthouseOn"]//text()')))

			item['location_accepted_verification_by'] = self.validate(''.join(tree.xpath('//span[@id="lblVerificationBy"]//text()')))

			item['location_accepted_verification_on'] = self.validate(''.join(tree.xpath('//span[@id="lblVerificationOn"]//text()')))

			item['subdivision_name'] = self.validate(''.join(tree.xpath('//span[@id="lblSubdivision"]//text()')))

			item['lot_number'] = self.validate(''.join(tree.xpath('//span[@id="lblLotNum"]//text()')))

			item['ft_w_of_el'] = self.validate(''.join(tree.xpath('//span[@id="lblWofE"]//text()')))

			item['ft_n_of_sl'] = self.validate(''.join(tree.xpath('//span[@id="lblNofS"]//text()')))

			item['ft_e_of_wl'] = self.validate(''.join(tree.xpath('//span[@id="lblEofW"]//text()')))

			item['ft_s_of_nl'] = self.validate(''.join(tree.xpath('//span[@id="lblSofN"]//text()')))

			item['ground_elevation'] = self.validate(''.join(tree.xpath('//span[@id="lblGroundElev"]//text()')))

			item['depth_of_bedrock'] = self.validate(''.join(tree.xpath('//span[@id="lblBedrockDepth"]//text()')))

			item['bedrock_elevation'] = self.validate(''.join(tree.xpath('//span[@id="lblBedrockElev"]//text()')))

			item['aquifer_elevation'] = self.validate(''.join(tree.xpath('//span[@id="lblAquiferElev"]//text()')))

			item['utm_easting'] = self.validate(''.join(tree.xpath('//span[@id="lblUTMEast"]//text()')))

			item['utm_northing'] = self.validate(''.join(tree.xpath('//span[@id="lblUTMNorth"]//text()')))

			well_log_table = tree.xpath('//table[@rules="all"]//tr')[1:]

			top = ''

			bottom = ''

			formation = ''

			for well_log in well_log_table:

				top += self.validate(''.join(well_log.xpath('.//td[1]/text()'))) + '-'

				bottom += self.validate(''.join(well_log.xpath('.//td[2]/text()'))) + '-'

				formation += self.validate(''.join(well_log.xpath('.//td[3]/text()'))) + '-'

			item['top'] = top[:-1]

			item['bottom'] = bottom[:-1]

			item['formation'] = formation[:-1]

			yield item
			
			self.driver.find_element_by_id('btnBack').click()

			time.sleep(1)

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