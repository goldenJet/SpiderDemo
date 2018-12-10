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
        # 初始化：文件打开
        self.f = codecs.open("doubanData.json", mode="w", encoding="utf-8")

    def process_item(self, item, spider):
        # 内容，结尾增加了换行
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        # 内容写入文件
        self.f.write(content)
        # 一定要记得 return，否则之后的 pipeline 拿不到 item，也就没法继续处理了
        return item

    def close_spider(self, spider):
        # 爬虫关闭时进行：文件关闭
        self.f.close()


class DoubanImgPipeline(ImagesPipeline):
    """
    处理图片信息
    """

    def get_media_requests(self, item, info):
        """
        图片下载
        """
        film_img_url = item['film_img_url']
        yield scrapy.Request(film_img_url)

    def item_completed(self, results, item, info):
        """
        图片重命名
        """
        # 获取文件下载的路径
        path = [x['path'] for ok, x in results if ok]
        # 原始的完整路径
        film_img_disk_url1 = settings.IMAGES_STORE + path[0]
        # 准备存放的新的完整路径
        film_img_disk_url = settings.IMAGES_STORE + 'full\\' + item['film_name'].split("/")[0].strip() + ".jpg"
        try:
            # 重命名
            os.rename(film_img_disk_url1, film_img_disk_url)
        except Exception as error:
            Logger(logLevel='error').getLogger().error("图片重命名失败，异常信息：%s" % error)
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
            # 数据库查重
            self.cursor.execute(
                """select film_name from douban_movie_top_250 where film_name = %s and film_img_url = %s""",
                (item['film_name'], item['film_img_url'])
            )
            # 查重
            repetition = self.cursor.fetchone()
            if repetition:
                # 数据重复
                Logger().getLogger().info("数据重复，film_name: %s，film_img_url：%s" % (item['film_name'], item['film_img_url']))
                pass
            else:
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
