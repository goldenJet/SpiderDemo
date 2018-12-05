# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import scrapy
import pymysql
from Douban.logger import Logger

from scrapy.pipelines.images import ImagesPipeline

from Douban import settings


class DoubanMoviePipeline(object):
    """
    处理电影信息
    """

    def __init__(self):
        self.f = codecs.open("doubanData.json", mode="w", encoding="utf-8")

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
        except Exception as error:
            Logger(logLevel='error').getLogger().error("图片重命名失败", error)
            pass
        return item


class DoubanDBPipeline(object):
    """
    数据存入mysql
    """

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插数据
            self.cursor.execute(
                """insert into douban_movie_top_250(film_name, director_performer_name, film_year, film_country, film_type, film_rating, film_reviews_num, film_quato, film_img_url)
                    VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['film_name'],
                    item['director_performer_name'],
                    item['film_year'],
                    item['film_country'],
                    item['film_type'],
                    item['film_rating'],
                    item['film_reviews_num'],
                    item['film_quato'],
                    item['film_img_url']
                )
            )
            # sql提交
            self.connect.commit()
        except Exception as error:
            Logger(logLevel='error').getLogger().error("数据插入数据库失败", error)

        return item

    def close_spider(self, spider):
        # 关闭数据库连接
        self.connect.close()
