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

class ChainxyPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_%s.csv' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        # self.exporter.fields_to_export = ['company_name','contact','phone1','phone2','email','average','reviews','address','member_for','based_in']
        self.exporter.fields_to_export = [
            'reference_number',
            'driving_dircetion_to_well',
            'date_completed',
            'well_use',
            'drilling_method',
            'pump_type',
            'depth',
            'pump_setting_depth',
            'water_quality',
            'casing_length',
            'casing_mateiral',
            'casing_diameter',
            'screen_length',
            'screen_material',
            'screen_diameter',
            'slot_size' ,
            'type_of_test',
            'test_rate',
            'bail_test_rate',
            'drawdown',
            'static_water_level',
            'bailer_drawdown',
            'material',
            'depth_2',
            'installation_method',
            'number_of_bags_used',
            'sealing_material',
            'well_abandonment_depth',
            'installation_method_2',
            'number_of_bags_used_2',
            'county',
            'township',
            'range',
            'section',
            'topo_map',
            'grant',
            'field_located_by',
            'field_located_on',
            'courthouse_location_by',
            'courthouse_location_on',
            'location_accepted_verification_by',
            'location_accepted_verification_on',
            'subdivision_name',
            'lot_number',
            'ft_w_of_el',
            'ft_n_of_sl',
            'ft_e_of_wl',
            'ft_s_of_nl',
            'ground_elevation',
            'depth_of_bedrock',
            'bedrock_elevation',
            'aquifer_elevation',
            'utm_easting',
            'utm_northing'
            ]
        self.exporter.start_exporting()        

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item