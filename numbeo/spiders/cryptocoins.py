
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import CryptocoinsItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class CryptocoinsSpider(CrawlSpider):
    name = 'cryptocoins'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['http://coinmarketcap.com/currencies/views/all/']
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/currencies/views/all'), callback='parse_item', follow=False),
    )

    # scrapy parse --spider=cryptocoins -c parse_item 'http://coinmarketcap.com//currencies/views/all/'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = CryptocoinsItem(
            name = hxs.select('//tr/td[2]/a/text()').extract(),
            code = hxs.select('//tr/td[3]/text()').extract(),
            marketcap = hxs.select('//table/tbody/tr/td[4]/@data-usd').extract(),
            price = hxs.select('//table/tbody/tr/td[5]/a/@data-usd').extract(),
            available_supply = hxs.select('//table/tbody/tr/td[6]/a/text()').extract(),
            volume = hxs.select('//table/tbody/tr/td[7]/a/@data-usd').extract(),
            percent_1hr = hxs.select('//table/tbody/tr/td[8]/@data-usd').extract(),
            percent_24hr = hxs.select('//table/tbody/tr/td[9]/@data-usd').extract(),
            percent_7days = hxs.select('//table/tbody/tr/td[10]/@data-usd').extract(),
        )
        
        for i in xrange(len(item['available_supply'])):
            item['available_supply'][i] = item['available_supply'][i].strip().replace(',','')
        
        item = self.qs.makeItems(item, 'numbeo.items.CryptocoinsItem')
        #print item
        return item
