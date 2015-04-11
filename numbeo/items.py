# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class NumbeoItem(Item):
    # define the fields for your item here like:
    city = Field()
    priceToIncomeRatio = Field()
    grossRentalYieldCityCentre = Field()
    grossRentalYieldOutsideOfCentre = Field()
    priceToRentRatioCityCentre = Field()
    priceToRentRatioOutsideOfCityCentre = Field()
    mortgageAsAPercentageOfIncome = Field()
    affordabilityIndex = Field()
    pass
