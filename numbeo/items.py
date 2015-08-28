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

class FreelancerItem(Item):
    # define the fields for your item here like:
    project = Field()
    description = Field()
    bids = Field()
    skills = Field()
    started = Field()
    price = Field()
    pass

class BillionaireItem(Item):
    # define the fields for your item here like:
    name = Field()
    rank = Field()

class EtoroTickerItem(Item):
    # define the fields for your item here like:
    name = Field()

class CryptocoinsItem(Item):
    # define the fields for your item here like:
    name = Field()
    code = Field()
    marketcap = Field()
    price = Field()
    available_supply = Field()
    volume = Field()
    percent_1hr = Field()
    percent_24hr = Field()
    percent_7days = Field()

class AmbitousdarsblueItem(Item):
    # define the fields for your item here like:
    fecha  = Field()
    compra = Field()
    venta  = Field()

class InvestingworldgovernmentbondsItem(Item):

    name    = Field()
    country = Field()
    currencyCode = Field()
    period  = Field()
    iyield  = Field()
    prev    = Field()
    high    = Field()
    low     = Field()
    chg     = Field()
    chgpcnt = Field()
    time    = Field()

class InvestingtechnicalItem(Item):

    name    = Field()
    summary = Field()
    period  = Field()
