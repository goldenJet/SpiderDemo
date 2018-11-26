# -*- coding: utf-8 -*-
import scrapy
from Lagou.items import LagouItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ["https://www.lagou.com/zhaopin/Java/1"]

    def parse(self, response):
        node_list = response.xpath("//ul[@class='item_con_list']/li[@class='con_list_item default_list']")

        for node in node_list:
            item = LagouItem()

            item['company'] = node.xpath("./div[@class='list_item_top']/div/div[@class='company_name']/a/text()").extract()[0]
            item['company_scale'] = str.strip(node.xpath("./div[@class='list_item_top']/div/div[@class='industry']/text()").extract()[0])
            item['position'] = node.xpath("./div[@class='list_item_top']/div/div[@class='p_top']/a/h3/text()").extract()[0]
            item['address'] = node.xpath("./div[@class='list_item_top']/div/div[@class='p_top']/a/span/em/text()").extract()[0]
            item['salary'] = node.xpath("./div[@class='list_item_top']/div/div[@class='p_bot']/div/span/text()").extract()[0]
            item['experience'] = str.strip(node.xpath("./div[@class='list_item_top']/div/div[@class='p_bot']/div/text()[3]").extract()[0])
            item['work'] = node.xpath("./div[@class='list_item_bot']/div[@class='li_b_l']/span/text()").extract()

            yield item

        # 翻页
        next_url = response.xpath("//div[@class='pager_container']/a[@class='page_no' and text()='下一页']/@href").extract()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url[0] + "?filterOption=3"), self.parse)
