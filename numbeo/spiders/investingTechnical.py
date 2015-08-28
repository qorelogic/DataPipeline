# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import InvestingtechnicalItem

import sys, time
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

def parseSt(st):
    di = {}
    di['60'] = 1 
    di['300'] = 5
    di['900'] = 15
    di['1800'] = 30
    di['3600'] = 60
    di['18000'] = 300
    di['86400'] = 86400/60
    di['week'] = 86400 * 7
    di['month'] = 60*60*24*31
    return str(di[str(st)])

class InvestingtechnicalSpider(CrawlSpider):
    name = 'investingTechnical'
    allowed_domains = ["investing.com"]
    qs = QoreScrapy()
    
    #self.start_urls = ['http://www.investing.com/quotes/single-currency-crosses']
    start_urls = [
        'http://www.investing.com/currencies/eur-usd-technical?period=60',   
        'http://www.investing.com/currencies/gbp-usd-technical?period=60',    
        'http://www.investing.com/currencies/usd-jpy-technical?period=60',    
        'http://www.investing.com/currencies/aud-usd-technical?period=60',    
        'http://www.investing.com/currencies/usd-cad-technical?period=60',    
        'http://www.investing.com/currencies/eur-jpy-technical?period=60',   
        'http://www.investing.com/currencies/eur-chf-technical?period=60',   

        'http://www.investing.com/currencies/nzd-usd-technical?period=60',
        'http://www.investing.com/currencies/eur-gbp-technical?period=60',
        'http://www.investing.com/currencies/gbp-jpy-technical?period=60',
        'http://www.investing.com/currencies/eur-aud-technical?period=60',   
        'http://www.investing.com/currencies/eur-cad-technical?period=60',   
        'http://www.investing.com/currencies/aud-jpy-technical?period=60',   
        'http://www.investing.com/currencies/chf-jpy-technical?period=60',   
        'http://www.investing.com/currencies/usd-hkd-technical?period=60',   
        'http://www.investing.com/currencies/usd-rub-technical?period=60',   
        'http://www.investing.com/currencies/usd-cnh-technical?period=60',   
        'http://www.investing.com/currencies/aud-chf-technical?period=60',   
        'http://www.investing.com/currencies/aud-cad-technical?period=60',
        'http://www.investing.com/currencies/aud-nzd-technical?period=60',   
        'http://www.investing.com/currencies/eur-nzd-technical?period=60',   
        'http://www.investing.com/currencies/gbp-aud-technical?period=60',
        'http://www.investing.com/currencies/gbp-chf-technical?period=60',
        'http://www.investing.com/currencies/gbp-nzd-technical?period=60',
        'http://www.investing.com/currencies/nzd-cad-technical?period=60',
        'http://www.investing.com/currencies/nzf-chf-technical?period=60',
        'http://www.investing.com/currencies/nzd-jpy-technical?period=60',
        'http://www.investing.com/currencies/cad-chf-technical?period=60',
        'http://www.investing.com/currencies/xau-usd-technical?period=60',
        'http://www.investing.com/currencies/xag-usd-technical?period=60',
    ]

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'/currencies/[\w]{3}-[\w]{3}'), follow=True),
        #Rule(SgmlLinkExtractor(allow=r'/currencies/[\w]{3}-[\w]{3}-technical'), follow=True),
        Rule(SgmlLinkExtractor(allow=r'/currencies/[\w]{3}-[\w]{3}-technical\?period=[\w\d]+'), callback='parse_item', follow=False),
    )

    # scrapy parse --spider=investingTechnical -c parse_item 'http://www.investing.com/currencies/eur-usd-technical?period=60'
    # scrapy shell 'http://www.investing.com/currencies/eur-usd-technical?period=60'
    # response.xpath('//*[@id="techStudiesInnerBoxRightBottom"]/div[1]/span/text()')
    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        item = InvestingtechnicalItem(
            name    = hxs.select('//*[@id="leftColumn"]/h1/text()').extract(),
            summary = hxs.select('//*[@id="techStudiesInnerBoxRightBottom"]/div[1]/span/text()').extract(),
            period  = [response.url],
        )
        
        for i in xrange(len(item['period'])):
            item['name'][i] = item['name'][i].split(' ')[0]
            item['period'][i] = parseSt(item['period'][i].split('=')[1])
        
        item = self.qs.makeItems(item, 'numbeo.items.InvestingtechnicalItem')
        #print item
        return item
