from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import AmbitousdarsblueItem

import sys, time
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class AmbitousdarsblueSpider(CrawlSpider):
    name = 'ambitoUSDARSblue'
    allowed_domains = ['ambito.com']
    time.time()
    mdate = time.strftime('%d/%m/%Y')
    start_urls = ['http://www.ambito.com/economia/mercados/monedas/dolar/info/?ric=ARSB=&desde=11/01/2002&hasta={0}&pag=1'.format(mdate)]
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/economia/mercados/monedas/dolar/info/\?ric=ARSB=&desde=11/01/2002&hasta={0}&pag=[\d]+'.format(mdate)), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=ambitoUSDARSblue -c parse_item 'http://www.ambito.com/economia/mercados/monedas/dolar/info/?ric=ARSB=&desde=11/01/2002&hasta={0}&pag=1'.format(mdate)
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = AmbitousdarsblueItem(
            fecha  = hxs.select('//table//tr/td[1]/div/text()').extract(),
            compra = hxs.select('//table//tr/td[2]/div/text()').extract(),
            venta  = hxs.select('//table//tr/td[3]/div/text()').extract(),
        )
        
        #for i in xrange(len(item['available_supply'])):
        #    item['available_supply'][i] = item['available_supply'][i].strip().replace(',','')
        
        item = self.qs.makeItems(item, 'numbeo.items.AmbitousdarsblueItem')
        #print item
        return item
