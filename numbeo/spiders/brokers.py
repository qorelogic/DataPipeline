
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import BrokerItem

import pandas as p
import re
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
from qore import XPath

class BrokersSpider(CrawlSpider):
    name = 'brokers'
    allowed_domains = ['londonstockexchange.com']
    start_urls = []
    for i in '0 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' '):
        start_urls.append('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/tools-and-services/find-a-broker/locate-a-broker-results.html?initial=%s' % i)
    #start_urls.append('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/tools-and-services/find-a-broker/locate-a-broker-results.html?initial=A')

    qs = QoreScrapy()
    xp = XPath()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'exchange\/prices-and-markets\/stocks\/tools-and-services\/find-a-broker\/locate-a-broker-results\.html\?initial=[\w]$'), callback='parse_item_brokers', follow=True),
        Rule(SgmlLinkExtractor(allow=r'exchange\/prices-and-markets\/stocks\/tools-and-services\/find-a-broker\/locate-a-broker-detail\.html\?brokerId=[\d]+$'), callback='parse_item_detail', follow=False),
    )
    # scrapy shell 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/tools-and-services/find-a-broker/locate-a-broker-results.html?initial=A'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=brokers -c parse_item_brokers 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/tools-and-services/find-a-broker/locate-a-broker-results.html?initial=A'
    def parse_item_brokers(self, response):
        hxs = HtmlXPathSelector(response)
        item = BrokerItem(
            name  = hxs.select('//*[@id="fullcontainer"]/div[1]/table/tbody/tr/td/a/text()').extract(),
            url   = hxs.select('//*[@id="fullcontainer"]/div[1]/table/tbody/tr/td/a/@href').extract(),
        )

        #item['exchange'] = [item['exchange'][0]] * len(item['symbol'])
        #item['exchange'] = map(lambda x: re.sub(re.compile(r'.+?\[([\w]+)\].+'), '\\1', x), item['exchange'])

        item = self.xp.fixNewlines(item, 'name',    '\r\n')

        item = self.qs.makeItems(item, 'numbeo.items.BrokerItem')
        return item

    # scrapy shell 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/tools-and-services/find-a-broker/locate-a-broker-detail.html?brokerId=300'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=brokers -c parse_item_detail 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/tools-and-services/find-a-broker/locate-a-broker-detail.html?brokerId=300'
    def parse_item_detail(self, response):
        hxs = HtmlXPathSelector(response)
        item = BrokerItem(
            name    = hxs.select('//*[@id="fullcontainer"]/div[1]/table//tr/td[1]/table/tr/td/b').extract(),
            website = hxs.select('//*[@id="fullcontainer"]/div[1]/table//tr/td[1]/table/tr/td/a/@href').extract(),
            address = hxs.select('//*[@id="fullcontainer"]/div[1]/table//tr/td[1]/table/tr/td').extract(),
        )

        #item['exchange'] = [item['exchange'][0]] * len(item['symbol'])
        #item['exchange'] = map(lambda x: re.sub(re.compile(r'.+?\[([\w]+)\].+'), '\\1', x), item['exchange'])

        item = self.xp.fixNewlines(item, 'address',    '\r\n')

        item = self.qs.makeItems(item, 'numbeo.items.BrokerItem')
        return item
