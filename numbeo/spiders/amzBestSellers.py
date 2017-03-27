
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import amzBestSellersItem

import pandas as p
import re
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy
from qore import XPath

class amzBestSellersSpider(CrawlSpider):
    name = 'amzBestSellers'
    allowed_domains = ['amazon.com']
    start_urls = []
    start_urls.append('https://www.amazon.com/Best-Sellers/zgbs')
    #start_urls.append('https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances')

    #start_urls.append('https://www.amazon.com/Best-Sellers-Appliances-Dishwashers/zgbs/appliances/3741271/ref=zg_bs_nav_la_2_3741261')

    qs = QoreScrapy()
    xp = XPath()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Best-Sellers.+?zgbs\/[\w-]+$'), callback='parse_item_amzBestSellers', follow=False),
        #Rule(SgmlLinkExtractor(allow=r'Best-Sellers(-[\w-]+\/zgbs)?\/[\w]+\/[\d]+(\/ref=[\w\d_-]+)?$'), callback='parse_item_amzBestSellers', follow=False),
    )

    #def __init__(self):
        #start_urls.append('https://www.amazon.com/Best-Sellers/zgbs')

    # scrapy shell 'https://www.amazon.com/Best-Sellers/zgbs'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=amzBestSellers -c parse_item_amzBestSellers 'https://www.amazon.com/Best-Sellers/zgbs'
    def parse_item_amzBestSellers(self, response):
        #print 
        #print
        #print response.body
        #print 
        #print
        try:
            hxs = Selector(response)
        except Exception as e:
            print e
            return False
        item = amzBestSellersItem(
            name           = hxs.xpath('//*[@id="zg_left_col1"]/div/div/div/div[2]/a/text()').extract(),
            url            = hxs.xpath('//*[@id="zg_left_col1"]/div/div/div/div[2]/a/@href').extract(),
            img            = hxs.xpath('//*[@id="zg_left_col1"]/div/div/div/div[2]/a/div/img/@src').extract(),
            feedback       = hxs.xpath('//*[@id="zg_left_col1"]/div/div/div/div[2]/div/a[1]/i/span/text()').extract(),
            reviews        = hxs.xpath('//*[@id="zg_left_col1"]/div/div/div/div[2]/div/a[2]/text()').extract(),
            productReviews = hxs.xpath('//*[@id="zg_left_col1"]/div/div/div/div[2]/div/a[2]/@href').extract(),
            #canonical = hxs.xpath('//*[@id="zg_left_col1"]/div[1]/div[2]/div/div[2]/div/a[2]/@href').extract(),
        )

        #canonical = [hxs.xpath('//link[@rel="canonical"]/@href').extract()] * 
        #print len(item['canonical'])
        #print item['canonical']
        item['canonical'] = hxs.xpath('//link[@rel="canonical"]/@href').extract() * len(item['name'])
        #item = self.xp.fixNewlines(item, 'name',    '\r\n')

        item = self.qs.makeItems(item, 'numbeo.items.amzBestSellersItem')
        return item
