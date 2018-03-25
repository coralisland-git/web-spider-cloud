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

        self.file.main_table_headers = ['ministry_reference_number', 'ebr_registry_number', 'company_name', 'instrument_type', 'notice_type', 'notice_date', 'proposal_date', 'proposal_address', 'related_locations']

        for index, header in enumerate(self.file.main_table_headers):

            self.file.main_table.write(0, index, header)

   
    def spider_closed(self, spider):

        self.file.close()


    def process_item(self, item, spider):

        for key, value in item.items():

            if key in self.file.main_table_headers:

                self.file.main_table.write(self.count, self.file.main_table_headers.index(key) , value)

        self.count += 1

        return item
