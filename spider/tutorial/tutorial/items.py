# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GetquotesItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义我们需要抓取的内容：
    # 1.名言内容
    # 2.作者
    # 3.标签
    content = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

    pass
