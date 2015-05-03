from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import NumbeoItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class PropertypricesSpider(CrawlSpider):
    name = 'propertyPrices'
    allowed_domains = ['numbeo.com']
    start_urls = ['http://www.numbeo.com/property-investment/rankings_current.jsp']
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/property-investment/rankings_current.jsp'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=propertyPrices -c parse_item 'http://www.numbeo.com/property-investment/rankings_current.jsp'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = NumbeoItem(
            city                                = hxs.select('//*[@id="t2"]/tbody/tr/td[1]/a/text()').extract(),
            priceToIncomeRatio                  = hxs.select('//tbody/tr/td[2]/text()').extract(),
            grossRentalYieldCityCentre          = hxs.select('//tbody/tr/td[3]/text()').extract(),
            grossRentalYieldOutsideOfCentre     = hxs.select('//tbody/tr/td[4]/text()').extract(),
            priceToRentRatioCityCentre          = hxs.select('//tbody/tr/td[5]/text()').extract(),
            priceToRentRatioOutsideOfCityCentre = hxs.select('//tbody/tr/td[6]/text()').extract(),
            mortgageAsAPercentageOfIncome       = hxs.select('//tbody/tr/td[7]/text()').extract(),
            affordabilityIndex                  = hxs.select('//tbody/tr/td[8]/text()').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.NumbeoItem')
        print item
        return item
