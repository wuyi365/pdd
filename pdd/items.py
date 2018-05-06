# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PddItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class PddItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class GetGoodsItem(scrapy.Item):

    goods_id = scrapy.Field()
    goods_json_doc = scrapy.Field()

class GetCategoryItem(scrapy.Item):

    """
    category_id, cat_id, the 3rd category id
    """

    category_id = scrapy.Field()
    category_json_doc = scrapy.Field()
