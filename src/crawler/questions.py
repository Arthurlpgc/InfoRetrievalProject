import scrapy
from urllib.parse import urlparse
from scrapy import Request
from scrapy.http import HtmlResponse
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from classifier.predict import check_if_is_coding_question

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

        codeforces =    [Token('/problemset',           self.increase),
                         Token('/problemset/page/',     self.increase),
                         Token('/problemset/tags/',     self.increase),
                         Token('/problemset/problem/',  self.maximize),
                         Token('mobile',                self.minimize),
                         Token('status',                self.minimize),
                         Token('standings',             self.minimize),
                         Token('submit',                self.minimize),
                         Token('locale=',               self.minimize),
                         Token('assets.',               self.minimize)]

        codechef =      [Token('/problems/',            self.maximize),
                         Token('/problems/school',      self.decrease),
                         Token('/problems/easy',        self.decrease),
                         Token('/problems/medium',      self.decrease),
                         Token('/problems/hard',        self.decrease),
                         Token('/problems/challenge',   self.decrease),
                         Token('/problems/extcontest',  self.decrease),
                         Token('/tags/',                self.minimize),
                         Token('discuss.',              self.minimize),
                         Token('blog.',                 self.minimize)]

        uri =           [Token('categories',            self.increase),
                         Token('/problems/index/',      self.increase),
                         Token('page=',                 self.increase),
                         Token('/problems/view/',       self.maximize),
                         Token('sort=',                 self.minimize)]

        spoj =          [Token('start=',                self.decrease),
                         Token('/problems/partial',     self.decrease),
                         Token('/problems/riddle',      self.decrease),
                         Token('/problems/tutorial',    self.decrease),
                         Token('/problems/basics',      self.decrease),
                         Token('/problems/tag',         self.decrease),
                         Token('discuss.spoj.com',      self.minimize),
                         Token('/tag/',                 self.minimize),
                         Token('/ranks/',               self.minimize),
                         Token('/users/',               self.minimize),
                         Token('blog.spoj.com',         self.minimize),
                         Token('/jobs',                 self.minimize)]

        dmoj =          [Token('/problem',              self.maximize),
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
        
        atcoder =       [Token('.contest.',             self.increase),
                         Token('/assignments',          self.increase),
                         Token('/contest',              self.increase),
                         Token('/contest?p=',           self.increase),
                         Token('/contest/archive',      self.increase),
                         Token('/contest/archive?p=',   self.increase),
                         Token('/tasks/',               self.maximize),
                         Token('/categories=',          self.minimize),
                         Token('/submit',               self.minimize),
                         Token('/submissions',          self.minimize),
                         Token('/clarifications',       self.minimize),
                         Token('/custom_test',          self.minimize),
                         Token('/editorial',            self.minimize),
                         Token('/tos',                  self.minimize),
                         Token('/privacy',              self.minimize),
                         Token('/personal',             self.minimize),
                         Token('/tutorial',             self.minimize),
                         Token('/rules',                self.minimize),
                         Token('/glossary',             self.minimize),
                         Token('/faq',                  self.minimize),
                         Token('/register',             self.minimize),
                         Token('/login',                self.minimize),
                         Token('/settings',             self.minimize)]

        csacademy =     [Token('/contest/interview-archive/',       self.increase),
                         Token('/contest/archive/',                 self.increase),
                         Token('/contest/interview-archive/task/',  self.maximize),
                         Token('/contest/archive/task/',            self.maximize),
                         Token('/solution/',                        self.minimize),
                         Token('/discussion/',                      self.minimize),
                         Token('/statistics/',                      self.minimize),
                         Token('/submissions/',                     self.minimize),
                         Token('/scoreboard/',                      self.minimize)]

        timus =         []

        caribbeanoj =   [Token('/24h/problems',     self.increase),
                         Token('pid=',              self.maximize)]

        self.tokens = []
        self.tokens.extend(codeforces)
        self.tokens.extend(codechef)
        self.tokens.extend(uri)
        self.tokens.extend(spoj)
        self.tokens.extend(dmoj)
        self.tokens.extend(a2)
        self.tokens.extend(atcoder)
        self.tokens.extend(csacademy)
        self.tokens.extend(timus)
        self.tokens.extend(caribbeanoj)

        self.specific = {}
        self.specific['http://codeforces.com/'] = codeforces
        self.specific['https://www.codechef.com/'] = codechef
        self.specific['https://www.urionlinejudge.com.br/'] = uri
        self.specific['http://www.spoj.com/'] = spoj
        self.specific['https://dmoj.ca/'] = dmoj
        self.specific['https://a2oj.com/'] = a2
        self.specific['http://atcoder.jp/'] = atcoder
        self.specific['https://csacademy.com/'] = csacademy
        self.specific['http://acm.timus.ru/'] = timus
        self.specific['http://coj.uci.cu/'] = caribbeanoj

    def get(self, anchor, url):
        rank = 0
        for token in self.tokens:
            if(token.word in url):
                rank = rank + token.rank
        return rank

    def getSpecific(self, anchor, url):
        if(self.getDomain(url) not in self.specific):
            return self.minimize
        rank = 0
        for token in self.specific[self.getDomain(url)]:
            if(token.word in url):
                rank = rank + token.rank
        return rank
        

    def getUniform(self, anchor, url):
        return 0

    def getDomain(self, url):
        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

class QuestionSpider(scrapy.Spider):
    name = 'questions'

    custom_settings = {
        'USER_AGENT': 'coding-questions-bot (https://github.com/Arthurlpgc/InfoRetrievalProject)',
        'DOWNLOAD_TIMEOUT': '5',
        'DOWNLOAD_MAXSIZE': '1000000',
        'CONCURRENT_REQUESTS': '1',
        'ROBOTSTXT_OBEY': 'True',
        'DOWNLOAD_DELAY': '0.05',
        'DEPTH_PRIORITY': '1',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }

    start_urls = [
        'http://codeforces.com/',
        'https://www.codechef.com/',
        'https://www.urionlinejudge.com.br/judge/en/login',
        'http://www.spoj.com/',
        'https://dmoj.ca/',
        'https://a2oj.com/',
        'http://atcoder.jp/',
        'https://csacademy.com/',
        'http://acm.timus.ru/',
        'http://coj.uci.cu',
    ]

    allowed_domains = [
        #'codeforces.com',
        #'codechef.com',
        #'urionlinejudge.com.br',
        'spoj.com',
        #'dmoj.ca',
        #'a2oj.com',
        #'atcoder.jp',
        #'csacademy.com',
        #'acm.timus.ru',
        #'coj.uci.cu'
    ]

    linkRanker = LinkRanker()
    maxPagesPerDomain = 200
    domainsCrawled = {}
    pagesCrawled = 0
    relevantPagesCrawled = 0
    
    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            raise scrapy.exceptions.IgnoreRequest()
        domain = self.getDomain(response.url)
        if(self.domainsCrawled.get(domain, 0) >= self.maxPagesPerDomain):
            raise scrapy.exceptions.IgnoreRequest()
        self.domainsCrawled[domain] = self.domainsCrawled.get(domain, 0) + 1
        self.savePage(response)
        self.pagesCrawled = self.pagesCrawled + 1
        if(self.pagesCrawled%50 == 0):
            self.generateLog()
        for a in response.selector.xpath('//a'):
            anchor = a.xpath('/text()').extract()
            for link in a.xpath('@href').extract():
                url = response.urljoin(link)
                if(self.domainsCrawled.get(url, 0) < self.maxPagesPerDomain):
                    yield Request(url=url, 
                                  callback=self.parse, 
                                  priority=self.linkRanker.get(anchor, url),
                                  dont_filter=False)


    def getDomain(self, url):
        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    def parseUrlName(self, url):
        forbidden = ['/', '\\', '>', '<', '?', '*', ':', '|']
        for c in forbidden:
            url = url.replace(c, '-')
        return url

    def savePage(self, response):
        filename = 'retrieved/documents/%s.html' % self.parseUrlName(response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.extractQuestion(filename)
    
    def extractQuestion(self, filename):
        with open(filename, 'rb') as f:
            relevant = check_if_is_coding_question(f)
            if(relevant == 'good'):
                self.relevantPagesCrawled = self.relevantPagesCrawled + 1

    def generateLog(self):
        print('\n -- CRAWLER LOG --\n')
        print('Pages In Queue per Domain:')
        for key in self.domainsCrawled:
            print(key, ': ', self.domainsCrawled[key])
        print('\nPages Crawled: ', self.pagesCrawled)
        print('Relevant Pages Found: ', self.relevantPagesCrawled)
        print('Precision: ', self.relevantPagesCrawled/self.pagesCrawled,'\n')
        with open('crawler/log.txt', 'a') as f:
            f.write('\n -- CRAWLER LOG --\n')
            f.write('Pages In Queue per Domain:\n')
            for key in self.domainsCrawled:
                f.write(key+': '+str(self.domainsCrawled[key])+'\n')
            f.write('\nPages Crawled: '+str(self.pagesCrawled)+'\n')
            f.write('Relevant Pages Found: '+str(self.relevantPagesCrawled)+'\n')
            f.write('Precision: '+str(self.relevantPagesCrawled/self.pagesCrawled)+'\n\n')


