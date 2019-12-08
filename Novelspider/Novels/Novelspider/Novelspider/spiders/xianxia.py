# -*- coding: utf-8 -*-
import scrapy
from Novelspider.items import NovelspiderItem

class XianxiaSpider(scrapy.Spider):
    name = 'xianxia'
    allowed_domains = ['ranwen8.com']
    start_urls = ['https://www.ranwen8.com/list/2/1.html']

    def parse(self, response):
        # 获取当前分类的小说的最大页数
        # max_page = response.xpath("//a[@class='last']/text()")
        links = response.xpath("//td[1]/a/@href").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.get_novel_info)

        next_URL = response.xpath("//a[@class='next']/@href").extract()
        current_index = response.xpath("//li[@class='active']/span/text()").extract()[0]

        if next_URL and int(current_index) <= 10:
            yield scrapy.Request(next_URL[0], callback=self.parse)
        else:
            pass

    def get_novel_info(self, response):
        first_URL = 'https://www.ranwen8.com'
        last_URL = response.xpath("//dd[@class='col-md-3'][1]/a/@href").extract()[0]
        item = NovelspiderItem()
        item['novel_name'] = response.xpath("//h1/text()").extract()[0]
        item['novel_author'] = response.xpath("//p[@class='booktag']/a[1]/text()").extract()[0]
        item['novel_img'] = response.xpath("//img[@class='img-thumbnail']/@src").extract()[0]
        item['novel_type'] = response.xpath("//p[@class='booktag']/a[2]/text()").extract()[0]
        item['novel_des'] = response.xpath("//p[@id='bookIntro']/text()").extract()
        item['novel_date'] = response.xpath("//span[@class='hidden-xs']/text()").extract()[0]
        item['novel_start'] = first_URL + last_URL
        for i in item['novel_des'][:]:
            if i.isspace():
                item['novel_des'].remove(i)

        yield item
