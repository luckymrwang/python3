# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class GetquotesPipeline(object):
    # 连接数据库
    def __init__(self):
        # 获取数据库连接信息
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)

        # 定义数据库
        db = client[dbname]
        self.table = db[settings['MONGODB_TABLE']]

    # 处理item
    def process_item(self, item, spider):
        # 使用dict转换item，然后插入数据库
        quote_info = dict(item)
        self.table.insert(quote_info)
        return item
