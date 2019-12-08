# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class NovelPipeline(object):
    # 打开数据库
    def open_spider(self, spider):
        if spider.name=='dushi':
            db_name = './novel_db/dushi.db'
        elif spider.name=='kehuan':
            db_name = './novel_db/kehuan.db'
        elif spider.name=='lishi':
            db_name = './novel_db/lishi.db'
        elif spider.name=='wangyou':
            db_name = './novel_db/wangyou.db'
        elif spider.name=='xianxia':
            db_name = './novel_db/xianxia.db'

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item, spider)
        return item

    # 插入数据
    def insert_db(self, item, spider):
        values = (
            str(item['title']),
            str(item['texts']),
        )
        sql = 'INSERT INTO ' + str(item['name']) + ' VALUES(?,?)'
        # if spider.name == 'xianxia':
        #     sql = 'INSERT INTO XIANXIA VALUES(?,?,?,?,?,?,?)'
        # elif spider.name == 'lishi':
        #     sql = 'INSERT INTO LISHI VALUES(?,?,?,?,?,?,?)'
        # elif spider.name == 'kehuan':
        #     sql = 'INSERT INTO KEHUAN VALUES(?,?,?,?,?,?,?)'
        # elif spider.name == 'wangyou':
        #     sql = 'INSERT INTO WANGYOU VALUES(?,?,?,?,?,?,?)'

        self.db_cur.execute(sql, values)
