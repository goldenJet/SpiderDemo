# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # 工作分类（大类，如：后端开发）
    job_classify = scrapy.Field()
    # 工作名（如 java）
    job_name = scrapy.Field()
    # 工作名的链接
    job_url = scrapy.Field()
    # 公司名
    company = scrapy.Field()
    # 公司性质和规模
    company_scale = scrapy.Field()
    # 区域
    address = scrapy.Field()
    # 职位
    position = scrapy.Field()
    # 薪水
    salary = scrapy.Field()
    # 经验和学历
    experience = scrapy.Field()
    # 工作内容
    work = scrapy.Field()

