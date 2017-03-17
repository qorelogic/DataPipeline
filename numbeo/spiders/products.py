
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import productItem

import pandas as p
import re
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
from qore import XPath

class productsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['amazon.com']
    start_urls = []
    start_urls.append('https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0')

    qs = QoreScrapy()
    xp = XPath()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'stocklist\/[\w]+/[\w]+\.htm$'), callback='parse_item_products', follow=True),
    )
    # scrapy shell 'https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=products -c parse_item_products 'https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0'
    def parse_item_products(self, response):
        hxs = HtmlXPathSelector(response)
        item = productItem(
            name     = hxs.select('//*[@id="zg_centerListWrapper"]/div/div[2]/div/a/div[2]/text()').extract(),
        )

        item = self.xp.fixNewlines(item, 'name',    '\r\n')

        item = self.qs.makeItems(item, 'numbeo.items.productItem')
        return item

