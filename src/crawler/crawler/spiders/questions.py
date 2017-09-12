import scrapy


class QuotesSpider(scrapy.Spider):
    name = "questions"
    start_urls = [
        'http://codeforces.com/',
    ]

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'documents/%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)