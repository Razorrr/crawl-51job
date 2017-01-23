# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SeekjobItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()          # job name
    location = scrapy.Field()       # job location
    company = scrapy.Field()        # which company
    salary = scrapy.Field()     # when po
    jobdc = scrapy.Field()          # job's description
    link = scrapy.Field()           # URL link