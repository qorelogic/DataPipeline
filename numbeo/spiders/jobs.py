from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import FreelancerItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

class JobsSpider(CrawlSpider):
    #name = 'com.freelancer-jobs'
    name = 'jobs'
    allowed_domains = ['freelancer.com']
    start_urls = ['http://www.freelancer.com/job/']
    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'jobs/[^\/]+/'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'jobs/[^\/]+/[\d]+'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'jobs/[^\/]+/[\d]+/[\d]+'), callback='parse_item', follow=True),
        #Rule(SgmlLinkExtractor(allow=r'jobs/.+/[\d]+'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=jobs -c parse_item 'https://www.freelancer.com/jobs/threed-animation/1/8'
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = FreelancerItem(
            project = hxs.select('//table[@id="project_table_static"]//tr/td[1]/text() ').extract(),
            description = hxs.select('//table[@id="project_table_static"]//tr/td[2]/text() ').extract(),
            bids = hxs.select('//table[@id="project_table_static"]//tr/td[3]/text() ').extract(),
            skills = hxs.select('//table[@id="project_table_static"]//tr/td[4]/a').extract(),
            started = hxs.select('//table[@id="project_table_static"]//tr/td[5]/text() ').extract(),
            price = hxs.select('//table[@id="project_table_static"]//tr/td[7]/text() ').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.FreelancerItem')
        return item
