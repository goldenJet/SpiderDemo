# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import scrapy

from scrapy.pipelines.images import ImagesPipeline

from Douban import settings


class DoubanMoviePipeline(object):
    """
    处理电影信息
    """

    def __init__(self):
        self.f = codecs.open("douban.json", mode="w", encoding="utf-8")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()


class DoubanImgPipeline(ImagesPipeline):
    """
    处理图片信息
    """

    def get_media_requests(self, item, info):
        film_img_url = item['film_img_url']
        yield scrapy.Request(film_img_url)

    def item_completed(self, results, item, info):
        path = [x['path'] for ok, x in results if ok]
        film_img_disk_url1 = settings.IMAGES_STORE + path[0]
        film_img_disk_url = settings.IMAGES_STORE + 'full\\' + item['film_name'].split("/")[0].strip() + ".jpg"
        try:
            # 重命名
            os.rename(film_img_disk_url1, film_img_disk_url)
        # except Exception as error:
            # log(error)
        except:
            # TODO
            pass
        return item

