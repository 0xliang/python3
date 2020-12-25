# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockeastmoneyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    lastPrice = scrapy.Field()
    stockName = scrapy.Field()
    stockCode = scrapy.Field()
    
