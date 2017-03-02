from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from numbeo.items import StartupsItem

import sys
try:    sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')
from qore import QoreScrapy

# http://stackoverflow.com/questions/4710483/scrapy-and-proxies

class StartupsSpider(CrawlSpider):
    name = 'startups'
    allowed_domains = [
        'gust.com',
    ]
    
    start_urls = []
    #start_urls.append('https://gust.com/search/new?utf8=%E2%9C%93&category=startups&keywords%5B%5D=&list_change_data=%7B%22filter_type%22%3A%22category%22%2C%22filter_value%22%3A%22startups%22%2C%22event_type%22%3A%22filtered%22%7D')
    start_urls.append('https://gust.com/search/new?category=startups&keywords[]=&list_change_data={%22filter_type%22:%22category%22,%22filter_value%22:%22startups%22,%22event_type%22:%22filtered%22}&page=1&partial=results&utf8=%E2%9C%93')

    qs = QoreScrapy()

    rules = (
        Rule(SgmlLinkExtractor(allow=r'search/new?utf8=%E2%9C%93&category=startups&keywords%5B%5D=&list_change_data=%7B%22filter_type%22%3A%22category%22%2C%22filter_value%22%3A%22startups%22%2C%22event_type%22%3A%22filtered%22%7D'), callback='parse_item_bookmarks', follow=True),
    )

    # scrapy shell 'https://gust.com/search/new?category=startups&keywords[]=&list_change_data={%22filter_type%22:%22category%22,%22filter_value%22:%22startups%22,%22event_type%22:%22filtered%22}&page=1&partial=results&utf8=%E2%9C%93'
    #   sel.select('<xpath>').extract()
    # scrapy parse --spider=startups -c parse_item_gustCompanies 'https://gust.com/search/new?category=startups&keywords[]=&list_change_data={%22filter_type%22:%22category%22,%22filter_value%22:%22startups%22,%22event_type%22:%22filtered%22}&page=1&partial=results&utf8=%E2%9C%93'
    def parse_item_gustCompanies(self, response):
        hxs = HtmlXPathSelector(response)
        item = StartupsItem(
            name        = hxs.select('//*[@id="search_results_list"]/ul[1]/li/div/div[2]/div[1]/a/text()').extract(),
            url         = hxs.select('//*[@id="search_results_list"]/ul[1]/li/div/div[2]/div[1]/a/@href').extract(),
            location    = hxs.select('//*[@id="search_results_list"]/ul[1]/li/div/div[2]/div[2]/text()').extract(),
            industry    = hxs.select('//*[@id="search_results_list"]/ul[1]/li/div/div[2]/div[2]/text()').extract(),
            description = hxs.select('//*[@id="search_results_list"]/ul[1]/li/div/div[2]/div[3]/p/text()').extract(),
        )
        
        item = self.qs.makeItems(item, 'numbeo.items.StartupsItem')
        return item
