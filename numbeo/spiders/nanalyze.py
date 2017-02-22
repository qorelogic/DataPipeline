from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import NanalyzeArticleItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

# http://stackoverflow.com/questions/4710483/scrapy-and-proxies

class NanalyzeSpider(CrawlSpider):
    name = 'nanalyze'
    allowed_domains = [
        'nanalyze.com',
    ]
    
    start_urls = []
    start_urls.append('http://www.nanalyze.com/articles/page/1/')

    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'articles/page/[\d]+.*'), callback='parse_item_bookmarks', follow=True),
        Rule(SgmlLinkExtractor(allow=r'tag/[\w\d\-]+.*'), callback='parse_item_tags', follow=True),
    )

    # scrapy shell 'http://www.nanalyze.com/articles/page/1/'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=nanalyze -c parse_item_bookmarks 'http://www.nanalyze.com/articles/page/1/'
    def parse_item_bookmarks(self, response):
        hxs = HtmlXPathSelector(response)
        item = NanalyzeArticleItem(
            title = hxs.select('//*[@id="container"]/article/header/h2/a/text()').extract(),
            url   = hxs.select('//*[@id="container"]/article/header/h2/a/@href').extract(),
            type  = hxs.select('//*[@id="container"]/article/header/h2/a/@rel').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.NanalyzeArticleItem')
        return item

    # scrapy shell 'http://www.nanalyze.com/articles/page/1/'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=nanalyze -c parse_item_tags 'http://www.nanalyze.com/articles/page/1/'
    def parse_item_tags(self, response):
        hxs = HtmlXPathSelector(response)
        item = NanalyzeArticleItem(
            title = hxs.select('//*[@id="container"]/article/footer/p/span[2]/a[@rel="tag"]/text()').extract(),
            url   = hxs.select('//*[@id="container"]/article/footer/p/span[2]/a[@rel="tag"]/@href').extract(),
            type  = hxs.select('//*[@id="container"]/article/footer/p/span[2]/a[@rel="tag"]/@rel').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.NanalyzeArticleItem')
        return item
