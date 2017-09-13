import scrapy

class QuestionSpider(scrapy.Spider):
    name = 'questions'

    custom_settings = {
        'USER_AGENT': 'coding-questions-bot (https://github.com/Arthurlpgc/InfoRetrievalProject)',
        'DOWNLOAD_DELAY': '0.25',
        'DOWNLOAD_TIMEOUT': '5',
        'DOWNLOAD_MAXSIZE': '1000000',
        'ROBOTSTXT_OBEY': 'True',
    }

    start_urls = [
        'http://codeforces.com/',
    ]

    allowed_domains = [
        'codeforces.com',
    ]

    def parse(self, response):
        self.savePage(response)
        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)

    def parseUrlName(self, url):
        forbidden = ['/', '\\', '>', '<', '?', '*', ':', '|']
        for c in forbidden:
            url = url.replace(c, '-')
        return url

    def savePage(self, response):
        filename = 'documents/%s.html' % self.parseUrlName(response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)

