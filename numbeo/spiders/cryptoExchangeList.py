
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import CryptoexchangelistItem
from numbeo.items import CryptoexchangelistCoinsItem

import sys, re
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class CryptoexchangelistSpider(CrawlSpider):
    name = "cryptoExchangeList"
    allowed_domains = ["cryptocoincharts.info"]
    start_urls = ['http://www.cryptocoincharts.info/']
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/markets/info'), callback='parse_item', follow=False),
        Rule(SgmlLinkExtractor(allow=r'/coins/info'), callback='parse_item_CryptoexchangelistCoins', follow=True),
        Rule(SgmlLinkExtractor(allow=r'/coins/info/101-to-1000'), callback='parse_item_CryptoexchangelistCoins', follow=True),
        Rule(SgmlLinkExtractor(allow=r'/coins/info/1001'), callback='parse_item_CryptoexchangelistCoins', follow=True),
    )

    # scrapy parse --spider=cryptoExchangeList -c parse_item 'http://www.cryptocoincharts.info/markets/info'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = CryptoexchangelistItem(
            name = hxs.select('//*[@id="tableMarkets"]/tbody/tr/td[1]/a/text()').extract(),
            code = hxs.select('//*[@id="tableMarkets"]/tbody/tr/td[1]/a/@href').extract(),
            tradingPairs = hxs.select('//*[@id="tableMarkets"]/tbody/tr/td[3]/span/text()').extract(),
            volume = hxs.select('//*[@id="tableMarkets"]/tbody/tr/td[4]/text()').extract(),
        )
        
        #for i in xrange(len(item['available_supply'])):
        #    item['available_supply'][i] = item['available_supply'][i].strip().replace(',','')
        item['type'] = ['exchange'] * len(item['code'])
        
        item = self.qs.makeItems(item, 'numbeo.items.CryptoexchangelistItem')
        print item
        return item

    # scrapy parse --spider=cryptoExchangeList -c parse_item_CryptoexchangelistCoins 'http://www.cryptocoincharts.info/coins/info'
    def parse_item_CryptoexchangelistCoins(self, response):
        hxs = HtmlXPathSelector(response)
        item = CryptoexchangelistCoinsItem(
            name = hxs.select('//*[@id="tableCoins"]/tbody/tr/td[2]/text()').extract(),
            symbol = hxs.select('//*[@id="tableCoins"]/tbody/tr/td[1]/a/text()').extract(),
            minedCoins = hxs.select('//*[@id="tableCoins"]/tbody/tr/td[3]/text()').extract(),
            difficulty = hxs.select('//*[@id="tableCoins"]/tbody/tr/td[4]/text()').extract(),
            volume = hxs.select('//*[@id="tableCoins"]/tbody/tr/td[6]/text()').extract(),
        )
        
        for i in xrange(len(item['volume'])):
            #item['volume'][i] = item['volume'][i].strip().replace('\xc2\xa0', ' ')
            item['volume'][i] = re.sub(re.compile(r'([\d\.]+).*?([\w]+)'), '\\1 \\2', item['volume'][i].strip())
        item['type'] = ['coin'] * len(item['symbol'])
        
        item = self.qs.makeItems(item, 'numbeo.items.CryptoexchangelistCoinsItem')
        print item
        return item
