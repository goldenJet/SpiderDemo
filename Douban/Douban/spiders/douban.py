# -*- coding: utf-8 -*-
import scrapy
from Douban.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    # 爬虫名称（必须唯一）
    name = 'douban'
    # 非此域名下的链接均不进行爬取
    allowed_domains = ['douban.com']
    base_url = 'https://movie.douban.com/top250'
    off_set = '?start=0&filter='
    # 起始的爬取地址
    start_urls = [base_url + off_set]

    # 每次的爬取都会默认走这个 parse 方法
    def parse(self, response):
        # xpath 解析出每个电影的信息模块
        films = response.xpath("//ol[@class='grid_view']/li/div[@class='item']")
        # 遍历每个电影模块
        for film in films:
            # 创建电影信息存储的item对象
            item = DoubanItem()
            # 标题
            titles = film.xpath("./div[@class='info']/div[@class='hd']/a/span/text()").extract()
            film_name = ''
            # 拼接电影名
            for title in titles:
                film_name += title.strip()
            # 电影信息
            infos = film.xpath("./div[@class='info']/div[@class='bd']/p/text()").extract()
            director_performer_name = ""
            for temp in infos[0]:
                director_performer_name += temp.strip()
            year_country = infos[1]
            film_year = year_country.split("/")[0].strip()
            film_country = year_country.split("/")[1].strip()
            film_type = year_country.split("/")[2].strip()
            # 电影评分
            film_rating = film.xpath("./div[@class='info']/div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()").extract()[0].strip()
            # 电影参与评论人数
            film_reviews_num = film.xpath("./div[@class='info']/div[@class='bd']/div[@class='star']/span[last()]/text()").extract()[0].strip()[:-3]
            # 电影经典语句
            film_quato = ""
            film_quato_temp = film.xpath("./div[@class='info']/div[@class='bd']/p[@class='quote']/span/text()").extract()
            if film_quato_temp:
                film_quato = film_quato_temp[0].strip()
            # 电影图片链接
            film_img_url = film.xpath("./div[@class='pic']/a/img/@src").extract()[0].strip()

            # item 字段赋值
            item['film_name'] = film_name
            item['director_performer_name'] = director_performer_name
            # item['director_name'] = director_name
            # item['performer_name'] = performer_name
            item['film_year'] = film_year
            item['film_country'] = film_country
            item['film_type'] = film_type
            item['film_rating'] = film_rating
            item['film_reviews_num'] = film_reviews_num
            item['film_quato'] = film_quato
            item['film_img_url'] = film_img_url
            # 返回 item 进行解析，解析完了之后再回到这里继续运行
            yield item

        # 翻页
        # 解析出下一页
        next_url = response.xpath("//div[@class='paginator']/span[@class='next']/a/@href").extract()
        if next_url:
            # 如果下一页存在的话再进行请求，并传递回调函数 parse()
            yield scrapy.Request(self.base_url + next_url[0], self.parse)
