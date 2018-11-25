# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    owner_uid = scrapy.Field()
    room_id = scrapy.Field()
    room_name = scrapy.Field()
    # 图片
    vertical_src = scrapy.Field()
    # 昵称
    nickname = scrapy.Field()
    # 城市
    anchor_city = scrapy.Field()
