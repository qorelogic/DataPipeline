from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import FreelancerItem

class JobsSpider(CrawlSpider):
    #name = 'com.freelancer-jobs'
    name = 'jobs'
    allowed_domains = ['freelancer.com']
    start_urls = ['http://www.freelancer.com/job/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'jobs/.+/'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'jobs/.+/[\d]+'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'jobs/.+/[\d]+/[\d]+'), callback='parse_item', follow=True),
        #Rule(SgmlLinkExtractor(allow=r'jobs/.+/[\d]+'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=jobs -c parse_item 'https://www.freelancer.com/jobs/threed-animation/1/8'
    def parse_item(self, response):
        
        hxs = HtmlXPathSelector(response)
        items = []
        #project = hxs.select('//table/tbody/tr/td/a/text()').extract()
        project = hxs.select('//html//tr/td[1]/text() ').extract()

        for pro in zip(project):
            #tik = tik.split('=')[1]
            #print [pro]
            items.append(FreelancerItem(project=pro))
            #di = {'company':com, 'country':count, 'industry':ind, 'ticker':tik}; items.append(di)
            #print di
        return items
