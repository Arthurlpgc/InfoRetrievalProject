import scrapy
from scrapy import Request

class Token():
    def __init__(self, word, rank):
        self.word = word
        self.rank = rank

class LinkRanker():
    def __init__(self):
        self.minRank = -10000
        self.maxRank = 100

        codeforcesGoodTokens = [Token('problemset',          self.maxRank),
                                Token('problemset/page/',    self.maxRank/2),
                                Token('problemset/tags/',    self.maxRank/2),
                                Token('problemset/problem/', self.maxRank),]
   
        codeforcesBadTokens =  [Token('mobile',     self.minRank),
                                Token('status',     self.minRank),
                                Token('standings',  self.minRank),
                                Token('submit',     self.minRank),]

        self.tokens = []
        self.tokens.extend(codeforcesGoodTokens)
        self.tokens.extend(codeforcesBadTokens)

    def get(self, anchor, url):
        rank = 0
        for token in self.tokens:
            if(token.word in url):
                rank = rank + token.rank
        return rank

class QuestionSpider(scrapy.Spider):
    name = 'questions'

    custom_settings = {
        'USER_AGENT': 'coding-questions-bot (https://github.com/Arthurlpgc/InfoRetrievalProject)',
        'DOWNLOAD_TIMEOUT': '5',
        'DOWNLOAD_MAXSIZE': '1000000',
        'ROBOTSTXT_OBEY': 'True',
        'DOWNLOAD_DELAY': '0.25',
        'REDIRECT_MAX_TIMES': '5',
        'CLOSESPIDER_PAGECOUNT': '3000',
        'DEPTH_PRIORITY': '1',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }

    start_urls = [
        'http://codeforces.com/',
    ]

    allowed_domains = [
        'codeforces.com',
    ]

    linkRanker = LinkRanker()
    
    def parse(self, response):
        self.savePage(response)
        for a in response.selector.xpath('//a'):
            anchor = a.xpath('/text()').extract()
            for link in a.xpath('@href').extract():
                url = response.urljoin(link)
                yield Request(url=url, callback=self.parse, priority=self.linkRanker.get(anchor, url), dont_filter=False)

    def parseUrlName(self, url):
        forbidden = ['/', '\\', '>', '<', '?', '*', ':', '|']
        for c in forbidden:
            url = url.replace(c, '-')
        return url

    def savePage(self, response):
        filename = 'documents/%s.html' % self.parseUrlName(response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)

