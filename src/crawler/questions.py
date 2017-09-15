import scrapy
import queue as Q
import threading

class QuestionSpider(scrapy.Spider):
    name = 'questions'

    custom_settings = {
        'USER_AGENT': 'coding-questions-bot (https://github.com/Arthurlpgc/InfoRetrievalProject)',
        'DOWNLOAD_TIMEOUT': '5',
        'DOWNLOAD_MAXSIZE': '1000000',
        'ROBOTSTXT_OBEY': 'True',
        'DOWNLOAD_DELAY': '1.0',
        'REDIRECT_MAX_TIMES': '5',
        'CLOSESPIDER_PAGECOUNT': '3000',
    }

    start_urls = [
        'http://codeforces.com/',
    ]

    allowed_domains = [
        'codeforces.com',
    ]
    
    def parse(self, response):
        self.savePage(response)
        for href in response.xpath('//a/@href'):
            yield scrapy.Request(url=href.extract(), callback=self.parse, priority=self.setLinkPriority(href))

    def setLinkPriority(self, url):
        return 0

    def parseUrlName(self, url):
        forbidden = ['/', '\\', '>', '<', '?', '*', ':', '|']
        for c in forbidden:
            url = url.replace(c, '-')
        return url

    def savePage(self, response):
        filename = 'documents/%s.html' % self.parseUrlName(response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)