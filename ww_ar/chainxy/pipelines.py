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

        self.file.main_table_headers = ['well_id', 'date_completed', 'well_depth', 'well_yield', 'use_type', 'remarks']

        for index, header in enumerate(self.file.main_table_headers):

            self.file.main_table.write(0, index, header)
            

        self.file.table_a = workbook.add_worksheet('Table A')

        self.file.table_a_headers = ['well_id', 'contractor_name', 'contractor_number', 'driller_name', 'driller_number', 'pump_installer_name', 'pump_installer_number', 'date_well_completed', 'country', 'fraction', 'section', 'township', 'range', 'longitude', 'latitude']

        for index, header in enumerate(self.file.table_a_headers):

            self.file.table_a.write(0, index, header)


    def spider_closed(self, spider):

        self.file.close()


    def process_item(self, item, spider):

        for key, value in item.items():

            if key in self.file.main_table_headers:

                self.file.main_table.write(self.count, self.file.main_table_headers.index(key) , value)

            if key in self.file.table_a_headers:

                self.file.table_a.write(self.count, self.file.table_a_headers.index(key) , value)

        self.count += 1

        return item
