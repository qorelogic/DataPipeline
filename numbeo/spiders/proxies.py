from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import ProxyItem

import pandas as p
import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

# http://stackoverflow.com/questions/4710483/scrapy-and-proxies

class ProxiesSpider(CrawlSpider):
    name = 'proxies'
    allowed_domains = [
        'google.com',
        'hidemyass.com',
        'xroxy.com',
    ]
    """
    #1. http://proxylist.hidemyass.com
    #2. http://www.xroxy.com/proxylist.htm
    #3. http://www.ultraproxies.com
    #4. https://proxy-list.org
    #5. http://list.proxylistplus.com
    
    <div class="textwidget">
    <li> 1. <a href="https://www.bestpaidproxies.com/visit/myprivateproxy/" target="_blank" rel="nofollow" title="Best Private Proxy Service - Shared Proxies">MyPrivateProxy</a></li>
    <li> 2. <a href="https://www.bestpaidproxies.com/visit/sslprivateproxy/" target="_blank" rel="nofollow" title="Best Twitter Proxy  Service - social media proxies">SSLPrivateProxy</a></li>
    <li> 3. <a href="https://www.bestpaidproxies.com/visit/squidproxies/" target="_blank" rel="nofollow" title="Best SEO Proxy Service - Scrapebox proxies">SquidProxies</a></li>
    <li> 4. <a href="https://www.bestpaidproxies.com/visit/instantproxies/" target="_blank" rel="nofollow" title="Best Cheap Private Proxy Service - Cost effective">InstantProxies</a></li>
    <li> 5. <a href="https://www.bestpaidproxies.com/visit/proxy-n-vpn/" target="_blank" rel="nofollow" title="Best Craigslist Proxy Service- Classified Ads proxies">Proxy-N-VPN</a></li>
    <li> 6. <a href="https://www.bestpaidproxies.com/visit/buyproxies/" target="_blank" rel="nofollow" title="Best Xrumer Proxy Service - NO restrictions">BuyProxies</a></li>
    <li> 7. <a href="https://www.bestpaidproxies.com/visit/proxykey/" target="_blank" rel="nofollow" title="highly secure and stable proxies">ProxyKey</a></li>
    <li> 8. <a href="https://www.bestpaidproxies.com/visit/newipnow/" target="_blank" rel="nofollow" title="Best Private Proxy Service with web proxy">NewIpNow</a></li>
    <li> 9. <a href="https://www.bestpaidproxies.com/visit/highproxies/" target="_blank" rel="nofollow" title="US premium instagram proxies">HighProxies</a></li>
    <li> 0. <a href="https://www.bestpaidproxies.com/visit/yourprivateproxy/" target="_blank" rel="nofollow" title="Best Nike proxy &amp; socks5 proxy">YourPrviateProxy</a></li>
    </div>
    """
    
    start_urls = []
    #start_urls.append('http://proxylist.hidemyass.com/4')
    start_urls.append('http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=0#table')

    qs = QoreScrapy()

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'.+'), callback='parse_item', follow=False),
        
        #Rule(SgmlLinkExtractor(allow=r'[\d]+'), callback='parse_item_hidemyass', follow=True),
        Rule(SgmlLinkExtractor(allow=r'proxylist.+?pnum=[\d]+'), callback='parse_item_xroxy', follow=True),
    )

    # scrapy shell 'http://proxylist.hidemyass.com/4'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=proxies -c parse_item_hidemyass 'http://proxylist.hidemyass.com/4'
    def parse_item_hidemyass(self, response):
        hxs = HtmlXPathSelector(response)
        item = ProxyItem(
            updated = hxs.select('//*[@id="listable"]/tbody/tr/td[1]/span/text()').extract(),
            port    = hxs.select('//*[@id="listable"]/tbody/tr/td[3]/text()').extract(),
            host    = hxs.select('//*[@id="listable"]/tbody/tr/td[2]/span').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.ProxyItem')
        return item

    # scrapy shell 'http://proxylist.hidemyass.com/4'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=proxies -c parse_item_xroxy 'http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=0#table'
    def parse_item_xroxy(self, response):
        hxs = HtmlXPathSelector(response)
        item = ProxyItem(
            #updated = hxs.select('//*[@id="listable"]/tbody/tr/td[1]/span/text()').extract(),
            port        = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[3]/a/text()').extract(),
            host        = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[2]/a/text()').extract(),
            latency     = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[7]/text()').extract(),
            reliability = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[8]//text()').extract(),
            ntype       = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[4]//text()').extract(),
            ssl         = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[5]//text()').extract(),
            country     = hxs.select('//table[1]//tr[@class="row0" or @class="row1"]/td[6]//text()').extract(),
        )
        
        li = item['host']
        li = p.DataFrame(li)
        for i in list(li[li[0] == '\n'].index):
            li = li.drop(i)
        item['host'] = list(li[0])
        
        item = self.qs.makeItems(item, 'numbeo.items.ProxyItem')
        return item

    # scrapy shell 'http://whatismyipaddress.com'
    # scrapy parse --spider=proxies -c parse_item_whatismyipaddress 'http://whatismyipaddress.com'
    def parse_item_whatismyipaddress(self, response):
        hxs = HtmlXPathSelector(response)
        item = IPAddressItem(
            ip  = hxs.select('//*[@id="section_left"]/div[2]/a/text()').extract(),
        )
        item = self.qs.makeItems(item, 'numbeo.items.IPAddressItem')
        return item

    # scrapy shell 'http://www.whatsmyip.org'
    # scrapy parse --spider=proxies -c parse_item_whatsmyip 'http://www.whatsmyip.org'
    def parse_item_whatsmyip(self, response):
        hxs = HtmlXPathSelector(response)
        item = IPAddressItem(
            ip  = hxs.select('//*[@id="ip"]/text()').extract(),
            hostname  = hxs.select('//*[@id="hostname"]/text()').extract(),
            userAgent  = hxs.select('//*[@id="useragent"]/text()').extract(),
        )
        item = self.qs.makeItems(item, 'numbeo.items.IPAddressItem')
        return item
