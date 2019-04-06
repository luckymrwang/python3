import scrapy
from tutorial.items import GetquotesItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # allowed_domains = ["stackoverflow.com"]

    # 设置起始网址
    # start_urls = ['http://quotes.toscrape.com']

    '''
        # 配置client，默认地址localhost，端口27017
        client = pymongo.MongoClient('localhost',27017)
        # 创建一个数据库，名称store_quote
        db_name = client['tutorial']
        # 创建一个表
        quotes_list = db_name['quotes']
    '''

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # 使用 css 选择要素进行抓取，如果喜欢用BeautifulSoup之类的也可以
        # 先定位一整块的quote，在这个网页块下进行作者、名言,标签的抓取
        for quote in response.css('.quote'):
            '''
            # 将页面抓取的数据存入mongodb,使用insert
            yield self.quotes_list.insert({
                'author' : quote.css('small.author::text').extract_first(),
                'tags' : quote.css('div.tags a.tag::text').extract(),
                'content' : quote.css('span.text::text').extract_first()
            })
            '''
            item = GetquotesItem()
            item['author'] = quote.css('small.author::text').extract_first()
            item['content'] = quote.css('span.text::text').extract_first()
            item['tags'] = quote.css('div.tags a.tag::text').extract()
            yield item

        # 使用xpath获取next按钮的href属性值
        next_href = response.xpath(
            '//li[@class="next"]/a/@href').extract_first()
        # 判断next_page的值是否存在
        if next_href is not None:

            # 如果下一页属性值存在，则通过urljoin函数组合下一页的url:
            # www.quotes.toscrape.com/page/2
            next_page = response.urljoin(next_href)

            # 回调parse处理下一页的url
            yield scrapy.Request(next_page, callback=self.parse)
