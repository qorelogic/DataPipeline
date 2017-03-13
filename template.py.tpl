
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import {{item}}Item

import pandas as p
import re
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
from qore import XPath

class {{name}}Spider(CrawlSpider):
    name = '{{name}}'
    allowed_domains = ['{{domain}}']
    start_urls = []
    start_urls.append('{{url}}')

    qs = QoreScrapy()
    xp = XPath()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'stocklist\/[\w]+/[\w]+\.htm$'), callback='parse_item_{{name}}', follow=True),
    )
    # scrapy shell '{{url}}'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider={{name}} -c parse_item_{{name}} '{{url}}'
    def parse_item_{{name}}(self, response):
        hxs = HtmlXPathSelector(response)
        item = {{item}}Item(
            name     = hxs.select('//table... /text()').extract(),
        )

        #item = self.xp.fixNewlines(item, 'name',    '\r\n')

        item = self.qs.makeItems(item, 'numbeo.items.{{item}}Item')
        return item
