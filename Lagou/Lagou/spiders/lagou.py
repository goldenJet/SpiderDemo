# -*- coding: utf-8 -*-
import scrapy
from Lagou.items import LagouItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    # start_urls = ["https://www.lagou.com/zhaopin/Java/1"]
    start_urls = ["https://www.lagou.com"]

    cookie = {
        'JSESSIONID': 'ABAAABAAAIAACBI6930FA480B9F0B2990D167F2C9A76996',
        'user_trace_token': '20180707140944-70516aee-e250-4eab-a0b6-e067efbecf4f',
        '_ga': 'GA1.2.1557777416.1530943791',
        'LGUID': '20180707140946-5940fa6d-81ac-11e8-993c-5254005c3644',
        'TG-TRACK-CODE': 'index_navigation',
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1543232738',
        'index_location_city': '%E4%B8%8A%E6%B5%B7',
        'X_HTTP_TOKEN': 'cda41d5c123e6df8734ff31427e19f94',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221675066f09c90-0d6f5d9b89484a-3a3a5f0c-1440000-1675066f09d83%22%2C%22%24device_id%22%3A%221675066f09c90-0d6f5d9b89484a-3a3a5f0c-1440000-1675066f09d83%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
        '_gid': 'GA1.2.1166736170.1543462674',
        '_gat': '1',
        'LGSID': '20181130224421-6ca5a694-f4ae-11e8-8820-525400f775ce',
        'PRE_UTM': '',
        'PRE_HOST': '',
        'PRE_SITE': 'https%3A%2F%2Fwww.lagou.com%2F',
        'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F%3FlabelWords%3Dlabel',
        'SEARCH_ID': '5b10c770135946acb7e3eacd91f4814c',
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1543589080',
        'LGRID': '20181130224437-76281788-f4ae-11e8-8820-525400f775ce'
    }

    def parse(self, response):
        for menu_sub in response.xpath("//div[@class='menu_sub dn']/dl"):
            job_classify = menu_sub.xpath("./dt/span/text()").extract()[0]
            for job in menu_sub.xpath("./dd/a"):
                job_name = job.xpath("./text()").extract()[0]
                job_url = job.xpath("./@href").extract()[0] + "1/"

                item = LagouItem()
                item['job_classify'] = job_classify
                item['job_name'] = job_name
                item['job_url'] = job_url
                # yield item
                yield scrapy.Request(job_url, cookies=self.cookie, meta={'item': item}, callback=self.parse_url)

    def parse_url(self, response):
        """
        解析每个工作类的url
        """
        item_base = response.meta['item']
        job_classify = item_base['job_classify']
        job_name = item_base['job_name']
        job_url = item_base['job_url']
        node_list = response.xpath("//ul[@class='item_con_list']/li[@class='con_list_item default_list']")
        for node in node_list:
            item = LagouItem()

            item['job_classify'] = job_classify
            item['job_name'] = job_name
            item['job_url'] = job_url
            item['company'] = \
                node.xpath("./div[@class='list_item_top']/div/div[@class='company_name']/a/text()").extract()[0]
            item['company_scale'] = str.strip(
                node.xpath("./div[@class='list_item_top']/div/div[@class='industry']/text()").extract()[0])
            item['position'] = \
                node.xpath("./div[@class='list_item_top']/div/div[@class='p_top']/a/h3/text()").extract()[0]
            item['address'] = \
                node.xpath("./div[@class='list_item_top']/div/div[@class='p_top']/a/span/em/text()").extract()[0]
            item['salary'] = \
                node.xpath("./div[@class='list_item_top']/div/div[@class='p_bot']/div/span/text()").extract()[0]
            item['experience'] = str.strip(
                node.xpath("./div[@class='list_item_top']/div/div[@class='p_bot']/div/text()[3]").extract()[0])
            item['work'] = node.xpath("./div[@class='list_item_bot']/div[@class='li_b_l']/span/text()").extract()

            yield item

        # 翻页
        next_url = response.xpath(
            "//div[@class='pager_container']/a[@class='page_no' and text()='下一页']/@href").extract()
        if next_url:
            # yield scrapy.Request(response.urljoin(next_url[0] + "?filterOption=3"), self.parse)
            # yield scrapy.Request(next_url[0], cookies=self.cookie, callback=self.parse)
            item_base['job_url'] = next_url[0]
            yield scrapy.Request(next_url[0], cookies=self.cookie, meta={'item': item_base}, callback=self.parse_url)
