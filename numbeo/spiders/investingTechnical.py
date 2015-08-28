# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import InvestingtechnicalItem

import sys, time
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class InvestingtechnicalSpider(CrawlSpider):
    name = 'investingTechnical'
    allowed_domains = ["investing.com"]
    time.time()
    start_urls = ['http://www.investing.com/quotes/single-currency-crosses']
    #start_urls = ['http://www.investing.com/currencies/eur-usd-technical?period=60']
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/currencies/[\w^-]+-[\w^-]+'), follow=True),
        Rule(SgmlLinkExtractor(allow=r'/currencies/[\w^-]+-[\w^-]+-technical'), follow=True),
        Rule(SgmlLinkExtractor(allow=r'/currencies/[\w^-]+-[\w^-]+-technical\?period=[\w\d]+'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=investingTechnical -c parse_item 'http://www.investing.com/currencies/eur-usd-technical?period=60'
    # scrapy shell 'http://www.investing.com/currencies/eur-usd-technical?period=60'
    # response.xpath('//*[@id="techStudiesInnerBoxRightBottom"]/div[1]/span/text()')
    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        item = InvestingtechnicalItem(
            name    = hxs.select('//*[@id="leftColumn"]/h1/text()').extract(),
            summary = hxs.select('//*[@id="techStudiesInnerBoxRightBottom"]/div[1]/span/text()').extract(),
            period  = hxs.select('//title/text()').extract(),
                                 
        )
        
        def parseName(tt):
            tt = tt.split(' ')
            ret = []
            ret.append(' '.join(tt[0:len(tt)-1]))
            ret.append(tt[len(tt)-1])
            return ret
        
        """
        for i in xrange(len(item['period'])):
            item['period'][i] = item['period'][i].split(' ')[5:]
        """
        
        item = self.qs.makeItems(item, 'numbeo.items.InvestingtechnicalItem')
        #print item
        return item
