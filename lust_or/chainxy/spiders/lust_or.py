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

class lust_or(scrapy.Spider):

	name = 'lust_or'

	domain = 'http://www.deq.state.or.us/lq/tanks/lust/LustPublicLookup.asp'

	history = []

	total_count = 0

	count = 0

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

		init_url  = 'http://www.deq.state.or.us/lq/tanks/lust/LustPublicLookup.asp'

		yield scrapy.Request(url=init_url, callback=self.parse)		


	def parse(self, response):

		county_list = response.xpath('//select[@name="County"]//option/@value').extract()

		for county in county_list[2:]:

			url = "http://www.deq.state.or.us/lq/tanks/lust/LustPublicList.asp"

			headers = {

				"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

				"Accept-Encoding":"gzip, deflate",

				"Content-Type":"application/x-www-form-urlencoded",

				"Upgrade-Insecure-Requests":"1",

				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

			}

			formdata = {

				"County":str(county),

				"Region":"BLANK"

			 }

			yield scrapy.FormRequest(url, callback=self.parse_list, headers=headers, method="post", formdata=formdata)

	
	def parse_list(self, response):

		loc_list = response.xpath('//table[@frame="box"]//tr')

		for loc in loc_list[1:]:

			url = loc.xpath('.//a/@href').extract_first()

			item = ChainItem()

			item['log_number'] = self.validate(''.join(loc.xpath('.//td[1]//text()').extract()))

			item['log_number_link'] = url

			item['fac_id'] = self.validate(''.join(loc.xpath('.//td[2]//text()').extract()))

			item['site_name'] = self.validate(''.join(loc.xpath('.//td[3]//text()').extract()))

			item['site_name_'] = self.validate(''.join(loc.xpath('.//td[3]//text()').extract()))

			item['address'] = self.validate(''.join(loc.xpath('.//td[4]//text()').extract()))

			item['city'] = self.validate(''.join(loc.xpath('.//td[5]//text()').extract()))

			item['zip_code'] = self.validate(''.join(loc.xpath('.//td[6]//text()').extract()))

			item['county'] = self.validate(''.join(loc.xpath('.//td[7]//text()').extract()))

			yield scrapy.Request(url, callback=self.parse_detail, meta={'item' : item})
			

	def parse_detail(self, response):

		item = response.meta['item']

		# for summary

		item['summary_information'] = ''

		item['received_data'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ReceivedDateLabel"]//text()').extract()))

		item['address_1'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_SiteAddressLabel"]//text()').extract()))

		item['address_2'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_SiteCityLabel"]//text()').extract())) + ', ' + self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_SiteZipLabel"]//text()').extract()))

		item['status'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_STATUSLabel"]//text()').extract()))

		item['tank_type'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_TankTypeLabel"]//text()').extract()))

		item['county'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_COUNTY_NAMELabel"]//text()').extract()))

		item['file_status'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ReceivedDateLabel"]//text()').extract()))

		item['site_type'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_SiteTypeLabel"]//text()').extract()))

		item['ust_facility_id'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_FacilityIdLabel"]//text()').extract()))

		item['project_manager'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ProjectManagerLabel"]//text()').extract()))

		item['cause_of_release'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ReleaseCauseDescriptionLabel"]//text()').extract()))

		item['source_of_release'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ReleaseSourceDescriptionLabel"]//text()').extract()))

		item['discovery_method'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_DiscoveryDescriptionLabel"]//text()').extract()))

		item['media_effected'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_MediaListLabel"]//text()').extract()))

		item['contaminants_released'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ContaminateListLabel"]//text()').extract()))

		delineate_detail = response.xpath('//table[@id="ctl00_Area2_ctl00_AsssessmentDyanmicTable"]//td')

		if len(delineate_detail) != 0:

			item['delineate_soil'] = self.validate(''.join(delineate_detail[1].xpath('.//text()').extract()))

			item['ground_water'] = self.validate(''.join(delineate_detail[3].xpath('.//text()').extract()))

			item['soil_delineated_release'] = self.validate(''.join(delineate_detail[5].xpath('.//text()').extract()))

		item['stopped_date'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ReleaseStopDateLabel"]//text()').extract()))

		item['cleanup_start_date'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_CleanupStartDateLabel"]//text()').extract()))

		item['cleanup_end_date'] = self.validate(''.join(response.xpath('//span[@id="ctl00_Area2_ctl00_ClosedDateLabel"]//text()').extract()))

		# for work reported

		work_reported_detail_list = response.xpath('//div[@id="ctl00_Area2_ctl01_RepeaterPanel"]//tr')

		if len(work_reported_detail_list) > 1:

			work_reported = ' '

			reported_date = ' '

			for work_reported_detail in work_reported_detail_list[1:]:

				work_reported += self.eliminate_space(work_reported_detail.xpath('.//text()').extract())[0] + '-'

				reported_date += self.eliminate_space(work_reported_detail.xpath('.//text()').extract())[1] + '-'

			item['work_reported'] = work_reported[:-1].strip()

			item['reported_date'] = reported_date[:-1].strip()

		# for documents

		document_detail_list = response.xpath('//table[@class="tbOuter"]//tr')

		file_name = ' '

		file_link = ' '

		category = ' '

		file_size_mb = ' '

		upload_date = ' '


		if len(document_detail_list) > 2:

			for document in document_detail_list[2:]:

				document_detail = self.eliminate_space(document.xpath('.//td//text()').extract())

				file_name += self.validate(document_detail[0]) + '+'

				file_link += 'http://www.deq.state.or.us/Webdocs/' + self.validate(document.xpath('.//a/@href').extract_first())[6:] + '+'

				category += self.validate(document_detail[1]) + '+'

				file_size_mb += self.validate(document_detail[2]) + '+'

				upload_date += self.validate(document_detail[3]) + '+'

		item['file_name'] = file_name[:-1].strip()

		item['file_link'] = file_link[:-1].strip()

		item['category'] = category[:-1].strip()

		item['file_size_mb'] = file_size_mb[:-1].strip()

		item['upload_date'] = upload_date[:-1].strip()

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
