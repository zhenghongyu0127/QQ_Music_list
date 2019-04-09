# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqMusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_group_name = scrapy.Field()
    category_name = scrapy.Field()
    category_id = scrapy.Field()
    category_sort = scrapy.Field()
    category_data = scrapy.Field()
    cd_list = scrapy.Field()
    pass
