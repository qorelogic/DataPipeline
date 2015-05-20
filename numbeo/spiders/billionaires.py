
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import BillionaireItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class BillionairesSpider(CrawlSpider):
    name = "billionaires"
    allowed_domains = ["bloomberg.com"]
    start_urls = (
        'http://www.bloomberg.com/billionaires',
    )
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/'), callback='parse_item', follow=False),
    )

    # scrapy parse --spider=billionaires -c parse_item 'http://www.bloomberg.com/billionaires'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = BillionaireItem(
            name = hxs.select('//*[@id="chooser"]/div/div[2]/ul/li/a/@data-id').extract(),
            rank = hxs.select('//*[@id="chooser"]/div/div[2]/ul/li/a/@data-id').extract(),
            #rank = hxs.select('//*[@id="profile"]/div/div[1]/ul/li[1]').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.BillionaireItem')
        print item
        return item

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        item = BillionaireItem(
            name = hxs.select('//*[@id="chooser"]/div/div[2]/ul/li/a/@data-id').extract(),
            rank = hxs.select('//*[@id="profile"]/div/div[1]/ul/li[1]').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.BillionaireItem')
        print item
        return item
