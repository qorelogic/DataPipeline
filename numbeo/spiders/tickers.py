
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import TickersItem

import pandas as p
import re
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
from qore import XPath

# http://stackoverflow.com/questions/5246843/how-to-get-a-complete-list-of-ticker-symbols-from-yahoo-finance
class TickersSpider(CrawlSpider):
    name = 'tickers'
    allowed_domains = ['eoddata.com']
    start_urls = []
    li = 'AMEX AMS ASX BRU CBOT CFE CME COMEX EUREX FOREX HKEX INDEX KCBT LIFFE LIS LSE MGEX MLSE MSE NASDAQ NYBOT NYMEX NYSE NZX OTCBB PAR SGX TSX TSVX USMF WCE'
    for i in li.split(' '):
        start_urls.append('http://www.eoddata.com/stocklist/%s/A.htm' % i)

    qs = QoreScrapy()
    xp = XPath()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'stocklist\/[\w]+/[\w]+\.htm$'), callback='parse_item_tickers', follow=True),
    )
    # scrapy shell 'http://www.eoddata.com/stocklist/NYSE/A.htm'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=businessesForSale -c parse_item_tickers 'http://www.eoddata.com/stocklist/NYSE/A.htm'
    def parse_item_tickers(self, response):
        hxs = HtmlXPathSelector(response)
        item = TickersItem(
            symbol   = hxs.select('//table[@class="quotes"]//tr[@class="ro" or @class="re"]/td[1]/a/text()').extract(),
            name     = hxs.select('//table[@class="quotes"]//tr[@class="ro" or @class="re"]/td[2]/text()').extract(),
            exchange = hxs.select('/html/head/title/text()').extract(),
        )

        item['exchange'] = [item['exchange'][0]] * len(item['symbol'])
        item['exchange'] = map(lambda x: re.sub(re.compile(r'.+?\[([\w]+)\].+'), '\\1', x), item['exchange'])

        item = self.xp.fixNewlines(item, 'exchange',    '\r\n')

        item = self.qs.makeItems(item, 'numbeo.items.TickersItem')
        return item
