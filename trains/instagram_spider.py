# -*- coding: utf-8 -*-
import scrapy
import json
import urllib.request
import os
import sys
import datetime
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


class InstagramSpider(scrapy.Spider):
    name = "Instagram"  # Name of the Spider, required value

    def __init__(self, account='', videos='', timestamp=''):
        self.videos = videos
        self.account = account

        if account == '':
            self.account = input("Name of the account ?")
        if videos == '':
            self.videos = input("Download videos ? (y/n) ")
        if timestamp == '':
            timestamp = input("Add timestamp ? (y/n) ")

        self.start_urls = ["https://www.instagram.com/"+self.account]

        self.savedir = "@"+self.account

        if timestamp == 'y':
            self.savedir = self.getCurrentTime() + self.savedir

        if not os.path.exists(self.savedir):
            os.makedirs(self.savedir)

    # Entry point for the spider

    def parse(self, response):
        # We get the json containing the photos's path
        js = response.selector.xpath(
            '//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]

        # Load it as a json object
        locations = json.loads(jscleaned)
        # with open('data.json', 'w') as f:
        #     json.dump(locations, f)
        # We check if there is a next page
        user = locations['entry_data']['ProfilePage'][0]['graphql']['user']
        is_private = user['is_private']

        if is_private == True:
            print("!!!!! Error !!!! : Looks like a private account")
            return

        has_next = user['edge_owner_to_timeline_media']['page_info']['has_next_page']
        medias = user['edge_owner_to_timeline_media']['edges']

        # We parse the photos
        for media in medias:
            node = media['node']
            url = node['display_url']
            id = node['id']
            type = node['__typename']
            code = node['shortcode']

            if type == "GraphSidecar":
                yield scrapy.Request("https://www.instagram.com/p/" + code, callback=self.parse_sideCar)

            elif type == "GraphImage":
                yield scrapy.Request(url,
                                     meta={'id': id, 'extension': '.jpg'},
                                     callback=self.save_media)

            elif type == "GraphVideo" and self.videos == 'y':
                yield scrapy.Request("https://www.instagram.com/p/" + code, callback=self.parse_page_video)

        # If there is a next page, we crawl it
        print("parse_falseOrtrue:", has_next)
        if has_next:
            url = "https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=" + \
                '{"id":"'+user['id']+'","first":12'+',"after":"' + \
                user['edge_owner_to_timeline_media']['page_info']['end_cursor']+'"}'
            print("parse_url:", url)

            yield scrapy.Request(url, callback=self.page_parse)

    # Method for parsing a page
    def page_parse(self, response):
        # Load it as a json object
        print("fjdlfjlsajfffdlsjfsajfdlsfj:", response.body)
        locations = json.loads(response.body)
        with open('data.json', 'w') as f:
            json.dump(locations, f)
        # We check if there is a next page
        user = locations['data']['user']
        has_next = user['edge_owner_to_timeline_media']['page_info']['has_next_page']
        print("parse_page_falseOrtrue:", has_next)
        medias = user['edge_owner_to_timeline_media']['edges']

        # We parse the photos
        for media in medias:
            node = media['node']
            url = node['display_url']
            id = node['id']
            type = node['__typename']
            code = node['shortcode']

            if type == "GraphSidecar":
                yield scrapy.Request("https://www.instagram.com/p/" + code, callback=self.parse_sideCar)

            elif type == "GraphImage":
                yield scrapy.Request(url,
                                     meta={'id': id, 'extension': '.jpg'},
                                     callback=self.save_media)

            elif type == "GraphVideo" and self.videos == 'y':
                yield scrapy.Request("https://www.instagram.com/p/" + code, callback=self.parse_page_video)

        # If there is a next page, we crawl it
        if has_next:
            url = "https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=" + \
                '{"id":"'+user['id']+'","first":12'+',"after":"' + \
                user['edge_owner_to_timeline_media']['page_info']['end_cursor']+'"}'
            print("parse_page_url:", url)

            yield scrapy.Request(url, callback=self.page_parse)

    # Method for parsing a video_page

    def parse_page_video(self, response):
        # Get the id from the last part of the url
        id = response.url.split("/")[-2]
        # We get the link of the video file
        js = response.selector.xpath(
            '//meta[@property="og:video"]/@content').extract()
        url = js[0]
        # We save the video
        yield scrapy.Request(url,
                             meta={'id': id, 'extension': '.mp4'},
                             callback=self.save_media)

    # Method for parsing a video_page
    def parse_sideCar(self, response):
        # We get the json containing the photos's path
        js = response.selector.xpath(
            '//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]

        json_data = json.loads(jscleaned)
        json_data = json_data["entry_data"]["PostPage"][0]

        edges = json_data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]

        for edge in edges:
            url = edge["node"]["display_url"]
            id = edge["node"]['id']
            yield scrapy.Request(url,
                                 meta={'id': id, 'extension': '.jpg'},
                                 callback=self.save_media)

    # We grab the media with urllib
    def save_media(self, response):
        print("Downloading : " + response.url)
        fullfilename = os.path.join(
            self.savedir, response.meta['id']+response.meta['extension'])
        urllib.request.urlretrieve(response.url, fullfilename)

    def getCurrentTime(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d_%H:%M")


# scrapy runspider instagram_spider.py -a account=<name of the account> -a videos=<y or n> -a timestamp=<y or n>
