import scrapy


class QuotesSpider(scrapy.Spider):
    name = "questions-bfs"

    start_urls = [
        'http://codeforces.com/',
    ]

    allowed_domains = [
        'codeforces.com',
    ]

    def parse(self, response):
        page = response.url.split('/')
        page.pop(0)
        name = '-'.join(page)
        filename = 'documents/%s.html' % name
        with open(filename, 'wb') as f:
            f.write(response.body)
        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)