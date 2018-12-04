# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名字
    film_name = scrapy.Field()
    # 导演和主演名字
    director_performer_name = scrapy.Field()
    # 主演名字
    # performer_name = scrapy.Field()
    # 电影上映年份
    film_year = scrapy.Field()
    # 电影国家
    film_country = scrapy.Field()
    # 电影类型
    film_type = scrapy.Field()
    # 电影评分
    film_rating = scrapy.Field()
    # 电影评论人数
    film_reviews_num = scrapy.Field()
    # 电影经典语句
    film_quato = scrapy.Field()
    # 电影图片
    film_img_url = scrapy.Field()
