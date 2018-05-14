# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals

import MySQLdb

import pdb

class ChainxyPipeline(object):

    def __init__(self):

        self.db = ''

    @classmethod

    def from_crawler(cls, crawler):

        pipeline = cls()

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)

        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline

    def spider_opened(self, spider):

        self.db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="zillow_db")       

        cur = self.db.cursor()

        table_name = 'parcel_estimate'

        _SQL = """SHOW TABLES"""

        cur.execute(_SQL)

        results = cur.fetchall()

        print('All existing tables: ', results) # Returned as a list of tuples

        results_list = [item[0] for item in results] 

        if table_name in results_list:

            print(table_name, 'was found!')

        else:

            print(table_name, 'was NOT found!')

            _SQL = """CREATE TABLE %s (
                id int auto_increment not null primary key,
                folio varchar(10),
                pin varchar(50),
                owner varchar(100),
                site_addr varchar(50) ,
                site_city varchar(30),
                site_state varchar(20),
                site_zip varchar(20),
                bed int(11),
                bath int(11),
                square_footage int(11),
                zestimate int(20),
                mark varchar(20)
                );""" %table_name

            cur.execute(_SQL)


    def spider_closed(self, spider):

        self.db.close()

    def process_item(self, item, spider):

        cur = self.db.cursor()

        sql = "INSERT INTO parcel_estimate " 

        sql += "(folio, pin, owner, site_addr, site_city, site_state, site_zip, bed, bath, square_footage, zestimate, mark) "

        sql += "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s' ); " %(item['Folio'], item['Pin'], item['Owner'], item['Site_Addr'], item['Site_City'], item['Site_State'], item['Site_Zip'], item['Bed'], item['Bath'], item['Square_Footage'], item['Zestimate'], item['Mark']);

        cur.execute(sql)

        self.db.commit()

        return item