# -*- coding: utf-8 -*-
import scrapy
import sqlite3
from Novel.items import NovelItem


class WangyouSpider(scrapy.Spider):
    name = 'wangyou'
    allowed_domains = ['ranwen8.com']
    start_urls = ['https://www.ranwen8.com/book/7842/4165669.html']

    # def get_infos(self):
    conn = sqlite3.connect('novel_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT novel_name, novel_start FROM WANGYOU')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    # return values

    links = []
    novel_names = []
    for i in range(0, len(values) - 1):
        links.append(values[i][1])
        novel_names.append(values[i][0])
    # print(links)
    # print(novel_names)
    #
    # conn = sqlite3.connect('./novel_db/wangyou.db')
    # cursor = conn.cursor()
    # for it in range(0, len(novel_names)):
    #     sql = 'CREATE TABLE ' + str(novel_names[it]) + '(title CHAR(200) NOT NULL, texts TEXT)'
    #     print(sql)
    #     # print(sql)
    #     cursor.execute(sql)
    # cursor.close()
    # conn.commit()
    # conn.close()

    count = 0
    link = 22

    def parse(self, response):
        next_text = response.xpath("//a[@id='linkNext']/text()").extract()[0]
        base_URL = response.xpath("//a[@id='linkNext']/@href").extract()[0]
        head_URL = response.xpath("//link[1]/@href").extract()[0]
        url = head_URL.split('/')[:5]
        s = '/'.join(url)
        next_URL = s + '/' + base_URL
        print(next_URL)

        if next_text == '下一页':
            global flag
            flag = response.xpath("//div[@class='panel-body']/text()").extract()
            yield scrapy.Request(next_URL, callback=self.parse)
        if next_text == '下一章':
            if self.count < 20:
                self.count += 1
                item = NovelItem()
                item['name'] = response.xpath("//a[@class='blue'][1]/text()").extract()[0]
                item['title'] = response.xpath("//h1/text()").extract()[0]
                item['texts'] = flag + response.xpath("//div[@class='panel-body']/text()").extract()
                print(self.count)
                yield item
                yield scrapy.Request(next_URL, callback=self.parse)
            else:
                # for i in range(1, len(self.links)):
                if self.link < 100:
                    self.start_urls = self.links[self.link]
                    self.link += 1
                    self.count = 0
                    yield scrapy.Request(self.start_urls, callback=self.parse)
                else:
                    pass
