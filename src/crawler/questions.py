import scrapy
from scrapy import Request

class Token():
    def __init__(self, word, rank):
        self.word = word
        self.rank = rank

class LinkRanker():
    def __init__(self):
        self.minimize = -10000
        self.decrease = -50
        self.maximize = 1000
        self.increase = 50

        codeforces =    [Token('problemset',            self.increase),
                         Token('problemset/page/',      self.increase),
                         Token('problemset/tags/',      self.increase),
                         Token('problemset/problem/',   self.maximize),
                         Token('mobile',                self.minimize),
                         Token('status',                self.minimize),
                         Token('standings',             self.minimize),
                         Token('submit',                self.minimize)]

        codechef =      [Token('problems/',             self.maximize),
                         Token('problems/school',       self.decrease),
                         Token('problems/easy',         self.decrease),
                         Token('problems/medium',       self.decrease),
                         Token('problems/hard',         self.decrease),
                         Token('problems/challenge',    self.decrease),
                         Token('problems/extcontest',   self.decrease)]

        uri =           [Token('categories',            self.increase),
                         Token('/problems/index/',      self.increase),
                         Token('page=',                 self.increase),
                         Token('/problems/view/',       self.maximize),
                         Token('sort=',                 self.minimize)]

        spoj =          [Token('start=',                self.decrease),
                         Token('problems/partial',      self.decrease),
                         Token('problems/riddle',       self.decrease),
                         Token('problems/tutorial',     self.decrease),
                         Token('problems/basics',       self.decrease),
                         Token('problems/tag',          self.decrease),
                         Token('discuss.spoj.com',      self.minimize)]

        dmoj =          [Token('problem/',              self.maximize),
                         Token('order=',                self.minimize),
                         Token('search=',               self.minimize),
                         Token('category=',             self.minimize),
                         Token('/rank/',                self.minimize)]

        a2 =            [Token('p?ID=',                 self.maximize),
                         Token('/ps',                   self.increase),
                         Token('/ps?From=',             self.increase),
                         Token('/profile?',             self.minimize),
                         Token('/registrants?',         self.minimize),
                         Token('/contest?',             self.minimize),
                         Token('/sigin?',               self.minimize),
                         Token('/category?',            self.minimize),
                         Token('/users?',               self.minimize)]

        self.tokens = []
        self.tokens.extend(codeforces)
        self.tokens.extend(codechef)
        self.tokens.extend(uri)
        self.tokens.extend(spoj)
        self.tokens.extend(dmoj)
        self.tokens.extend(a2)

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
        'DOWNLOAD_TIMEOUT': '20',
        'DOWNLOAD_MAXSIZE': '1000000',
        'ROBOTSTXT_OBEY': 'True',
        'DOWNLOAD_DELAY': '0.1',
        'REDIRECT_MAX_TIMES': '5',
        'CLOSESPIDER_PAGECOUNT': '3000',
        'DEPTH_PRIORITY': '1',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }

    start_urls = [
        'http://codeforces.com/',
        'https://www.codechef.com/',
        'https://www.urionlinejudge.com.br',
        'http://www.spoj.com/',
        'https://dmoj.ca/',
        'https://a2oj.com/',
    ]

    allowed_domains = [
        #'codeforces.com',
        #'codechef.com',
        #'urionlinejudge.com.br',
        #'spoj.com',
        #'dmoj.ca',
        'a2oj.com',
    ]

    linkRanker = LinkRanker()
    
    def parse(self, response):
        self.savePage(response)
        for a in response.selector.xpath('//a'):
            anchor = a.xpath('/text()').extract()
            for link in a.xpath('@href').extract():
                url = response.urljoin(link)
                yield Request(url=url, 
                              callback=self.parse, 
                              priority=self.linkRanker.get(anchor, url),
                              dont_filter=False)

    def parseUrlName(self, url):
        forbidden = ['/', '\\', '>', '<', '?', '*', ':', '|']
        for c in forbidden:
            url = url.replace(c, '-')
        return url

    def savePage(self, response):
        filename = 'documents/%s.html' % self.parseUrlName(response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)

