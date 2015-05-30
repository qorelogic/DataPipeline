
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import EtoroTickerItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class EtorotickersSpider(CrawlSpider):
    name = 'etoroTickers'
    allowed_domains = ['etoro.com']
    start_urls = [
        #'http://www.etoro.com/',
        #'https://openbook.etoro.com/markets/stocks/',
        'https://openbook.etoro.com/m/markets',
        'https://openbook.etoro.com/m/markets/stocks',
    ]

    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/m/markets/stocks'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'/m/markets/stocks/industry/technology'), callback='parse_item', follow=True),

        #Rule(SgmlLinkExtractor(allow=r'/markets/[\w\.\d]+/[\w\.\d]+'), callback='parse_item', follow=True),
        #Rule(SgmlLinkExtractor(allow=r'/markets/[\w\.\d]+'), callback='parse_markets', follow=True),
    )

    # scrapy parse --spider=etoroTickers -c parse_item 'https://openbook.etoro.com/markets/atvi/stats/'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = EtoroTickerItem(
            name = hxs.select('//title/text()').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.EtoroTickerItem')
        print item
        return item

    # scrapy parse --spider=etoroTickers -c parse_markets 'https://openbook.etoro.com/markets/stocks'
    def parse_markets(self, response):
        hxs = HtmlXPathSelector(response)
        item = EtoroTickerItem(
            name = hxs.select('//div[3]/div/div/div[3]/div/div[2]/div/div/div[1]/a/text()').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.EtoroTickerItem')
        print item
        return item
