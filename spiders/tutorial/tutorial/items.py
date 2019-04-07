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


class ProfileItem(scrapy.Item):
    """
    账号的微博数、关注数、粉丝数及详情
    """
    _id = scrapy.Field()
    nick_name = scrapy.Field()
    profile_pic = scrapy.Field()
    tweet_stats = scrapy.Field()
    following_stats = scrapy.Field()
    follower_stats = scrapy.Field()
    sex = scrapy.Field()
    location = scrapy.Field()
    birthday = scrapy.Field()
    bio = scrapy.Field()


class FollowingItem(scrapy.Item):
    """
    关注的微博账号
    """
    _id = scrapy.Field()
    relationship = scrapy.Field()


class FollowedItem(scrapy.Item):
    """
    粉丝的微博账号
    """
    _id = scrapy.Field()
    relationship = scrapy.Field()
