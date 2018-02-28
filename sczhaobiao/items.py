# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CommitItem(scrapy.Item):
    pass

class SczhaobiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    area = scrapy.Field()
    start_time = scrapy.Field()
    detail_url = scrapy.Field()

