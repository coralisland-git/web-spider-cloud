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

        table_name_icomps = 'parcel_estimate_icomps'

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
                owner_addr varchar(50) ,
                owner_city varchar(30),
                owner_state varchar(20),
                owner_zip varchar(20),
                site_addr varchar(50) ,
                site_city varchar(30),
                site_state varchar(20),
                site_zip varchar(20),
                bed varchar(20),
                bath varchar(20),
                square_footage varchar(20),
                zestimate varchar(20),
                active varchar(20),
                icomps varchar(20),
                redfin varchar(20),
                trulia varchar(20)
                );""" %table_name

            cur.execute(_SQL)


    def spider_closed(self, spider):

        self.db.close()

    def process_item(self, item, spider):

        cur = self.db.cursor()

        check_query = "select * from parcel_estimate where folio='%s'" %item['Folio']

        count = cur.execute(check_query)

        if count == 0:

            sql = "INSERT INTO parcel_estimate " 

            sql += "(folio, pin, owner, owner_addr, owner_city, owner_state, owner_zip, site_addr, site_city, site_state, site_zip, bed, bath, square_footage, zestimate, active, icomps, redfin, trulia) "

            sql += "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); " %(item['Folio'], item['Pin'], item['Owner'], item['Owner_Addr'], item['Owner_City'], item['Owner_State'], item['Owner_Zip'], item['Site_Addr'], item['Site_City'], item['Site_State'], item['Site_Zip'], item['Bed'], item['Bath'], item['Square_Footage'], item['Zestimate'], item['Active'], item['Icomps'], item['Redfin'], item['Trulia'])

        else :

            sql = "UPDATE parcel_estimate SET folio='%s', pin='%s', owner='%s', owner_addr='%s', owner_city='%s', owner_state='%s', owner_zip='%s', site_addr='%s', site_city='%s', site_state='%s', site_zip='%s', bed='%s', bath='%s', square_footage='%s', "

            sql += " zestimate='%s', active='%s', icomps='%s', redfin='%s', trulia='%s' WHERE folio='%s'"

            sql = sql %(item['Folio'], item['Pin'], item['Owner'], item['Owner_Addr'], item['Owner_City'], item['Owner_State'], item['Owner_Zip'], item['Site_Addr'], item['Site_City'], item['Site_State'], item['Site_Zip'], item['Bed'], item['Bath'], item['Square_Footage'], item['Zestimate'], item['Active'], item['Icomps'], item['Redfin'], item['Trulia'] , item['Folio'])


        cur.execute(sql)

        self.db.commit()

        return item