import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import random
import pdb
from lxml import html


class ZillowSpider(scrapy.Spider):
    name = "zillow"

    request_url = 'https://www.zillow.com/ajax/directory/DirectoryContent.htm?apiVer=1&jsonVer=1&callback=YUI.Env.JSONP.yui_3_18_1_1_1527049824639_2987&page=#index#&showAdvancedItems=false&regionID=&locationText=#text#&location=&profession=real-estate-agent-reviews&proType=real-estate-agent&large=true'
    proxy_list = []

    def __init__(self):
        fp = open('cities.json', 'rb')
        self.cities = json.loads(fp.read())        
        self.data = ""

        script_dir = os.path.dirname(__file__)
        file_path = script_dir + '/data/proxy list.txt'

        with open(file_path, 'rb') as text:
            content = text.readlines()

        for proxy in content :
            proxy = proxy.replace('\n', '')
            proxy = 'http://' + proxy
            self.proxy_list.append(proxy)

    def get_json_data(self, response_body):
        txt= response_body
        txt=txt[txt.find('(')+1:-2]
        data = json.loads(txt)
        self.all_lists = []
        return data

    def start_requests(self):
        for row in self.cities:
            location = row['city'] + ' ' + row['state']
            request = scrapy.Request(url=self.request_url.replace('#text#', location).replace('#index#', '1'), meta={'proxy' : random.choice(self.proxy_list) }, dont_filter=True)
            
            yield request

    def parse(self, response):
        pdb.set_trace()
        pages = int(self.get_json_data(response.body)['model']['viewModel']['pagination']['items'][-1]["num"]["value"])

        for index in range(0, pages):
            location = response.meta['location']
            yield scrapy.Request(url=self.request_url.replace('#text#', location).replace('#index#', str(index+1)), callback=self.parse_json, meta={'proxy' : random.choice(self.proxy_list) }, dont_filter=True)

    def parse_json(self, response):
        self.data = self.get_json_data(response.body)['model']['viewModel']['boards']['boards']

        for d in data:
            url = self.base_url + d['profileLink']['href']
            yield scrapy.Request(url=url, callback=self.parse_body, meta={'proxy' : random.choice(self.proxy_list) }, dont_filter=True)

    def parse_body(self, response):
        pdb.set_trace()
        item = ChainItem()
        try:
            item['name'] = response.xpath('//span[@class="ctcd-user-name"]/text()').extract_first()
        except Exception as e:
            pdb.set_trace()

        try:
            item['reviews'] = response.xpath('//li[@class="ctcd-item ctcd-item_reviews pfl-fs_13"]/text()').extract_first().split(' ')[0]
        except Exception as e:
            pdb.set_trace()

        try:
            item['sales'] = response.xpath('//li[@class="ctcd-item ctcd-item_sales pfl-fs_13"]/text()').extract_first().split(' ')[0]
        except Exception as e:
            pdb.set_trace()

        try:
            item['address'] = ''.join(response.xpath('//dd[@class="zsg-lg-3-5 profile-information-address"]//text()').extract())
        except Exception as e:
            pdb.set_trace()

        try:
            item['phone_number'] = response.xpath('//dd[@class="zsg-lg-3-5 profile-information-cell"]/text()').extract_first()
        except Exception as e:
            try:
                item['phone_number'] = response.xpath('//dd[@class="zsg-lg-3-5 profile-information-mobile"]/text()').extract_first()
            except Exception as e:
                pdb.set_trace()

            

        urls = response.xpath('//dd[@class="zsg-lg-3-5 profile-information-websites"]/a/@href').extract()

        for url in urls:
            if 'linkedin' in url:
                item['linkedin'] = url
            elif 'facebook' in url:
                item['facebook'] = url
            elif 'twitter' in url:
                print(url)
            else:
                item['website'] = url

        yield item           