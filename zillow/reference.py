# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
import json
import csv
import requests
import re
import chainxy.utils as utils
from pprint import pprint
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
from lxml import html
from lxml import etree
import pdb

class TemplateSpider(scrapy.Spider):
    name = "template"
    start_urls = ['']
    base_url = ''
    handle_httpstatus_list = [301]
    parse_address={'enabled':True}
    history = []


    def __init__(self, *args, **kwargs):
        script_dir = os.path.dirname(__file__)
        file_path = script_dir + '/US_Cities.json'
        with open(file_path) as data_file:    
            self.location_list = json.load(data_file)
        file_path = script_dir + '/CA_Cities.json'
        with open(file_path) as data_file:    
            self.location_list.append(json.load(data_file))

        with open('cities_us.json') as data_file:    
            self.location_list = json.load(data_file)

    def start_requests(self):
        url = ""
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        store_list = response.xpath('')
        for store in store_list:
            item = ChainItem()
            item['store_name'] = ''
            item['store_number'] = ''
            item['store_type'] = ''
            item['address'] = ''
            item['address2'] = ''
            item['city'] = ''
            item['state'] = ''
            item['zip_code'] = ''
            item['country'] = ''
            item['phone_number'] = ''
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_hours'] = ''
            item['other_fields'] = ''
            item['coming_soon'] = ''
            if item['store_name']+item['phone_number'] not in self.history:
                self.history.append(item['store_name']+item['phone_number'])
                yield item

    def validate(self, item):
        if item:
            try:
                return str(item).strip().replace('\n', '').replace('\t','').replace('\r', '').encode('ascii','ignore').replace('\0xc2', ' ').replace('\u2013', ' ')
            except:
                return ''

    def eliminate_space(self, items):
        tmp = []
        for item in items:
            if self.validate(item) != '':
                tmp.append(self.validate(item))
        return tmp

seed = Seed()
seed.setConfig(seed_type="grid", distance="250", countries=['US'], regions=['ALL'], sample=False)
s = seed.query_points()
for p in s['results']:
	formdata = {
		"address":"",
		"formdata":"addressInput=",
		"lat":p['latitude'],
		"lng":p['longitude'],
		"name":"",
		"radius":"10000",
		"tags":"",
		"action":"csl_ajax_onload"
	}

print("=========  Checking	========")
with open('response-'+self.name+'.html', 'wb') as f:
	f.write(response.body)

address = ''
item['phone_number'] = ''
for de in detail:
    if '-' in de and len(de.split('-')) == 3 :
        item['phone_number'] = self.validate(de)
    else:
        if self.validate(de) != '':
            address += self.validate(de) + ', '

----------- regular Expression ------------

data = self.eliminate_space(response.xpath('//div[@class="leftpromoarea"]/p[1]//text()').extract())
address = ''
res = ''
r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
for da in data[1:]:
    res = r.match(da)
    if res:
        item['phone_number'] = da
        break
    else:
        address += da + ', '

---------------------------------------------

	
h_temp = ''
cnt = 1
for hour in hour_list:
    h_temp += hour
    if cnt % 2 == 0:
        h_temp += ', '
    else:
        h_temp += ' '
    cnt += 1
item['store_hours'] = h_temp[:-2]


if item['store_name']+item['phone_number'] not in self.history:
        self.history.append(item['store_name']+item['phone_number'])
        yield item


def validate(self, item):
	try:
		return item.strip().replace('\n', '').replace('\t','').replace('\r', '').encode('ascii','ignore').replace('\0xc2', ' ').replace('\u2013', ' ')
	except:
		pass

def eliminate_space(self, items):
    tmp = []
    for item in items:
        if self.validate(item) != '':
            tmp.append(self.validate(item))
    return tmp

def str_concat(self, items, unit):
    tmp = ''
    for item in items[:-1]:
        if self.validate(item) != '':
            tmp += self.validate(item) + unit
    tmp += self.validate(items[-1])
    return tmp


        item.encode('raw-unicode-escape').replace('\xa0', unit).strip()

------------  when occurs errors like "HTTP status code is not handled or not allowed"

            DOWNLOADER_MIDDLEWARES = {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            }

------------