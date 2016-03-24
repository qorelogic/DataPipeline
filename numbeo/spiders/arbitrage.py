# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import ArbitrageItem

import sys, re
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class ArbitrageSpider(CrawlSpider):
    name = "arbitrage"
    allowed_domains = ["cryptocoincharts.info"]
    start_urls = ['http://www.cryptocoincharts.info/']
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/arbitrage'), callback='parse_item', follow=False),
    )

    # scrapy parse --spider=arbitrage -c parse_item 'http://www.cryptocoincharts.info/arbitrage'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = ArbitrageItem(
            profit = hxs.xpath('/html/body/div[1]/div/div[2]/p/b[3]/text()').extract(),
            amount = hxs.xpath('/html/body/div[1]/div/div[2]/p/b[3]/text()').extract(),
            unit   = hxs.xpath('/html/body/div[1]/div/div[2]/p/b[3]/text()').extract(),
            buy    = hxs.xpath('/html/body/div[1]/div/div[2]/p/b[1]/text()').extract(),
            trade  = hxs.xpath('/html/body/div[1]/div/div[1]/b[1]/text()').extract(),
            time   = hxs.xpath('/html/body/div[1]/div/div[1]/span/b/text()').extract(),
            fromCoin = hxs.xpath('/html/body/div[1]/div/div[1]/b[2]/text()').extract(),
            toCoin   = hxs.xpath('/html/body/div[1]/div/div[1]/b[3]/text()').extract(),
            highestBid   = hxs.xpath('/html/body/div[1]/div/div[2]/div/div[1]/div/text()').extract(),
            lowestAsk    = hxs.xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/text()').extract(),
            spread       = hxs.xpath('/html/body/div[1]/div/div[2]/div/div[3]/div/text()').extract(),
            maximumVolume = hxs.xpath('/html/body/div[1]/div/div[2]/div/div[4]/div/text()').extract(),
        )
        
        for i in xrange(len(item['amount'])):
            item['amount'][i] = re.sub(re.compile(r'.*?([\d\.]+).*?([\w]+)'), '\\1', item['amount'][i].strip())
        item['unit']   = item['unit']
        for i in xrange(len(item['unit'])):
            item['unit'][i] = re.sub(re.compile(r'.*?([\d\.]+).*?([\w]+)'), '\\2', item['unit'][i].strip())
        for i in xrange(len(item['profit'])):
            #item['volume'][i] = item['volume'][i].strip().replace('\xc2\xa0', ' ')
            item['profit'][i] = re.sub(re.compile(r'.*?([\d\.]+).*?([\w]+)'), '\\1 \\2', item['profit'][i].strip())
        item['source'] = ['cryptocoincharts.info'] * len(item['profit'])
        
        item = self.qs.makeItems(item, 'numbeo.items.ArbitrageItem')
        print item
        return item

