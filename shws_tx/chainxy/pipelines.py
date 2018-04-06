# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

import time

import datetime

from scrapy import signals

from scrapy.contrib.exporter import CsvItemExporter

import pdb

import xlsxwriter

class ChainxyPipeline(object):

    def __init__(self):

        self.file = {}

        self.count = 1

    @classmethod

    def from_crawler(cls, crawler):

        pipeline = cls()

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)

        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline

    def spider_opened(self, spider):
        
        workbook=xlsxwriter.Workbook('%s_%s.xlsx' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')))

        self.file = workbook

        self.file.main_table = workbook.add_worksheet('Main Table')

        self.file.main_table_headers =  [
            
            'facility_name', 'status', 'type_of_facility', 'site_link', 'location', 'latitude', 'longitude', 'site_phase', 'hazard_ranking_score', 'contaminants', 'state_superfund_registry_status', 'media_affected', 'tceq_region', 'funded_by', 'contacts', 'records_repositories', 'tceq_central_file_room', 'site_details'
        
        ]

        for index, header in enumerate(self.file.main_table_headers):

            self.file.main_table.write(0, index, self.capitalize(header))
        

    def spider_closed(self, spider):

        self.file.close()


    def process_item(self, item, spider):

        for key, value in item.items():

            if key in self.file.main_table_headers:

                self.file.main_table.write(self.count, self.file.main_table_headers.index(key) , value)


        self.count += 1

        return item

    def capitalize(self, item):
        try:
            item = item.replace('_', ' ').title()
            return item
        except:
            pass