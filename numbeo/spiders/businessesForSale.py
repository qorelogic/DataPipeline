
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import BusinessForSaleItem

import pandas as p
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
import sys

def fixNewlines(item, field, kw='\n'):
    try:
        li = item[field]
        li = p.DataFrame(li)
        #srch = li[li[0] == kw]
        srch = li[p.Series(map(lambda x: True if x.strip() == kw.strip() else False, li[0]), index=li.index)]
        #print srch
        for i in list(srch.index):
            li = li.drop(i)
        li[0] = map(lambda x: x.strip(), li[0])
        li[0] = map(lambda x: x.replace(kw, ''), li[0])
        #print li
        item[field] = list(li[0])
    except Exception as e:
        #print e
        ''
    return item

def fixItemsearchReplace(item, field, regex, replace):
    import re
    try:
        li = item[field]
        li = p.DataFrame(li)
        li[0] = map(lambda x: x.strip(), li[0])
        li[0] = map(lambda x: re.sub(re.compile(regex), replace, x), li[0])
        #print li
        item[field] = list(li[0])
    except Exception as e:
        #print e
        ''
    return item

class BusinessesforsaleSpider(CrawlSpider):
    name = 'businessesForSale'
    allowed_domains = ['businessesforsale.com']
    start_urls = []
    #import numpy as n
    #rin = n.random.randint(1,50)
    #start_urls.append('http://www.businessesforsale.com/search/businesses-for-sale-%s?PageSize=50'%rin)
    start_urls.append('http://www.businessesforsale.com/search/businesses-for-sale-1?PageSize=50')

    qs = QoreScrapy()

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'search\/businesses-for-sale-[\d]+\?PageSize=50'), callback='parse_item_businessesforsale', follow=True),
        Rule(SgmlLinkExtractor(allow=r'search\/businesses-for-sale-[\d]+\?PageSize=50$'), callback='parse_item_businessesforsale', follow=True),
    )
    # scrapy shell 'http://www.businessesforsale.com/search/businesses-for-sale-2?PageSize=50'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=businessesForSale -c parse_item_businessesforsale 'http://www.businessesforsale.com/search/businesses-for-sale-2?PageSize=50'
    def parse_item_businessesforsale(self, response):
        hxs = HtmlXPathSelector(response)
        item = BusinessForSaleItem(
            name     = hxs.select('//*[@id="results-wrap"]/div/dl/dt[2]/a/text()').extract(),
            url      = hxs.select('//*[@id="results-wrap"]/div/dl/dt[2]/a/@href').extract(),
            location = hxs.select('//*[@id="results-wrap"]/div/dl/dd[1]/text()').extract(),
            city     = hxs.select('//*[@id="results-wrap"]/div/dl/dd[1]/text()').extract(),
            country  = hxs.select('//*[@id="results-wrap"]/div/dl/dd[1]/text()').extract(),
            price    = hxs.select('//*[@id="results-wrap"]/div/dl/dd[2]/ul/li[1]/span/../text()').extract(),
            currency = hxs.select('//*[@id="results-wrap"]/div/dl/dd[2]/ul/li[1]/span/../text()').extract(),
            revenue  = hxs.select('//*[@id="results-wrap"]/div/dl/dd[2]/ul/li[2]/span/../text()').extract(),
            cashflow = hxs.select('//*[@id="results-wrap"]/div/dl/dd[2]/ul/li[3]/span/../text()').extract(),
            description = hxs.select('//*[@id="results-wrap"]/div/dl/dd[3]/text()').extract(),
        )

        item = fixNewlines(item, 'price',    '\r\n')
        item = fixNewlines(item, 'currency',    '\r\n')

        item = fixItemsearchReplace(item, 'currency', r',', '')
        item = fixItemsearchReplace(item, 'currency', r'[\d]', '')
        
        item = fixNewlines(item, 'revenue',  '\r\n')
        item = fixNewlines(item, 'cashflow', '\r\n')
        item = fixNewlines(item, 'description', '\r\n')
        
        
        try: item['city']    = map(lambda x: x.split(',')[0].strip(), item['city'])
        except: ''
        try: item['country'] = map(lambda x: x.split(',')[1].strip(), item['country'])
        except: ''

        item = self.qs.makeItems(item, 'numbeo.items.BusinessForSaleItem')
        return item
