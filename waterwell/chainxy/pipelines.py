# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

import time

import datetime

from scrapy import signals

import xlsxwriter

class ChainxyPipeline(object):

    def __init__(self):

        self.files = {}

        self.count = 1

        self.count_well_log = 1

        self.count_owner_contractor = 1

    @classmethod

    def from_crawler(cls, crawler):

        pipeline = cls()

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)

        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline

    def spider_opened(self, spider):

        file = open('%s_%s.xls' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')), 'w+b')

        workbook=xlsxwriter.Workbook('%s_%s.xlsx' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')))

        self.file = workbook

        self.file.well_details_sheet = workbook.add_worksheet('Well Details')

        self.file.well_details_sheet_headers = [

            'reference_number','driving_dircetion_to_well','date_completed','well_use','drilling_method','pump_type','depth','pump_setting_depth','water_quality','casing_length','casing_mateiral','casing_diameter','screen_length','screen_material','screen_diameter','slot_size' ,'type_of_test','test_rate','bail_test_rate','drawdown','static_water_level','bailer_drawdown','material','depth_2',

            'installation_method','number_of_bags_used','sealing_material','well_abandonment_depth','installation_method_2','number_of_bags_used_2','county','township','range','section','topo_map','grant','field_located_by','field_located_on','courthouse_location_by','courthouse_location_on','location_accepted_verification_by','location_accepted_verification_on','subdivision_name','lot_number','ft_w_of_el','ft_n_of_sl','ft_e_of_wl','ft_s_of_nl','ground_elevation','depth_of_bedrock','bedrock_elevation','aquifer_elevation','utm_easting','utm_northing'
            
            ]

        for index, header in enumerate(self.file.well_details_sheet_headers):

            self.file.well_details_sheet.write(0, index, header)

        self.file.owner_contractor_sheet = workbook.add_worksheet('Owner Contractor')

        self.file.owner_contractor_sheet_headers = ['reference_number', 'owner_contractor', 'name', 'address', 'telephone']

        for index, header in enumerate(self.file.owner_contractor_sheet_headers):

            self.file.owner_contractor_sheet.write(0, index, header)

        self.file.well_log_sheet = workbook.add_worksheet('Well Log')

        self.file.well_log_sheet_headers = ['reference_number', 'top', 'bottom', 'formation']

        for index, header in enumerate(self.file.well_log_sheet_headers):

            self.file.well_log_sheet.write(0, index, header)

    def spider_closed(self, spider):

        self.file.close()

    def process_item(self, item, spider):

        well_log_num = 0

        owner_contractor_num = 0

        for key, value in item.items():

            if key in self.file.well_details_sheet_headers:

                self.file.well_details_sheet.write(self.count, self.file.well_details_sheet_headers.index(key) , value)

            if key in self.file.owner_contractor_sheet_headers:

                temp = value.split('-')

                local_count = self.count_owner_contractor

                owner_contractor_num = len(temp)

                for te in temp:

                    self.file.owner_contractor_sheet.write(local_count, self.file.owner_contractor_sheet_headers.index(key) , te)

                    self.file.owner_contractor_sheet.write(local_count, 0 , item['reference_number'])

                    local_count += 1

            if key in self.file.well_log_sheet_headers:

                temp = value.split('-')

                local_count = self.count_well_log

                well_log_num = len(temp)

                for te in temp:
                    
                    self.file.well_log_sheet.write(local_count, self.file.well_log_sheet_headers.index(key) , te)

                    self.file.well_log_sheet.write(local_count, 0 , item['reference_number'])

                    local_count += 1


        self.count += 1

        self.count_well_log += well_log_num

        self.count_owner_contractor += owner_contractor_num

        return item