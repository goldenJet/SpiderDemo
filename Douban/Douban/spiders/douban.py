# -*- coding: utf-8 -*-
import scrapy
from Douban.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    base_url = 'https://movie.douban.com/top250'
    off_set = '?start=0&filter='
    start_urls = [base_url + off_set]

    def parse(self, response):
        films = response.xpath("//ol[@class='grid_view']/li/div[@class='item']")
        for film in films:
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
            yield item

        # 翻页
        next_url = response.xpath("//div[@class='paginator']/span[@class='next']/a/@href").extract()
        if next_url:
            yield scrapy.Request(self.base_url + next_url[0], self.parse)
