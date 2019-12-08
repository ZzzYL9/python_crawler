# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import json

# class NovelspiderPipeline(object):
#     def __init__(self):
#         self.f = open("novel.json", "w")
#
#     def process_item(self, item, spider):
#         content = json.dumps(dict(item),ensure_ascii=False) + ',\n'
#         self.f.write(content)
#         return item
#
#     def close_spider(self,spider):
#         self.f.close()

# 爬取到的数据写入到SQLite数据库
import sqlite3

class NovelspiderPipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'novel_info.db')

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    #对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item,spider)
        return item

    #插入数据
    def insert_db(self, item, spider):
        values = (
            str(item['novel_name']),
            str(item['novel_author']),
            str(item['novel_img']),
            str(item['novel_type']),
            str(item['novel_des']),
            str(item['novel_date']),
            str(item['novel_start']),
        )
        if spider.name=='xianxia':
            sql = 'INSERT INTO XIANXIA VALUES(?,?,?,?,?,?,?)'
        elif spider.name=='lishi':
            sql = 'INSERT INTO LISHI VALUES(?,?,?,?,?,?,?)'
        elif spider.name=='kehuan':
            sql = 'INSERT INTO KEHUAN VALUES(?,?,?,?,?,?,?)'
        elif spider.name=='wangyou':
            sql = 'INSERT INTO WANGYOU VALUES(?,?,?,?,?,?,?)'

        self.db_cur.execute(sql, values)