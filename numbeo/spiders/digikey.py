
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from numbeo.items import DigikeyAllproductsItem

class DigikeyAllproductsSpider(CrawlSpider):
    name = "digikeyallproduct"
    allowed_domains = ["digikey.com"]
    start_urls = ["http://www.digikey.com/product-search/en?FV=fff40027%2Cfff800cd&mnonly=0&newproducts=0&ColumnSort=1000001&page=1&stock=0&pbfree=0&rohs=0&quantity=&ptm=0&fid=0&pageSize=500"]
    rules = (Rule (SgmlLinkExtractor(allow=("", ),restrict_xpaths=('//*[@class="Next"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//table[@class='stickyHeader']/tbody/tr")
        items = []
        for titles in titles:
            item = DigikeyAllproductsItem()
            item ["Datasheet"] = titles.select("td[@class='rd-datasheet']/center/a/@href").extract()
            item ["Image"] = titles.select("td[@class='image']/a/@href").extract()
            item ["Digikey_Part_Number"] = titles.select("td[@class='digikey-partnumber']/a/text()").extract()
            item ["Product_link"] = titles.select("td[@class='digikey-partnumber']/a/@href").extract()
            item ["Manufacturer_Part_Number"] = titles.select("td[@class='mfg-partnumber']/a/span/text()").extract()
            item ["Part_Number_link"] = titles.select("td[@class='mfg-partnumber']/a/@href").extract()
            item ["Vendor"] = titles.select("td[@class='vendor']/span/a/span/text()").extract()
            item ["Vendor_link"] = titles.select("td[@class='vendor']/span/a/@href").extract()
            item ["Description"] = titles.select("td[@class='description']/text()").extract()
            item ["Quantity_Available"] = titles.select("td[@class='qtyAvailable']/text()").extract()
            item ["UnitPrice_USD"] = titles.select("td[@class='unitprice']/text()").extract()
            item ["Minimum_Quantity"] = titles.select("td[@class='minQty']/text()").extract()
            item ["Packaging"] = titles.select("td[@class='packaging']/text()").extract()
            item ["Series"] = titles.select("td[@class='series']/a/text()").extract()
            item ["Core_Processor"] = titles.select("td[@class='CLS 506']/text()").extract()
            item ["Core_Size"] = titles.select("td[@class='CLS 689']/text()").extract()
            item ["Speed"] = titles.select("td[@class='CLS 143']/text()").extract()
            item ["Connectivity"] = titles.select("td[@class='CLS 1,113']/text()").extract()
            item ["Peripherals"] = titles.select("td[@class='CLS 1,114']/text()").extract()
            item ["Number_of_IO"] = titles.select("td[@class='CLS 157']/text()").extract()
            item ["Program_Memory_Size"] = titles.select("td[@class='CLS 155']/text()").extract()
            item ["Program_Memory_Type"] = titles.select("td[@class='CLS 290']/text()").extract()
            item ["EEPROM_Size"] = titles.select("td[@class='CLS 291']/text()").extract()
            item ["RAM_Size"] = titles.select("td[@class='CLS 156']/text()").extract()
            item ["Voltage_Supply"] = titles.select("td[@class='CLS 1,112']/text()").extract()
            item ["Data_Converters"] = titles.select("td[@class='CLS 519']/text()").extract()
            item ["Oscillator_Type"] = titles.select("td[@class='CLS 283']/text()").extract()
            item ["Operating_Temperature"] = titles.select("td[@class='CLS 252']/text()").extract()
            item ["Package_Case"] = titles.select("td[@class='CLS 16']/text()").extract()
            item ["Supplier_Device_Package"] = titles.select("td[@class='CLS 1,291']/text()").extract()
            items.append(item)
        return items

        #//*[@id="content"]/div[8]/div/a[12]
