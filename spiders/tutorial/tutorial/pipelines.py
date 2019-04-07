# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymongo
from scrapy.conf import settings
from tutorial.items import ProfileItem, FollowingItem, FollowedItem


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


class WeiboPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            host=settings['MONGODB_HOST'],
            port=settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DBNAME']]
        self.info = db[settings['INFO']]
        self.following = db[settings['FOLLOWING']]
        self.followed = db[settings['FOLLOWED']]

    def process_item(self, item, spider):
        if isinstance(item, ProfileItem):
            self.info.insert(dict(item))
        elif isinstance(item, FollowingItem):
            self.following.insert(dict(item))
        elif isinstance(item, FollowedItem):
            self.followed.insert(dict(item))
        scrapy.log.msg("Weibo added to MongoDB database!",
                       level=scrapy.log.DEBUG, spider=spider)
        return item
