# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import InvestingworldgovernmentbondsItem

import sys, time
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
from qore import fetchURL
from pandas import DataFrame as p_DataFrame

def parseName(tt):
    tt = tt.split(' ')
    ret = []
    ret.append(' '.join(tt[0:len(tt)-1]))
    ret.append(tt[len(tt)-1])
    return ret

import xmltodict #, json
class ISO:
    
    def __init__(self):
        
        # source: http://www.iso.org/iso/home/standards/currency_codes.htm,
        #         http://www.currency-iso.org/en/home/tables/table-a1.html
        xml = fetchURL('http://www.currency-iso.org/dam/downloads/lists/list_one.xml', mode='')
        #print xml
        
        # source: http://stackoverflow.com/questions/191536/converting-xml-to-json-using-python
        o = xmltodict.parse(xml)
        #js = json.dumps(o)
        
        self.di = o['ISO_4217']['CcyTbl'][u'CcyNtry']
        #print di
        
    def countryName2CurrencyCode(self, countryName):
        return p_DataFrame(self.di).set_index('CtryNm').ix[countryName.upper(),'Ccy']


class InvestingworldgovernmentbondsSpider(CrawlSpider):
    name = 'investingWorldGovernmentBonds'
    allowed_domains = ["investing.com"]
    time.time()
    start_urls = ['http://www.investing.com/rates-bonds/world-government-bonds']
    qs = QoreScrapy()

    rules = (
    #http://www.investing.com/rates-bonds/government-bond-spreads
        Rule(SgmlLinkExtractor(allow=r'/rates-bonds/world-government-bonds'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=investingWorldGovernmentBonds -c parse_item 'http://www.investing.com/rates-bonds/world-government-bonds'
    # scrapy shell 'http://www.investing.com/rates-bonds/world-government-bonds'
    # response.xpath('//section/table//td[2]/a/text()').extract()
    def parse_item(self, response):

        timestamp = time.time()
        
        hxs = HtmlXPathSelector(response)
        item = InvestingworldgovernmentbondsItem(
            name     = hxs.xpath('//section/table//td[2]/a/text()').extract(),
            country  = hxs.xpath('//section/table//td[2]/a/text()').extract(),
            currencyCode  = hxs.xpath('//section/table//td[2]/a/text()').extract(),
            period   = hxs.xpath('//section/table//td[2]/a/text()').extract(),
            iyield   = hxs.xpath('//section/table//td[3]/text()').extract(),
            prev     = hxs.xpath('//section/table//td[4]/text()').extract(),
            high     = hxs.xpath('//section/table//td[5]/text()').extract(),
            low      = hxs.xpath('//section/table//td[6]/text()').extract(),
            chg      = hxs.xpath('//section/table//td[7]/text()').extract(),
            chgpcnt  = hxs.xpath('//section/table//td[8]/text()').extract(),
            time     = hxs.xpath('//section/table//td[9]/text()').extract(),
            timestamp = hxs.xpath('//section/table//td[9]/text()').extract(), # stub
        )
        
        iso = ISO()
        #iso.countryName2CurrencyCode
        
        for i in xrange(len(item['chg'])):
            item['chg'][i]     = item['chg'][i].replace('+','')
            item['chgpcnt'][i] = item['chgpcnt'][i].replace('+','').replace('%','')
            item['country'][i] = parseName(item['country'][i])[0]
            item['currencyCode'][i] = parseName(item['currencyCode'][i])[0]
            item['period'][i]       = parseName(item['period'][i])[1]
            item['timestamp'][i]    = str(timestamp)
        
        item = self.qs.makeItems(item, 'numbeo.items.InvestingworldgovernmentbondsItem')
        #print item
        return item

# www.teletrader.com/currencies www.forexmillion.com/ www.investing.com/analysis/forex www.bloomberg.com/markets www.dailyfx.com/forex_market_news/forecasts www.actionforex.com/action-insight/ www.forexcrunch.com/category/forex-weekly-outlook/ www.forecasts.org/exchange-rate/index.htm
# http://darkpoolfx.net/