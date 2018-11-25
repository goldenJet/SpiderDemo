# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from Douyu.settings import IMAGES_STORE as image_base_url


class DouyuPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        vertical_src = item['vertical_src']
        yield scrapy.Request(vertical_src)

    def item_completed(self, results, item, info):
        path = [x['path'] for ok, x in results if ok]
        os.rename(image_base_url + path[0], image_base_url + 'full\\' + item['nickname'] + ".jpg")
        return item
