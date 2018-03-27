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

        self.count_work_reported = 1

        self.count_document = 1

    @classmethod

    def from_crawler(cls, crawler):

        pipeline = cls()

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)

        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline

    def spider_opened(self, spider):
        
        workbook=xlsxwriter.Workbook('%s_%s.xlsx' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')))

        self.file = workbook

        self.file.main_table = workbook.add_worksheet('Summary')

        self.file.main_table_headers = ['log_number', 'log_number_link', 'fac_id', 'site_name', 'address', 'city', 'zip_code', 'county',
                        'summary_information', 'site_name_', 'received_data', 'address_1', 'address_2', 'status', 'tank_type', 'county',
                        'file_status', 'site_type', 'ust_facility_id', 'project_manager', 'cause_of_release', 'source_of_release', 'discovery_method',
                        'media_efected', 'contaminants_released', 'delineate_soil', 'ground_water', 'soil_delineated_release', 'stopped_date',
                        'cleanup_start_date', 'cleanup_end_date'
                        ]

        for index, header in enumerate(self.file.main_table_headers):

            self.file.main_table.write(0, index, header)


        self.file.table_work_reported = workbook.add_worksheet('Work Reported')

        self.file.table_work_reported_headers = ['log_number', 'work_reported', 'reported_date']

        for index, header in enumerate(self.file.table_work_reported_headers):

            self.file.table_work_reported.write(0, index, header)


        self.file.table_document = workbook.add_worksheet('Documents')

        self.file.table_document_headers = ['log_number', 'file_name', 'file_link', 'category', 'file_size_mb', 'upload_date']

        for index, header in enumerate(self.file.table_document_headers):

            self.file.table_document.write(0, index, header)


    def spider_closed(self, spider):

        self.file.close()


    def process_item(self, item, spider):

        work_reported_num = 0

        document_num = 0

        for key, value in item.items():

            if key in self.file.main_table_headers:

                self.file.main_table.write(self.count, self.file.main_table_headers.index(key) , value)

            if key in self.file.table_work_reported_headers and key != 'log_number':

                if value != '':

                    temp = value.split('-')

                    local_count = self.count_work_reported

                    work_reported_num = len(temp)

                    for te in temp:

                        self.file.table_work_reported.write(local_count, self.file.table_work_reported_headers.index(key) , te)

                        self.file.table_work_reported.write(local_count, 0, item['log_number'])

                        local_count += 1


            if key in self.file.table_document_headers and key != 'log_number':

                if value != '':

                    temp = value.split('+')

                    local_count = self.count_document

                    document_num = len(temp)

                    for te in temp:

                        self.file.table_document.write(local_count, self.file.table_document_headers.index(key) , te)

                        self.file.table_document.write(local_count, 0, item['log_number'])

                        local_count += 1

        self.count += 1

        self.count_work_reported += work_reported_num

        self.count_document += document_num

        return item
