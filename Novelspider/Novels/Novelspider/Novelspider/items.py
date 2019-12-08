# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NovelspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 小说名字
    novel_name = scrapy.Field()
    # 小说作者
    novel_author = scrapy.Field()
    # 小说图片
    novel_img = scrapy.Field()
    # 小说类型
    novel_type = scrapy.Field()
    # 小说简介
    novel_des = scrapy.Field()
    # 小说更新日期
    novel_date = scrapy.Field()
    # 小说第一章
    novel_start = scrapy.Field()