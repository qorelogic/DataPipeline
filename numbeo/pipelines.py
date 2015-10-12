# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.contrib.exporter import CsvItemExporter

import pymongo
from settings import *

class NumbeoPipeline(object):

    def __init__(self):
        self.proj = BOT_NAME

    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(NumbeoPipeline):

    def __init__(self):
        super(JsonWithEncodingPipeline, self).__init__()
        self.suffix = 'json'
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('{0}_{1}.{2}'.format(spider.name, self.proj, self.suffix), 'w+b')
        self.files[spider] = file
        #self.exporter = JsonItemExporter(file)
        self.exporter = JsonLinesItemExporter(file)        
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class CsvExportPipeline(NumbeoPipeline):

    def __init__(self):
        super(CsvExportPipeline, self).__init__()
        self.suffix = 'csv'
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('{0}_{1}.{2}'.format(spider.name, self.proj, self.suffix), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)        
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MongoDBBrokerPipeline(NumbeoPipeline):
    def __init__(self):
        super(MongoDBBrokerPipeline, self).__init__()
	try:
	        connection = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
	except Exception as e:
		print e
		return
        self.db = connection[MONGODB_DB]
        self.collections = {}
        self.collections['propertyPrices'] = self.db['propertyPrices']
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.collections[spider.name] = self.db[spider.name]
        # remove all for clean insertion
        #if spider.name != 'trades' and spider.name != 'brokers':
        #self.collections[spider.name].remove()

    def spider_closed(self, spider):
        stub=''

    def process_item(self, item, spider):
        #if not isinstance(item, items.ProfitlyItem):
        #return item # return the item to let other pipeline to handle it
        try: self.collections[spider.name].insert(dict(item))
	except Exception as e: 
		print e
		item
        return item # return the item to let other pipeline to handle it

from scrapy import log
from pysqlite2 import dbapi2 as sqlite
# This pipeline takes the Item and stuffs it into scrapedata.db
class SQLitePipeline(object):
    
    database = MONGODB_DB
    
    def __init__(self):
        # Possible we should be doing this in spider_open instead, but okay
        self.connection = sqlite.connect('./'+self.database+'.sqlite')
        self.cursor = self.connection.cursor()
        #self.collections['brokers'] = self.db['brokers']

        dispatcher.connect(self.spider_opened, signals.spider_opened)
        #dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        #self.collections[spider.name] = self.db[spider.name]
        # remove all for clean insertion
        self.cursor.execute('drop table if exists '+spider.name)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '+spider.name+' ( '+\
            'id INTEGER PRIMARY KEY, '+ \
            'city VARCHAR(80), '+ \
            'priceToIncomeRatio float(80), '+ \
            'grossRentalYieldCityCentre float(80), '+ \
            'grossRentalYieldOutsideOfCentre float(80), '+ \
            'priceToRentRatioCityCentre float(80), '+ \
            'priceToRentRatioOutsideOfCityCentre float(80), '+ \
            'mortgageAsAPercentageOfIncome float(80), '+ \
            'affordabilityIndex float(80) '+ \
            ')')

    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        """
        self.cursor.execute("select * from "+spider.name+" where company=?", item['company'])
        result = self.cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
        else:
        """
        print item
        try:
            self.cursor.execute(
                "insert into {0} (city, priceToIncomeRatio, grossRentalYieldCityCentre, grossRentalYieldOutsideOfCentre, priceToRentRatioCityCentre, priceToRentRatioOutsideOfCityCentre, mortgageAsAPercentageOfIncome, affordabilityIndex) values (?, ?, ?, ?, ?, ?, ?, ?)".format(spider.name),
                    (item['city'], item['priceToIncomeRatio'], item['grossRentalYieldCityCentre'], item['grossRentalYieldOutsideOfCentre'], item['priceToRentRatioCityCentre'], item['priceToRentRatioOutsideOfCityCentre'], item['mortgageAsAPercentageOfIncome'], item['affordabilityIndex']))
            self.connection.commit()
        except:
            ''
            #import sys
            #sys.exit()

        log.msg("Item stored : " % item, level=log.DEBUG)
        return item

    def handle_error(self, e):
        log.err(e)
