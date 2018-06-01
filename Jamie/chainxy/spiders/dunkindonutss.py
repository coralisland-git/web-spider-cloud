import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

from lxml import html


class DunkindonutsSpider(scrapy.Spider):
    name = "dunkindonuts"

    request_url = 'https://www.mapquestapi.com/search/v2/radius?callback=jQuery1112045193983284142347_1493035174591&key=Gmjtd%7Clu6t2luan5%252C72%253Do5-larsq&origin=$$$city$$$&units=m&maxMatches=4000&radius=3000&hostedData=mqap.33454_DunkinDonuts&ambiguities=ignore&_=1493035174595'
 
    def __init__(self):
        fp = open('cities.json', 'rb')
        self.locations = json.loads(fp.read())

        self.city_list = [
            'New York',
            'Jacksonville',
            'Chicago',
            'Sioux Falls',
            'Dallas',
            'Denver',
            'Nampa',
            'Las Vegas'
        ]

    def get_json_data(self, response_body):
        txt= response_body
        txt=txt[txt.find('(')+1:-2]
        data = json.loads(txt)
        self.all_lists = []
        return data
 
    def get_city(self, city):
        city_string = str(city).replace(' ', '+')
        return city_string.lower()

    def start_requests(self):
        for row in self.locations:
            yield scrapy.Request(url=self.request_url.replace('$$$city$$$', self.get_city(row['city'])))
            
         # for row in self.city_list:
         #    yield scrapy.Request(url=self.request_url.replace('$$$city$$$', self.get_city(row)))

    def parse(self, response):
        data = self.get_json_data(response.body)['searchResults']
        for d_item in data:
            d = d_item['fields']
            if d['phonenumber'] in self.all_lists:
                continue

            self.all_lists.append(d['phonenumber'])
            try:
                item = ChainItem()
                item['store_name'] = d_item['name']
                item['store_number'] = ''
                item['address'] = d["address"]
                item['address2'] = d["address2"]
                item['phone_number'] = d["phonenumber"]
                item['latitude'] = d_item["shapePoints"][0]
                item['longitude'] = d_item["shapePoints"][1]
                item['city'] = d["city"]
                item['state'] = d["state"]
                item['zip_code'] = d["postal"]
                item['country'] = d["country"]
                item['store_hours'] = "MON: " + str(d['mon_hours']) + " TUE: " + str(d['tue_hours']) + " WED: " + str(d['wed_hours']) + " THU: " + str(d['thu_hours']) + " FRI: " + str(d['fri_hours']) + " SAT: " + str(d['sat_hours']) + " SUN: " + str(d['sun_hours'])
                #item['store_type'] = info_json["@type"]
                item['other_fields'] = ""
                item['coming_soon'] = "0"

                yield item

            except:
                continue