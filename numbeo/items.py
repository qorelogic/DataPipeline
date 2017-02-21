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
    timestamp = Field()

class InvestingtechnicalItem(Item):

    name    = Field()
    summary = Field()
    period  = Field()

class CryptoexchangelistItem(Item):

    type         = Field()
    name         = Field()
    code         = Field()
    tradingPairs = Field()
    volume       = Field()

class CryptoexchangelistCoinsItem(Item):

    type        = Field()
    name        = Field()
    symbol      = Field()
    minedCoins  = Field()
    difficulty  = Field()
    volume      = Field()

class ArbitrageItem(Item):

    profit        = Field()
    source        = Field()
    amount        = Field()
    unit          = Field()
    buy           = Field()
    trade         = Field()
    time          = Field()
    fromCoin      = Field()
    toCoin        = Field()
    highestBid    = Field()
    lowestAsk     = Field()
    spread        = Field()
    maximumVolume = Field()

class DigikeyAllproductsItem(Item):
    
	Datasheet = Field()
	Image = Field()
	Digikey_Part_Number = Field()
	Product_link = Field()
	Manufacturer_Part_Number = Field()
	Part_Number_link = Field()
	Vendor = Field()
	Vendor_link = Field()
	Description = Field()
	Quantity_Available = Field()
	UnitPrice_USD = Field()
	Minimum_Quantity = Field()
	Packaging = Field()
	Series = Field()
	Core_Processor = Field()
	Core_Size = Field()
	Speed = Field()
	Connectivity = Field()
	Peripherals = Field()
	Number_of_IO = Field()
	Program_Memory_Size = Field()
	Program_Memory_Type = Field()
	EEPROM_Size = Field()
	RAM_Size = Field()
	Voltage_Supply = Field()
	Data_Converters = Field()
	Oscillator_Type = Field()
	Operating_Temperature = Field()
	Package_Case = Field()
	Supplier_Device_Package = Field()


class ArcoirisproductsItem(Item):
    
	code  = Field()
	desc  = Field()
	price = Field()

class IPAddressItem(Item):
    
	ip = Field()
	hostname = Field()
	userAgent = Field()

class ProxyItem(Item):
    
	host = Field()
	port = Field()
	updated = Field()
	latency = Field()
	reliability = Field()
	ntype = Field()
	ssl = Field()
	country = Field()
