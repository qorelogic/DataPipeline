
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import ArcoirisproductsItem

import sys, re, time
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class ArcoirisproductsSpider(CrawlSpider):
    name = "arcoirisProducts"
    #allowed_domains = ['ambito.com']
    allowed_domains = ["arcoiriscapilla.com.ar"]
    time.time()
    mdate = time.strftime('%d/%m/%Y')
    start_urls = (
        'http://arcoiriscapilla.com.ar/index.php/cart/get_lista_precios/',
    )
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'index.php/cart/get_lista_precios/'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=arcoirisProducts -c parse_item 'http://arcoiriscapilla.com.ar/index.php/cart/get_lista_precios'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = ArcoirisproductsItem(
            code  = hxs.select('//table/tr/td[1]/text()').extract(),
            desc  = hxs.select('//table/tr/td[2]/text()').extract(),
            price = hxs.select('//table/tr/td[3]/text()').extract(),
        )
        
        #for i in xrange(len(item['fecha'])):
        #    item['fecha'][i] = re.sub(re.compile(r'(.*)\/(.*)\/(.*)'), '\\3-\\2-\\1', item['fecha'][i].strip())
        #    item['compra'][i] = item['compra'][i].strip().replace(',','.')
        #    item['venta'][i] = item['venta'][i].strip().replace(',','.')
        
        item = self.qs.makeItems(item, 'numbeo.items.ArcoirisproductsItem')
        #print item
        return item
