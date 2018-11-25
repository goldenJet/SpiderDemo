# -*- coding: utf-8 -*-
import scrapy
import json
from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['doiyucdn.cn']
    off_set = 0
    base_url = 'http://capi.douyucdn.cn/api/v1/getverticalroom?limit=20&offset='
    start_urls = [base_url + str(off_set)]

    def parse(self, response):
        data_list = json.loads(response.body)['data']
        # print(data_list)
        if len(data_list) == 0:
            return

        for data in data_list:
            item = DouyuItem()
            item['owner_uid'] = data['owner_uid']
            item['room_id'] = data['room_id']
            item['room_name'] = data['room_name']
            item['vertical_src'] = data['vertical_src']
            item['nickname'] = data['nickname']
            item['anchor_city'] = data['anchor_city']
            yield item

        # 继续拼接URL地址
        self.off_set += 20
        yield scrapy.Request(self.base_url + str(self.off_set), callback=self.parse(response))
