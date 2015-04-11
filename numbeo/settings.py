# Scrapy settings for numbeo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'numbeo'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['numbeo.spiders']
NEWSPIDER_MODULE = 'numbeo.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = {
    BOT_NAME+'.pipelines.CsvExportPipeline': 2000,
    BOT_NAME+'.pipelines.JsonWithEncodingPipeline': 3000,
    #BOT_NAME+'.pipelines.PrintPipeline': 300,
    #BOT_NAME+'.pipelines.XmlExportPipeline': 300,
    BOT_NAME+'.pipelines.MongoDBBrokerPipeline':3001,
    BOT_NAME+'.pipelines.SQLitePipeline':3002,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = BOT_NAME # db name
