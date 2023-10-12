# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QscspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BrandItem(scrapy.Item):
    start = scrapy.Field()
    brand = scrapy.Field()
    categorize = scrapy.Field()
    name = scrapy.Field()
